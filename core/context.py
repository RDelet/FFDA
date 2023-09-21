import functools

from maya import cmds

from fdda.core import api_utils


class Context(object):

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self) -> str:
        return self.__repr__
    
    def __repr__(self) -> str:
        return f"FDDA(class: {self.__class__.__name__})"

    def __enter__(self, *args, **kwargs):
        raise NotImplementedError('{0}.__enter__ need to be reimplemented !'.format(self.__class__.__name__))

    def __exit__(self, *args, **kwargs):
        raise NotImplementedError('{0}.__exit__ need to be reimplemented !'.format(self.__class__.__name__))


class ContextDecorator(Context):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._func = None
        self._func_args = None
        self._func_kwargs = None
        self._kwargs = kwargs

    def __call__(self, f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            with self:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    raise e

        return wrapper


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
        cmds.refresh(suspend=False, force=True)

    def __exit__(self, *args):
        cmds.refresh(suspend=True, force=True)
