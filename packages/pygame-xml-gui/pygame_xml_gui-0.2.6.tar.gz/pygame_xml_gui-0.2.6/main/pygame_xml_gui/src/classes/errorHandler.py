from rich import print

class ErrorHandler:
    @staticmethod
    def error(message: str, *, info: str = "", stop: bool = True):
        print(f"[red]ERROR:[white] {message}")
        if info != "":
            print(f"[green]INFO:[white]  {info}")
        if stop:
            raise SystemExit
