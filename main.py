import sys
import time

from ui import App

def main():
    if sys.platform.startswith('win'):
        from windows import WindowsMouseController
        mouse = WindowsMouseController()
    else:
        raise NotImplementedError("This OS is not supported yet.")

    # Create and run the application
    app = App(mouse)
    app.run()

if __name__ == "__main__":
    main()