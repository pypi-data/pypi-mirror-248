import os
import sys
import time
import pygame

from rich import print

from pygame_xml_gui.src.UserInterface import UserInterface
from pygame_xml_gui.src.classes.errorHandler import ErrorHandler


class UserInterfaceConstructor:
    def __init__(self):
        self.ui = UserInterface()

        self.__structure_path = None
        self.__classes_path = None
        self.__source_path = None
        self.__variabels = None

        # for refreshing
        self.__old_structure = ""
        self.__old_classes = ""
        self.__old_source = ""

        # either 'file' or 'vars'
        # exclusive, because that's easier to manage
        self.__source_mode = ""

        self.__space = 20
        self.__refresh_seconds = 1
        self.__background_color = (0, 0, 0)

    def __print(self, msg):
        print(f"[purple][CONSTRUCTOR] {msg}[/]")

    def set_structure(self, path: str):
        """
        Set the location of the structure file.
        This file should have the extension '.xml'.
        """
        if not os.path.exists(path):
            ErrorHandler.error(f"Given path '{path}' does not exist.")
        if not os.path.isfile(path):
            ErrorHandler.error(f"Given path '{path}' does not point to a file.")
        self.__structure_path = path

    def set_classes(self, path: str):
        """
        Set the location of the 'classes' file.
        This file should have the extension '.json'.
        """
        if not os.path.exists(path):
            ErrorHandler.error(f"Given path '{path}' does not exist.")
        if not os.path.isfile(path):
            ErrorHandler.error(f"Given path '{path}' does not point to a file.")
        if not path.endswith(".json"):
            ErrorHandler.error(f"Given path '{path}' is not a json file")
        self.__classes_path = path

    def set_source(self, path: str):
        """
        Set the location of the source file, from which the variables should be imported.
        This file should have the extension '.py' or '.pyw'.

        Sets the source mode to 'file'
        """
        if not os.path.exists(path):
            ErrorHandler.error(f"Given path '{path}' does not exist.")
        if not os.path.isfile(path):
            ErrorHandler.error(f"Given path '{path}' does not point to a file.")
        if not (path.endswith(".py") or path.endswith(".pyw")):
            ErrorHandler.error(f"Given path '{path}' is not a .py or .pyw file.")
        self.__source_path = path
        self.__source_mode = "file"

    def set_variables(self, variables: dict):
        """
        Set the variables.
        These can take any form, but the 'variabels' object has to be a dict.

        Sets the source mode to 'vars'.
        """
        if not isinstance(variables, dict):
            ErrorHandler.error(f"Given variables object is not of type dict", info=f"found object of type {type(variables)}")
        self.__variabels = variables
        self.__source_mode = "vars"
    
    def set_space(self, space: int):
        """
        Draw a black margin around the UI.
        """
        if space < 0:
            ErrorHandler.error(f"Space has to be greater than or equal to zero", info=f"given: {space}")
        self.__space = space

    def set_refresh_interval(self, seconds: float):
        """
        Set the time (in seconds) between refreshes.
        During a refresh, the given files are checked for changes and
        if any change is found the window will be reloaded.
        """
        if seconds < 0:
            ErrorHandler.error(f"Interval has to be greater than or equal to 0.5", info=f"given: {seconds}")
        self.__refresh_seconds = seconds

    def set_background_color(self, color: tuple[int, int, int]):
        """
        Set the background color.
        """
        self.__background_color = color

    def __refresh(self):
        if self.__classes_path is not None:
            self.ui.set_classes(self.__classes_path)

        if self.__source_mode == "file":
            variables = {}
            with open(self.__source_path, "r") as f:
                code = f.read()
            try:
                exec(
                    code,
                    None,
                    variables,
                )
            except Exception as e:
                ErrorHandler.error("Could not run source file", info=e)
            self.ui.set_variables(variables)
        elif self.__source_mode == "vars":
            self.ui.set_variables(self.__variabels)

        self.ui.set_structure(self.__structure_path)

        # little workaround to always trigger ui.__process_structure and ui.__process_classes
        self.ui._UserInterface__initialized = False
        self.ui.initialize()

        if self.ui.get_rect()[2] != self.__old["width"] or self.ui.get_rect()[3] != self.__old["height"]:
            self.__screen = pygame.display.set_mode((self.ui.get_rect()[2] + self.__space, self.ui.get_rect()[3] + self.__space))
            self.__center = self.__screen.get_rect()[2] // 2, self.__screen.get_rect()[3] // 2
            self.ui.set_pos(self.__center)
            # necessary for positioning
            self.ui.refresh()
            self.__old["width"] = self.__screen.get_rect()[2]
            self.__old["height"] = self.__screen.get_rect()[3]
    
    def __check_for_refresh(self) -> bool:
        """
        Refresh every self.__refresh_seconds seconds if:
            - structure file has been changed
            OR
            - classes file is used AND classes file has been changed
            OR
            - source file is used AND source file has been changed
        """

        if time.time() - self.__last_check < self.__refresh_seconds:
            return False

        structure_changed = False
        classes_changed = False
        source_changed = False

        # structure
        with open(self.__structure_path, "r") as f:
            new_structure = f.read()
        if self.__old_structure != new_structure:
            structure_changed = True
            self.__old_structure = new_structure
        
        # classes
        if self.__classes_path is not None:
            with open(self.__classes_path, "r") as f:
                new_classes = f.read()
            if self.__old_classes != new_classes:
                classes_changed = True
                self.__old_classes = new_classes
        
        if self.__source_path is not None and self.__source_mode == "file":
            with open(self.__source_path, "r") as f:
                new_source = f.read()
            if self.__old_source != new_source:
                source_changed = True
                self.__old_source = new_source

        self.__last_check = time.time()

        return (
            structure_changed or \
            (self.__classes_path is not None and classes_changed) or \
            (self.__source_path is not None and source_changed)
        )

    def run(self):
        """
        Runs the UserInterfaceConstructor.
        """
        if self.__structure_path == None:
            ErrorHandler.error("No structure file given")

        self.__old = {
            "width": -1,
            "height": -1
        }

        pygame.init()
        self.__screen = pygame.display.set_mode((100, 100))
        self.__fpsclock = pygame.time.Clock()
        self.__fps = 60
        self.__center = self.__screen.get_rect()[2] // 2, self.__screen.get_rect()[3] // 2
        pygame.display.set_caption("UserInterfaceConstructor")

        self.__last_check = time.time() - self.__refresh_seconds - 1
        self.__error = False
        
        run = True
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.__print("Stopping")
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__print("Stopping")
                        pygame.quit()
                        sys.exit()

            if self.__check_for_refresh():
                self.__print("Refreshing")
                self.__last_check = time.time()
                try:
                    self.__refresh()
                    self.__error = False
                    self.__print("[green]Success")
                except SystemExit:
                    self.__print("^ This error occurred during compilation ^")
                    self.__error = True

            self.__screen.fill(self.__background_color)
            if self.__error == False:
                self.ui.draw(self.__screen)

            pygame.display.flip()
            self.__fpsclock.tick(self.__fps)
