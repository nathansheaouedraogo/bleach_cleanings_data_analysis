import pandas as pd
import plotly.express as px  
import file_management as fm
from tkinter import messagebox
import plotting
import process_peak 
import matplotlib
from processed_peak_class import data_dict

# update matplotlib paras to use stix font and tex notation
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.family'] = 'stixgeneral'
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'



def pm_analysis(time_resolution, timescale):
    # if timescale.lower() not in ['seconds', 'minutes', 'hours']:
    # messagebox.showerror(message='Fatal Error: Invalid timescale!')
    # print(process finished with exit code 1 (invalid timescale))
    # exit()
    
    # load raw data 
    raw_data_path = fm.select_raw_data()
    
    # prompt experiment_date
    experiment_date = fm.input_date_of_experiment()
    
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
    df_long=pd.melt(df_wide, id_vars=['datetime'], value_vars=['pm_conc'])
    fig = px.line(df_long, x='datetime', y='value', color='variable')
    fig.show()
    messagebox.showinfo(message='Please fill out experimental data dictionary')
    while True:
        input = messagebox.askyesnocancel(title=None, message='Are all times inputted?')
        if input == True: 
            break 
        elif input == False: 
            continue
        else: 
            messagebox.showerror(None, 'Fatal Error: \n\n Cancelled processing experiments')
            print(f'\nprocess finished with exit code 1 (Cancelled processing experiments)\n')
            exit()
    # here we will load the experimental data dictionary using fm.load_dict
    experimental_data_dict = fm.load_experimental_data_dict()
    resolved_peaks_dict = data_dict()
    print(resolved_peaks_dict)
    
    
    for dict_name in experimental_data_dict.keys():        
        
        for i in range(len(experimental_data_dict[dict_name]['condition'])):
            
            ## analyze dataset ##
            
            # process peak
            peak_conc, peak_area, num_of_measurements, slope, y_int, rsq, df_decay, df_peak_processed = process_peak.process_peak()
            
            # initialize resolved_peaks_dict
            resolved_peaks_dict.add_to(dict_name)
            
            # fill resolved_peaks_dict
            resolved_peaks_dict.append_value(dict_name, dict_name['condition'][i])
            resolved_peaks_dict.append_value(dict_name, 'peak_area', peak_area)
            resolved_peaks_dict.append_value(dict_name, 'peak_concentration', peak_conc)
            resolved_peaks_dict.append_value_to_fit_params(dict_name, 'negative_decay_const', slope)
            resolved_peaks_dict.append_value_to_fit_params(dict_name, 'ln_A', y_int)
            resolved_peaks_dict.append_value_to_fit_params(dict_name, 'RSQ', rsq)
            resolved_peaks_dict.append_value_to_fit_params(dict_name, 'num_of_measurements', num_of_measurements)
            
            ## save peak data ##
            
            # initialize dir for peak data
            peak_name = f"{dict_name}_{dict_name['condition'][i]}_{i+1}"
            peak_dir = fm.create_dir(processed_data_path, peak_name)
            
            # dump peak dictionary
            # TODO: might not work! supposed to get index and dump to folder
            resolved_peaks_dict.at_index(i, dict_name).dump_dict(peak_name, peak_dir)
            print(f"\nanalysis of {peak_name} saved to {peak_dir}")
            
            # save non-linearized peak data
            save_path = fm.concatenate_path(f"{peak_name}_peak.csv", peak_dir)
            df_peak_processed.to_csv(save_path, index=False)
            print(f"\ncsv of {peak_name} data saved to {peak_dir}")
            
            # save plot of non-linearized peak data
            exp_fig = plotting.plot_peak(df_peak_processed)
            save_path = fm.concatenate_path(f"{peak_name}_peak.png", peak_dir)
            exp_fig.savefig(save_path, bbox_inches='tight', dpi=600)
            print(f"\ngraph of {peak_name} saved to {peak_dir}")
            
            # save linearized decay data
            save_path = fm.concatenate_path(f"{peak_name}_lin_decay.csv", peak_dir)
            df_decay.to_csv(save_path, index=False)
            print(f"\ncsv of linearized {peak_name} decay data saved to {peak_dir}")
            
            # save plot of linearized decay
            lin_fig = plotting.plot_lin_decay(df_decay, y_int, slope, rsq)
            save_path = fm.concatenate_path(f"{peak_name}_lin_decay.png", peak_dir)
            lin_fig.savefig(save_path, bbox_inches="tight",dpi=600)
            print(f"\ngraph of linearized decay of {peak_name} saved to {peak_dir}")
            
    # save analysis of ENTIRE dataset
    resolved_peaks_dict.dump_dict(f'pm_analysis', processed_data_path)
    messagebox.showinfo(f'analysis saved to: \n{processed_data_path}\n')
    print(f'\nprocess finished with exit code 0\n\n')
pm_analysis()