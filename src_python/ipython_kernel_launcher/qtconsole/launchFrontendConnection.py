from jupyter_core.application import JupyterApp
from jupyter_client.consoleapp import (JupyterConsoleApp)
from qtconsole.client import QtKernelClient
from qtconsole.mainwindow import MainWindow
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from PyQt5.QtWidgets import QApplication
from traitlets.config.application import catch_config_error
from traitlets import (CBool, Any)

class MyJupyterQtConsoleAppInProgress(JupyterApp, JupyterConsoleApp):

    display_banner = CBool(True, config=True,
        help="Whether to display a banner upon starting the QtConsole."
    )
    
    widget_factory = Any(RichJupyterWidget)

    def new_frontend_connection(self, connection_file):
        """Create and return a new frontend attached to an existing kernel.

        Parameters
        ----------
        connection_file : str
            The connection_file path this frontend is to connect to
        """
        kernel_client = QtKernelClient(
            connection_file=connection_file,
            #config=self.config,
        )
        kernel_client.load_connection_file('/home/jfricou/.local/share/jupyter/runtime/kernel-' +
            '66865' + '.json')
        kernel_client.start_channels()
        widget = self.widget_factory(local_kernel=False) #, config=self.config)
                                     
        #self.init_colors(widget)
        widget._existing = True
        widget._may_close = False
        widget._confirm_exit = False
        widget._display_banner = self.display_banner
        widget.kernel_client = kernel_client
        widget.kernel_manager = None
        return widget

    def init_qt_elements(self):
        # Create the widget.

        self.widget = self.widget_factory(local_kernel=False #, config=self.config)
                                        )
        #self.init_colors(self.widget)
        self.widget._existing = True # self.existing
        self.widget._may_close = False # not self.existing
        self.widget._confirm_exit = False # self.confirm_exit
        self.widget._display_banner = True # self.display_banner

        self.widget.kernel_manager = self.kernel_manager
        self.widget.kernel_client = self.kernel_client
        self.window = MainWindow(self.app,
                                confirm_exit=self.confirm_exit,
                                new_frontend_factory=self.new_frontend_master_empty,
                                slave_frontend_factory=self.new_frontend_slave_empty,
                                connection_frontend_factory=self.new_frontend_connection,
                                )
        self.window.log = self.log
        self.window.add_tab_with_frontend(self.widget)
        self.window.init_menu_bar()

        self.window.setWindowTitle('Jupyter QtConsole')

    def new_frontend_master_empty():
        print("new_frontend_master_empty")

    def new_frontend_slave_empty():
        print("new_frontend_slave_empty")

    @catch_config_error
    def initialize(self, argv=None):
        self.init_qt_app()
        super().initialize(argv)
        if self._dispatching:
            return
        # handle deprecated renames
        """ for old_name, new_name in [
            ('IPythonQtConsoleApp', 'JupyterQtConsole'),
            ('IPythonWidget', 'JupyterWidget'),
            ('RichIPythonWidget', 'RichJupyterWidget'),
        ]:
            cfg = self._deprecate_config(self.config, old_name, new_name)
            if cfg:
                self.update_config(cfg) """
        JupyterConsoleApp.initialize(self,argv)
        self.init_qt_elements()
        self.init_signal()

    def init_qt_app(self):
        # separate from qt_elements, because it must run first
        if QApplication.instance() is None:
            self.app = QApplication(['jupyter-qtconsole'])
            self.app.setApplicationName('jupyter-qtconsole')
        else:
            self.app = QApplication.instance()


def main():
    MyJupyterQtConsoleAppInProgress().launch_instance()
    """ console.initialize(argv=[])

    while 1:
        a = 0 """

    """ console.window.confirm_exit = False
    console.window.show()

    yield console

    console.window.close() """

if __name__ == "__main__" :
    main()


# new_frontend_connection = connection_frontend_factory
# in create_tab_with_existing_kernel

# in init_qt_elements : look for add_tab_with_frontend
# initialize in qtconsoleapp.py