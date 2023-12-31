from .drawwidget import AdwDrawWidget


class AdwSeparator(AdwDrawWidget):
    def __init__(self,
                 *args,
                 border_width_default=1,
                 rounded: bool = True,
                 fore="#d0d0d0",
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.args(
            border_width_default=border_width_default,
            rounded=rounded,
            fore_default=fore,
        )

    def _draw(self, event=None):
        super()._draw(event)

        self._line = self.create_line(
            self._border_width_default,
            self.winfo_height()/2,
            self.winfo_width()-self._border_width_default,
            self.winfo_height() / 2,
            width=self._border_width_default,
            fill=self._fore_default,
        )

        if self._rounded:
            self.itemconfigure(self._line, capstyle="round", joinstyle="round", smooth=True)

    def palette(self, palette: dict):
        if self.id in palette:
            if "rounded" in palette[self.id]:
                self._rounded = palette[self.id]["rounded"]
            if "border_width" in palette[self.id]:
                self._border_width_default = palette[self.id]["border_width"]
            if "fore" in palette[self.id]:
                self._fore_default = palette[self.id]["fore"]
        self.update()