#!/usr/bin/env python3
"""
AI Debate Application
Orchestrates debates between two LLM models using OpenAI or OpenRouter APIs.
Supports MCP (Model Context Protocol) tools for enhanced capabilities.
"""

import sys
import asyncio
import json
import os
from datetime import datetime
from openai import OpenAI
from config import (
    parse_arguments,
    get_api_key,
    get_base_url
)
from mcp_client import MCPManager


class ToolLogger:
    """Handles logging of tool calls to a file."""
    
    def __init__(self):
        """Initialize the tool logger."""
        self.log_file = None
        self.log_path = None
        
    def initialize(self):
        """Create logs directory and log file."""
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = f"logs/debate_tools_{timestamp}.log"
        self.log_file = open(self.log_path, 'w', encoding='utf-8')
        
        # Write header
        self.log_file.write("=" * 80 + "\n")
        self.log_file.write("AI Debate - Tool Call Log\n")
        self.log_file.write(f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.log_file.write("=" * 80 + "\n\n")
        self.log_file.flush()
        
    def log_tool_call(self, debater_name, tool_name, tool_args, result):
        """
        Log a tool call with details.
        
        Args:
            debater_name: Name of the debater making the call
            tool_name: Name of the tool called
            tool_args: Arguments passed to the tool
            result: Result from the tool execution
        """
        if not self.log_file:
            return
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.log_file.write(f"[{timestamp}] {debater_name}\n")
        self.log_file.write("-" * 80 + "\n")
        self.log_file.write(f"Tool: {tool_name}\n")
        self.log_file.write(f"Arguments:\n{json.dumps(tool_args, indent=2)}\n")
        self.log_file.write("Result:\n")
        
        # Format MCP result for logging
        try:
            if hasattr(result, 'content'):
                # Handle MCP content which can be a list of content items
                if isinstance(result.content, list):
                    for i, item in enumerate(result.content):
                        if hasattr(item, 'text'):
                            self.log_file.write(f"  Content[{i}] (text):\n")
                            self.log_file.write(f"    {item.text}\n")
                        elif hasattr(item, '__dict__'):
                            self.log_file.write(f"  Content[{i}]:\n")
                            self.log_file.write(f"    {json.dumps(item.__dict__, indent=4, default=str)}\n")
                        else:
                            self.log_file.write(f"  Content[{i}]: {str(item)}\n")
                else:
                    self.log_file.write(f"  {json.dumps(result.content, indent=2, default=str)}\n")
            else:
                # Fallback for non-standard result objects
                self.log_file.write(f"  {json.dumps(result.__dict__ if hasattr(result, '__dict__') else str(result), indent=2, default=str)}\n")
        except Exception as e:
            self.log_file.write(f"  [Error formatting result: {str(e)}]\n")
            self.log_file.write(f"  Raw result: {str(result)}\n")
        
        self.log_file.write("=" * 80 + "\n\n")
        self.log_file.flush()
        
    def close(self):
        """Close the log file."""
        if self.log_file:
            self.log_file.write(f"\nSession ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.log_file.close()
            if self.log_path:
                print(f"\n📝 Tool call log saved to: {self.log_path}")


class DebateModel:
    """Handles LLM API calls and message history for a debater."""
    
    def __init__(self, name, provider, model, base_url, api_key, 
                 system_prompt, temperature, max_tokens, mcp_manager=None, tool_logger=None):
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
            mcp_manager: Optional MCP manager for tool access
            tool_logger: Optional tool logger for logging tool calls
        """
        self.name = name
        self.provider = provider
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.messages = []
        self.mcp_manager = mcp_manager
        self.tool_logger = tool_logger
        
        # Initialize OpenAI client (works for both OpenAI and OpenRouter)
        client_kwargs = {'api_key': api_key}
        if base_url:
            client_kwargs['base_url'] = base_url
        
        self.client = OpenAI(**client_kwargs)
        
        print(f"✓ {self.name} initialized: {provider}/{model}")
    
    def add_message(self, role, content):
        """Add a message to the conversation history."""
        self.messages.append({"role": role, "content": content})
    
    async def generate_response(self):
        """
        Generate a response based on the current conversation history.
        Supports tool calling if MCP manager is available.
        
        Returns:
            str: The model's response
        """
        # Build the full message list with system prompt
        full_messages = [{"role": "system", "content": self.system_prompt}]
        full_messages.extend(self.messages)
        
        try:
            # Get available tools if MCP is enabled
            tools = None
            if self.mcp_manager and self.mcp_manager.has_tools():
                tools = self.mcp_manager.get_available_tools()
            
            # Call the API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                tools=tools if tools else None
            )
            
            response_message = completion.choices[0].message
            
            # Check if model wants to use tools
            if response_message.tool_calls:
                # Handle tool calls
                response = await self._handle_tool_calls(response_message, full_messages)
            else:
                response = response_message.content
            
            # Add the assistant's response to history
            self.add_message("assistant", response)
            
            return response
            
        except Exception as e:
            error_msg = f"Error generating response from {self.name}: {str(e)}"
            print(f"\n❌ {error_msg}", file=sys.stderr)
            raise
    
    async def _handle_tool_calls(self, response_message, full_messages):
        """
        Handle tool calls from the model.
        
        Args:
            response_message: The message containing tool calls
            full_messages: The full conversation history
            
        Returns:
            str: Final response after tool execution
        """
        # Add the assistant's message with tool calls to history
        tool_call_message = {
            "role": "assistant",
            "content": response_message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in response_message.tool_calls
            ]
        }
        full_messages.append(tool_call_message)
        
        # Execute each tool call
        tool_results = []
        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
            
            # Display brief summary to console
            print(f"   🔧 [{self.name}] Using tool: {tool_name}")
            
            try:
                # Execute tool through MCP
                result = await self.mcp_manager.execute_tool(tool_name, tool_args)
                
                # Log detailed tool call
                if self.tool_logger:
                    self.tool_logger.log_tool_call(self.name, tool_name, tool_args, result)
                
                # Format result for API
                result_content = result.content if hasattr(result, 'content') else str(result)
                if isinstance(result_content, list):
                    # Handle list of content items from MCP
                    result_text = "\n".join([
                        item.text if hasattr(item, 'text') else str(item) 
                        for item in result_content
                    ])
                else:
                    result_text = str(result_content)
                
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": result_text
                })
                
            except Exception as e:
                error_msg = f"Error executing tool {tool_name}: {str(e)}"
                print(f"   ⚠️  {error_msg}")
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": f"Error: {error_msg}"
                })
        
        # Add tool results to messages
        full_messages.extend(tool_results)
        
        # Get final response from model with tool results
        final_completion = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        return final_completion.choices[0].message.content


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


async def run_debate(args):
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
    
    # Initialize MCP Manager
    mcp_manager = MCPManager()
    mcp_connected = await mcp_manager.connect_servers()
    
    # Initialize tool logger if MCP is enabled
    tool_logger = None
    if mcp_connected:
        tool_logger = ToolLogger()
        tool_logger.initialize()
        print(f"📝 Tool call logging enabled\n")
    
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
            max_tokens=args.debater1_max_tokens,
            mcp_manager=mcp_manager if mcp_connected else None,
            tool_logger=tool_logger
        )
        
        debater2 = DebateModel(
            name="Debater 2",
            provider=args.debater2_provider,
            model=args.debater2_model,
            base_url=get_base_url(args.debater2_provider, args.debater2_base_url),
            api_key=get_api_key(args.debater2_provider),
            system_prompt=args.debater2_persona,
            temperature=args.debater2_temperature,
            max_tokens=args.debater2_max_tokens,
            mcp_manager=mcp_manager if mcp_connected else None,
            tool_logger=tool_logger
        )
    except Exception as e:
        print(f"\n❌ Initialization error: {e}", file=sys.stderr)
        print("\nPlease ensure your .env file contains the required API keys:", file=sys.stderr)
        print("  - OPENAI_API_KEY (for OpenAI)", file=sys.stderr)
        print("  - OPENROUTER_API_KEY (for OpenRouter)", file=sys.stderr)
        await mcp_manager.cleanup()
        if tool_logger:
            tool_logger.close()
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
            response1 = await debater1.generate_response()
            print_message("Debater 1", response1)
            
            # Debater 2 responds to Debater 1's new message
            debater2.add_message("user", response1)
            response2 = await debater2.generate_response()
            print_message("Debater 2", response2)
            
        except Exception as e:
            print(f"\n❌ Debate stopped due to error in round {round_num}", file=sys.stderr)
            await mcp_manager.cleanup()
            if tool_logger:
                tool_logger.close()
            sys.exit(1)
    
    # Debate conclusion
    print_separator("=")
    print("🏁 DEBATE CONCLUDED")
    print_separator("=")
    print(f"Total rounds completed: {args.rounds}")
    print(f"Thank you for watching this AI debate on {args.topic}!")
    print()
    
    # Cleanup
    await mcp_manager.cleanup()
    if tool_logger:
        tool_logger.close()


def main():
    """Main entry point for the debate application."""
    try:
        args = parse_arguments()
        asyncio.run(run_debate(args))
    except KeyboardInterrupt:
        print("\n\n⚠️  Debate interrupted by user. Exiting...\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
