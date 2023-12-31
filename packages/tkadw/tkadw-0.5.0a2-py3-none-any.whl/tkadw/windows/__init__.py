from .base import AdwBase, Arg as AdwArgument
from .button import AdwButton
from .drawengine import AdwDrawEngine
from .drawwidget import AdwDrawWidget
from .entry import AdwEntry
from .gradient import Gradient as AdwGradient, Gradient2 as AdwGradient2, ARC, CENTRAL, CIRCULAR, HORIZONTAL, VERTICAL, X, Y
from .icon import ICONLIGHT,  ICONDARK
from .label import AdwLabel
from .layout import AdwLayout
from .roundrect import RoundRect as AdwRoundRect
from .run import AdwRun, run
from .style import WindowStyle as AdwWindowStyle, LIGHT, DARK
from .text import AdwText
from .theme import (
    AdwThemed, theme, theme_mode,
    AdwTMainWindow, AdwTButton, AdwTEntry, AdwTLabel, AdwTText
)
from .widget import AdwWidget
from .window import AdwMainWindow

# 中文版
from .base import AdwBase as 基本, Arg as 参数
from .button import AdwButton as 按钮
from .drawengine import AdwDrawEngine as 绘画引擎
from .drawwidget import AdwDrawWidget as 绘画组件
from .entry import AdwEntry as 输入框
from .gradient import Gradient as 渐变, Gradient2 as 渐变2, ARC as 弧形, CENTRAL as 中心, CIRCULAR as 圆形, HORIZONTAL as 水平, VERTICAL as 垂直, X as X坐标, Y as Y坐标
from .icon import ICONLIGHT,  ICONDARK
from .label import AdwLabel as 标签
from .layout import AdwLayout as 布局
from .roundrect import RoundRect as 圆角矩形
from .run import AdwRun as 运行
from .style import WindowStyle as 窗口样式, LIGHT as 浅亮, DARK as 深黑
from .text import AdwText as 多文本输入框
from .theme import (
    AdwThemed as 主题化, theme as 主题, theme_mode as 主题模式,
    AdwTMainWindow as 主题主窗口, AdwTButton as 主题按钮,
    AdwTEntry as 主题输入框, AdwTLabel as 主题标签,
    AdwTText as 主题多文本输入框
)
from .widget import AdwWidget as 小组件
from .window import AdwMainWindow as 主窗口
