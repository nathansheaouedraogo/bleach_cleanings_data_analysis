import pandas as pd
import plotly.express as px  
import file_management as fm
from tkinter import messagebox
import plotting
import process_peak 
import matplotlib

# update matplotlib paras to use stix font and tex notation
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.family'] = 'stixgeneral'
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

def pm_analysis():
    # # load raw data 
    # raw_data_path = fm.select_raw_data()
    
    # # prompt experiment_date
    # experiment_date = fm.input_date_of_experiment()
    
    # # create dirs in 'processed_data', return path
    # processed_data_path = fm.create_dir(f'processed_data', experiment_date)
    
    # # load df
    # df_wide = pd.read_csv(raw_data_path)
    # df_wide = df_wide[['Timestamp', 'PM Estimate']]
    # df_wide.reset_index(drop=True, inplace=True)
    # df_wide.rename(columns={
    #     'Timestamp':'datetime', 
    #     'PM Estimate':'pm_conc'}, 
    #     inplace=True)
    
    # # convert to long data frame, show on plotly 
    # df_long=pd.melt(df_wide, id_vars=['datetime'], value_vars=['pm_conc'])
    # fig = px.line(df_long, x='datetime', y='value', color='variable')
    # fig.show()
    # messagebox.showinfo(message='Please fill out experimental data dictionary')
    # while True:
    #     input = messagebox.askyesnocancel(title=None, message='Are all times inputted?')
    #     if input == True: 
    #         break 
    #     elif input == False: 
    #         continue
    #     else: 
    #         messagebox.showerror(None, 'Fatal Error: \n\n Cancelled processing experiments')
    #         print(f'\nprocess finished with exit code 1 (Cancelled processing experiments)\n')
    #         exit()
    # here we will load the experimental data dictionary using fm.load_dict
    experimental_data_dict = fm.load_experimental_data_dict()
    resolved_peaks_dict = {}
    print(resolved_peaks_dict)
    exit()
    
    
    for key in experimental_data_dict.keys():        
        resolved_peaks_dict[key] = process_peak.resolved_peaks_dict
        for i in range(len(experimental_data_dict[key]['condition'])):
            
            ## analyze dataset ##
            
            # process peak
            peak_conc, peak_area, num_of_measurements, slope, y_int, rsq, df_decay, df_peak_processed = process_peak.process_peak(key, i, df_wide, decimals=2)
            
            # fill resolved_peaks_dicts
            resolved_peaks_dict[key]['condition'].append(key['condition'][i])
            resolved_peaks_dict[key]['peak_area'].append(peak_area)
            resolved_peaks_dict[key]['peak_concentration'].append(peak_conc)
            resolved_peaks_dict[key]['linearized_decay_fit']['negative_decay_const'].append(slope)
            resolved_peaks_dict[key]['linearized_decay_fit']['ln_A'].append(y_int)
            resolved_peaks_dict[key]['linearized_decay_fit']['RSQ'].append(rsq)
            resolved_peaks_dict[key]['linearized_decay_fit']['#_measurements_taken_during_decay'] = num_of_measurements
            
            ## create plot of decay ##
            exp_fig = plotting.plot_peak(df_peak_processed)
            
            ## create plot of linearized decay##
            lin_fig = plotting.plot_lin_decay(df_decay, y_int, slope, rsq)
            
            
            ## save peak data ##
            fm.dump_processed_peak(processed_data_path, resolved_peaks_dict, resolved_peaks_dict[key]['condition'][i], df_peak_processed, df_decay, key, i, lin_fig, exp_fig)
            
            ## save graph of peak ##
            # df_peak_processed_wide=pd.melt(df_peak_processed, id_vars=['datetime'], value_vars=['pm_conc'])
            # fig = px.line(df_peak_processed, x='datetime', y='value', color='variable')
            # fig.update_layout(
            #     yaxis_title=r'$\text{PM Concentration} \left(\displaystyle\frac{\mu{g}}{m^3}\right)$',
            #     xaxis_title=r'Time (CST)'
            # )
            # fig.show()

            
    # save analysis of ENTIRE dataset
    fm.dump_dict(resolved_peaks_dict, f'pm_analysis', processed_data_path)
    print(f'\analysis of {experiment_date} saved to {processed_data_path}')

pm_analysis()