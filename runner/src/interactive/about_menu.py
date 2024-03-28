from interactive_menu.src.interactive_menu import InteractiveMenu

class AboutMenu(InteractiveMenu):
    
    def __init__(self, manager, path):
        super().__init__(manager, path)

    def title(self):
        return "About"

    def main_loop(self):
        print("Runner reader. Version 2.0") ## TODO no hardcode
