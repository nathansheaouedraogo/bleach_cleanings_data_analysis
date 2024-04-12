import json
from tkinter import filedialog, messagebox, simpledialog
import os
from pathlib import Path
from datetime import date

# load/create directories
def cwd():
    """
    returns absolute path of working directory
    """
    return Path(__file__).absolute().parent

def load_dir(child_dir_name, parent_dir_path=cwd()):
    """
    returns path of selected directory, defaulted to cwd
    NOTE: child_dir_name is the string NAME whereas parent_dir_path is a FILEPATH! 
    """
    return os.path.join(parent_dir_path, child_dir_name)

def create_dir(parent_dir_name, child_dir_name):
    """
    creates a child inside parent dir which itself is in the cwd
    """
    
    parent_dir_path = os.path.join(cwd(), parent_dir_name)
    
    os.mkdir(os.path.join(parent_dir_path, child_dir_name))


def create_processed_data_dir(date):
    
    """
    Creates directory in 'processed_data' for all processed data from specific date
    Returns the absolute path of said directory
    """
    
    path = os.path.join(cwd(), f'processed_data\{date}')
    os.mkdir(path)
    return path


# load file(s)
def select_raw_data():
    """
    Prompts user to select .csv file of raw data 
    """
    
    raw_data_dir = load_dir('raw_data')
    
    title = f'Please select the raw data'
    
    file = filedialog.askopenfilename(initialdir = raw_data_dir, filetypes=(("CSV Files", "*.csv"),), title=title)
    
    if not file:
        messagebox.showerror(None, 'Fatal Error: \nNo raw data selected!')
        print(f'\nprocess finished with exit code 1 (no raw data selected)\n')
        exit()
    else:
        return file    

def load_experimental_data_dict():
    """
    Prompts user to select .txt file of experimental start/end times
    NOTE: loaded file must be formatted in the following way: 
        experimental_data_dict = {

    # input times for bleachings with air freshener
    'bleachings_with_airfresh':{ 

        # refers to lighting condition of a specific peak (or any other identifier you want)
        'condition' : [],

        # start of the peak of interest
        'peak_start_datetime' : [],

        # end of the peak of interest
        'peak_end_datetime' : [],

        # start of the background
        'background_start_datetime' : [],
        
        # end of the background
        'background_end_datetime' : [],
        },
    
    
        # input times for bleachings without air freshener
        'bleachings_without_airfresh':{ 

            # refers to lighting condition of a specific peak (or any other identifier you want)
            'condition' : [],

            # start of the peak of interest
            'peak_start_datetime' : [],

            # end of the peak of interest
            'peak_end_datetime' : [],

            # start of the background
            'background_start_datetime' : [],
            
            # end of the background
            'background_end_datetime' : [],
            },
        }
    """
    
    experiment_data_dir_path = load_dir('experimental_times_dicts')
    
    title = f'Please select the filled dictionary of experimental times'
    
    file = filedialog.askopenfilename(initialdir = experiment_data_dir_path, filetypes=(("Text Files", "*.txt"),), title=title)
    
    if not file:
        messagebox.showerror(None, 'Fatal Error: \nNo dictionary selected!')
        print(f'\nprocess finished with exit code 1 (no dictionary selected)\n')
        exit() 
    else:
        try: 
            with open(file) as f: 
                json.loads(f.read())
        except: 
            messagebox.showerror(None, 'Fatal Error: \n\nFile improperly formatted!\n\nFile: {file}!')
            print(f'\nprocess finished with exit code 1 (improperly formatted file):\n{file}')
            exit() 
        else: 
            with open(file) as f: 
                return json.loads(f.read())

def dump_dict(dict, file_name):
    """
    creates .txt file of inputted dict
    """
    file_path = os.path.join(cwd(), file_name)
    with open(file_path, 'w') as f:
        json.dump(dict, f, indent=4) 


def input_date_of_experiment():
    
    while True:
        
        messagebox.showinfo(message='In the following prompts, please input the date(s) of the experiment(s)')
        
        # INPUT DATE(S) OF EXPERIMENTS 
        ## IF SINGLE EXPERIMENT: 'yyyy-mm-dd'
        ## IF RANGE OF EXPERIMENTS: 'yyyy-mm-dd - yyyy-mm-dd'
        # ask if muliple days
        message = 'were the experiments performed on multiple days?'
        result = messagebox.askyesnocancel(title=None, message=message)
        if result == None: 
            messagebox.showerror(None, 'Fatal Error: \nNo no date inputted!')
            print(f'\nprocess finished with exit code 1 (no date inputted)\n')
            exit()        
        
        # experiments performed on single day
        elif result == False:
            message_input_date = f'Input the date of the experiment as follows: \n\nyyyy-mm-dd'
            experiment_date = simpledialog.askstring(title=None, prompt=message_input_date)
            
            # test validity of date
            try: 
                date.fromisoformat(experiment_date)
            except ValueError():
                messagebox.showerror(None, 'Fatal Error: \nImproper date format!')
                print(f'\nprocess finished with exit code 1 (improper date format: {experiment_date})\n')
                exit()
            else: 
                
                message_line_1 = 'Press "yes" if the dates are correct, "no" if they are incorrect, or "cancel" to exit'
                message_line_2 = f'\nyear:   \t{experiment_date[0:4]}'
                message_line_3 = f'\nmonth:  \t{experiment_date[5:7]}'
                message_line_4 = f'\nday:    \t{experiment_date[8:]}'
                message = message_line_1+'\n'+message_line_2+message_line_3+message_line_4
                result = messagebox.askyesnocancel(title=None, message=message)
                if result == True: 
                    break
                elif result == False:
                    continue 
                else: 
                    messagebox.showerror(None, 'Fatal Error: \nNo date inputted!')
                    print(f'\nprocess finished with exit code 1 (no date inputted)\n')
                    exit()
            
        # experiments performed on multiple days
        else:
            message_input_date = f'Input the first date of the experiment as follows: \n\nyyyy-mm-dd'
            date_1 = simpledialog.askstring(title=None, prompt=message_input_date)
            message_input_date = f'Input the last date of the experiment as follows: \n\nyyyy-mm-dd'
            date_2 = simpledialog.askstring(title=None, prompt=message_input_date)

            # test validity of date
            try: 
                date.fromisoformat(date_1)
            except ValueError():
                messagebox.showerror(None, 'Fatal Error: \nImproper date format!')
                print(f'\nprocess finished with exit code 1 (improper date format: {date_1})\n')
                exit()
            else: 
                try: 
                    date.fromisoformat(date_2)
                except ValueError():
                    messagebox.showerror(None, 'Fatal Error: \nImproper date format!')
                    print(f'\nprocess finished with exit code 1 (improper date format: {date_2})\n')
                    exit()
            
            
            message_line_1 = 'Press "yes" if the dates are correct, "no" if they are incorrect, or "cancel" to exit'
            message_line_2 = f'\nyear:   \t{date_1[0:4]}'
            message_line_3 = f'\nmonth:  \t{date_1[5:7]}'
            message_line_4 = f'\nday:    \t{date_1[8:]}'
            message_line_5 = f'\nyear:   \t{date_2[0:4]}'
            message_line_6 = f'\nmonth:  \t{date_2[5:7]}'
            message_line_7 = f'\nday:    \t{date_2[8:]}'
            message = message_line_1+'\n\nFirst Date'+message_line_2+message_line_3+message_line_4+'\n\nLast Date'+message_line_5+message_line_6+message_line_7
            result = messagebox.askyesnocancel(title=None, message=message)
            if result == True: 
                experiment_date = date_1 + ' - ' + date_2
                break
            elif result == False:
                continue 
            else: 
                messagebox.showerror(None, 'Fatal Error: \nNo date inputted!')
                print(f'\nprocess finished with exit code 1 (no date inputted)\n')
                exit()
    return experiment_date





