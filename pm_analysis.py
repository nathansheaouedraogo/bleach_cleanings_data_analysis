import pandas as pd
import plotly.express as px  
import file_management as fm
from tkinter import messagebox
import plotting
from process_peak import process_peak as process
from processed_peak_class import data_dict
pd.options.mode.chained_assignment = None  # default='warn', shuts up useless pd warnings 


def pm_analysis(time_resolution, timescale, show_raw_peaks):
    
    """
    Summary:
        Function analyzes pm peaks inputted by the user and saves analysis to "processed_peaks" directory. 
        Please see "README.md" before running this function.
    Arguments: 
        time_resolution (_int_, _float_): time resolution of measurements
        timescale (_str_): 'seconds', 'minutes', or 'hours'; unit of time resolution 
        show_raw_peaks(_bool_): set to true if wanting to view interactive plot of dataset
    """
    
    # init output log
    log = fm.track_log()
    
    # test input validity
    if not isinstance(time_resolution, int):
        if not isinstance(time_resolution, float):
            messagebox.showerror(message='Fatal Error: Invalid time resolution!\n')            
            message_1 = f'\nprocess finished with exit code 1 (invalid time resolution)\n'
            log.add_line(message_1)
            log.output(fm.cwd())
            print(message_1)
            exit()
    if timescale.lower() not in ['seconds', 'minutes', 'hours']:
        messagebox.showerror(message='Fatal Error: Invalid timescale!\n')
        message_2 = '\nprocess finished with exit code 1 (invalid timescale)\n'
        log.add_line(message_2)
        log.output(fm.cwd())
        print(message_2)
        exit()
    if not isinstance(show_raw_peaks, bool):
        messagebox.showerror(message='Fatal Error: Invalid input to show raw peaks!\n')
        message_3 = '\nprocess finished with exit code 1 (invalid input to show raw peaks)\n'
        log.add_line(message_3)
        log.output(fm.cwd())
        print(message_3)
        exit()
    
    # prompt experiment_date
    experiment_date = fm.input_date_of_experiment(log, fm.cwd())

    # create dirs in 'processed_data', return path
    processed_data_path = fm.create_dir(f'processed_data', experiment_date, log)
    
    # load raw data 
    raw_data_path = fm.select_raw_data(log, processed_data_path)
    
    
    # experiment_date = '2024-03-28 - 2024-03-29'
    
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
                message_4 = f'\nprocess finished with exit code 1 (Cancelled processing experiments)\n'
                log.add_line(message_4)
                log.output(fm.cwd())
                print(message_4)
                exit()
    
    # here we will load the experimental data dictionary using fm.load_dict
    messagebox.showinfo(message='Please load the experimental times dictionary')
    experimental_data_dict = fm.load_experimental_data_dict(log, processed_data_path)
    resolved_peaks_dict = data_dict()
    
    for dict_name in experimental_data_dict.keys():        
        
        # initialize resolved_peaks_dict
        resolved_peaks_dict.add_to(dict_name)
        
        for i in range(len(experimental_data_dict[dict_name]['condition'])):
            
            ## analyze dataset ##
            
            # process peak please see "process_peak.process_peak()" docstring for information 
            processed_peak = process(experimental_data_dict[dict_name], i, df_wide, time_resolution, timescale, log_file=log)
            
            
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
                message = f'process finished with exit code 0 (invalid resolved peaks dictionary, will not save this peak):'
                message_5 = message+f'\n{resolved_peaks_dict.return_dict()}\n'
                log.add_line(message_5)
                print(message_5)
                continue
            
            # initialize dir for peak data
            peak_name = f"{dict_name}_{experimental_data_dict[dict_name]['condition'][i]}_{i+1}"
            peak_dir_path = fm.create_dir(processed_data_path, peak_name, log)
            
            # dump peak dictionary
            peak_dict = resolved_peaks_dict.at_index(i, dict_name)
            fm.dump_dict(peak_dict, peak_name, peak_dir_path)
            message_6 = f"\nanalysis of {peak_name} saved to {peak_dir_path}"
            log.add_line(message_6)
            print(message_6)
            
            # save non-linearized peak data
            save_path = fm.concatenate_path(f"{peak_name}_peak.csv", peak_dir_path)
            processed_peak[6].to_csv(save_path, index=False)
            message_7 = f"\ncsv of {peak_name} data saved to {peak_dir_path}"
            log.add_line(message_7)
            print(message_7)
            
            # save plot of non-linearized peak data
            exp_fig = plotting.plot_peak(processed_peak[6])
            save_path = fm.concatenate_path(f"{peak_name}_peak.png", peak_dir_path)
            exp_fig.savefig(save_path, bbox_inches='tight', dpi=600)
            message_8 = f"\ngraph of {peak_name} saved to {peak_dir_path}"
            log.add_line(message_8)
            print(message_8)
            
            # save linearized decay data
            save_path = fm.concatenate_path(f"{peak_name}_lin_decay.csv", peak_dir_path)
            processed_peak[7].to_csv(save_path, index=False)
            message_9 = f"\ncsv of linearized {peak_name} decay data saved to {peak_dir_path}"
            log.add_line(message_9)
            print(message_9)
            
            # save plot of linearized decay
            lin_fig = plotting.plot_lin_decay(processed_peak[7], processed_peak[3], processed_peak[2], processed_peak[4])
            save_path = fm.concatenate_path(f"{peak_name}_lin_decay.png", peak_dir_path)
            lin_fig.savefig(save_path, bbox_inches="tight",dpi=600)
            message_10 = f"\ngraph of linearized decay of {peak_name} saved to {peak_dir_path}"
            log.add_line(message_10)
            print(message_10)
            
    # save analysis of ENTIRE dataset
    resolved_peaks_dict.dump_json(f'analysis', processed_data_path)
    message_11 = f'\nanalysis saved to: \n\n{processed_data_path}\n'
    log.add_line(message_11)
    print(message_11)
    
    # exit script execution
    exit_message = f'\nprocess finished with exit code 0\n\n'
    log.add_line(exit_message)
    log.output(processed_data_path)
    print(exit_message)
    exit() #TODO dk why the analysis runs after finishing...
