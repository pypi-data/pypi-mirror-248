from tkadwold.windows.widgets import *
from tkadwold.utility.appconfig import appconfig as AdwReadAppConfig

from tkadwold.windows import *

# 0.3.0加入
from tkadwold.windows.theme import *

from tkadwold.game import *

# 0.3.5加入
from tkadwold.layout import *

# 0.3.9加入
from tkadwold.designer.designerframe import AdwDesignerFrame
from tkadwold.designer.designer import AdwDesigner
from tkadwold.designer.builder import AdwBuilder

try:
    from tkadw_material import *
except ModuleNotFoundError:
    pass


# from tkadwold.tkite import * 已废弃移除
# from tkadwold.win11 import * 已废弃移除
# from tkadwold.advanced import * 已废弃移除，改为from tkadwold.adw import Adw导入
# from tkadwold.bilibili import BiliBiliButton, BiliBiliDarkButton, BiliBiliFrame, BiliBiliDarkFrame, \
#     BiliBiliEntry, BiliBiliDarkEntry, BiliBiliDarkTextBox, BiliBiliTextBox 已废弃移除

# 0.3.7补充
from tkadwold.utility import *


def get_version():
    return "0.4.6"


def get_major_version():
    return "0"

def get_micro_version():
    return "4"


if __name__ == '__main__':
    from tkinter import Tk, Toplevel

    root = Tk()

    adw_run(root)