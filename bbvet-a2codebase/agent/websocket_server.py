from __future__ import annotations

import asyncio
import logging
import sys
from contextlib import suppress
from pathlib import Path

from websockets.asyncio.server import ServerConnection, serve
from websockets.exceptions import ConnectionClosed


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

HOST = "127.0.0.1"
PORT = 7331
PATH = "/acp"

AGENT_SCRIPT = (
    Path(__file__).parent
    / "bbvet_acp_agent.py"
)

LOGGER = logging.getLogger("bbvet-acp-websocket")


# ------------------------------------------------------------
# Browser -> ACP agent
# ------------------------------------------------------------

async def copy_to_agent(
    websocket: ServerConnection,
    stdin: asyncio.StreamWriter,
) -> None:
    """
    Copy WebSocket text messages into the ACP agent's stdin.

    ACP over stdio expects one JSON-RPC message per line.
    """

    async for message in websocket:

        # ACP messages should be text, not raw WebSocket bytes.
        if isinstance(message, bytes):
            raise ValueError(
                "ACP WebSocket messages must be text."
            )

        # One WebSocket message should correspond to one ACP record.
        if "\n" in message or "\r" in message:
            raise ValueError(
                "ACP WebSocket messages must contain one JSON-RPC record."
            )

        stdin.write(
            message.encode("utf-8") + b"\n"
        )

        await stdin.drain()


# ------------------------------------------------------------
# ACP agent -> browser
# ------------------------------------------------------------

async def copy_to_browser(
    stdout: asyncio.StreamReader,
    websocket: ServerConnection,
) -> None:
    """
    Read newline-delimited ACP messages from stdout and
    send each one back as a WebSocket text message.
    """

    while True:

        line = await stdout.readline()

        if not line:
            break

        message = line.rstrip(b"\r\n")

        if message:
            await websocket.send(
                message.decode("utf-8")
            )


# ------------------------------------------------------------
# Agent stderr logging
# ------------------------------------------------------------

async def log_agent_stderr(
    stderr: asyncio.StreamReader,
) -> None:
    """
    Forward diagnostic output from the ACP subprocess
    to the WebSocket server terminal.
    """

    while True:

        line = await stderr.readline()

        if not line:
            break

        LOGGER.error(
            "ACP agent: %s",
            line.decode(
                "utf-8",
                errors="replace",
            ).rstrip(),
        )


# ------------------------------------------------------------
# Stop ACP subprocess
# ------------------------------------------------------------

async def stop_agent(
    process: asyncio.subprocess.Process,
) -> None:
    """
    Shut down the child ACP agent cleanly when the browser
    connection closes.
    """

    if process.returncode is not None:
        return

    # Closing stdin gives the ACP process a chance to finish cleanly.
    if process.stdin is not None:
        process.stdin.close()

        with suppress(Exception):
            await process.stdin.wait_closed()

    try:
        await asyncio.wait_for(
            process.wait(),
            timeout=2,
        )

    except asyncio.TimeoutError:

        process.terminate()

        try:
            await asyncio.wait_for(
                process.wait(),
                timeout=2,
            )

        except asyncio.TimeoutError:

            process.kill()
            await process.wait()


# ------------------------------------------------------------
# One browser connection
# ------------------------------------------------------------

async def relay(
    websocket: ServerConnection,
) -> None:
    """
    Start one ACP agent subprocess and relay messages between
    that process and one browser WebSocket connection.
    """

    if websocket.request.path != PATH:

        LOGGER.warning(
            "Rejected WebSocket connection to %s",
            websocket.request.path,
        )

        await websocket.close(
            code=1008,
            reason="Use the /acp WebSocket endpoint.",
        )

        return

    LOGGER.info("Browser connected.")

    # Start a fresh ACP agent for this browser connection.
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "-u",
        str(AGENT_SCRIPT),

        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,

        cwd=AGENT_SCRIPT.parent,
    )

    LOGGER.info(
        "Started BBVet ACP agent process %s",
        process.pid,
    )

    assert process.stdin is not None
    assert process.stdout is not None
    assert process.stderr is not None

    browser_to_agent = asyncio.create_task(
        copy_to_agent(
            websocket,
            process.stdin,
        )
    )

    agent_to_browser = asyncio.create_task(
        copy_to_browser(
            process.stdout,
            websocket,
        )
    )

    stderr_logger = asyncio.create_task(
        log_agent_stderr(
            process.stderr,
        )
    )

    try:

        # Stop when either side of the connection finishes.
        done, pending = await asyncio.wait(
            [
                browser_to_agent,
                agent_to_browser,
            ],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

        await asyncio.gather(
            *pending,
            return_exceptions=True,
        )

        # Propagate any unexpected exception.
        for task in done:
            task.result()

    except ConnectionClosed:
        pass

    except ValueError as error:

        LOGGER.warning(
            "Invalid WebSocket message: %s",
            error,
        )

        with suppress(ConnectionClosed):
            await websocket.close(
                code=1003,
                reason=str(error),
            )

    except Exception:

        LOGGER.exception(
            "ACP WebSocket relay failed."
        )

        with suppress(ConnectionClosed):
            await websocket.close(
                code=1011,
                reason="ACP relay failed.",
            )

    finally:

        await stop_agent(process)

        if not stderr_logger.done():
            stderr_logger.cancel()

        await asyncio.gather(
            stderr_logger,
            return_exceptions=True,
        )

        LOGGER.info(
            "ACP agent process stopped."
        )


# ------------------------------------------------------------
# Start WebSocket server
# ------------------------------------------------------------

async def main() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    LOGGER.info(
        "BBVet ACP server listening at ws://%s:%s%s",
        HOST,
        PORT,
        PATH,
    )

    async with serve(
        relay,
        HOST,
        PORT,
    ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())