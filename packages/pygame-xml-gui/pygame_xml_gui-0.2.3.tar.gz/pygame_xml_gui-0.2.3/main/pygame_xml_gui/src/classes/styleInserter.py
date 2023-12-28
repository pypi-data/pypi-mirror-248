from pygame_xml_gui.src.classes.errorHandler import ErrorHandler
from pygame_xml_gui.src.classes.styleImporter import StyleImporter

from .widget import Widget

class StyleInserter:
    def __init__(self, widgets: list[Widget], classes: dict = None):
        self.__widgets = widgets

        self.__classes: dict = classes

        self.__sanity_check()

        styleImporter = StyleImporter()

        self.__canvas_style_name = self.__widgets[0].attributes.get("pyStyle", "default")
        if self.__canvas_style_name not in styleImporter.get_styles():
            ErrorHandler.error(f"Unknown pyStyle: '{self.__canvas_style_name}'", info=f"Known styles: {list(styleImporter.get_styles())}")
        self.__canvas_style = styleImporter.get_style(self.__canvas_style_name)

        self.__run()

    def __sanity_check(self):
        assert len(self.__widgets) == 1
        assert self.__widgets[0].name == "canvas"
        if self.__classes is not None:
            assert isinstance(self.__classes, dict)

    def __run(self):
        self.__widgets = [
            self.__run_recursive(widget) for widget in self.__widgets
        ]

    def __run_recursive(self, widget: Widget):
        if widget.name in ["label", "button", "entry"]:
            return self.__get_widget_with_injected_style_attributes(widget)
        elif widget.name in ["canvas", "list", "list-item"]:
            return Widget(
                widget.name,
                widget.attributes,
                [
                    self.__run_recursive(item) for item in widget.content
                ]
            )

    def __get_widget_with_injected_style_attributes(self, widget: Widget) -> Widget:
        pyStyleDefault_attributes = self.__extract_pyStyleDefault(widget)
        pyClassDefault_attributes = self.__extract_pyClassDefault(widget)
        pyClass_attributes = self.__extract_pyClass(widget)
        pyStyle_attributes = self.__extract_pyStyle(widget)

        for k, v in pyStyleDefault_attributes.items():
            widget.attributes[k] = v
        
        for k, v in pyClassDefault_attributes.items():
            widget.attributes[k] = v

        for k, v in pyClass_attributes.items():
            widget.attributes[k] = v

        for k, v in pyStyle_attributes.items():
            widget.attributes[k] = v

        return Widget(widget.name, widget.attributes, widget.content)

    def __extract_pyStyle(self, widget: Widget):
        if "pyStyle" in widget.attributes.keys():
            styles_dict = {}
            string = widget.attributes["pyStyle"]
            styles = string.split(";")
            styles = [s.strip() for s in styles if s.strip() != ""]
            for style in styles:
                try:
                    key = style.split("=")[0]
                    value = eval(style.split("=")[1])
                    styles_dict[key] = value
                except NameError:
                    ErrorHandler.error(f"Could not interpret key-value pair: {style}", info="Maybe you forgot quotation marks or a semicolon?")
                except:
                    ErrorHandler.error(f"Could not interpret key-value pair: {style}")
            return styles_dict
        return {}
    
    def __extract_pyClass(self, widget: Widget) -> dict:
        if "pyClass" in widget.attributes.keys():
            if self.__classes is None:
                ErrorHandler.error("Using pyClass without specifing a class file")
            styles_dict = {}
            string = widget.attributes["pyClass"]
            classes = string.split(" ")
            classes = [s.strip() for s in classes if s.strip() != ""]
            for class_ in classes:
                if class_ not in self.__classes.keys():
                    ErrorHandler.error(f"unknown class: {class_}", info=f"known classes: {list(self.__classes.keys())}")
                try:
                    for k, v in self.__classes[class_].items():
                        styles_dict[k] = v
                except Exception:
                    ErrorHandler.error(f"Could not copy attributes of class '{class_}' into widget")
            return styles_dict
        return {}

    def __extract_pyClassDefault(self, widget: Widget):
        """
        returns styles for any style classes named after widgets (label, button, entry)
        """
        if self.__classes is not None and widget.name in self.__classes.keys():
            styles_dict = {}
            try:
                for k, v in self.__classes[widget.name].items():
                    styles_dict[k] = v
            except Exception:
                ErrorHandler.error(f"Could not copy attributes of class '{widget.name}' into widget")
            return styles_dict
        return {}

    def __extract_pyStyleDefault(self, widget: Widget):
        if widget.name in self.__canvas_style.keys():
            styles_dict = {}
            # no error checking, because styles are preset by developer of pygame_xml_gui,
            # so no error should occur
            for k, v in self.__canvas_style[widget.name].items():
                styles_dict[k] = v
            return styles_dict
        return {}
