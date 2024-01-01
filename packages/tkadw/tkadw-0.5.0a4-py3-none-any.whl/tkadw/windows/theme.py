from os import environ


class AdwTheme():
    def __init__(self):
        self.theme = {}

    def configure(self, mode: str, id: str, sheet, var, state=None):
        if state:
            self.theme[mode][id][state][sheet] = var
        else:
            self.theme[mode][id][sheet] = var

    def get(self):
        return self.theme


class AdwWin11Theme(AdwTheme):
    def __init__(self):
        self.theme = {
            "light": {
                "window": {
                    "back": "#f4f4f4"
                },

                "button": {
                    "radius": 13,

                    "default": {
                        "back": "#fdfdfd",
                        "border": "#ededed",
                        "fore": "#202020",
                        "border_width": 1,
                    },

                    "active": {
                        "back": "#f9f9f9",
                        "border": "#d5d5d5",
                        "fore": "#202020",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#fafafa",
                        "border": "#ebebeb",
                        "fore": "#202020",
                        "border_width": 1,
                    },
                },

                "entry": {
                    "radius": 13,

                    "default": {
                        "back": "#ffffff",
                        "border": "#e6e6e6",
                        "fore": "#000000",
                        "border_width": 1,

                        "bottomsheet": "#9c9c9c",
                        "bottomsheet_width": 1,
                    },

                    "focus": {
                        "back": "#ffffff",
                        "border": "#ebebeb",
                        "fore": "#000000",
                        "border_width": 1,

                        "bottomsheet": "#005fb8",
                        "bottomsheet_width": 2,
                    }
                },

                "frame": {
                    "radius": 15,
                    "back": "#fafafa",
                    "border": "#e7e7e7",
                    "border_width": 1,
                },

                "label": {
                    "fore": "#000000"
                },

                "menubar": {
                    "back": "#fdfdfd",
                    "border": "#ededed",
                },

                "separator": {
                    "fore": "#d0d0d0",
                    "border_width": 1,
                    "rounded": True
                },

                "text": {
                    "radius": 13,

                    "default": {
                        "back": "#ffffff",
                        "border": "#e6e6e6",
                        "fore": "#000000",
                        "border_width": 1,

                        "bottomsheet": "#9c9c9c",
                        "bottomsheet_width": 1,
                    },

                    "focus": {
                        "back": "#ffffff",
                        "border": "#ebebeb",
                        "fore": "#000000",
                        "border_width": 1,

                        "bottomsheet": "#005fb8",
                        "bottomsheet_width": 2,
                    }
                },

            },
            "dark": {
                "window": {
                    "back": "#202020"
                },

                "button": {
                    "radius": 13,

                    "default": {
                        "back": "#2a2a2a",
                        "border": "#313131",
                        "fore": "#ebebeb",
                        "border_width": 1,
                    },

                    "active": {
                        "back": "#2f2f2f",
                        "border": "#313131",
                        "fore": "#ebebeb",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#232323",
                        "border": "#2c2c2c",
                        "fore": "#ebebeb",
                        "border_width": 1,
                    },
                },

                "entry": {
                    "radius": 13,

                    "default": {
                        "back": "#2c2c2c",
                        "border": "#383838",
                        "fore": "#ffffff",
                        "border_width": 1,

                        "bottomsheet": "#686868",
                        "bottomsheet_width": 1,
                    },

                    "focus": {
                        "back": "#1c1c1c",
                        "border": "#2c2c2c",
                        "fore": "#ffffff",
                        "border_width": 1,

                        "bottomsheet": "#57c8ff",
                        "bottomsheet_width": 2,
                    }
                },

                "frame": {
                    "radius": 15,
                    "back": "#1c1c1c",
                    "border": "#2f2f2f",
                    "border_width": 1,
                },

                "label": {
                    "fore": "#ffffff"
                },

                "menubar": {
                    "back": "#2a2a2a",
                    "border": "#313131",
                },

                "separator": {
                    "fore": "#404040",
                    "border_width": 1,
                    "rounded": True
                },

                "text": {
                    "radius": 13,

                    "default": {
                        "back": "#2c2c2c",
                        "border": "#383838",
                        "fore": "#ffffff",
                        "border_width": 1,

                        "bottomsheet": "#686868",
                        "bottomsheet_width": 1,
                    },

                    "focus": {
                        "back": "#1c1c1c",
                        "border": "#2c2c2c",
                        "fore": "#ffffff",
                        "border_width": 1,

                        "bottomsheet": "#57c8ff",
                        "bottomsheet_width": 2,
                    }
                },

            }
        }

    def accent(self, color, darkcolor):
        self.configure("light", "entry", "bottomsheet", color, state="focus")
        self.configure("dark", "entry", "bottomsheet", darkcolor, state="focus")
        self.configure("light", "text", "bottomsheet", color, state="focus")
        self.configure("dark", "text", "bottomsheet", darkcolor, state="focus")


from json import dumps

environ["ADWTHEME"] = dumps(AdwWin11Theme().get())
environ["ADWTHEME.MODE"] = "light"


def theme(name=None):
    if name:
        if "ADWTHEME" in environ:
            from json import dumps
            environ["ADWTHEME"] = dumps(name)
    else:
        if "ADWTHEME" in environ:
            from json import loads
            return loads(environ["ADWTHEME"])


def theme_mode(mode=None):
    if mode:
        environ["ADWTHEME.MODE"] = mode
    else:
        if "ADWTHEME" in environ:
            return environ["ADWTHEME.MODE"]


class AdwThemed(object):
    def dark_palette(self):
        if theme():
            self.palette(theme()["dark"])

    def default_palette(self):
        if theme():
            self.palette(theme()[theme_mode()])

    def light_palette(self):
        if theme():
            if theme_mode():
                self.palette(theme()["light"])


from .button import AdwButton


class AdwTButton(AdwThemed, AdwButton):
    pass


from .entry import AdwEntry


class AdwTEntry(AdwThemed, AdwEntry):
    pass


from .frame import AdwFrame


class AdwTFrame(AdwThemed, AdwFrame):
    pass


from .label import AdwLabel


class AdwTLabel(AdwThemed, AdwLabel):
    pass


from .menubar import AdwMenuBar


class AdwTMenuBar(AdwThemed, AdwMenuBar):
    pass


from .separator import AdwSeparator


class AdwTSeparator(AdwThemed, AdwSeparator):
    pass


from .text import AdwText


class AdwTText(AdwThemed, AdwText):
    pass


from .window import AdwMainWindow


class _AdwTMainWindow(AdwThemed, AdwMainWindow):
    def dark(self, enable: bool, width_icon=True):
        if width_icon:
            self.icon(enable)
        if enable:
            self.styles(["dark"])
        else:
            self.styles(["light"])

    def theme(self, themename, thememode="system"):
        from .themebuilder import AdwSimpleThemeBuilder
        if themename == "win11":
            theme(AdwWin11Theme().get())
        elif issubclass(themename.__class__, AdwSimpleThemeBuilder) or issubclass(themename.__class__, AdwTheme):
            theme(themename.get())
        else:
            theme(themename)
        if thememode == "system":
            try:
                from darkdetect import isDark
            except ModuleNotFoundError:
                pass
            else:
                if isDark():
                    theme_mode("dark")
                else:
                    theme_mode("light")
        else:
            theme_mode(thememode)

        self.palette(theme()[theme_mode()])

        self.update()

        for child in self.winfo_children():
            if hasattr(child, "palette"):
                child.palette(theme()[theme_mode()])
                child.update()


class AdwTMainWindow(_AdwTMainWindow):
    pass
