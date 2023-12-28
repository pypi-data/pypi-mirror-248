import logging
import os
import pathlib

from draft.constants import CWD
from draft.exceptions import NoProjectRootException


def is_asset_project(dir_path: pathlib.Path, count=10):
    try:
        get_project_root(dir_path, count)
    except NoProjectRootException:
        return_value = False
    else:
        return True


def get_project_root(dir_path: pathlib.Path, count=10):
    dir_path = pathlib.Path(dir_path)
    if count <= 0 or str(dir_path) == dir_path.anchor:
        raise NoProjectRootException
    elif os.path.exists(dir_path / '.draft'):
        return dir_path
    else:
        return get_project_root(dir_path.parent, count - 1)

# TODO: make streamhandler respect stdout and stderr
# This stream handler sends everything to stderr, not stdout
# That means that command line tool won't work with piping
# unless you redirect the sterr stream to stdout.
# However, this can be fixed, but it is a bit of work.
# See: https://docs.python.org/3/howto/logging-cookbook.html
# Basically, you create three handlers, file, stdout and stderr
# set the stream to ext://sys.stdout, ext://sys.stderr etc.
# and then use filters to remove unwanted content
# ALSO: we might want to consider using an entirely different logger or print
# functionality for the command.py. Logically, command.py is user interface to drafttool.py
# but by using the same logger as draftool.py, command.py is giving over to draftool.py it's
# user-interface decisions. Instead, it should make its own decisions, based on exeptions thrown
# or input received from drafttool.py

def configure_logger(logger_to_be_configured, log_level=logging.DEBUG,
                     stream_level=logging.INFO):
    logger_to_be_configured.setLevel(logging.DEBUG)  # We'll let the handlers filter
    file_formatter = logging.Formatter('%(asctime)s;%(name)s;%(levelname)s;%(message)s')
    stream_formatter = logging.Formatter('%(message)s')

    try:
        project_root = get_project_root(CWD)
        logging_file_name = project_root / '.draft' / 'draft.log'
        fh = logging.FileHandler(logging_file_name)
        fh.setLevel(log_level)
        fh.setFormatter(file_formatter)
        logger_to_be_configured.addHandler(fh)
    except (NoProjectRootException, NotADirectoryError):
        pass

    # To stream
    sh = logging.StreamHandler()
    sh.setLevel(stream_level)
    sh.setFormatter(stream_formatter)
    logger_to_be_configured.addHandler(sh)

    return logger_to_be_configured
