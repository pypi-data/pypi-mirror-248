import os

from pygame_xml_gui.src.classes.errorHandler import ErrorHandler
from .widget import Widget


class SourceReader:
    """
    SourceReader only needs to run if the GUI is being tested with example
    data from a file. In production, the local variables will be supplied
    by the parent program.
    """

    def __init__(self, widgets: list[Widget]):
        self.__widgets = widgets
        self.__sanity_check()
        self.__source = self.__widgets[0].attributes.get("pySource", None)
        self.__vars = {}
        self.__import_source()
    
    def get_variables(self):
        return self.__vars

    def __sanity_check(self):
        assert len(self.__widgets) == 1
        assert self.__widgets[0].name == "canvas"

    def __import_source(self):
        if self.__source == None:
            return

        # checking for errors
        s = os.path.abspath(self.__source)
        if not os.path.exists(s):
            ErrorHandler.error(f"Source file does not exist", info=s)
        if not os.path.isfile(s):
            ErrorHandler.error(f"Given source file is not a path", info=s)
        if not (str(s).endswith(".py") or str(s).endswith(".pyw")):
            ErrorHandler.error(f"Given source file has to be a python file (.py or .pyw)", info=s)

        # trying to load the variables
        try:
            with open(self.__source, "r") as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Could not find source file ('{self.__source}')")
        try:
            exec(
                "import warnings\nwarnings.filterwarnings('ignore')\n" + code,
                None,
                self.__vars,
            )
        except Exception as e:
            ErrorHandler.error("Error executing source file", info=e)
            # TODO: can i not just use this class in the UIC?
