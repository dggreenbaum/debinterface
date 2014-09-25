import os
from contextlib import contextmanager
import subprocess


def safe_subprocess(command_array):
    ''' return True/False, command output '''

    try:
        return True, subprocess.check_output(command_array, stderr=subprocess.STDOUT)
    except OSError as e:
        return False, e.__str__()
    except subprocess.CalledProcessError as e:
        return False, e.output


@contextmanager
def atomic_write(filepath, fsync=True, binary=False):
    """ Writeable file object that atomically updates a file (using a temporary file).

    from http://stackoverflow.com/questions/2333872/atomic-writing-to-file-with-python
    :param filepath: the file path to be opened
    :param fsync: whether to force write the file to disk
    :param binary: whether to open the file in a binary mode instead of textual
    """

    tmppath = filepath + '~'
    while os.path.isfile(tmppath):
        tmppath += '~'
    try:
        with open(tmppath, 'wb' if binary else 'w') as file:
            yield file
            if fsync:
                file.flush()
                os.fsync(file.fileno())
        os.rename(tmppath, filepath)
    finally:
        try:
            os.remove(tmppath)
        except (IOError, OSError):
            pass
