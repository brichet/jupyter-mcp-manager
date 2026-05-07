# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from jupyter_server.extension.application import ExtensionApp
from jupyter_server.utils import url_path_join
from traitlets import Bool, List, Unicode

from .mcp_manager import get_mcp_manager
from .handlers import (
    McpServerHandler,
    McpServersHandler,
)


class McpManagerExtension(ExtensionApp):
    """
    Jupyter Server extension for managing MCP servers.

    This extension provides REST API endpoints for:
    - Listing configured MCP servers
    - Getting specific server configurations
    - Reloading configuration
    """

    name = "jupyter_mcp_manager"
    extension_url = "/jupyter-mcp-manager"

    # Configuration traits
    enable_builtin_servers = Bool(
        True,
        help="Whether to include built-in MCP servers"
    ).tag(config=True)

    extra_config_paths = List(
        Unicode(),
        help="Additional config file paths to load"
    ).tag(config=True)

    def initialize_settings(self):
        """Initialize extension settings and create the MCP manager."""
        super().initialize_settings()

        # Built-in servers (defined in code, not as traits)
        builtin_servers = []
        if self.enable_builtin_servers:
            try:
                import jupyter_server_mcp  # noqa: F401
                builtin_servers = [{"name": "jupyter_server_mcp", "type": "http", "url": "http://localhost:8000"}]
            except ImportError:
                pass

        # Create manager once with extension config and store on server app settings
        manager = get_mcp_manager(
            log=self.log,
            extra_config_paths=self.extra_config_paths,
            builtin_servers=builtin_servers
        )
        self.serverapp.web_app.settings["mcp_manager"] = manager

    def initialize_handlers(self):
        """Register the API handlers."""
        super().initialize_handlers()

        base_url = self.serverapp.web_app.settings["base_url"]
        host_pattern = ".*$"

        # Define route patterns
        servers_route = url_path_join(base_url, "jupyter-mcp-manager", "servers")
        server_route = url_path_join(
            base_url, "jupyter-mcp-manager", "servers", "(?P<server_name>.+)"
        )

        handlers = [
            (servers_route, McpServersHandler),
            (server_route, McpServerHandler),
        ]

        self.serverapp.web_app.add_handlers(host_pattern, handlers)
        self.log.info(
            "Registered jupyter_mcp_manager extension with endpoints: "
            f"{servers_route}"
        )
