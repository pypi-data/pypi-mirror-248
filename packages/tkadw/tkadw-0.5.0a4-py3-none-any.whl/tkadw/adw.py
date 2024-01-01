import click


doc_tkadw = """
# tkadw
> tkadw - # 自0.5.0版本开始，正式重做
"""


@click.group()
def main():
    from colorama import Fore
    from tkadw import __version__
    print(f"🐋你好！当前{Fore.BLUE}tkadw{Fore.RESET}版本是{Fore.RED}{__version__}{Fore.RESET}")


@click.command()
def demo():
    from tkadw import AdwTMainWindow, AdwWin11Theme, AdwTFrame, AdwTButton, AdwTEntry, AdwTText

    window = AdwTMainWindow()

    theme = AdwWin11Theme()
    theme.accent("darkblue", "skyblue")
    window.theme(theme, "dark")

    mainframe = AdwTFrame(window)

    for btn in range(0, 3):
        AdwTButton(mainframe, text=str(btn + 1)).grid(row=0, column=btn, padx=5, pady=5)

    for entry in range(0, 2):
        AdwTEntry(mainframe, text=str(entry + 1)).grid(row=1, column=entry, padx=5, pady=5)

    for text in range(0, 2):
        AdwTText(mainframe, text=str(text + 1)).grid(row=2, column=text, padx=5, pady=5)

    mainframe.pack(fill="both", expand="yes", padx=15, pady=15)

    window.mainloop()


@click.command()
@click.argument("name")
def doc(name):
    if name == "tkadw":
        from rich.console import Console
        from rich.markdown import Markdown
        console = Console()
        md = Markdown(doc_tkadw)
        console.print(md)

@click.command()
@click.argument("path")
def run(path):
    from colorama import Fore
    from os.path import abspath
    print(f"🐇准备运行{Fore.BLUE}文件'{abspath(path)}'{Fore.RESET}！")
    with open(path) as file:
        exec(file.read())


main.add_command(demo)
main.add_command(doc)
main.add_command(run)


if __name__ == '__main__':
    main()
