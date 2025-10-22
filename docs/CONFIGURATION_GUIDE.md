# Configuration Guide

## Overview

The AI Debate application now supports **three levels of configuration**:

1. **Hardcoded defaults** (fallback)
2. **`.env` file** (persistent settings)
3. **Command-line arguments** (override for specific runs)

This guide shows you how to configure models and providers flexibly.

---

## Quick Start Examples

### Example 1: OpenAI Only (Simplest)

**1. Create `.env` file:**

```bash
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-actual-openai-key-here
DEBATER1_PROVIDER=openai
DEBATER1_MODEL=gpt-4o-mini
DEBATER2_PROVIDER=openai
DEBATER2_MODEL=gpt-4o-mini
EOF
```

**2. Run debate:**

```bash
python debate.py
```

That's it! No CLI arguments needed.

---

### Example 2: OpenRouter Only

**1. Create `.env` file:**

```bash
cat > .env << 'EOF'
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
DEBATER1_PROVIDER=openrouter
DEBATER1_MODEL=anthropic/claude-3-haiku
DEBATER2_PROVIDER=openrouter
DEBATER2_MODEL=meta-llama/llama-3-8b-instruct
EOF
```

**2. Run debate:**

```bash
python debate.py
```

Now you're using Claude vs Llama with just one API key!

---

### Example 3: Mix Providers

**1. Create `.env` file:**

```bash
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-openai-key
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key
DEBATER1_PROVIDER=openai
DEBATER1_MODEL=gpt-4o-mini
DEBATER2_PROVIDER=openrouter
DEBATER2_MODEL=anthropic/claude-3-haiku
EOF
```

**2. Run debate:**

```bash
python debate.py
```

GPT-4o-mini debates Claude!

---

## Configuration Priority

Settings are applied in this order (later overrides earlier):

```
Hardcoded Defaults → .env File → CLI Arguments
```

### Example Walkthrough

**`.env` file contains:**

```bash
DEBATER1_PROVIDER=openai
DEBATER1_MODEL=gpt-4o-mini
DEBATER2_PROVIDER=openrouter
DEBATER2_MODEL=anthropic/claude-3-haiku
```

**Different command-line overrides:**

```bash
# Use all settings from .env
python debate.py

# Override just debater1's model (keeps provider=openai from .env)
python debate.py --debater1-model gpt-4o

# Override debater2 completely
python debate.py --debater2-provider openai --debater2-model gpt-3.5-turbo

# Override rounds and topic, keep models from .env
python debate.py --rounds 10 --topic "AI safety"
```

---

## Environment Variables Reference

### Required (at least one)

```bash
OPENAI_API_KEY=sk-...           # For OpenAI models
OPENROUTER_API_KEY=sk-or-v1-... # For OpenRouter models
```

You only need the key for the provider(s) you're using.

### Optional Model Configuration

```bash
# Debater 1
DEBATER1_PROVIDER=openai         # or: openrouter
DEBATER1_MODEL=gpt-4o-mini       # or any model name

# Debater 2
DEBATER2_PROVIDER=openai         # or: openrouter
DEBATER2_MODEL=gpt-4o-mini       # or any model name
```

If not set, defaults to `openai` / `gpt-4o-mini`.

---

## Popular Model Combinations

### OpenAI Models

```bash
DEBATER1_PROVIDER=openai
DEBATER1_MODEL=gpt-4o-mini       # Fast, cheap
# DEBATER1_MODEL=gpt-4o           # More capable
# DEBATER1_MODEL=gpt-3.5-turbo    # Budget option
```

### OpenRouter Models

```bash
DEBATER1_PROVIDER=openrouter

# Anthropic Claude
DEBATER1_MODEL=anthropic/claude-3-haiku
# DEBATER1_MODEL=anthropic/claude-3-sonnet
# DEBATER1_MODEL=anthropic/claude-3-opus

# Meta Llama
# DEBATER1_MODEL=meta-llama/llama-3-8b-instruct
# DEBATER1_MODEL=meta-llama/llama-3-70b-instruct

# Google Gemini
# DEBATER1_MODEL=google/gemini-pro
# DEBATER1_MODEL=google/gemini-flash-1.5

# Mistral
# DEBATER1_MODEL=mistralai/mistral-7b-instruct
```

Browse all models: https://openrouter.ai/models

---

## Use Cases

### 1. Development Setup

Set your favorite models in `.env` for quick testing:

```bash
DEBATER1_PROVIDER=openai
DEBATER1_MODEL=gpt-4o-mini
DEBATER2_PROVIDER=openai
DEBATER2_MODEL=gpt-4o-mini
```

Then just run: `python debate.py`

### 2. Multiple Configurations

Create different `.env` files:

```bash
cp .env .env.openai-only
cp .env .env.openrouter-only
cp .env .env.mixed

# Switch between them:
cp .env.openai-only .env
python debate.py
```

### 3. Experimentation

Keep your preferred setup in `.env`, override via CLI for experiments:

```bash
# Your .env has gpt-4o-mini for both
# Try GPT-4o for debater 1 without editing .env:
python debate.py --debater1-model gpt-4o
```

---

## Tips

### 💡 Only Add API Keys You Need

If you only use OpenRouter, you don't need to add `OPENAI_API_KEY` at all.

### 💡 Use `.env` for Convenience

Set your most-used configuration in `.env` so you can run:

```bash
python debate.py
```

instead of:

```bash
python debate.py --debater1-provider openrouter --debater1-model anthropic/claude-3-haiku --debater2-provider openrouter --debater2-model meta-llama/llama-3-8b-instruct
```

### 💡 CLI for Quick Tests

Keep your default setup in `.env`, use CLI args to try different models:

```bash
# Try GPT-4o just once without changing .env
python debate.py --debater1-model gpt-4o --rounds 3
```

### 💡 Check What You're Using

The application prints which models it initialized:

```
✓ Debater 1 initialized: openai/gpt-4o-mini
✓ Debater 2 initialized: openrouter/anthropic/claude-3-haiku
```

---

## Troubleshooting

### Error: "API Key not found"

**Problem:** The application can't find the API key for your configured provider.

**Solution:** Check that your `.env` file has the correct key:

```bash
# If using openai provider:
OPENAI_API_KEY=sk-...

# If using openrouter provider:
OPENROUTER_API_KEY=sk-or-v1-...
```

### Models from `.env` not being used

**Problem:** Application still uses default `gpt-4o-mini` despite `.env` config.

**Solution:**

1. Check `.env` is in the project root directory
2. Verify variable names are correct (e.g., `DEBATER1_MODEL` not `DEBATER_1_MODEL`)
3. No quotes around values: `DEBATER1_MODEL=gpt-4o` not `DEBATER1_MODEL="gpt-4o"`

### CLI arguments not overriding `.env`

**Problem:** This should work! If it doesn't, it's a bug.

**Check:** Run with `--help` to see current defaults:

```bash
python debate.py --help | grep "default:"
```

---

## Getting API Keys

### OpenAI

1. Go to: https://platform.openai.com/api-keys
2. Create new secret key
3. Copy it to your `.env` file
4. Make sure you have credits in your account

### OpenRouter

1. Go to: https://openrouter.ai/keys
2. Create API key
3. Copy it to your `.env` file
4. Add credits to your OpenRouter account: https://openrouter.ai/credits

---

## Summary

The new configuration system gives you:

✅ **Convenience** - Set defaults in `.env`, run without arguments  
✅ **Flexibility** - Override anything via CLI when needed  
✅ **Simplicity** - Only add API keys for providers you use  
✅ **Experimentation** - Test different models without editing config files

**Recommended workflow:**

1. Set your preferred models in `.env`
2. Run `python debate.py` for most debates
3. Use CLI arguments to try different configurations
4. Update `.env` when you find a setup you like

Happy debating! 🎭
