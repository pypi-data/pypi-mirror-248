from .drawwidget import AdwDrawWidget


class AdwButton(AdwDrawWidget):

    id = "button"

    def __init__(self,
                 *args,
                 command=None,
                 drawmode: int = 1,
                 text: str = "",
                 radius: int = 14,
                 **kwargs):
        super().__init__(*args, **kwargs)

        if command is None:
            def _():
                pass
            command = _

        # 初始属性
        self.args(
            drawmode=drawmode,
            back_default="#fdfdfd",
            back_enter="#f9f9f9",
            back_button="#fafafa",
            border_default="#ededed",
            border_enter="#d5d5d5",
            border_button="#ebebeb",
            border_width_default=1,
            border_width_enter=1,
            border_width_button=1,
            radius=radius,
            text=text,
            text_default="#202020",
            text_enter="#202020",
            text_button="#202020",
        )

        self.bind("<<Click>>", lambda event=None: command())

        self.default_palette()

    def _draw(self, event=None):
        super()._draw(event)
        if self._is_enter:
            if self._is_button:
                __back = self._back_button
                __border = self._border_button
                __border_width = self._border_width_button
                __text = self._text_button
            else:
                __back = self._back_enter
                __border = self._border_enter
                __border_width = self._border_width_enter
                __text = self._text_enter
        else:
            __back = self._back_default
            __border = self._border_default
            __border_width = self._border_width_default
            __text = self._text_default

        # 绘制框架
        if self._drawmode == 0:
            self.roundrect_draw(
                x=0, y=0,
                width=self.winfo_width(), height=self.winfo_height(),
                fill=__border, outline=__border, radius=self._radius + 2, tag="frame_border"
            )
            self._frame_border = "frame_border"
            self.roundrect_draw(
                x=__border_width, y=__border_width,
                width=self.winfo_width() - 2 * __border_width,
                height=self.winfo_height() - 2 * __border_width,
                fill=__back, outline=__back, radius=self._radius, tag="frame"
            )
        elif self._drawmode == 1:
            self.roundrect2_draw(
                x1=0, y1=0,
                x2=self.winfo_width() - __border_width,
                y2=self.winfo_height() - __border_width,
                fill=__back, outline=__border, radius=self._radius, tag="frame"
            )
        self._frame = "frame"

        # 绘制文字
        self._label = self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2,
            text=self._text, fill=__text
        )

    def command(self, func):
        self.bind("<<Click>>", lambda event=None: func())

    def default_palette(self):
        pass

    def palette(self, palette: dict):
        if self.id in palette:
            if "radius" in palette[self.id]:
                self._radius = palette[self.id]["radius"]
            if "default" in palette[self.id]:
                if "back" in palette[self.id]["default"]:
                    self._back_default = palette[self.id]["default"]["back"]
                if "border" in palette[self.id]["default"]:
                    self._border_default = palette[self.id]["default"]["border"]
                if "border_width" in palette[self.id]["default"]:
                    self._border_width_default = palette[self.id]["default"]["border_width"]
                if "fore" in palette[self.id]["default"]:
                    self._text_default = palette[self.id]["default"]["fore"]
            if "active" in palette[self.id]:
                if "back" in palette[self.id]["active"]:
                    self._back_enter = palette[self.id]["active"]["back"]
                if "border" in palette[self.id]["active"]:
                    self._border_enter = palette[self.id]["active"]["border"]
                if "border_width" in palette[self.id]["active"]:
                    self._border_width_enter = palette[self.id]["active"]["border_width"]
                if "fore" in palette[self.id]["active"]:
                    self._text_enter = palette[self.id]["active"]["fore"]
            if "pressed" in palette[self.id]:
                if "back" in palette[self.id]["pressed"]:
                    self._back_button = palette[self.id]["pressed"]["back"]
                if "border" in palette[self.id]["pressed"]:
                    self._border_button = palette[self.id]["pressed"]["border"]
                if "border_width" in palette[self.id]["pressed"]:
                    self._border_width_button = palette[self.id]["pressed"]["border_width"]
                if "fore" in palette[self.id]["pressed"]:
                    self._text_button = palette[self.id]["pressed"]["fore"]
        self.update()
