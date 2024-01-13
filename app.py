from ui import App
import customtkinter
import logging
import os
import sys

if __name__ == "__main__":
    customtkinter.set_default_color_theme("green")
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")

    if sys.version_info < (3, 11):
        logging.error(msg=f"This script requires Python 3.11 or greater.  You are running Python {sys.version_info.major}.{sys.version_info.minor}.")
    else:
        app = App()
        app.mainloop()

