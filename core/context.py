import functools


class Context(object):

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        return f"FDDA(class: {self.__class__.__name__})"

    def __enter__(self, *args, **kwargs):
        raise NotImplementedError('{0}.__enter__ need to be reimplemented !'.format(self.__class__.__name__))

    def __exit__(self, *args, **kwargs):
        raise NotImplementedError('{0}.__exit__ need to be reimplemented !'.format(self.__class__.__name__))


class ContextDecorator(Context):

    def __call__(self, f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            with self:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    raise e

        return wrapper
