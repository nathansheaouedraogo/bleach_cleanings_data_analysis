import pandas as pd
import plotly.express as px  
import file_management as fm
from tkinter import messagebox
import plotting
from process_peak import process_peak as process
import matplotlib
from processed_peak_class import data_dict

# update matplotlib paras to use stix font and tex notation
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.family'] = 'stixgeneral'
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'



def pm_analysis(time_resolution, timescale, show_raw_peaks=True):
    # if timescale.lower() not in ['seconds', 'minutes', 'hours']:
    # messagebox.showerror(message='Fatal Error: Invalid timescale!')
    # print(process finished with exit code 1 (invalid timescale))
    # exit()
    
    # load raw data 
    raw_data_path = fm.select_raw_data()
    
    # prompt experiment_date
    # experiment_date = fm.input_date_of_experiment()
    experiment_date = '2024-03-28 - 2024-03-29'
    # create dirs in 'processed_data', return path
    processed_data_path = fm.create_dir(f'processed_data', experiment_date)
    
    # load df
    df_wide = pd.read_csv(raw_data_path)
    df_wide = df_wide[['Timestamp', 'PM Estimate']]
    df_wide.reset_index(drop=True, inplace=True)
    df_wide.rename(columns={
        'Timestamp':'datetime', 
        'PM Estimate':'pm_conc'}, 
        inplace=True)
    
    # convert to long data frame, show on plotly 
    if show_raw_peaks:
        df_long=pd.melt(df_wide, id_vars=['datetime'], value_vars=['pm_conc'])
        fig = px.line(df_long, x='datetime', y='value', color='variable')
        fig.show()
    
        while True:
            input = messagebox.askyesnocancel(title=None, message='Are all times inputted?')
            if input == True: 
                break 
            elif input == False: 
                continue
            else: 
                messagebox.showerror(None, 'Fatal Error: \n\n Cancelled processing experiments\n')
                print(f'\nprocess finished with exit code 1 (Cancelled processing experiments)\n')
                exit()
    
    # here we will load the experimental data dictionary using fm.load_dict
    messagebox.showinfo(message='Please load the experimental times dictionary')
    experimental_data_dict = fm.load_experimental_data_dict()
    resolved_peaks_dict = data_dict()
    
    for dict_name in experimental_data_dict.keys():        
        
        for i in range(len(experimental_data_dict[dict_name]['condition'])):
            
            ## analyze dataset ##
            
            # process peak please see "process_peak.process_peak()" docstring for information 
            processed_peak = process(experimental_data_dict, i, df_wide, time_resolution, timescale)
            
            # initialize resolved_peaks_dict
            resolved_peaks_dict.add_to(dict_name)
            
            # fill resolved_peaks_dict
            resolved_peaks_dict.append_condition(dict_name, experimental_data_dict[dict_name]['condition'][i])
            resolved_peaks_dict.append_peak_area(dict_name, processed_peak[0])            
            resolved_peaks_dict.append_peak_concentration(dict_name, processed_peak[1]) 
            resolved_peaks_dict.append_negative_decay_constant(dict_name, processed_peak[2])           
            resolved_peaks_dict.append_decay_y_int(dict_name, processed_peak[3])
            resolved_peaks_dict.append_decay_rsq(dict_name, processed_peak[4])
            resolved_peaks_dict.append_decay_length_minutes(dict_name, processed_peak[5])
            
            # check validity
            if resolved_peaks_dict.is_invalid():
                messagebox.showerror('Error: Invalid Resolved Peaks Dictionary\n')
                exit_message = f'process finished with exit code 0 (invalid resolved peaks dictionary, will not save this peak):'
                print(exit_message+f'\n{resolved_peaks_dict.return_dict()}\n')
                continue
            
            # initialize dir for peak data
            peak_name = f"{dict_name}_{dict_name['condition'][i]}_{i+1}"
            peak_dir = fm.create_dir(processed_data_path, peak_name)
            
            # dump peak dictionary
            # TODO: might not work! supposed to get index and dump to folder
            resolved_peaks_dict.at_index(i, dict_name).dump_json(peak_name, peak_dir)
            print(f"\nanalysis of {peak_name} saved to {peak_dir}")
            
            # save non-linearized peak data
            save_path = fm.concatenate_path(f"{peak_name}_peak.csv", peak_dir)
            processed_peak[6].to_csv(save_path, index=False)
            print(f"\ncsv of {peak_name} data saved to {peak_dir}")
            
            # save plot of non-linearized peak data
            exp_fig = plotting.plot_peak(processed_peak[6])
            save_path = fm.concatenate_path(f"{peak_name}_peak.png", peak_dir)
            exp_fig.savefig(save_path, bbox_inches='tight', dpi=600)
            print(f"\ngraph of {peak_name} saved to {peak_dir}")
            
            # save linearized decay data
            save_path = fm.concatenate_path(f"{peak_name}_lin_decay.csv", peak_dir)
            processed_peak[7].to_csv(save_path, index=False)
            print(f"\ncsv of linearized {peak_name} decay data saved to {peak_dir}")
            
            # save plot of linearized decay
            lin_fig = plotting.plot_lin_decay(processed_peak[7], processed_peak[3], processed_peak[2], processed_peak[4])
            save_path = fm.concatenate_path(f"{peak_name}_lin_decay.png", peak_dir)
            lin_fig.savefig(save_path, bbox_inches="tight",dpi=600)
            print(f"\ngraph of linearized decay of {peak_name} saved to {peak_dir}")
            
    # save analysis of ENTIRE dataset
    resolved_peaks_dict.dump_dict(f'pm_analysis', processed_data_path)
    messagebox.showinfo(f'analysis saved to: \n{processed_data_path}\n')
    print(f'\nprocess finished with exit code 0\n\n')
