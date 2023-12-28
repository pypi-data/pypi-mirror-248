from pygame_xml_gui.src.classes.errorHandler import ErrorHandler
import xmlschema

class Validator:
    def __init__(self, structure, schema):
        """This class validates the form of the xml file and its structure.\nCommand: pyxg_validate_xml {path_to_file}"""

        self.structure = structure
        self.schema = schema

        self.check()

    def check(self):
        """Checks if the xml file is valid against the schema"""
        try:
            xmlschema.validate(self.structure, self.schema)
        except Exception as e:
            ErrorHandler.error("Error while checking xml file", info=e)
