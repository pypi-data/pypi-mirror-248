from tkadw import *

window = AdwTMainWindow()
window.frameless(True)

theme = AdwFluentTheme()
theme.accent("darkorange", "orange")
window.theme(theme, "dark")
window.dark(True)

titlebar = AdwTTitleBar(window)
titlebar.show()

menubar = AdwTMenuBar(window)
AdwBindMove(menubar)
menubar.show()

mainframe = AdwTFrame(window)

AdwTButton(mainframe, text="AdwTButton").pack(fill="x")

mainframe.pack(fill="both", expand="yes", padx=10, pady=10)

window.mainloop()

