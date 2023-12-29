import os

from pygame_xml_gui.src.UserInterfaceConstructor import UserInterfaceConstructor

wd = os.path.dirname(__file__)
PATH_XML = os.path.join(wd, "test_uic.xml")
PATH_JSON = os.path.join(wd, "test_uic.json")
PATH_SOURCE = os.path.join(wd, "test_uic_source.py")

uic = UserInterfaceConstructor()
uic.set_structure(PATH_XML)
uic.set_classes(PATH_JSON)
uic.set_source(PATH_SOURCE)
uic.set_refresh_interval(1)
uic.run()
