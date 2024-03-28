from interactive_menu.src.interactive_menu import InteractiveMenu

class ConfigMenu(InteractiveMenu):
    
    def __init__(self, manager, path):
        super().__init__(manager, path)

    def title(self):
        return "Config"

    def main_loop(self):
        print("Coming soon! Configs!")
