from distutils.core import setup
import py2exe

includes = ['sqlite3', 'os.path', 'tkMessageBox', 'Tkinter', 'datetime']
setup(windows=['EclampsiaModel.py'])
