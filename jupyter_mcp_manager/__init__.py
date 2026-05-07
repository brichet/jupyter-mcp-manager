try:
    from ._version import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip. It is highly recommended to install
    # the package from a stable release or in editable mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    import warnings
    warnings.warn("Importing 'jupyter_mcp_manager' outside a proper installation.")
    __version__ = "dev"

from .mcp_manager import (
    McpServerManager,
    get_mcp_manager,
)
from .models import (
    McpSettings,
    McpServerStdio,
    McpServerHttp,
    EnvVariable,
    HttpHeader,
)
from .extension import McpManagerExtension


def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "jupyter-mcp-manager"
    }]


def _jupyter_server_extension_points():
    return [{"module": "jupyter_mcp_manager", "app": McpManagerExtension}]
