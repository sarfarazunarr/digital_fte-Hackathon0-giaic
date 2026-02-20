# Skill: MCP Integration

## Description
Provides the agent with external capabilities via the Model Context Protocol (MCP).

## Current Server: Email Service
- **Tool**: `send_email(to, subject, body)`
- **Function**: Allows the agent to send emails directly if the orchestrator is bypassed or if used by an autonomous agent.

## Configuration
The `mcp_config.json` file in the root directory defines the server connection.
Agents like `claude code` or `gemini cli` can use this configuration to gain email capabilities.
