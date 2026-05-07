# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import json

from jupyter_server.base.handlers import APIHandler
import tornado

class McpServersHandler(APIHandler):
    """Handler for getting all configured MCP servers."""

    @tornado.web.authenticated
    def get(self):
        """Get all configured MCP servers."""
        manager = self.settings["mcp_manager"]
        if self.get_query_argument("reload", default=None):
            manager.clear_cache()
        settings = manager.get_settings()

        # Convert to JSON-serializable format
        servers = [server.model_dump() for server in settings.mcp_servers]

        self.finish(json.dumps({
            "mcp_servers": servers,
            "count": len(settings.mcp_servers)
        }))


class McpServerHandler(APIHandler):
    """Handler for getting a specific MCP server by name."""

    @tornado.web.authenticated
    def get(self, server_name: str):
        """Get a specific MCP server configuration by name."""
        manager = self.settings["mcp_manager"]
        server = manager.get_server_by_name(server_name)

        if server is None:
            self.set_status(404)
            self.finish(json.dumps({
                "error": f"MCP server '{server_name}' not found"
            }))
            return

        self.finish(json.dumps(server.model_dump()))
