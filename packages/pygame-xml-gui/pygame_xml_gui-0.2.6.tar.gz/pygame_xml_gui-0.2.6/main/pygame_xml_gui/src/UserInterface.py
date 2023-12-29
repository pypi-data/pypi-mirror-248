import io
import json
import os
import xml.sax
from xml.sax.xmlreader import InputSource

import PygameXtras as pe
import pygame
from .classes.errorHandler import ErrorHandler

from .classes.validator import Validator
from .files.schema.xml_schema import SCHEMA
from .classes.xmlHandler import XMLHandler
from .classes.styleInserter import StyleInserter
from .classes.sizeInserter import SizeInserter
from .classes.sourceInserter import SourceInserter
from .classes.guiMaker import GUIMaker


class UserInterface:
    def __init__(self):
        self.__structure_string = None
        self.__structure_widgets = None
        self.__raw_structure_widgets = None

        self.__background = None
        self.__background_color = None

        self.__widgets = None
        self.__variables = {}
        self.__methods = None

        self.__size = None
        self.__pos = (0, 0)
        self.__pos_given = (0, 0)
        self.__anchor = "center"
        self.__line_height = 30

        self.__classes_string = None
        self.__classes = None

        self.__initialized = False
    
    def __process_structure(self):
        
        # validate structure
        Validator(self.__structure_string, SCHEMA)

        # transform structure from xml to widgets
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        handler = XMLHandler()
        parser.setContentHandler(handler)
        inpsrc = InputSource()
        inpsrc.setCharacterStream(io.StringIO(self.__structure_string))
        parser.parse(inpsrc)

        # get structure
        widgets = handler.get_widget_structure()

        # store size
        self.__size = handler.get_size()

        # inject style
        StyleInserter(widgets, classes=self.__classes)

        # inject size
        SizeInserter(widgets, self.__line_height)

        self.__raw_structure_widgets = widgets.copy()

    def set_structure(self, path: str):
        """
        Imports the widget structure from a file.
        If you want to use classes, be sure to import them with self.set_classes before
        calling this method!

        'path' should be a string pointing to the xml file the structure is saved in.
        """

        if not os.path.exists(path):
            ErrorHandler.error("Path for structure file does not exist", info=os.path.abspath(path))
        if not os.path.isfile(path):
            ErrorHandler.error("Path for structure file is not a file", info=os.path.abspath(path))
        if not path.endswith(".xml"):
            ErrorHandler.error("Path for structure file does not point at an xml file", info=os.path.abspath(path))
        
        try:
            with open(path, "r") as f:
                self.__structure_string = f.read()
        except Exception as e:
            ErrorHandler.error(f"An error occurred while reading from the structure file at '{os.path.abspath(path)}'", info=e)

    def set_structure_from_string(self, structure: str):
        if not isinstance(structure, str):
            ErrorHandler.error("Given structure is not a string")
        self.__structure_string = structure

    def set_classes(self, path: str):
        """
        Imports the available styling classes from a file.

        'path' should be a string pointing to the json file the styling classes are saved in.
        """
        if not os.path.exists(path):
            ErrorHandler.error("Path for classes file does not exist", info=os.path.abspath(path))
        if not os.path.isfile(path):
            ErrorHandler.error("Path for classes file is not a file", info=os.path.abspath(path))
        if not path.endswith(".json"):
            ErrorHandler.error("Path for structure file does not point at a json file", info=os.path.abspath(path))

        try:
            with open(path, "r") as f:
                self.__classes_string = f.read()
        except Exception as e:
            ErrorHandler.error(f"An error occurred while reading from the classes file at '{os.path.abspath(path)}'", info=e)

    def set_classes_from_dict(self, classes: dict):
        if not isinstance(classes, dict):
            ErrorHandler.error("Given classes object is not a dict")
        self.__classes_string = str(classes).replace("'", '"')

    def __process_classes(self):
        try:
            self.__classes = json.loads(self.__classes_string)
        except Exception as e:
            ErrorHandler.error(f"An error occurred while interpreting the classes file", info=e)
        
        if not isinstance(self.__classes, dict):
            ErrorHandler.error("Content of classes file is not a dict", info=f"Type found: {type(self.__classes)}")

    def set_methods(self, methods: dict):
        # TODO: safety checks
        self.__methods = methods

    def __run_method(self, widget):
        if widget.info["pyAction"] is None:
            return
        # TODO: safety checks
        if (args := widget.info["pyArgs"]) != None:
            self.__methods[widget.info["pyAction"]](args)
        else:
            self.__methods[widget.info["pyAction"]]()

    def update(self, event_list, button: int = 1, offset: tuple = (0, 0)):
        """
        Update all buttons of the UI.
        """
        if not self.__initialized:
            ErrorHandler.error("Not initialized yet")

        real_offset = (offset[0] + self.__pos[0], offset[1] + self.__pos[1])
        for widget in self.__widgets:
            if isinstance(widget, pe.Button):
                if widget.update(event_list, button, real_offset):
                    self.__run_method(widget)

    def set_variables(self, variables: dict):
        """
        Sets the variables.
        """
        self.__variables = variables.copy()

    def set_line_height(self, height: int = 30):
        self.__line_height = height

    def refresh(self):
        """
        Creates the UI from the given structure, classes and variables.
        """
        if not self.__initialized:
            ErrorHandler.error("Not initialized yet")

        self.__structure_widgets = SourceInserter(self.__raw_structure_widgets, self.__variables).get_widgets()
        gm = GUIMaker(self.__structure_widgets)
        self.__entries_mapping = gm.get_entries_mapping()
        self.__widgets: list[pe.Label | pe.Button | pe.Entry] = gm.get_widgets()
        self.__background = pygame.Surface(gm.get_size())
        self.__background_color = gm.get_background_color()

        self.__apply_position()
    
    def __apply_position(self):
        r = pygame.Rect(0, 0, self.__size[0], self.__size[1])
        r.__setattr__(self.__anchor, self.__pos_given)
        self.__pos = r.topleft
    
    def get_entry(self, id: str) -> pe.Entry:
        if not self.__initialized:
            ErrorHandler.error("Not initialized yet")
        try:
            return self.__widgets[self.__entries_mapping[id]]
        except KeyError:
            ErrorHandler.error(f"Could not find any entry with id '{id}'", info=f"Keys found: {list(self.__entries_mapping.keys())}")

    def set_pos(self, pos: tuple[int, int], anchor: str = "center"):
        """
        Sets the position of the canvas.
        """
        if not isinstance(pos, (tuple, list)) or len(pos) != 2:
            ErrorHandler.error(f"invalid input for 'pos': {pos}")
        allowed = ("topleft", "midtop", "topright", "midright", "bottomright", "midbottom", "bottomleft", "midleft", "center")
        if anchor not in allowed:
            ErrorHandler.error(f"invalid input for 'anchor': {anchor}", info=f'possible values: {allowed}')

        self.__pos_given = pos
        self.__anchor = anchor

    def draw(self, screen: pygame.Surface):
        if not self.__initialized:
            ErrorHandler.error("Not initialized yet")
        # TODO: better draw method? technically only needs redraw if something changes...
        self.__background.fill(self.__background_color)
        for widget in self.__widgets:
            widget.draw_to(self.__background)
        screen.blit(self.__background, self.__pos)
    
    def get_rect(self):
        if not self.__initialized:
            ErrorHandler.error("Not initialized yet")
        return pygame.Rect(self.__pos[0], self.__pos[1], self.__background.get_width(), self.__background.get_height())

    def initialize(self):
        """
        Initializes the UI.
        Has to be called after all configurations and before updating or drawing.
        """
        if self.__initialized:
            ErrorHandler.error("Already initialized", info="If you want to refresh the widgets, use 'self.refresh()'")
        if self.__classes_string is not None:
            self.__process_classes()
        self.__process_structure()

        self.__initialized = True
        self.refresh()
    
    def is_initialized(self):
        return self.__initialized
    
    def has_classes_file(self):
        return self.__classes_string is not None
