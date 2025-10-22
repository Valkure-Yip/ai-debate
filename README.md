# AI Debate Application

A command-line Python application that orchestrates debates between two Large Language Model (LLM) instances. Watch as two AI models engage in structured, multi-round debates on any topic you choose!

Based on the article: [How to Make Two AIs Argue: Building a Real-Time Debate Between LLMs](https://medium.com/@aisgandy/title-how-to-make-two-ais-argue-building-a-real-time-debate-between-llms-d591a7900db1)

## Features

- ✅ Support for **OpenAI** and **OpenRouter** APIs
- ✅ Customizable base URLs for any OpenAI-compatible endpoint
- ✅ Default capitalism debate with full customization options
- ✅ Configurable number of debate rounds
- ✅ Custom debate topics and personas
- ✅ Model parameter tuning (temperature, max tokens)
- ✅ Clean command-line interface with formatted output

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

**Benefits of configuring models in .env:**

- No need to specify provider/model in CLI every time
- Easy to switch between favorite configurations
- CLI arguments can still override .env settings

**Note:** You only need the API keys for the providers you plan to use.

## Usage

### Basic Usage

If you configured models in `.env`, simply run:

```bash
python debate.py
```

This will use your configured providers and models from `.env` (or defaults if not set).

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

### Full Customization Example

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

### Debate Configuration

- `--rounds, -r`: Number of debate rounds (default: 5)
- `--topic, -t`: Debate topic (default: "capitalism")

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
3. **Command-line arguments** - `--debater1-provider`, `--debater1-model`, etc.

**Example:**

```bash
# .env file contains:
DEBATER1_PROVIDER=openai
DEBATER1_MODEL=gpt-4o-mini

# This command overrides debater1's model but keeps the provider from .env:
python debate.py --debater1-model gpt-4o
# Result: Uses openai/gpt-4o (provider from .env, model from CLI)
```

This allows you to:

- Set your preferred defaults in `.env`
- Quickly override specific settings via CLI
- Run different experiments without editing `.env`

## Help

View all available options:

```bash
python debate.py --help
```

## Project Structure

```
ai-debate/
├── venv/                # Virtual environment
├── .env                 # API keys (create from example)
├── requirements.txt     # Python dependencies
├── config.py           # Configuration and argument parsing
├── debate.py           # Main debate script
└── README.md           # This file
```

## How It Works

1. **Initialization**: Two `DebateModel` instances are created, each with its own:

   - API provider (OpenAI or OpenRouter)
   - Model selection
   - System prompt (persona)
   - Response parameters

2. **Opening Statements**: Both debaters present their initial positions

3. **Debate Rounds**: For each round:

   - Debater 1 reads Debater 2's last message and responds
   - Debater 2 reads Debater 1's new response and counters
   - All messages are tracked in conversation history

4. **Context Preservation**: Each model maintains its full conversation history, enabling coherent, context-aware responses throughout the debate

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

## Future Enhancements

Potential upgrades for this application:

- Web UI with real-time streaming
- Support for more than 2 debaters
- Audience voting and interaction
- Debate judging by a third AI
- Export debates to various formats (PDF, JSON, HTML)
- Visual debate flow diagrams

## License

This project is provided as-is for educational and experimental purposes.

## Credits

Inspired by the article by Joon Woo Park: [How to Make Two AIs Argue: Building a Real-Time Debate Between LLMs](https://medium.com/@aisgandy/title-how-to-make-two-ais-argue-building-a-real-time-debate-between-llms-d591a7900db1)
