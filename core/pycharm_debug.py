import os
import sys

kDebugModule = "pydevd_pycharm.py"
kRootPath = r"C:\Program Files\JetBrains"

def find_last_version(root_path: str) -> str:
    dir = None
    last = 0
    for elem in os.listdir(root_path):
        flat_str = elem.replace(" ", "").replace(".", "").replace("_", "").replace("-", "")
        num_str = ""
        for s in flat_str:
            if s.isdigit():
                num_str += s
        
        if int(num_str) > last:
            dir = elem
    
    return os.path.normpath(os.path.join(root_path, dir))


def find_debugger(root_path: str) -> str:
    pycharm_last_version = find_last_version(root_path)
    for dir_path, _, file_names in os.walk(pycharm_last_version):
        for f in file_names:
            if f.endswith(kDebugModule):
                return os.path.normpath(os.path.join(dir_path, f))


def connect(root_path: str = kRootPath, port: int = 50015):
    debug_module_path = find_debugger(root_path)
    sys.path.insert(0, os.path.split(debug_module_path)[0])

    import pydevd_pycharm
    pydevd_pycharm.settrace('localhost', port=port, stdoutToServer=True, stderrToServer=True)
