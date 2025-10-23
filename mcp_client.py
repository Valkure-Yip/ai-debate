"""
MCP Client Module
Manages connections to MCP servers and tool execution for the debate application.
"""

import asyncio
import json
import os
from typing import Optional, Dict, List, Any
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPManager:
    """Manages MCP server connections and tool execution."""
    
    def __init__(self, config_path: str = "mcp_config.json"):
        """
        Initialize the MCP Manager.
        
        Args:
            config_path: Path to the MCP configuration JSON file
        """
        self.config_path = config_path
        self.servers: Dict[str, Dict[str, Any]] = {}
        self.sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()
        self.tools_map: Dict[str, str] = {}  # Maps tool name to server name
        self.all_tools: List[Dict] = []
        
    def load_config(self) -> Dict[str, Any]:
        """
        Load MCP server configuration from JSON file.
        
        Returns:
            Dict containing server configurations
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        if not os.path.exists(self.config_path):
            print(f"⚠️  MCP config file not found: {self.config_path}")
            print("   MCP tools will not be available. Create mcp_config.json from template to enable.")
            return {"servers": {}}
        
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        return config
    
    async def connect_servers(self) -> bool:
        """
        Connect to all configured MCP servers.
        
        Returns:
            bool: True if at least one server connected successfully, False otherwise
        """
        config = self.load_config()
        servers_config = config.get("servers", {})
        
        if not servers_config:
            print("ℹ️  No MCP servers configured.")
            return False
        
        print(f"\n🔌 Connecting to {len(servers_config)} MCP server(s)...")
        
        connected_count = 0
        for server_name, server_config in servers_config.items():
            try:
                await self._connect_server(server_name, server_config)
                connected_count += 1
                print(f"   ✓ Connected to '{server_name}'")
            except Exception as e:
                print(f"   ✗ Failed to connect to '{server_name}': {str(e)}")
        
        if connected_count > 0:
            print(f"✓ {connected_count}/{len(servers_config)} MCP server(s) connected successfully\n")
            return True
        else:
            print("⚠️  No MCP servers could be connected. Tools will not be available.\n")
            return False
    
    async def _connect_server(self, server_name: str, config: Dict[str, Any]):
        """
        Connect to a single MCP server.
        
        Args:
            server_name: Name identifier for the server
            config: Server configuration dict with command, args, env
        """
        # Prepare server parameters
        server_params = StdioServerParameters(
            command=config["command"],
            args=config.get("args", []),
            env=config.get("env", None)
        )
        
        # Create stdio transport
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        stdio, write = stdio_transport
        
        # Create and initialize session
        session = await self.exit_stack.enter_async_context(
            ClientSession(stdio, write)
        )
        await session.initialize()
        
        # Store session
        self.sessions[server_name] = session
        self.servers[server_name] = config
        
        # Get available tools from this server
        response = await session.list_tools()
        
        # Convert tools to OpenAI format and track which server owns each tool
        for tool in response.tools:
            converted_tool = self._convert_tool_format(tool)
            self.all_tools.append(converted_tool)
            self.tools_map[tool.name] = server_name
    
    def _convert_tool_format(self, tool) -> Dict[str, Any]:
        """
        Convert MCP tool definition to OpenAI-compatible format.
        
        Args:
            tool: MCP tool definition
            
        Returns:
            Dict in OpenAI tool format
        """
        converted_tool = {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": tool.inputSchema.get("properties", {}),
                    "required": tool.inputSchema.get("required", [])
                }
            }
        }
        return converted_tool
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get all available tools in OpenAI-compatible format.
        
        Returns:
            List of tool definitions
        """
        return self.all_tools
    
    async def execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Any:
        """
        Execute a tool call through the appropriate MCP server.
        
        Args:
            tool_name: Name of the tool to execute
            tool_args: Arguments to pass to the tool
            
        Returns:
            Tool execution result
            
        Raises:
            ValueError: If tool or server not found
            Exception: If tool execution fails
        """
        # Find which server owns this tool
        server_name = self.tools_map.get(tool_name)
        if not server_name:
            raise ValueError(f"Tool '{tool_name}' not found in any connected server")
        
        session = self.sessions.get(server_name)
        if not session:
            raise ValueError(f"Server '{server_name}' not connected")
        
        # Execute the tool
        result = await session.call_tool(tool_name, tool_args)
        return result
    
    async def cleanup(self):
        """Close all MCP server connections."""
        await self.exit_stack.aclose()
        print("\n🔌 MCP connections closed")
    
    def has_tools(self) -> bool:
        """Check if any tools are available."""
        return len(self.all_tools) > 0

