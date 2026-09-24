from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from fastmcp.client.transports import StdioTransport
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.providers.bedrock import BedrockProvider


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

REGION = "ap-southeast-2"
MODEL_ID = "nvidia.nemotron-super-3-120b"

# ------------------------------------------------------------
# MCP connection
# ------------------------------------------------------------

MCP_SERVER = (
    Path(__file__).parents[1]
    / "mcp-server"
    / "bbvet_mcp_server.py"
)

mcp_toolset = MCPToolset(
    StdioTransport(
        command=sys.executable,
        args=[str(MCP_SERVER)],
    )
)

# ------------------------------------------------------------
# Bedrock model
# ------------------------------------------------------------

model = BedrockConverseModel(
    MODEL_ID,
    provider=BedrockProvider(
        region_name=REGION,
    ),
)

# ------------------------------------------------------------
# Agent
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# Conversation
# ------------------------------------------------------------

async def chat() -> None:

    message_history = None

    print("BBVet Knowledge Custodian")
    print("Type 'quit' to exit.")

    async with agent:

        while True:

            prompt = input("\nYou > ").strip()

            if prompt.lower() in {
                "quit",
                "exit",
                "q",
            }:
                break

            if not prompt:
                continue

            result = await agent.run(
                prompt,
                message_history=message_history,
            )

            # Keeps the full conversation, including tool calls
            # and tool results.
            message_history = result.all_messages()

            print(f"\nAssistant > {result.output}")


if __name__ == "__main__":
    asyncio.run(chat())

# ChatGPT was used to assist writing this code. 
# The code was reviewed and tested by myself.