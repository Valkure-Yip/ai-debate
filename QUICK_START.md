# Quick Start Guide

Get your AI debate application up and running in minutes!

## Step 1: Set Up Virtual Environment

```bash
# Navigate to project directory
cd /Users/yezhitong/my-projects/ai-debate

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

## Step 2: Create .env File

Create a file named `.env` in the project root. You have several options:

### Option A: API Keys Only (Minimal Setup)

Just add the API key(s) you need:

```bash
# If you only have OpenAI:
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-actual-openai-key-here
EOF
```

```bash
# If you only have OpenRouter:
cat > .env << 'EOF'
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
EOF
```

### Option B: Configure Models in .env (Recommended)

Set your default models so you don't need CLI arguments each time:

```bash
# Copy the template
cp env.template .env

# Then edit with your keys and preferred models:
nano .env
```

**Example .env configurations:**

```bash
# Example 1: Both debaters use OpenAI
OPENAI_API_KEY=sk-your-key-here
DEBATER1_PROVIDER=openai
DEBATER1_MODEL=gpt-4o-mini
DEBATER2_PROVIDER=openai
DEBATER2_MODEL=gpt-3.5-turbo
```

```bash
# Example 2: Both use OpenRouter (only need one API key!)
OPENROUTER_API_KEY=sk-or-v1-your-key-here
DEBATER1_PROVIDER=openrouter
DEBATER1_MODEL=anthropic/claude-3-haiku
DEBATER2_PROVIDER=openrouter
DEBATER2_MODEL=meta-llama/llama-3-8b-instruct
```

```bash
# Example 3: Mix providers
OPENAI_API_KEY=sk-your-openai-key
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key
DEBATER1_PROVIDER=openai
DEBATER1_MODEL=gpt-4o-mini
DEBATER2_PROVIDER=openrouter
DEBATER2_MODEL=anthropic/claude-3-haiku
```

## Step 3: Run Your First Debate!

```bash
# If you configured models in .env, just run:
python debate.py

# Otherwise, specify provider/model via CLI:
python debate.py --debater1-provider openrouter --debater1-model anthropic/claude-3-haiku

# Customize rounds or topic:
python debate.py --rounds 3 --topic "artificial intelligence"

# CLI arguments override .env settings:
python debate.py --debater2-model gpt-4o  # Override debater 2's model
```

## Example Output

You'll see something like this:

```
================================================================================
🎭 AI DEBATE APPLICATION
================================================================================
Topic: capitalism
Rounds: 5
================================================================================

✓ Debater 1 initialized: openai/gpt-4o-mini
✓ Debater 2 initialized: openai/gpt-4o-mini

🎬 Starting debate...

================================================================================
🔵 Debater 1 (Opening Statement):
--------------------------------------------------------------------------------
Capitalism is a parasitic system that enriches a tiny elite while leaving
billions in poverty. It's collapsing under its own greed, and history will
remember it as a failure.

================================================================================
🔵 Debater 2 (Opening Statement):
--------------------------------------------------------------------------------
That's a tired cliché. Capitalism is why you're even able to type that message.
It's the only system that scales innovation, rewards merit, and evolves to meet
society's needs.

================================================================================
🔄 ROUND 1/5
================================================================================

[... debate continues ...]
```

## Common Commands

```bash
# View all options
python debate.py --help

# Short debate (3 rounds)
python debate.py --rounds 3

# Different topic
python debate.py --topic "space exploration"

# Use different models
python debate.py \
  --debater1-model gpt-4o \
  --debater2-provider openrouter \
  --debater2-model anthropic/claude-3-haiku
```

## Troubleshooting

### "API Key not found" Error

- Make sure your `.env` file exists in the project root
- Check that you've replaced `sk-your-openai-api-key-here` with your actual key
- Verify there are no extra spaces or quotes around the key

### Import Errors

- Make sure you've activated the virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

## Next Steps

- Read the full [README.md](README.md) for advanced usage
- Experiment with different debate topics
- Try mixing different models (OpenAI vs OpenRouter)
- Adjust temperature settings for more creative responses

Happy debating! 🎭
