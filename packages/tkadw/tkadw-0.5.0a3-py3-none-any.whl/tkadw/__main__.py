from tkadw import *

root = AdwTMainWindow(
    styles=["optimised"]
)

theme = AdwWin11Theme()
theme.accent("dark orange", "orange")

root.theme(theme, "dark")
#root.styles(["aero"])
root.dark(True)

frame = AdwTFrame()
frame.pack(fill="both", expand="yes", padx=15, pady=(15, 7.5))

label = AdwTLabel(frame, text="Label")
label.pack(fill="both", expand="yes", padx=15, pady=(7.5, 15))

button = AdwTButton(frame, text="Button", command=lambda: print("Button"))
button.pack(fill="both", expand="yes", padx=15, pady=(7.5, 15))

entry = AdwTEntry(frame, text="Entry")
entry.pack(fill="both", expand="yes", padx=15, pady=(7.5, 15))

text = AdwTText(frame, text="Entry")
text.pack(fill="both", expand="yes", padx=15, pady=(7.5, 15))

root.run()