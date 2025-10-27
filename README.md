# AI Debate Application

A command-line Python application that orchestrates debates between two Large Language Model (LLM) instances. Watch as two AI models engage in structured, multi-round debates on any topic you choose!

Based on the article: [How to Make Two AIs Argue: Building a Real-Time Debate Between LLMs](https://medium.com/@aisgandy/title-how-to-make-two-ais-argue-building-a-real-time-debate-between-llms-d591a7900db1)

## Features

- ✅ Support for **OpenAI** and **OpenRouter** APIs
- ✅ Customizable base URLs for any OpenAI-compatible endpoint
- ✅ **MCP (Model Context Protocol)** integration for tool access
- ✅ Web search capabilities via Tavily MCP server
- ✅ Extensible tool system - add any MCP server
- ✅ Default capitalism debate with full customization options
- ✅ Configurable number of debate rounds
- ✅ Custom debate topics and personas
- ✅ Model parameter tuning (temperature, max tokens)
- ✅ Clean command-line interface with formatted output
- ✅ Detailed tool call logging

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys and Models

You have three ways to configure the application:

#### Option 1: Environment Variables (Recommended for API keys)

Create a `.env` file in the project root. You can start with the template:

```bash
cp env.template .env
nano .env  # Edit with your settings
```

**Minimal configuration (API keys only):**

```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Recommended configuration (with default models):**

```bash
# API Keys (only add the ones you need)
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-api-key-here

# Default Model Configuration (optional)
DEBATER1_PROVIDER=openai
DEBATER1_MODEL=gpt-4o-mini
DEBATER2_PROVIDER=openrouter
DEBATER2_MODEL=anthropic/claude-3-haiku
```

**Note:** You only need the API keys for the providers you plan to use.

#### Option 2: JSON Configuration File (Recommended for debate configurations)

For managing multiple debate configurations, create a JSON config file:

```bash
cp config.template.json my_debate_config.json
nano my_debate_config.json  # Edit with your settings
```

**Example JSON configuration:**

```json
{
  "rounds": 8,
  "topic": "artificial intelligence safety",
  "common_persona": "You are participating in a formal debate. Present well-reasoned arguments, respond to your opponent's points, and maintain a respectful yet assertive tone.",
  "debater1_provider": "openai",
  "debater1_model": "gpt-4o-mini",
  "debater1_persona": "You are a cautious AI safety researcher...",
  "debater1_opening": "AI development is outpacing safety measures",
  "debater1_temperature": 0.8,
  "debater1_max_tokens": 500,
  "debater2_provider": "openrouter",
  "debater2_model": "anthropic/claude-3-haiku",
  "debater2_persona": "You are an optimistic technologist...",
  "debater2_opening": "AI is humanity's greatest tool",
  "debater2_temperature": 0.7,
  "debater2_max_tokens": 500
}
```

**Benefits of JSON configuration:**

- Save and reuse complete debate setups
- Easy to share debate configurations
- Cleaner than long command-line arguments
- Can still override specific settings via CLI

**See [docs/JSON_CONFIG_GUIDE.md](docs/JSON_CONFIG_GUIDE.md) for detailed JSON configuration documentation.**

#### Option 3: Command-Line Arguments

Pass all settings directly via command line (see Usage section below).

### 4. Configure MCP Tools (Optional)

MCP (Model Context Protocol) allows debaters to use external tools like web search during debates.

**Quick setup for Tavily web search:**

1. Get a free API key from [Tavily](https://tavily.com/)
2. Create MCP configuration:
   ```bash
   cp mcp_config.template.json mcp_config.json
   ```
3. Edit `mcp_config.json` and add your Tavily API key:
   ```json
   {
     "servers": {
       "tavily": {
         "command": "npx",
         "args": [
           "-y",
           "mcp-remote",
           "https://mcp.tavily.com/mcp/?tavilyApiKey=tvly-your-api-key-here"
         ],
         "env": {
           "TAVILY_API_KEY": "tvly-your-api-key-here"
         }
       }
     }
   }
   ```
   **Note:** Replace `tvly-your-api-key-here` with your actual API key in both the URL and env section.
4. Ensure Node.js is installed: `node --version` (v16+ required)

**Benefits:**

- Debaters can search for current facts and statistics
- Real-time information enhances debate quality
- Automatically cited sources

**See [docs/MCP_GUIDE.md](docs/MCP_GUIDE.md) for detailed configuration and adding more tools.**

## Usage

### Basic Usage

If you configured models in `.env`, simply run:

```bash
python debate.py
```

This will use your configured providers and models from `.env` (or defaults if not set).

**With MCP tools enabled:**

- Debaters automatically access tools when needed
- Tool usage appears as: `🔧 [Debater 1] Using tool: tavily_search`
- Detailed logs saved to `logs/debate_tools_TIMESTAMP.log`

### Using JSON Configuration File

Run a debate with a saved configuration:

```bash
python debate.py --config my_debate_config.json
```

Override specific settings from the JSON file:

```bash
# Use JSON config but change number of rounds
python debate.py --config my_debate_config.json --rounds 10

# Use JSON config but change one debater's model
python debate.py --config my_debate_config.json --debater1-model gpt-4o
```

### Custom Number of Rounds

```bash
python debate.py --rounds 10
```

### Custom Debate Topic

```bash
python debate.py --topic "climate change" \
  --debater1-opening "Climate change is an existential threat requiring immediate action" \
  --debater2-opening "Climate policies must balance environmental and economic concerns"
```

### Use OpenRouter for a Debater

```bash
python debate.py --debater2-provider openrouter \
  --debater2-model anthropic/claude-3-haiku
```

### Custom Base URL

For using custom OpenAI-compatible endpoints:

```bash
python debate.py --debater1-base-url https://api.custom-endpoint.com/v1
```

### Full Customization Example (Command-Line)

```bash
python debate.py \
  --rounds 8 \
  --topic "artificial intelligence" \
  --debater1-provider openai \
  --debater1-model gpt-4o-mini \
  --debater1-persona "You are a cautious AI safety researcher who warns about AI risks" \
  --debater1-opening "AI development is outpacing our ability to ensure safety" \
  --debater1-temperature 0.8 \
  --debater2-provider openrouter \
  --debater2-model anthropic/claude-3-haiku \
  --debater2-persona "You are an optimistic technologist who believes in AI benefits" \
  --debater2-opening "AI is humanity's greatest tool for solving global challenges" \
  --debater2-temperature 0.7
```

## Command-Line Arguments

### Configuration File

- `--config, -c`: Path to JSON configuration file (optional)

### Debate Configuration

- `--rounds, -r`: Number of debate rounds (default: 5)
- `--topic, -t`: Debate topic (default: "capitalism")
- `--common-persona`: Common instructions applied to both debaters' system prompts (optional)

### Debater 1 Configuration

- `--debater1-provider`: API provider - `openai` or `openrouter` (default: openai)
- `--debater1-model`: Model identifier (default: gpt-4o-mini)
- `--debater1-base-url`: Custom API base URL (optional)
- `--debater1-persona`: System prompt defining debater's stance
- `--debater1-opening`: Opening statement
- `--debater1-temperature`: Sampling temperature 0.0-2.0 (default: 0.7)
- `--debater1-max-tokens`: Maximum response length (default: 500)

### Debater 2 Configuration

- `--debater2-provider`: API provider - `openai` or `openrouter` (default: openai)
- `--debater2-model`: Model identifier (default: gpt-4o-mini)
- `--debater2-base-url`: Custom API base URL (optional)
- `--debater2-persona`: System prompt defining debater's stance
- `--debater2-opening`: Opening statement
- `--debater2-temperature`: Sampling temperature 0.0-2.0 (default: 0.7)
- `--debater2-max-tokens`: Maximum response length (default: 500)

## Configuration Priority

Settings are loaded in this order (later overrides earlier):

1. **Hardcoded defaults** - `openai` provider, `gpt-4o-mini` model
2. **`.env` file** - `DEBATER1_PROVIDER`, `DEBATER1_MODEL`, etc.
3. **JSON config file** - Settings from `--config` file (if specified)
4. **Command-line arguments** - `--debater1-provider`, `--debater1-model`, etc. (highest priority)

**Examples:**

```bash
# Example 1: .env + CLI override
# .env file contains:
DEBATER1_PROVIDER=openai
DEBATER1_MODEL=gpt-4o-mini

# This command overrides debater1's model but keeps the provider from .env:
python debate.py --debater1-model gpt-4o
# Result: Uses openai/gpt-4o (provider from .env, model from CLI)
```

```bash
# Example 2: JSON + CLI override
# config.json contains:
{
  "rounds": 8,
  "debater1_model": "gpt-4o-mini",
  "debater2_model": "gpt-4o"
}

# This command uses JSON config but overrides the rounds:
python debate.py --config config.json --rounds 3
# Result: Uses 3 rounds (from CLI), gpt-4o-mini and gpt-4o (from JSON)
```

```bash
# Example 3: Full precedence chain
# .env file contains:
DEBATER1_MODEL=gpt-3.5-turbo

# config.json contains:
{
  "debater1_model": "gpt-4o-mini"
}

# Command:
python debate.py --config config.json --debater1-model gpt-4o
# Result: Uses gpt-4o (CLI > JSON > .env)
```

This allows you to:

- Store API keys in `.env` (secure, not committed to git)
- Save debate configurations in JSON files (shareable, version-controlled)
- Quickly override specific settings via CLI (experimentation)
- Reuse configurations without repeating long command lines

## Help

View all available options:

```bash
python debate.py --help
```

## Project Structure

```
ai-debate/
├── venv/                      # Virtual environment
├── .env                       # API keys (create from env.template)
├── config.template.json       # JSON configuration template
├── mcp_config.json           # MCP server configuration (create from template)
├── mcp_config.template.json  # MCP configuration template
├── requirements.txt          # Python dependencies
├── config.py                 # Configuration and argument parsing
├── debate.py                 # Main debate script
├── mcp_client.py             # MCP client for tool integration
├── logs/                     # Tool call logs (auto-created)
├── docs/                     # Documentation
│   ├── JSON_CONFIG_GUIDE.md # JSON configuration guide
│   ├── MCP_GUIDE.md         # Detailed MCP configuration guide
│   └── ...                   # Other documentation
└── README.md                 # This file
```

## How It Works

1. **Initialization**: Two `DebateModel` instances are created, each with its own:

   - API provider (OpenAI or OpenRouter)
   - Model selection
   - System prompt (persona)
   - Response parameters
   - Access to MCP tools (if configured)

2. **MCP Tool Connection**: If `mcp_config.json` exists:

   - Connect to configured MCP servers (e.g., Tavily for web search)
   - Load available tools and make them accessible to debaters

3. **Opening Statements**: Both debaters present their initial positions

4. **Debate Rounds**: For each round:

   - Debater 1 reads Debater 2's last message and responds
   - If needed, debater uses tools (web search, file access, etc.)
   - Debater 2 reads Debater 1's new response and counters
   - Tool calls are logged and displayed
   - All messages are tracked in conversation history

5. **Context Preservation**: Each model maintains its full conversation history, enabling coherent, context-aware responses throughout the debate

6. **Tool Enhancement**: Models automatically decide when to use tools based on their information needs

## Examples of Debate Topics

- **Philosophy**: "Is free will an illusion?"
- **Technology**: "Should AI development be regulated?"
- **Economics**: "Universal Basic Income vs traditional welfare"
- **Science**: "Space exploration vs ocean exploration funding"
- **Ethics**: "Privacy vs security in the digital age"

## API Providers

### OpenAI

- Models: `gpt-4o-mini`, `gpt-4o`, `gpt-3.5-turbo`, etc.
- Get API key: https://platform.openai.com/api-keys

### OpenRouter

- Unified interface to multiple LLM providers
- Models: `anthropic/claude-3-haiku`, `meta-llama/llama-3-8b`, `google/gemini-pro`, etc.
- Get API key: https://openrouter.ai/keys
- Browse models: https://openrouter.ai/models

## Tips for Great Debates

1. **Clear Personas**: Give each debater a distinct, well-defined stance
2. **Balanced Temperature**: 0.7-0.8 often works well for natural yet focused responses
3. **Strong Openings**: Craft opening statements that clearly establish each position
4. **Appropriate Length**: 5-10 rounds typically provides good depth without repetition
5. **Model Selection**: Try different model combinations to see varied debate styles

## Troubleshooting

### "API Key not found" Error

Make sure your `.env` file exists and contains the correct API key for your chosen provider.

### Connection Errors

- Verify your internet connection
- Check that your API keys are valid and have available credits
- For custom base URLs, ensure the endpoint is accessible

### Rate Limits

If you hit rate limits, try:

- Reducing the number of rounds
- Using different models (smaller/less popular ones often have higher limits)
- Adding delays between rounds (modify `debate.py` if needed)

### MCP Server Issues

**"MCP config file not found"**

- This is normal if you haven't configured MCP tools
- Create `mcp_config.json` from template to enable tools:
  ```bash
  cp mcp_config.template.json mcp_config.json
  ```

**"Failed to connect to 'tavily'"**

- Verify your Tavily API key in `mcp_config.json`
- Ensure Node.js is installed: `node --version` (requires v16+)
- Check network connectivity

**Tool calls slowing down debate**

- Tool execution (especially web search) takes time
- This is expected behavior
- Consider reducing rounds or max tokens for faster debates

**For detailed MCP troubleshooting**, see [docs/MCP_GUIDE.md](docs/MCP_GUIDE.md)

## Future Enhancements

Potential upgrades for this application:

- Web UI with real-time streaming
- Support for more than 2 debaters
- Audience voting and interaction
- Debate judging by a third AI
- Export debates to various formats (PDF, JSON, HTML)
- Visual debate flow diagrams
- Voice synthesis for audio debates
- Multi-language debate support

## License

This project is provided as-is for educational and experimental purposes.

## Credits

Inspired by the article by Joon Woo Park: [How to Make Two AIs Argue: Building a Real-Time Debate Between LLMs](https://medium.com/@aisgandy/title-how-to-make-two-ais-argue-building-a-real-time-debate-between-llms-d591a7900db1)
