import logging
import os


_formatter = logging.Formatter("%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(_formatter)


def set_output_path(p, formatter=_formatter):
    p = os.path.normpath(p)
    if os.path.isdir(p):
        p = os.path.normpath(os.path.join(p, "FFDA.log"))
    # make sure directory exists
    directory = os.path.split(p)[0]
    if not os.path.exists(directory):
        os.mkdir(directory)
    # make sure file exists
    if not os.path.exists(p):
        with open(p, "w") as stream:
            stream.write("")

    file_handler = logging.FileHandler(p, "w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)


def set_log_level(log_level):
    log.setLevel(log_level)
    stream_handler.setLevel(log_level)


log = logging.getLogger("FFDA")
log.addHandler(stream_handler)
set_log_level(logging.INFO)
