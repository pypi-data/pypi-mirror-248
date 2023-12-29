from dataclasses import dataclass


@dataclass
class Human:
    name: str
    age: int

humans = [
    Human("Lena", 20),
    Human("Marcel", 21),
    Human("Pascal", 20),
    Human("Nahee", 20),
    Human("Laurenz", 21),
    Human("Anni", 21),
    Human("Benni", 21),
    Human("Amelie", 18),
]