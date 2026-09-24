"""Expose the existing PydanticAI/MCP teaching agent through ACP over stdio."""

from __future__ import annotations

import os
import sys
import warnings
from pathlib import Path

from fastmcp.client.transports import StdioTransport
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.providers.bedrock import BedrockProvider
from pydantic_ai_harness.experimental import HarnessExperimentalWarning

# ACP is an explicitly experimental Harness capability; keep its expected warning out of server logs.
warnings.filterwarnings("ignore", category=HarnessExperimentalWarning)
from pydantic_ai_harness.experimental.acp import run_acp_stdio_sync

# Use the configured region, defaulting to the unit's Sydney region.
REGION = os.getenv("AWS_REGION", "ap-southeast-2")
MODEL_ID = "nvidia.nemotron-super-3-120b"
# The MCP practical is extracted beside this directory.
MCP_SERVER = Path(__file__).parents[1] / "mcp_servers_python" / "fastmcp_server.py"

#region agent-configuration
# This is the same Bedrock model and local MCP toolset as the terminal agent.
model = BedrockConverseModel(MODEL_ID, provider=BedrockProvider(region_name=REGION))
mcp_toolset = MCPToolset(StdioTransport(command=sys.executable, args=[str(MCP_SERVER)]))
agent = Agent(
    model,
    instructions=(
        "You are a concise CAB432 teaching assistant. "
        "Use the celsius_to_fahrenheit MCP tool for Celsius-to-Fahrenheit conversions."
    ),
    toolsets=[mcp_toolset],
)
#endregion agent-configuration


if __name__ == "__main__":
    #region acp-runner
    # The Pydantic AI Harness supplies ACP sessions, history, streaming and cancellation.
    # websocket_server.py exposes this stdio server to the browser over WebSocket.
    run_acp_stdio_sync(agent, name="CAB432 Bedrock MCP agent", version="1.0.0")
    #endregion acp-runner
