import os
import os.path
import shutil

try:
    if r.ok is True:
        del(r)
    elif r is not None:
        del(r)
    else:
        pass
except NameError:
    pass

try:
    if local is not None:
        del(local)
    else:
        pass
except NameError:
    pass

if os.path.exists(os.path.realpath("local/__pycache__/")) is True:
    shutil.rmtree(os.path.realpath("local/__pycache__/"))
else:
    pass

if os.path.exists(os.path.realpath("__pycache__/")) is True:
    shutil.rmtree(os.path.realpath("__pycache__/"))
else:
    pass 
