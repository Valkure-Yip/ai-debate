# Testing MCP Integration

This guide helps you test the MCP integration to ensure everything is working correctly.

## Test 1: Verify Installation

### Check Dependencies

```bash
# Activate virtual environment
source venv/bin/activate  # On macOS/Linux

# Install/update requirements
pip install -r requirements.txt
```

Expected packages:

- `openai>=1.0.0`
- `python-dotenv>=1.0.0`
- `mcp>=1.0.0`

### Check Node.js

```bash
node --version
npm --version
```

Required: Node.js v16 or higher

## Test 2: Run Without MCP (Baseline)

Test that the basic debate still works without MCP:

```bash
python debate.py --rounds 2
```

Expected output:

```
⚠️  MCP config file not found: mcp_config.json
   MCP tools will not be available. Create mcp_config.json from template to enable.
ℹ️  No MCP servers configured.

✓ Debater 1 initialized: openai/gpt-4o-mini
✓ Debater 2 initialized: openai/gpt-4o-mini

🎬 Starting debate...
```

Debate should run normally without MCP tools.

## Test 3: Configure MCP with Invalid Key

Test error handling with an invalid API key:

```bash
# Create config
cp mcp_config.template.json mcp_config.json

# Edit mcp_config.json and use a fake key like "test-key"
```

Run debate:

```bash
python debate.py --rounds 2
```

Expected output:

```
🔌 Connecting to 1 MCP server(s)...
   ✗ Failed to connect to 'tavily': [error message]
⚠️  No MCP servers could be connected. Tools will not be available.
```

Debate should still run, just without tools.

## Test 4: Configure MCP with Valid Key

### Get Tavily API Key

1. Visit https://tavily.com/
2. Sign up for a free account
3. Copy your API key (starts with `tvly-`)

### Configure

Edit `mcp_config.json`:

```json
{
  "servers": {
    "tavily": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.tavily.com/mcp/?tavilyApiKey=tvly-your-real-key-here"
      ],
      "env": {
        "TAVILY_API_KEY": "tvly-your-real-key-here"
      }
    }
  }
}
```

**Important:** Replace `tvly-your-real-key-here` in both the URL and env section with your actual API key.

### Run Test Debate

```bash
python debate.py --topic "major technological breakthroughs in 2025" --rounds 3
```

Expected output:

```
🔌 Connecting to 1 MCP server(s)...
   ✓ Connected to 'tavily'
✓ 1/1 MCP server(s) connected successfully

📝 Tool call logging enabled

✓ Debater 1 initialized: openai/gpt-4o-mini
✓ Debater 2 initialized: openai/gpt-4o-mini

🎬 Starting debate...
```

## Test 5: Verify Tool Usage

During the debate, watch for tool calls:

```
🔄 ROUND 1/3
================================================================================

   🔧 [Debater 1] Using tool: tavily_search

================================================================================
🔵 Debater 1:
--------------------------------------------------------------------------------
According to recent reports from 2025...
```

This indicates the debater is using web search!

## Test 6: Check Log Files

After the debate completes:

```bash
ls -la logs/
```

You should see:

```
debate_tools_YYYYMMDD_HHMMSS.log
```

View the log:

```bash
cat logs/debate_tools_*.log
```

Expected content:

```
================================================================================
AI Debate - Tool Call Log
Session started: 2025-10-23 14:30:45
================================================================================

[2025-10-23 14:30:47] Debater 1
--------------------------------------------------------------------------------
Tool: tavily_search
Arguments:
{
  "query": "technological breakthroughs 2025"
}
Result:
  Content[0] (text):
    [{"title": "Top Tech Breakthroughs 2025", "url": "https://...",
      "content": "Major technological advancements in 2025 include...",
      "score": 0.98}]
================================================================================
```

The result section includes the complete MCP response with all returned data.

## Test 7: Test Multiple Servers

Add a second server to `mcp_config.json`:

```json
{
  "servers": {
    "tavily": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.tavily.com/mcp/?tavilyApiKey=tvly-your-key"
      ],
      "env": {
        "TAVILY_API_KEY": "tvly-your-key"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "env": null
    }
  }
}
```

Run debate:

```bash
python debate.py --rounds 2
```

Expected:

```
🔌 Connecting to 2 MCP server(s)...
   ✓ Connected to 'tavily'
   ✓ Connected to 'filesystem'
✓ 2/2 MCP server(s) connected successfully
```

## Test 8: OpenRouter Integration

Test MCP with OpenRouter:

```bash
python debate.py \
  --debater1-provider openrouter \
  --debater1-model anthropic/claude-3-haiku \
  --topic "climate change initiatives in 2025" \
  --rounds 2
```

MCP should work with any provider that supports OpenAI-compatible tool calling.

## Test 9: Error Recovery

Test that the app handles errors gracefully:

### Kill connection mid-debate

1. Start a debate: `python debate.py --rounds 5`
2. If a tool call happens, press `Ctrl+C`
3. App should cleanup: `🔌 MCP connections closed`

### Invalid tool arguments

The app should handle this internally and show tool errors in logs without crashing.

## Test 10: Performance

Compare debate times:

**Without MCP:**

```bash
time python debate.py --rounds 3
```

**With MCP:**

```bash
time python debate.py --rounds 3
```

Tool-enabled debates will be slower due to web searches, but should still complete successfully.

## Common Issues and Solutions

### Issue: `ModuleNotFoundError: No module named 'mcp'`

**Solution:**

```bash
pip install --upgrade -r requirements.txt
```

### Issue: `command not found: npx`

**Solution:** Install Node.js from https://nodejs.org/

### Issue: Tools never get called

**Reasons:**

- Topic doesn't require external information
- Model chose not to use tools
- Try a more data-intensive topic like "latest statistics on..."

### Issue: `Permission denied` for filesystem server

**Solution:** Use a directory you have access to, like `/tmp` or your home directory

## Success Criteria

✅ **All tests pass if:**

1. App runs without MCP config (fallback works)
2. App handles invalid API keys gracefully
3. App connects to MCP servers with valid config
4. Tools are called during debates (visible in console)
5. Tool logs are created with detailed information
6. App works with both OpenAI and OpenRouter
7. App cleans up connections properly on exit
8. Multiple MCP servers can run simultaneously

## Next Steps

After successful testing:

- Experiment with different MCP servers
- Try debates on topics requiring current information
- Review tool logs to understand model behavior
- Share your setup in the project repository!

---

**Found an issue?** Check [docs/MCP_GUIDE.md](MCP_GUIDE.md) troubleshooting section.
