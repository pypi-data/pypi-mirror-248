from tkinter import Tk
from .base import AdwBase
from .run import AdwRun


class AdwMainWindow(AdwBase, Tk):
    def __init__(self, *args, styles=None, title: str = "adwite", **kwargs):
        super().__init__(*args, **kwargs)

        self.protocol("WM_DELETE_WINDOW", self.quit)

        self.is_quit = None

        self.title(title)

        self.default_palette()

        from .style import WindowStyle

        self.windowstyle = WindowStyle(self)
        if styles:
            self.styles(styles)

        self.icon()

    def default_palette(self):
        pass

    def icon(self, dark=False):
        from .icon import PHOTOLIGHT, PHOTODARK
        if dark:
            self.iconphoto(False, PHOTODARK())
        else:
            self.iconphoto(False, PHOTOLIGHT())

    def palette(self, palette: dict):
        if "window" in palette:
            if "back" in palette["window"]:
                self.configure(background=palette["window"]["back"])

    def quit(self):
        self.is_quit = True
        self.destroy()

    def run(self):
        self.is_quit = False
        while not self.is_quit:
            self.update()

    def styles(self, names: list):
        """
        设置多个窗口样式

        Args:
            names (list): 样式名称
        """
        for style in names:
            self.windowstyle.style(style)
