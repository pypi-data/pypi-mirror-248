
from .window import AdwMainWindow


class AdwCustomWindow(AdwMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

