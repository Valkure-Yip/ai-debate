# MCP (Model Context Protocol) Integration Guide

This guide explains how to configure and use MCP servers with the AI Debate application, enabling debaters to access external tools and data sources during debates.

## Table of Contents

- [What is MCP?](#what-is-mcp)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Available Tools](#available-tools)
- [Adding New MCP Servers](#adding-new-mcp-servers)
- [Tool Usage in Debates](#tool-usage-in-debates)
- [Troubleshooting](#troubleshooting)

## What is MCP?

Model Context Protocol (MCP) is an open standard for connecting LLMs to external tools and data sources. MCP servers provide specific capabilities (like web search, file access, database queries) that AI models can use during conversations.

In the AI Debate application, debaters can:

- Search the web for facts and recent information (via Tavily)
- Access file systems
- Query databases
- Use any MCP-compatible tool

## Quick Start

### 1. Install Node.js and npm

MCP servers often run as Node.js packages. Ensure you have Node.js installed:

```bash
node --version  # Should be v16 or higher
npm --version
```

If not installed, download from [nodejs.org](https://nodejs.org/).

### 2. Create MCP Configuration

Copy the template to create your configuration:

```bash
cp mcp_config.template.json mcp_config.json
```

### 3. Configure Tavily (Web Search)

Edit `mcp_config.json` and add your Tavily API key:

```json
{
  "servers": {
    "tavily": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.tavily.com/mcp/?tavilyApiKey=tvly-your-actual-api-key-here"
      ],
      "env": {
        "TAVILY_API_KEY": "tvly-your-actual-api-key-here"
      }
    }
  }
}
```

**Important:** Replace `tvly-your-actual-api-key-here` with your actual Tavily API key in BOTH the URL and the env section.

Get your Tavily API key from: https://tavily.com/

### 4. Run a Debate

Start a debate as usual. MCP tools will be automatically available:

```bash
python debate.py --topic "climate change in 2025"
```

When debaters need information, they can automatically use the Tavily search tool.

## Configuration

### Configuration File Structure

The `mcp_config.json` file defines all MCP servers:

```json
{
  "servers": {
    "server_name": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "env": {
        "API_KEY": "value"
      }
    }
  }
}
```

**Fields:**

- `command`: The executable to run (e.g., `npx`, `python`, `node`)
- `args`: Array of command-line arguments
- `env`: Environment variables (including API keys)

### Multiple Servers

You can configure multiple MCP servers simultaneously:

```json
{
  "servers": {
    "tavily": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.tavily.com/mcp/?tavilyApiKey=tvly-xxx"
      ],
      "env": {
        "TAVILY_API_KEY": "tvly-xxx"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/you/documents"
      ],
      "env": null
    }
  }
}
```

## Available Tools

### Tavily (Web Search)

**Server:** `mcp-remote` (connecting to https://mcp.tavily.com/mcp/)

**Tools provided:**

- `tavily_search`: Search the web for current information

**Example use case in debates:**

- Finding recent statistics
- Verifying current events
- Getting latest research findings

**Setup:**

1. Get API key from https://tavily.com/
2. Add to `mcp_config.json`:
   ```json
   {
     "servers": {
       "tavily": {
         "command": "npx",
         "args": [
           "-y",
           "mcp-remote",
           "https://mcp.tavily.com/mcp/?tavilyApiKey=YOUR-KEY-HERE"
         ],
         "env": {
           "TAVILY_API_KEY": "YOUR-KEY-HERE"
         }
       }
     }
   }
   ```
3. Replace `YOUR-KEY-HERE` with your actual API key in both places

### File System

**Server:** `@modelcontextprotocol/server-filesystem`

**Tools provided:**

- `read_file`: Read file contents
- `write_file`: Write to files
- `list_directory`: List directory contents
- `search_files`: Search for files

**Example use case in debates:**

- Reading reference documents
- Accessing local data files
- Citing specific sources

**Setup:**

```json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/directory"
      ],
      "env": null
    }
  }
}
```

**Security note:** Only directories specified in args will be accessible.

### Other Popular MCP Servers

- **GitHub**: `@modelcontextprotocol/server-github` - Repository operations
- **Slack**: `@modelcontextprotocol/server-slack` - Slack integration
- **PostgreSQL**: `@modelcontextprotocol/server-postgres` - Database queries
- **Google Drive**: Community servers available

Find more at: https://github.com/modelcontextprotocol/servers

## Adding New MCP Servers

### Step 1: Find or Create an MCP Server

Browse available servers:

- Official servers: https://github.com/modelcontextprotocol/servers
- Community servers: Search npm for "mcp-server-\*"

### Step 2: Determine Command and Args

For npm packages:

```json
{
  "command": "npx",
  "args": ["-y", "package-name", "additional-args"]
}
```

For Python servers:

```json
{
  "command": "python",
  "args": ["/path/to/server.py"]
}
```

### Step 3: Configure Environment Variables

If the server requires API keys or configuration:

```json
{
  "env": {
    "API_KEY": "your-key",
    "CONFIG_OPTION": "value"
  }
}
```

### Step 4: Test the Configuration

Run a debate and check the startup messages:

```
🔌 Connecting to 2 MCP server(s)...
   ✓ Connected to 'tavily'
   ✓ Connected to 'your-new-server'
✓ 2/2 MCP server(s) connected successfully
```

### Example: Adding Weather MCP Server

```json
{
  "servers": {
    "tavily": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.tavily.com/mcp/?tavilyApiKey=tvly-xxx"
      ],
      "env": {
        "TAVILY_API_KEY": "tvly-xxx"
      }
    },
    "weather": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-weather"],
      "env": {
        "WEATHER_API_KEY": "your-key"
      }
    }
  }
}
```

## Tool Usage in Debates

### Automatic Tool Selection

Debaters automatically decide when to use tools based on their needs. No special prompting required.

### Example Debate with Tools

```bash
$ python debate.py --topic "impact of AI on employment in 2025" --rounds 3

🔌 Connecting to 1 MCP server(s)...
   ✓ Connected to 'tavily'
✓ 1/1 MCP server(s) connected successfully

📝 Tool call logging enabled

🎬 Starting debate...

================================================================================
🔵 Debater 1:
--------------------------------------------------------------------------------
Let me search for recent data on AI employment impact...
   🔧 [Debater 1] Using tool: tavily_search

According to recent studies from 2025, AI has displaced 2.3 million jobs
but created 3.1 million new positions in AI-related fields...
```

### Tool Call Logging

All tool calls are logged to `logs/debate_tools_TIMESTAMP.log` with complete details:

```
[2025-10-23 14:30:45] Debater 1
--------------------------------------------------------------------------------
Tool: tavily_search
Arguments:
{
  "query": "AI employment impact 2025 statistics"
}
Result:
  Content[0] (text):
    [{"title": "AI Employment Report 2025", "url": "https://example.com/ai-report",
      "content": "According to the latest research, AI has transformed employment
      patterns with 2.3 million jobs displaced but 3.1 million new positions
      created in AI-related fields...", "score": 0.95}]
================================================================================
```

The log includes:

- Timestamp of the tool call
- Which debater made the call
- Tool name and all arguments
- **Complete MCP result** including all returned data
- Structured formatting for easy reading

### Console Output

The console shows brief summaries:

- `🔧 [Debater 1] Using tool: tavily_search` - Tool being used
- Full results are in the log file
- Final response incorporates tool results

## Troubleshooting

### Issue: "MCP config file not found"

**Cause:** No `mcp_config.json` file exists.

**Solution:** Create it from template:

```bash
cp mcp_config.template.json mcp_config.json
```

### Issue: "No MCP servers configured"

**Cause:** `mcp_config.json` exists but has no servers defined.

**Solution:** Add at least one server to the `servers` object.

### Issue: "Failed to connect to 'tavily'"

**Possible causes:**

1. Invalid or missing API key
2. Node.js not installed
3. Network connectivity issues
4. npm package not accessible

**Solutions:**

- Verify API key is correct in `mcp_config.json` (both in URL and env section)
- Check Node.js: `node --version`
- Test npm connectivity: `npx -y mcp-remote --version`
- Check firewall/proxy settings
- Verify the Tavily MCP endpoint is accessible: https://mcp.tavily.com/mcp/

### Issue: "Tool 'X' not found in any connected server"

**Cause:** The model is trying to use a tool that isn't available.

**Solution:**

- Add the required MCP server to `mcp_config.json`
- Or adjust debater personas to work with available tools

### Issue: MCP servers slow down debate

**Cause:** Tool execution takes time, especially web searches.

**Solutions:**

- Use faster MCP servers when available
- Reduce number of debate rounds
- Accept that tool-augmented debates take longer
- Consider running with `--debater1-max-tokens 300` for shorter responses

### Issue: Tool results are too long/verbose

**Cause:** Some tools return extensive data.

**Solution:** The application already handles this by:

- Logging full details to file
- Showing brief summaries in console
- Model automatically summarizes tool results

### Debugging Tips

1. **Check startup messages**: Connection status shown at beginning
2. **Review log file**: Detailed tool calls in `logs/debate_tools_*.log`
3. **Test MCP server directly**: Test the mcp-remote package:
   ```bash
   npx -y mcp-remote --help
   ```
4. **Simplify config**: Test with one server first
5. **Check permissions**: Ensure proper access for filesystem servers

## Best Practices

### API Key Security

- Never commit `mcp_config.json` to version control
- Add to `.gitignore`
- Use environment variables for sensitive keys
- Rotate keys periodically

### Server Selection

- Start with one server (Tavily recommended)
- Add more as needed for specific debates
- Too many tools can confuse models

### Debate Topics

Tool-enhanced debates work best for topics requiring:

- Current events and statistics
- Factual verification
- Data-driven arguments
- Real-world examples

### Performance

- Each tool call adds latency
- Plan for longer debate sessions
- Consider token limits (tools consume tokens)

## Additional Resources

- MCP Official Documentation: https://modelcontextprotocol.io/
- MCP Servers Repository: https://github.com/modelcontextprotocol/servers
- Tavily API Docs: https://docs.tavily.com/
- OpenRouter MCP Guide: https://openrouter.ai/docs/use-cases/mcp-servers

## Support

For issues specific to:

- **This application**: Create an issue in the project repository
- **MCP protocol**: Visit https://github.com/modelcontextprotocol
- **Specific servers**: Check the server's own documentation
- **Tavily**: Visit https://tavily.com/docs

---

Happy debating with enhanced AI capabilities! 🎭🔧
