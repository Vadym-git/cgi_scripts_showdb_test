import webbrowser
import os
def path():
    webbrowser.open("http://localhost:8000/")
    os.system("python3 -m http.server --cgi")
path()