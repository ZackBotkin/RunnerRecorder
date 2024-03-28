from interactive_menu.src.interactive_menu import InteractiveMenu

class BackupMenu(InteractiveMenu):
    
    def __init__(self, manager, path):
        super().__init__(manager, path)

    def title(self):
        return "Backup"

    def main_loop(self):
        print("Coming soon! Backups!")
