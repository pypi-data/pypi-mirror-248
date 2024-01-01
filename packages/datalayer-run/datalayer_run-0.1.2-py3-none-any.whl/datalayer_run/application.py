import sys
import warnings
from pathlib import Path

from datalayer.application import NoStart

from ._version import __version__
from .application_base import DatalayerRunBaseApp
from .app.operator_app import RunApp


HERE = Path(__file__).parent


class ConfigExportApp(DatalayerRunBaseApp):
    """An application to export the configuration."""

    description = """
      An application to export the configuration
    """

    def initialize(self, *args, **kwargs):
        """Initialize the app."""
        super().initialize(*args, **kwargs)

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for workspace export.")
            self.exit(1)
        self.log.info("ConfigApp %s", self.version)


class ConfigApp(DatalayerRunBaseApp):
    """A config app."""

    description = """
    Manage the configuration.
    """

    subcommands = {}
    subcommands["export"] = (
        ConfigExportApp,
        ConfigExportApp.description.splitlines()[0],
    )

    def start(self):
        try:
            super().start()
            self.log.error(f"One of `{'`, `'.join(ConfigApp.subcommands.keys())}` must be specified.")
            self.exit(1)
        except NoStart:
            pass
        self.exit(0)


class ShellApp(DatalayerRunBaseApp):
    """A shell application."""

    description = """
      Run predefined scripts.
    """

    def start(self):
        super().start()
        args = sys.argv
        self.log.info(args)


class DatalayerRunApp(DatalayerRunBaseApp):
    description = """
      The DatalayerRun application.
    """

    subcommands = {
        "config": (ConfigApp, ConfigApp.description.splitlines()[0]),
        "router": (RunApp, RunApp.description.splitlines()[0]),
        "sh": (ShellApp, ShellApp.description.splitlines()[0]),
    }

    def initialize(self, argv=None):
        """Subclass because the ExtensionApp.initialize() method does not take arguments."""
        super().initialize()

    def start(self):
        super(DatalayerRunApp, self).start()
        self.log.info("DatalayerRun - Version %s - Cloud %s ", self.version, self.cloud)


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = DatalayerRunApp.launch_instance

if __name__ == "__main__":
    main()
