from tkadw import *

window = AdwTMainWindow()

theme = AdwWin11Theme()
theme.accent("darkorange", "orange")
window.theme(theme, "light")
window.dark(True)

menubar = AdwTMenuBar(window)
menubar.show()

mainframe = AdwTFrame(window)

for btn in range(0, 3):
    AdwTButton(mainframe, text=str(btn+1)).grid(row=0, column=btn, padx=5, pady=5)

for entry in range(0, 2):
    AdwTEntry(mainframe, text=str(entry+1)).grid(row=1, column=entry, padx=5, pady=5)

for text in range(0, 2):
    AdwTText(mainframe, text=str(text+1)).grid(row=2, column=text, padx=5, pady=5)

mainframe.pack(fill="both", expand="yes", padx=10, pady=10)

window.mainloop()
