from maya import cmds

from fdda.maya.core import api_utils
from fdda.core.context import ContextDecorator


class KeepCurrentFrame(ContextDecorator):

    def __init__(self):
        super().__init__()
        self._current_frame = None

    def __enter__(self):
        if self._current_frame is None:
            self._current_frame = api_utils.get_current_time()

    def __exit__(self, *args):
        api_utils.set_current_time(self._current_frame)
        self._current_frame = None


class DisableRefresh(ContextDecorator):

    def __enter__(self):
        cmds.refresh(suspend=True)

    def __exit__(self, *args):
        cmds.refresh(suspend=False)
