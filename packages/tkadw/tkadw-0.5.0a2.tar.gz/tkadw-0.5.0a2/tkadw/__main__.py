from tkadw import *

root = AdwTMainWindow(
    styles=["optimised"]
)
root.theme("win11", "dark")
#root.styles(["aero"])
root.dark(True)

label = AdwTLabel(text="Label")
label.pack(fill="both", expand="yes", padx=15, pady=(15, 7.5))

button = AdwTButton(text="Button", command=lambda: print("Button"))
button.pack(fill="both", expand="yes", padx=15, pady=(7.5, 15))

entry = AdwTEntry(text="Entry")
entry.pack(fill="both", expand="yes", padx=15, pady=(7.5, 15))

text = AdwTText(text="Entry")
text.pack(fill="both", expand="yes", padx=15, pady=(7.5, 15))

root.run()