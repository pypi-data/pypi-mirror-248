if __name__ == '__main__':
    from tkadwold.windows.theme import Adwite
    from tkadwold.designer.designer import AdwDesigner

    root = Adwite(default_theme="metro")

    designer = AdwDesigner(root)
    designer.row()

    root.animation()
    root.run()