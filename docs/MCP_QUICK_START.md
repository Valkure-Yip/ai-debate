# MCP Quick Start Guide

Get MCP tools running in 5 minutes!

## Prerequisites

- Node.js v16 or higher: `node --version`
- Tavily API key (free at https://tavily.com/)

## Setup Steps

### 1. Create Configuration File

```bash
cp mcp_config.template.json mcp_config.json
```

### 2. Add Your Tavily API Key

Edit `mcp_config.json`:

```json
{
  "servers": {
    "tavily": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.tavily.com/mcp/?tavilyApiKey=tvly-your-actual-key-here"
      ],
      "env": {
        "TAVILY_API_KEY": "tvly-your-actual-key-here"
      }
    }
  }
}
```

**Important:** Replace `tvly-your-actual-key-here` with your actual API key in BOTH the URL and the env section.

### 3. Run a Debate

```bash
python debate.py --topic "latest developments in AI in 2025" --rounds 3
```

## What You'll See

```
🔌 Connecting to 1 MCP server(s)...
   ✓ Connected to 'tavily'
✓ 1/1 MCP server(s) connected successfully

📝 Tool call logging enabled

🎬 Starting debate...
```

When debaters use tools:

```
   🔧 [Debater 1] Using tool: tavily_search
```

## Where to Find Logs

Detailed tool call logs are saved to:

```
logs/debate_tools_YYYYMMDD_HHMMSS.log
```

## Troubleshooting

**Error: "Failed to connect to 'tavily'"**

- Check your API key in `mcp_config.json`
- Verify Node.js is installed: `node --version`

**No tools being used?**

- Try a topic that requires current information
- Example: `--topic "AI developments in 2025"`
- Models decide when tools are needed

**Want more tools?**

- See [MCP_GUIDE.md](MCP_GUIDE.md) for adding more MCP servers

## Next Steps

- Read [MCP_GUIDE.md](MCP_GUIDE.md) for detailed configuration
- Add more MCP servers (filesystem, weather, etc.)
- Explore tool call logs to understand usage patterns

---

**Need help?** Check the full guide: [docs/MCP_GUIDE.md](MCP_GUIDE.md)
