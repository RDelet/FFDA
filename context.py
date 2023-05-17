from fdda import utils as maya_utils


class QDContext(object):

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self, *args, **kwargs):
        raise NotImplementedError('{0}.__enter__ need to be reimplemented !'.format(self.__class__.__name__))

    def __exit__(self, *args, **kwargs):
        raise NotImplementedError('{0}.__exit__ need to be reimplemented !'.format(self.__class__.__name__))


class KeepCurrentFrame(QDContext):

    def __init__(self):
        super(KeepCurrentFrame, self).__init__()
        self._current_frame = None

    def __enter__(self):
        if self._current_frame is None:
            self._current_frame = maya_utils.get_current_time()

    def __exit__(self, *args):
        maya_utils.set_current_time(self._current_frame)
        self._current_frame = None
