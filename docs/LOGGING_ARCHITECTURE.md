# Logging Architecture

## Overview

The AI Debate application uses a modular logging system to capture both debate transcripts and tool call details. The logging functionality has been refactored into a separate module for better code organization and reusability.

## File Structure

```
ai-debate/
├── logger.py          # Logging module with all logger classes
├── debate.py          # Main debate application (imports loggers)
└── logs/              # Output directory for log files
    ├── debate_*.log           # Debate transcripts
    └── debate_tools_*.log     # Tool call logs
```

## Logger Classes

### BaseLogger (Abstract Base Class)

The `BaseLogger` class provides common functionality for all loggers:

- **File Management**: Creates log directory, generates timestamped filenames
- **Header Writing**: Standardized header format with metadata
- **Utility Methods**: Separators, flushing, closing
- **Extensibility**: Subclasses override specific methods as needed

### DebateLogger

Logs the complete debate transcript including:

- Debate topic and configuration
- Opening statements from both debaters
- All round-by-round exchanges with timestamps
- Conclusion and session metadata

**Output File**: `logs/debate_YYYYMMDD_HHMMSS.log`

**Key Methods**:

- `initialize()`: Set up log file with debate metadata
- `log_opening_statement(debater_name, statement)`: Log opening statements
- `log_round_header(round_num)`: Log round separators
- `log_message(debater_name, message)`: Log individual debate messages
- `log_conclusion()`: Log debate conclusion
- `close()`: Close and save the file

### ToolLogger

Logs MCP tool calls made by debaters:

- Tool name and arguments
- Execution results
- Timestamps for each call
- Formatted MCP response content

**Output File**: `logs/debate_tools_YYYYMMDD_HHMMSS.log`

**Key Methods**:

- `initialize()`: Set up tool call log file
- `log_tool_call(debater_name, tool_name, tool_args, result)`: Log tool execution
- `close()`: Close and save the file

## Benefits of the Refactoring

### Code Reusability

- Common logging patterns are implemented once in `BaseLogger`
- Both loggers inherit shared functionality
- Eliminates code duplication

### Maintainability

- Centralized logging logic in `logger.py`
- Easy to add new logger types by extending `BaseLogger`
- Changes to common functionality only need to be made once

### Separation of Concerns

- Logging logic is separated from debate orchestration
- `debate.py` focuses on debate logic, not logging implementation
- Clean imports: `from logger import DebateLogger, ToolLogger`

### Testability

- Logger classes can be tested independently
- Mock loggers can be easily created for testing
- Clear interfaces for each logger type

## Usage Example

```python
from logger import DebateLogger, ToolLogger

# Initialize debate logger
debate_logger = DebateLogger(topic="AI Ethics", rounds=5)
debate_logger.initialize()

# Log debate content
debate_logger.log_opening_statement("Debater 1", "AI ethics is crucial...")
debate_logger.log_round_header(1)
debate_logger.log_message("Debater 1", "In this round...")
debate_logger.log_conclusion()
debate_logger.close()

# Initialize tool logger (if MCP is enabled)
tool_logger = ToolLogger()
tool_logger.initialize()
tool_logger.log_tool_call("Debater 1", "web_search", {"query": "AI"}, result)
tool_logger.close()
```

## Future Enhancements

Potential improvements to the logging system:

1. **Structured Logging**: Add JSON/CSV output formats for analysis
2. **Log Levels**: Implement DEBUG, INFO, WARNING, ERROR levels
3. **Configuration**: Make log directory and format configurable
4. **Rotation**: Add log rotation for long-running sessions
5. **Statistics**: Add summary statistics at the end of logs
6. **Database Integration**: Option to log to a database instead of files

## Design Principles

The logging architecture follows these principles:

- **DRY (Don't Repeat Yourself)**: Common code is in the base class
- **Single Responsibility**: Each logger has one clear purpose
- **Open/Closed Principle**: Open for extension (new loggers), closed for modification
- **Inheritance Over Composition**: Loggers share behavior through inheritance
- **Clear Interfaces**: Simple, well-documented public methods
