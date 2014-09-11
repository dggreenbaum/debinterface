import subprocess


def safe_subprocess(command_array):
    ''' return True/False, command output '''

    try:
        return True, subprocess.check_output(command_array, stderr=subprocess.STDOUT)
    except OSError as e:
        return False, e.__str__()
    except subprocess.CalledProcessError as e:
        return False, e.output
