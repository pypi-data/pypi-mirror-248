from tkinter.filedialog import askopenfilenames


def select_files():
    filenames = askopenfilenames()
    return filenames
