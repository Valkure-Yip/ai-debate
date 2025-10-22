#!/usr/bin/env python3
"""
AI Debate Application
Orchestrates debates between two LLM models using OpenAI or OpenRouter APIs.
"""

import sys
from openai import OpenAI
from config import (
    parse_arguments,
    get_api_key,
    get_base_url
)


class DebateModel:
    """Handles LLM API calls and message history for a debater."""
    
    def __init__(self, name, provider, model, base_url, api_key, 
                 system_prompt, temperature, max_tokens):
        """
        Initialize a debate model.
        
        Args:
            name: Display name for this debater
            provider: API provider ('openai' or 'openrouter')
            model: Model identifier
            base_url: Custom base URL (or None for default)
            api_key: API key for authentication
            system_prompt: System message defining the debater's persona
            temperature: Sampling temperature for responses
            max_tokens: Maximum tokens in response
        """
        self.name = name
        self.provider = provider
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.messages = []
        
        # Initialize OpenAI client (works for both OpenAI and OpenRouter)
        client_kwargs = {'api_key': api_key}
        if base_url:
            client_kwargs['base_url'] = base_url
        
        self.client = OpenAI(**client_kwargs)
        
        print(f"✓ {self.name} initialized: {provider}/{model}")
    
    def add_message(self, role, content):
        """Add a message to the conversation history."""
        self.messages.append({"role": role, "content": content})
    
    def generate_response(self):
        """
        Generate a response based on the current conversation history.
        
        Returns:
            str: The model's response
        """
        # Build the full message list with system prompt
        full_messages = [{"role": "system", "content": self.system_prompt}]
        full_messages.extend(self.messages)
        
        try:
            # Call the API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            response = completion.choices[0].message.content
            
            # Add the assistant's response to history
            self.add_message("assistant", response)
            
            return response
            
        except Exception as e:
            error_msg = f"Error generating response from {self.name}: {str(e)}"
            print(f"\n❌ {error_msg}", file=sys.stderr)
            raise


def print_separator(char="=", length=80):
    """Print a separator line."""
    print(char * length)


def print_message(debater_name, message, is_opening=False):
    """Print a formatted debate message."""
    print_separator()
    if is_opening:
        print(f"🔵 {debater_name} (Opening Statement):")
    else:
        print(f"🔵 {debater_name}:")
    print_separator("-")
    print(message)
    print()


def run_debate(args):
    """
    Run the debate between two models.
    
    Args:
        args: Parsed command-line arguments
    """
    print("\n" + "=" * 80)
    print("🎭 AI DEBATE APPLICATION")
    print("=" * 80)
    print(f"Topic: {args.topic}")
    print(f"Rounds: {args.rounds}")
    print("=" * 80 + "\n")
    
    # Initialize debaters
    try:
        debater1 = DebateModel(
            name="Debater 1",
            provider=args.debater1_provider,
            model=args.debater1_model,
            base_url=get_base_url(args.debater1_provider, args.debater1_base_url),
            api_key=get_api_key(args.debater1_provider),
            system_prompt=args.debater1_persona,
            temperature=args.debater1_temperature,
            max_tokens=args.debater1_max_tokens
        )
        
        debater2 = DebateModel(
            name="Debater 2",
            provider=args.debater2_provider,
            model=args.debater2_model,
            base_url=get_base_url(args.debater2_provider, args.debater2_base_url),
            api_key=get_api_key(args.debater2_provider),
            system_prompt=args.debater2_persona,
            temperature=args.debater2_temperature,
            max_tokens=args.debater2_max_tokens
        )
    except Exception as e:
        print(f"\n❌ Initialization error: {e}", file=sys.stderr)
        print("\nPlease ensure your .env file contains the required API keys:", file=sys.stderr)
        print("  - OPENAI_API_KEY (for OpenAI)", file=sys.stderr)
        print("  - OPENROUTER_API_KEY (for OpenRouter)", file=sys.stderr)
        sys.exit(1)
    
    print("\n🎬 Starting debate...\n")
    
    # Print opening statements
    print_message("Debater 1", args.debater1_opening, is_opening=True)
    print_message("Debater 2", args.debater2_opening, is_opening=True)
    
    # Initialize message histories with opening statements
    debater1.add_message("assistant", args.debater1_opening)
    debater2.add_message("assistant", args.debater2_opening)
    
    # Run debate rounds
    for round_num in range(1, args.rounds + 1):
        print(f"\n{'=' * 80}")
        print(f"🔄 ROUND {round_num}/{args.rounds}")
        print(f"{'=' * 80}\n")
        
        try:
            # Debater 1 responds to Debater 2's last message
            debater1.add_message("user", debater2.messages[-1]["content"])
            response1 = debater1.generate_response()
            print_message("Debater 1", response1)
            
            # Debater 2 responds to Debater 1's new message
            debater2.add_message("user", response1)
            response2 = debater2.generate_response()
            print_message("Debater 2", response2)
            
        except Exception as e:
            print(f"\n❌ Debate stopped due to error in round {round_num}", file=sys.stderr)
            sys.exit(1)
    
    # Debate conclusion
    print_separator("=")
    print("🏁 DEBATE CONCLUDED")
    print_separator("=")
    print(f"Total rounds completed: {args.rounds}")
    print(f"Thank you for watching this AI debate on {args.topic}!")
    print()


def main():
    """Main entry point for the debate application."""
    try:
        args = parse_arguments()
        run_debate(args)
    except KeyboardInterrupt:
        print("\n\n⚠️  Debate interrupted by user. Exiting...\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

