from setuptools import setup

MODULES = ['sqlite3', 'os.path', 'tkMessageBox', 'Tkinter', 'datetime']
APP = ['EclampsiaModel.py']
OPTIONS = {'argv_emulation':True, 'includes':MODULES}
DATA_FILES = []

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],)
