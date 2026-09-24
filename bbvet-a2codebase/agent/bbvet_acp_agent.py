from __future__ import annotations

import os
import sys
import warnings
from pathlib import Path

from fastmcp.client.transports import StdioTransport

from pydantic_ai_harness.experimental.acp import (
    AcpSession,
    AcpSessionConfig,
    run_acp_stdio_sync,
)

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.providers.bedrock import BedrockProvider

from pydantic_ai_harness.experimental import HarnessExperimentalWarning
from pydantic_ai_harness.experimental.acp import run_acp_stdio_sync

# ACP is an explicitly experimental Harness capability; keep its expected warning out of server logs.
warnings.filterwarnings("ignore", category=HarnessExperimentalWarning)
from pydantic_ai_harness.experimental.acp import run_acp_stdio_sync

# Use the configured region, defaulting to the unit's Sydney region.
REGION = os.getenv("AWS_REGION", "ap-southeast-2")
MODEL_ID = "nvidia.nemotron-super-3-120b"
# The MCP practical is extracted beside this directory.
MCP_SERVER = Path(__file__).parents[1] / "mcp_servers_python" / "fastmcp_server.py"

mcp_toolset = MCPToolset(
    StdioTransport(
        command=sys.executable,
        args=[str(MCP_SERVER)],
    )
)

model = BedrockConverseModel(
    MODEL_ID,
    provider=BedrockProvider(
        region_name=REGION,
    ),
)

agent = Agent(
    model,
    instructions=(
        "You are the BBVet Knowledge Custodian. "
        "Help users understand information contained in the BBVet "
        "knowledge repository. "

        "Use the search_bbvet_knowledge MCP tool when a question "
        "requires information about BBVet meetings, product decisions, "
        "Clinic Health, Clinic Performance, Industry Insight, "
        "subscriptions, project decisions, or repository knowledge. "

        "Base repository-specific answers on information returned by "
        "the tool. Do not invent BBVet facts that are not supported "
        "by the retrieved repository information. "

        "If the available repository information does not contain the "
        "answer, clearly say so."
    ),
    toolsets=[
        mcp_toolset,
    ],
)

def session_config(
    session: AcpSession,
) -> AcpSessionConfig[None]:
    """
    Configure each ACP browser session.

    The QUT ACP client includes an empty mcpServers list when
    creating a session. Current Pydantic AI Harness requires a
    session_config when that field is supplied.

    The BBVet MCP server is already attached directly to the
    PydanticAI agent, so there are no additional client-provided
    MCP servers to connect here.    
    """

    return AcpSessionConfig(
        deps=None,
        toolsets=[],
    )

if __name__ == "__main__":

    run_acp_stdio_sync(
        agent,
        name="BBVet Knowledge Custodian",
        version="1.0.0",
        session_config=session_config,
    )

# ChatGPT was used to assist writing this code. 
# The code was reviewed and tested by myself.