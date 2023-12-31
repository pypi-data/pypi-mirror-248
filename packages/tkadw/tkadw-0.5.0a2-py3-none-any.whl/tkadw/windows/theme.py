from os import environ

win11 = {
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

        "label": {
            "fore": "#000000"
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

        "label": {
            "fore": "#ffffff"
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

from json import dumps

environ["ADWTHEME"] = dumps(win11)
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


from .label import AdwLabel


class AdwTLabel(AdwThemed, AdwLabel):
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

    深黑模式 = dark

    def theme(self, themename, thememode="system"):
        if themename == "win11":
            theme(win11)
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

        for child in self.winfo_children():
            if hasattr(child, "palette"):
                child.palette(theme()[theme_mode()])
                child.update()

    使用主题 = theme


class AdwTMainWindow(_AdwTMainWindow):
    pass
