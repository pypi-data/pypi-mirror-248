import json
import os

from pygame_xml_gui.src.files.paths import STYLE_FOLDER


class StyleImporter:
    """
    This class adds all styles it finds in STYLE_FOLDER to its list and makes them 
    available through the method self.get_style(name).
    The styles are named after the filenames, without the file ending ("abc.json" -> "abc").
    """

    def __init__(self):
        assert os.path.exists(STYLE_FOLDER) and os.path.isdir(STYLE_FOLDER)

        self.__styles: dict[dict] = {}

        for file in os.scandir(STYLE_FOLDER):
            with open(file.path, "r") as f:
                style: dict = json.load(f)
                assert any((
                    "label" in style.keys(),
                    "button" in style.keys(),
                    "entry" in style.keys()
                )), f"invalid form of pyStyle file '{file.name}'"
            name = file.name.removesuffix(".json")

            self.__styles[name] = style

    def get_styles(self) -> list[str]:
        return list(self.__styles.keys())

    def get_style(self, name) -> dict:
        return self.__styles[name]
