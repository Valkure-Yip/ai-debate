# JSON Configuration - Quick Reference

## Quick Start

```bash
# 1. Create a config file
cp config.template.json my_debate.json

# 2. Edit it with your settings
nano my_debate.json

# 3. Run your debate
python debate.py --config my_debate.json
```

## JSON Parameter Names

| CLI Argument             | JSON Key               | Example Value                 |
| ------------------------ | ---------------------- | ----------------------------- |
| `--config`               | (command-line only)    | `"config.json"`               |
| `--rounds`               | `rounds`               | `5`                           |
| `--topic`                | `topic`                | `"climate change"`            |
| `--debater1-provider`    | `debater1_provider`    | `"openai"`                    |
| `--debater1-model`       | `debater1_model`       | `"gpt-4o-mini"`               |
| `--debater1-base-url`    | `debater1_base_url`    | `"https://api.custom.com/v1"` |
| `--debater1-persona`     | `debater1_persona`     | `"You are..."`                |
| `--debater1-opening`     | `debater1_opening`     | `"I believe..."`              |
| `--debater1-temperature` | `debater1_temperature` | `0.7`                         |
| `--debater1-max-tokens`  | `debater1_max_tokens`  | `500`                         |
| `--debater2-*`           | `debater2_*`           | (same as debater1)            |

**Rule:** Replace hyphens with underscores when converting CLI args to JSON keys

## Configuration Priority

```
CLI Arguments > JSON Config > .env File > Defaults
(highest)                                  (lowest)
```

## Minimal Example

```json
{
  "rounds": 3,
  "topic": "artificial intelligence"
}
```

## Full Example

```json
{
  "rounds": 5,
  "topic": "universal basic income",
  "debater1_provider": "openai",
  "debater1_model": "gpt-4o-mini",
  "debater1_persona": "You are an advocate for UBI...",
  "debater1_opening": "UBI will solve poverty...",
  "debater1_temperature": 0.7,
  "debater1_max_tokens": 500,
  "debater2_provider": "openai",
  "debater2_model": "gpt-4o-mini",
  "debater2_persona": "You oppose UBI...",
  "debater2_opening": "UBI is too expensive...",
  "debater2_temperature": 0.7,
  "debater2_max_tokens": 500
}
```

## Common Use Cases

### Override just the rounds

```bash
python debate.py --config my_config.json --rounds 10
```

### Override the model

```bash
python debate.py --config my_config.json --debater1-model gpt-4o
```

### Use different configs for different debates

```bash
python debate.py --config configs/philosophy.json
python debate.py --config configs/economics.json
python debate.py --config configs/technology.json
```

## Important Notes

- All JSON parameters are **optional**
- Use **underscores** in JSON (`debater1_model`), **hyphens** in CLI (`--debater1-model`)
- **Never** put API keys in JSON files - keep them in `.env`
- JSON files are safe to commit to git (unlike `.env`)

## See Full Documentation

- **Detailed Guide**: [docs/JSON_CONFIG_GUIDE.md](docs/JSON_CONFIG_GUIDE.md)
- **Implementation**: [docs/JSON_CONFIG_IMPLEMENTATION.md](docs/JSON_CONFIG_IMPLEMENTATION.md)
- **Main README**: [README.md](README.md)
