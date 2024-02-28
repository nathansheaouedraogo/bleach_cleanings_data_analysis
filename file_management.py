
from tkinter import filedialog, messagebox
from pathlib import Path


def parent_dir():
    """
    returns absolute path of working directory
    """
    return Path(__file__).absolute().parent


def select_file(cwd):
    """
    Prompts user to select .csv file of data 
    """
    
    title = f'Please select files'
    
    files = filedialog.askopenfilenames(initialdir = cwd, filetypes=(("CSV Files", "*.csv"),), title=title)
    
    if not files:
        messagebox.showerror(None, 'Fatal Error: \n\nNo file selected!')
        print(f'\nprocess finished with exit code 1 (no file selected)\n')
        exit()
    else:
        return files    

def dump_dict(dict, file_path):
    with open(file_path, 'w') as f:
        json.dump(dict, f, indent=4) 
