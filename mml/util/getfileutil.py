from tkinter import Tk, filedialog

def get_file_path():
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file")
    return root.filename


def get_file_dir():
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askdirectory(initialdir="/", title="Select file")
    return root.filename