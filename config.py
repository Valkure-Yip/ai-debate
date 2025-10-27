"""
Configuration module for the AI debate application.
Handles argument parsing and default configurations.
"""

import argparse
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Default debate configurations
DEFAULT_TOPIC = "capitalism"

# Get model/provider defaults from .env or use hardcoded defaults
DEFAULT_DEBATER1_PROVIDER = os.getenv('DEBATER1_PROVIDER', 'openai')
DEFAULT_DEBATER1_MODEL = os.getenv('DEBATER1_MODEL', 'gpt-4o-mini')
DEFAULT_DEBATER2_PROVIDER = os.getenv('DEBATER2_PROVIDER', 'openai')
DEFAULT_DEBATER2_MODEL = os.getenv('DEBATER2_MODEL', 'gpt-4o-mini')

# Default common persona applied to all debaters
DEFAULT_COMMON_PERSONA = (
    "You are participating in a formal debate. "
    "Present well-reasoned arguments, respond to your opponent's points, "
    "and maintain a respectful yet assertive tone. "
    "Focus on logic, evidence, and persuasion. "
    "Present evidence-based arguments and respond directly to criticisms. You will use web search tools to find information to support your arguments whenever possible, and list relevant sources in your response."
    "Do not refer to or list any sources in your response unless you have used the web search tool to find the information."
)

DEFAULT_DEBATER1_PERSONA = (
    "You are a fiercely argumentative and critical debater who opposes capitalism. "
    "You believe capitalism is inherently exploitative, unsustainable, and the root of growing inequality. "
    "You challenge your opponent at every turn, dismantle pro-capitalist arguments with sharp logic, "
    "and never back down in a debate. Make sure your response is succinct and to the point."
)

DEFAULT_DEBATER2_PERSONA = (
    "You are a confident and assertive defender of capitalism. "
    "You believe capitalism is the most successful system in history, and you vigorously defend it. "
    "You counter every anti-capitalist point with strong arguments, facts, and dismiss emotional rhetoric. "
    "You debate with clarity, aggression, and conviction. Make sure your response is succinct and to the point."
)

DEFAULT_DEBATER1_OPENING = (
    "Capitalism is a parasitic system that enriches a tiny elite while leaving billions in poverty. "
    "It's collapsing under its own greed, and history will remember it as a failure."
)

DEFAULT_DEBATER2_OPENING = (
    "That's a tired cliché. Capitalism is why you're even able to type that message. "
    "It's the only system that scales innovation, rewards merit, and evolves to meet society's needs."
)

# Default model configurations
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 500
DEFAULT_ROUNDS = 5


def load_json_config(config_path):
    """Load configuration from a JSON file."""
    if not config_path:
        return {}
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")


def parse_arguments():
    """Parse command-line arguments with support for JSON config file.
    
    Precedence order (highest to lowest):
    1. Command-line arguments
    2. JSON config file
    3. Environment variables
    """
    # First, create a parser just to get the config file path
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument('--config', '-c', type=str, help='Path to JSON configuration file')
    pre_args, _ = pre_parser.parse_known_args()
    
    # Load JSON config if provided
    json_config = load_json_config(pre_args.config) if pre_args.config else {}
    
    # Helper function to get default value with precedence: JSON > ENV
    def get_default(json_key, env_default):
        """Get default value from JSON config or environment variable."""
        # Use underscore for nested keys in JSON (e.g., debater1_provider)
        return json_config.get(json_key, env_default)
    
    # Create the main parser
    parser = argparse.ArgumentParser(
        description="AI Debate Application - Let two LLM models debate with each other",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with defaults (5 rounds, capitalism debate)
  python debate.py
  
  # Use a JSON config file
  python debate.py --config config.json
  
  # Custom number of rounds
  python debate.py --rounds 10
  
  # Custom debate topic
  python debate.py --topic "climate change" --debater1-opening "Climate change is an existential threat" --debater2-opening "Climate policies hurt the economy"
  
  # Use OpenRouter for one debater
  python debate.py --debater2-provider openrouter --debater2-model anthropic/claude-3-haiku
  
  # Custom base URL
  python debate.py --debater1-base-url https://api.custom-endpoint.com/v1
  
  # Combine JSON config with command-line overrides
  python debate.py --config config.json --rounds 10
        """
    )
    
    # Configuration file
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Path to JSON configuration file'
    )
    
    # Debate configuration
    parser.add_argument(
        '--rounds', '-r',
        type=int,
        default=get_default('rounds', DEFAULT_ROUNDS),
        help=f'Number of debate rounds (default: {DEFAULT_ROUNDS})'
    )
    
    parser.add_argument(
        '--topic', '-t',
        type=str,
        default=get_default('topic', DEFAULT_TOPIC),
        help=f'Debate topic (default: "{DEFAULT_TOPIC}")'
    )
    
    parser.add_argument(
        '--common-persona',
        type=str,
        default=get_default('common_persona', DEFAULT_COMMON_PERSONA),
        help='Common persona/instructions applied to both debaters'
    )
    
    # Debater 1 configuration
    parser.add_argument(
        '--debater1-provider',
        type=str,
        choices=['openai', 'openrouter'],
        default=get_default('debater1_provider', DEFAULT_DEBATER1_PROVIDER),
        help=f'API provider for debater 1 (default: {DEFAULT_DEBATER1_PROVIDER})'
    )
    
    parser.add_argument(
        '--debater1-model',
        type=str,
        default=get_default('debater1_model', DEFAULT_DEBATER1_MODEL),
        help=f'Model name for debater 1 (default: {DEFAULT_DEBATER1_MODEL})'
    )
    
    parser.add_argument(
        '--debater1-base-url',
        type=str,
        default=get_default('debater1_base_url', None),
        help='Custom base URL for debater 1 (optional)'
    )
    
    parser.add_argument(
        '--debater1-persona',
        type=str,
        default=get_default('debater1_persona', DEFAULT_DEBATER1_PERSONA),
        help='System prompt/persona for debater 1'
    )
    
    parser.add_argument(
        '--debater1-opening',
        type=str,
        default=get_default('debater1_opening', DEFAULT_DEBATER1_OPENING),
        help='Opening statement for debater 1'
    )
    
    parser.add_argument(
        '--debater1-temperature',
        type=float,
        default=get_default('debater1_temperature', DEFAULT_TEMPERATURE),
        help=f'Temperature for debater 1 (default: {DEFAULT_TEMPERATURE})'
    )
    
    parser.add_argument(
        '--debater1-max-tokens',
        type=int,
        default=get_default('debater1_max_tokens', DEFAULT_MAX_TOKENS),
        help=f'Max tokens for debater 1 (default: {DEFAULT_MAX_TOKENS})'
    )
    
    # Debater 2 configuration
    parser.add_argument(
        '--debater2-provider',
        type=str,
        choices=['openai', 'openrouter'],
        default=get_default('debater2_provider', DEFAULT_DEBATER2_PROVIDER),
        help=f'API provider for debater 2 (default: {DEFAULT_DEBATER2_PROVIDER})'
    )
    
    parser.add_argument(
        '--debater2-model',
        type=str,
        default=get_default('debater2_model', DEFAULT_DEBATER2_MODEL),
        help=f'Model name for debater 2 (default: {DEFAULT_DEBATER2_MODEL})'
    )
    
    parser.add_argument(
        '--debater2-base-url',
        type=str,
        default=get_default('debater2_base_url', None),
        help='Custom base URL for debater 2 (optional)'
    )
    
    parser.add_argument(
        '--debater2-persona',
        type=str,
        default=get_default('debater2_persona', DEFAULT_DEBATER2_PERSONA),
        help='System prompt/persona for debater 2'
    )
    
    parser.add_argument(
        '--debater2-opening',
        type=str,
        default=get_default('debater2_opening', DEFAULT_DEBATER2_OPENING),
        help='Opening statement for debater 2'
    )
    
    parser.add_argument(
        '--debater2-temperature',
        type=float,
        default=get_default('debater2_temperature', DEFAULT_TEMPERATURE),
        help=f'Temperature for debater 2 (default: {DEFAULT_TEMPERATURE})'
    )
    
    parser.add_argument(
        '--debater2-max-tokens',
        type=int,
        default=get_default('debater2_max_tokens', DEFAULT_MAX_TOKENS),
        help=f'Max tokens for debater 2 (default: {DEFAULT_MAX_TOKENS})'
    )
    
    return parser.parse_args()


def get_api_key(provider):
    """Get API key for the specified provider."""
    if provider == 'openai':
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return api_key
    elif provider == 'openrouter':
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        return api_key
    else:
        raise ValueError(f"Unknown provider: {provider}")


def get_base_url(provider, custom_base_url=None):
    """Get base URL for the specified provider."""
    if custom_base_url:
        return custom_base_url
    
    if provider == 'openrouter':
        return "https://openrouter.ai/api/v1"
    
    # For OpenAI, return None to use the default
    return None

