from ui import App
import customtkinter
import logging
import os

if __name__ == "__main__":
    customtkinter.set_default_color_theme("green")
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
    app = App()
    app.mainloop()
