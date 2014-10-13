import os
import tempfile
import shutil
from contextlib import contextmanager
import subprocess


def safe_subprocess(command_array):
    ''' return True/False, command output '''

    try:
        return True, subprocess.check_output(command_array,
                                             stderr=subprocess.STDOUT)
    except OSError as e:
        return False, e.__str__()
    except subprocess.CalledProcessError as e:
        return False, e.output


@contextmanager
def atomic_write(filepath):
    """
        Writeable file object that atomically
        updates a file (using a temporary file).

        :param filepath: the file path to be opened
    """

    with tempfile.NamedTemporaryFile() as tf:
        with open(tf.name, mode='w+') as tmp:
            yield tmp
            tmp.flush()
            os.fsync(tmp.fileno())
        shutil.copy(tf.name, filepath)
