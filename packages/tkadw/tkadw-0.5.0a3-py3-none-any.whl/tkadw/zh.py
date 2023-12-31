from tkadw import *

根 = 主题主窗口(
    styles=["optimised"]
)
根.使用主题("win11", "light")
根.深黑模式(True)

按钮1 = 主题按钮(text="按钮1", command=lambda: print("Button1"))
按钮1.set_drawmode(0)
按钮1.pack(fill="both", expand="yes", padx=15, pady=(15, 7.5))

按钮2 = 主题按钮(text="按钮2", command=lambda: print("Button2"))
按钮2.configure(drawmode=1)
按钮2.pack(fill="both", expand="yes", padx=15, pady=(7.5, 15))

根.run()