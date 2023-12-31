from tkadw import *

root = AdwTMainWindow(
    styles=["optimised"]
)
root.theme("win11", "dark")
#root.styles(["aero"])
root.dark(True)

button = AdwTButton(text="Button", command=lambda: print("Button"))
button.pack(fill="both", expand="yes", padx=15, pady=(7.5, 15))

entry = AdwTEntry(text="Entry")
entry.pack(fill="both", expand="yes", padx=15, pady=(7.5, 15))

root.run()