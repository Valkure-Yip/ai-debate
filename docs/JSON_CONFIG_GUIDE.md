# JSON Configuration Guide

This guide explains how to use JSON configuration files to manage debate settings in the AI Debate application.

## Overview

JSON configuration files provide a convenient way to:

- Save and reuse complete debate configurations
- Share debate setups with others
- Organize multiple debate scenarios
- Avoid long command-line arguments
- Version control your debate configurations

## Quick Start

1. **Create a config file from the template:**

   ```bash
   cp config.template.json my_debate.json
   ```

2. **Edit the configuration:**

   ```bash
   nano my_debate.json
   ```

3. **Run a debate with your config:**
   ```bash
   python debate.py --config my_debate.json
   ```

## Configuration File Format

A JSON configuration file can contain any or all of the following parameters:

```json
{
  "rounds": 5,
  "topic": "your debate topic",

  "debater1_provider": "openai",
  "debater1_model": "gpt-4o-mini",
  "debater1_base_url": null,
  "debater1_persona": "System prompt for debater 1",
  "debater1_opening": "Opening statement for debater 1",
  "debater1_temperature": 0.7,
  "debater1_max_tokens": 500,

  "debater2_provider": "openai",
  "debater2_model": "gpt-4o-mini",
  "debater2_base_url": null,
  "debater2_persona": "System prompt for debater 2",
  "debater2_opening": "Opening statement for debater 2",
  "debater2_temperature": 0.7,
  "debater2_max_tokens": 500
}
```

### Parameter Reference

| Parameter              | Type           | Description                                | Example                       |
| ---------------------- | -------------- | ------------------------------------------ | ----------------------------- |
| `rounds`               | integer        | Number of debate rounds                    | `5`                           |
| `topic`                | string         | Debate topic                               | `"climate change"`            |
| `debater1_provider`    | string         | API provider: `"openai"` or `"openrouter"` | `"openai"`                    |
| `debater1_model`       | string         | Model identifier                           | `"gpt-4o-mini"`               |
| `debater1_base_url`    | string or null | Custom API endpoint (optional)             | `"https://api.custom.com/v1"` |
| `debater1_persona`     | string         | System prompt defining stance              | `"You are a..."`              |
| `debater1_opening`     | string         | Opening statement                          | `"I believe..."`              |
| `debater1_temperature` | float          | Sampling temperature (0.0-2.0)             | `0.7`                         |
| `debater1_max_tokens`  | integer        | Maximum response length                    | `500`                         |
| `debater2_*`           | various        | Same parameters for debater 2              | -                             |

**Note:** All parameters are optional. Any parameter not specified in the JSON will fall back to environment variables or hardcoded defaults.

## Configuration Precedence

Settings are loaded in this order (later overrides earlier):

1. **Hardcoded defaults** - Built-in fallback values
2. **Environment variables** (.env file) - API keys and default models
3. **JSON config file** - Settings from `--config` file
4. **Command-line arguments** - Highest priority, overrides everything

### Precedence Examples

#### Example 1: Basic JSON Config

```json
// my_config.json
{
  "rounds": 8,
  "debater1_model": "gpt-4o-mini"
}
```

```bash
python debate.py --config my_config.json
```

Result:

- Uses 8 rounds (from JSON)
- Uses `gpt-4o-mini` for debater1 (from JSON)
- Other settings from .env or defaults

#### Example 2: JSON + CLI Override

```json
// my_config.json
{
  "rounds": 8,
  "topic": "AI safety"
}
```

```bash
python debate.py --config my_config.json --rounds 3
```

Result:

- Uses 3 rounds (CLI overrides JSON)
- Uses "AI safety" topic (from JSON)

#### Example 3: Full Chain (.env + JSON + CLI)

```bash
# .env
DEBATER1_MODEL=gpt-3.5-turbo
```

```json
// my_config.json
{
  "debater1_model": "gpt-4o-mini"
}
```

```bash
python debate.py --config my_config.json --debater1-model gpt-4o
```

Result:

- Uses `gpt-4o` (CLI wins over JSON and .env)

## Example Configurations

### Example 1: Quick 3-Round Debate

```json
{
  "rounds": 3,
  "topic": "cryptocurrency regulation",
  "debater1_opening": "Cryptocurrencies need strict regulation to protect investors and prevent crime.",
  "debater2_opening": "Excessive regulation will stifle innovation and financial freedom.",
  "debater1_max_tokens": 200,
  "debater2_max_tokens": 200
}
```

### Example 2: Philosophy Debate

```json
{
  "rounds": 6,
  "topic": "free will vs determinism",
  "debater1_provider": "openai",
  "debater1_model": "gpt-4o-mini",
  "debater1_persona": "You are a philosopher who argues for hard determinism. You believe all events, including human actions, are determined by prior causes. Challenge the notion of free will with logical arguments.",
  "debater1_opening": "Free will is an illusion. Every choice we make is the inevitable result of prior causes beyond our control.",
  "debater1_temperature": 0.8,
  "debater2_provider": "openai",
  "debater2_model": "gpt-4o-mini",
  "debater2_persona": "You are a philosopher who defends libertarian free will. You believe humans have genuine agency and can make choices independent of deterministic causes.",
  "debater2_opening": "We experience free will directly. Our ability to deliberate and choose between alternatives is real, not illusory.",
  "debater2_temperature": 0.8
}
```

### Example 3: Mixed Provider Debate

```json
{
  "rounds": 5,
  "topic": "space exploration priorities",
  "debater1_provider": "openai",
  "debater1_model": "gpt-4o-mini",
  "debater1_persona": "You advocate for Mars colonization as humanity's top space priority. Argue for the importance of becoming a multi-planetary species.",
  "debater1_opening": "Mars colonization is essential for humanity's long-term survival and should be our primary space focus.",
  "debater2_provider": "openrouter",
  "debater2_model": "anthropic/claude-3-haiku",
  "debater2_persona": "You believe we should focus on Earth orbit infrastructure and asteroid mining before Mars. Prioritize practical benefits over aspirational goals.",
  "debater2_opening": "We should master near-Earth space and solve Earth's problems before attempting Mars colonization."
}
```

## Best Practices

### 1. Organize Your Configurations

Create a `configs/` directory to organize different debate scenarios:

```bash
configs/
├── philosophy/
│   ├── free_will.json
│   └── ethics.json
├── technology/
│   ├── ai_safety.json
│   └── privacy.json
└── economics/
    ├── ubi.json
    └── capitalism.json
```

### 2. Use Descriptive Filenames

Good:

- `capitalism_vs_socialism.json`
- `ai_safety_3rounds.json`
- `climate_action_debate.json`

Avoid:

- `config1.json`
- `test.json`
- `debate.json`

### 3. Partial Configurations

You don't need to specify every parameter. Create minimal configs that override just what you need:

```json
{
  "rounds": 10,
  "topic": "nuclear energy"
}
```

This uses defaults/.env for everything else.

### 4. Template-Based Approach

Create base templates for different debate styles:

**quick_debate_template.json:**

```json
{
  "rounds": 3,
  "debater1_max_tokens": 200,
  "debater2_max_tokens": 200
}
```

**deep_debate_template.json:**

```json
{
  "rounds": 10,
  "debater1_temperature": 0.8,
  "debater2_temperature": 0.8,
  "debater1_max_tokens": 800,
  "debater2_max_tokens": 800
}
```

### 5. Version Control

Add your config files to git for sharing and tracking:

```bash
git add configs/*.json
git commit -m "Add debate configurations"
```

**Important:** Never commit `.env` files with API keys!

### 6. Comments in JSON

Standard JSON doesn't support comments, but you can add a `"_comment"` field:

```json
{
  "_comment": "Quick 3-round debate for testing new topics",
  "rounds": 3,
  "topic": "test topic"
}
```

## Troubleshooting

### Config File Not Found

```
FileNotFoundError: Config file not found: my_config.json
```

**Solution:** Check the file path. Use absolute paths or ensure you're running from the correct directory:

```bash
python debate.py --config configs/my_config.json
```

### Invalid JSON

```
ValueError: Invalid JSON in config file: ...
```

**Solution:** Validate your JSON:

1. Use a JSON validator online
2. Check for:
   - Missing commas
   - Trailing commas (not allowed in JSON)
   - Unquoted keys
   - Single quotes instead of double quotes

**Common mistakes:**

```json
{
  "rounds": 5, // No comments allowed!
  "topic": "test", // Use double quotes
  "debater1_model": "gpt-4o-mini" // No trailing comma before }
}
```

**Correct:**

```json
{
  "rounds": 5,
  "topic": "test",
  "debater1_model": "gpt-4o-mini"
}
```

### Parameter Not Working

If a parameter from your JSON isn't being used:

1. **Check spelling:** Parameter names use underscores: `debater1_model` (not `debater1-model`)
2. **Check case:** All lowercase: `debater1_provider` (not `Debater1_Provider`)
3. **Check CLI override:** Command-line arguments override JSON
4. **Check the full key:** Use `debater1_temperature`, not just `temperature`

### API Keys Not Found

JSON configs don't store API keys. You must have them in your `.env` file:

```bash
# .env
OPENAI_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-v1-...
```

## Advanced Usage

### Dynamic Configuration

Generate configs programmatically:

```python
import json

config = {
    "rounds": 5,
    "topic": "generated topic",
    "debater1_model": "gpt-4o-mini",
    "debater2_model": "gpt-4o-mini"
}

with open("generated_config.json", "w") as f:
    json.dump(config, f, indent=2)
```

Then run:

```bash
python debate.py --config generated_config.json
```

### Testing Multiple Configurations

Batch test different configurations:

```bash
for config in configs/*.json; do
    echo "Running debate with $config"
    python debate.py --config "$config"
done
```

### Environment-Specific Configs

Create configs for different environments:

- `config.dev.json` - Development with small models
- `config.prod.json` - Production with larger models
- `config.test.json` - Testing with minimal rounds

```bash
# Development
python debate.py --config config.dev.json

# Production
python debate.py --config config.prod.json
```

## Migration Guide

### From Command-Line to JSON

If you have a long command like this:

```bash
python debate.py \
  --rounds 8 \
  --topic "climate change" \
  --debater1-provider openai \
  --debater1-model gpt-4o-mini \
  --debater1-temperature 0.8 \
  --debater2-provider openrouter \
  --debater2-model anthropic/claude-3-haiku \
  --debater2-temperature 0.7
```

Convert it to a JSON config:

```json
{
  "rounds": 8,
  "topic": "climate change",
  "debater1_provider": "openai",
  "debater1_model": "gpt-4o-mini",
  "debater1_temperature": 0.8,
  "debater2_provider": "openrouter",
  "debater2_model": "anthropic/claude-3-haiku",
  "debater2_temperature": 0.7
}
```

**Note:** Replace hyphens with underscores: `--debater1-model` → `"debater1_model"`

## See Also

- [README.md](../README.md) - Main documentation
- [QUICK_START.md](QUICK_START.md) - Getting started guide
- [MCP_GUIDE.md](MCP_GUIDE.md) - MCP tools configuration

## Support

For issues or questions:

1. Check this guide
2. Verify your JSON syntax
3. Test with `config.template.json` first
4. Review the main README.md
