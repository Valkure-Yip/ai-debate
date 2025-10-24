"""
Logging utilities for the AI debate application.
Provides logging for both debate transcripts and tool calls.
"""

import os
import json
from datetime import datetime


class BaseLogger:
    """Base class for logging with common functionality."""
    
    def __init__(self):
        """Initialize the base logger."""
        self.log_file = None
        self.log_path = None
        
    def _create_log_directory(self):
        """Create logs directory if it doesn't exist."""
        os.makedirs("logs", exist_ok=True)
        
    def _create_log_file(self, filename_prefix):
        """
        Create a log file with timestamp.
        
        Args:
            filename_prefix: Prefix for the log filename
            
        Returns:
            str: Path to the created log file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = f"logs/{filename_prefix}_{timestamp}.log"
        return log_path
        
    def _write_header(self, title, **metadata):
        """
        Write a standard header to the log file.
        
        Args:
            title: Title for the log file
            **metadata: Additional metadata to include in the header
        """
        if not self.log_file:
            return
            
        self.log_file.write("=" * 80 + "\n")
        self.log_file.write(f"{title}\n")
        self.log_file.write("=" * 80 + "\n")
        
        for key, value in metadata.items():
            # Convert snake_case to Title Case for display
            display_key = key.replace('_', ' ').title()
            self.log_file.write(f"{display_key}: {value}\n")
            
        self.log_file.write(f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.log_file.write("=" * 80 + "\n\n")
        self.log_file.flush()
        
    def _write_separator(self, char="=", length=80):
        """Write a separator line."""
        if self.log_file:
            self.log_file.write(char * length + "\n")
            
    def _flush(self):
        """Flush the log file buffer."""
        if self.log_file:
            self.log_file.flush()
            
    def close(self):
        """Close the log file with end timestamp."""
        if self.log_file:
            self.log_file.write(f"\nSession ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.log_file.close()
            if self.log_path:
                self._print_close_message()
                
    def _print_close_message(self):
        """Print a message when the log file is closed. Override in subclasses."""
        print(f"📝 Log saved to: {self.log_path}")


class DebateLogger(BaseLogger):
    """Handles logging of the debate transcript to a file."""
    
    def __init__(self, topic, rounds):
        """
        Initialize the debate logger.
        
        Args:
            topic: The debate topic
            rounds: Number of debate rounds
        """
        super().__init__()
        self.topic = topic
        self.rounds = rounds
        
    def initialize(self):
        """Create logs directory and log file."""
        self._create_log_directory()
        self.log_path = self._create_log_file("debate")
        self.log_file = open(self.log_path, 'w', encoding='utf-8')
        self._write_header(
            "AI DEBATE TRANSCRIPT",
            topic=self.topic,
            total_rounds=self.rounds
        )
        
    def log_opening_statement(self, debater_name, statement):
        """
        Log an opening statement.
        
        Args:
            debater_name: Name of the debater
            statement: Opening statement text
        """
        if not self.log_file:
            return
            
        self._write_separator("=")
        self.log_file.write(f"{debater_name} (Opening Statement):\n")
        self._write_separator("-")
        self.log_file.write(f"{statement}\n\n")
        self._flush()
        
    def log_round_header(self, round_num):
        """
        Log a round header.
        
        Args:
            round_num: Round number
        """
        if not self.log_file:
            return
            
        self.log_file.write("\n")
        self._write_separator("=")
        self.log_file.write(f"ROUND {round_num}/{self.rounds}\n")
        self._write_separator("=")
        self.log_file.write("\n")
        self._flush()
        
    def log_message(self, debater_name, message):
        """
        Log a debate message.
        
        Args:
            debater_name: Name of the debater
            message: Message text
        """
        if not self.log_file:
            return
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._write_separator("=")
        self.log_file.write(f"[{timestamp}] {debater_name}:\n")
        self._write_separator("-")
        self.log_file.write(f"{message}\n\n")
        self._flush()
        
    def log_conclusion(self):
        """Log the debate conclusion."""
        if not self.log_file:
            return
            
        self._write_separator("=")
        self.log_file.write("DEBATE CONCLUDED\n")
        self._write_separator("=")
        self.log_file.write(f"Total rounds completed: {self.rounds}\n")
        self.log_file.write(f"Session ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self._flush()
        
    def _print_close_message(self):
        """Print a message when the log file is closed."""
        print(f"📄 Debate transcript saved to: {self.log_path}")


class ToolLogger(BaseLogger):
    """Handles logging of tool calls to a file."""
    
    def initialize(self):
        """Create logs directory and log file."""
        self._create_log_directory()
        self.log_path = self._create_log_file("debate_tools")
        self.log_file = open(self.log_path, 'w', encoding='utf-8')
        self._write_header("AI Debate - Tool Call Log")
        
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
        self._write_separator("-")
        self.log_file.write(f"Tool: {tool_name}\n")
        self.log_file.write(f"Arguments:\n{json.dumps(tool_args, indent=2)}\n")
        self.log_file.write("Result:\n")
        
        # Format MCP result for logging
        self._format_tool_result(result)
        
        self._write_separator("=")
        self.log_file.write("\n")
        self._flush()
        
    def _format_tool_result(self, result):
        """
        Format and write tool result to log file.
        
        Args:
            result: Result object from tool execution
        """
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
                result_dict = result.__dict__ if hasattr(result, '__dict__') else str(result)
                self.log_file.write(f"  {json.dumps(result_dict, indent=2, default=str)}\n")
        except Exception as e:
            self.log_file.write(f"  [Error formatting result: {str(e)}]\n")
            self.log_file.write(f"  Raw result: {str(result)}\n")
            
    def _print_close_message(self):
        """Print a message when the log file is closed."""
        print(f"📝 Tool call log saved to: {self.log_path}")

