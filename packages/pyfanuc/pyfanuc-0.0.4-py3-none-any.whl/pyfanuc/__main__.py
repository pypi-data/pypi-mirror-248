import pyfanuc
import subprocess
command = "pip3 install -e git+https://github.com/tonejca/pyfwlib.git@pyfanucable#egg=fwlib"
try:
    import fwlib
except ModuleNotFoundError:
    print("trying to execute:")
    print("\u0332".join(command))
    try:
        subprocess.call([command])
    except ModuleNotFoundError:
        print("failed, please first install fwlib by executing"+command)