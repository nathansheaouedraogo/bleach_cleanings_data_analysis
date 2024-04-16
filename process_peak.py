## module processes peaks and returns all data 

import peak_ops

def process_peak(experimental_dict, i, df_wide, time_resolution, timescale, log_file=None):
    """
    Resolves inputted peak based on values from experimental_dict. 
    Outputs all operations and calculations done on peak. 

    Args:
        experimental_dict (_dict_): user inputted background, peak start/end times
        i (_int_): iterator to keep track of peak
        df_wide (_dataframe_): dataframe of experiment
        time_resolution (_float_): #measurements/timescale
        timescale (_str_): 'seconds', 'minutes', 'hours'
        log (_list_, opt): log file from file_management.track_log(). Defaulted to none.
    Returns:
        output (_tuple_):
            >>> peak_area (_float_): area of peak based on start/end times (output[0])
            >>> peak_conc (_float_): background-corrected maximum concentration measured (output[1])
            >>> slope (_float_): slope of linearized peak decay fit (output[2])
            >>> y_int (_float_): y_int of linearized peak decay fit (output[3])
            >>> rsq (_float_): rsq of linearized peak decay fit (output[4])
            >>> decay_length (_float_, _int_): length of peak decay in minutes (output[5])
            >>> df_peak_processed (_dataframe_): background corrected dataframe of peak (output[6]) 
            >>> df_decay  (_dataframe_): linearized dataset of peak decay (output[7]) 
    """
    # output messages 
    message_1 = f'~~~Loading Peak {i+1}~~~'
    if log_file:
        log_file.add_line(message_1)
    print(message_1)

    # load peak data
    peak_start_index, peak_end_index, background_start_index, background_end_index = peak_ops.load_peak(experimental_dict, i, df_wide)
    
    # peak id output
    message_2 = f'\n            Condition:    {experimental_dict["condition"][i]}'
    if log_file:
        log_file.add_line(message_2)
    print(message_2)
    message_3 = f'\n      Peak Start Time:    {experimental_dict["peak_start_datetime"][i]}'
    if log_file:
        log_file.add_line(message_3)
    print(message_3)
    message_4 = f'\n        Peak End Time:    {experimental_dict["peak_end_datetime"][i]}'
    if log_file:
        log_file.add_line(message_4)
    print(message_4)
    message_5 = f'\nBackground Start Time:    {experimental_dict["background_start_datetime"][i]}'
    if log_file:
        log_file.add_line(message_5)
    print(message_5)
    message_6 = f'\n  Background End Time:    {experimental_dict["background_end_datetime"][i]}'
    if log_file:
        log_file.add_line(message_6)
    print(message_6)
    
    # background value
    message_17 = '\n~~~Calculating Background~~~'
    if log_file: 
        log_file.add_line(message_17)
    print(message_17)
    background_value = peak_ops.background(background_start_index, background_end_index, df_wide)
    message_7 = f'\n           Background:    {background_value}'
    if log_file:
        log_file.add_line(message_7)
    print(message_7)
    
    # subtract dataframe from peak data
    df_peak_processed = peak_ops.subtract_background(df_wide, peak_start_index, peak_end_index, background_value)
    
    # calculate peak_conc, peak_area
    message_8 = f'\n~~~Calculating Peak Area\Conc.~~~'
    if log_file:
        log_file.add_line(message_8)
    print(message_8)
    peak_conc, peak_area = peak_ops.calculate_peak_area_and_conc(df_peak_processed)
    message_9 = f'\n            Peak Area:    {peak_area}'
    if log_file:
        log_file.add_line(message_9)
    print(message_9)
    message_10 = f'\n            Peak Conc:    {peak_conc}'
    if log_file:
        log_file.add_line(message_10)
    print(message_10)
    
    # calculate decay_length, slope, y_int, rsq, df_decay
    message_11 =  f'\n\n~~~Calculating Linearized Decay Params~~~'
    if log_file: 
        log_file.add_line(message_11)
    print(message_11)
    decay_length, slope, y_int, rsq, df_decay = peak_ops.calculate_decay(df_peak_processed, time_resolution, timescale)
    message_12 = f'           decay length:    {df_decay["minutes"].max()} minutes'
    if log_file: 
        log_file.add_line(message_12)
    print(message_12)
    message_13 = f'                  slope:    {slope}'
    if log_file: 
        log_file.add_line(message_13)
    print(message_13)
    message_15 = f'                  y_int:    {y_int}'
    if log_file: 
        log_file.add_line(message_15)
    print(message_15)
    message_16 = f'                  r_sqr:    {rsq}'
    if log_file: 
        log_file.add_line(message_16)
    print(message_16)
    
    # output tuple (big boy!)
    output = (peak_area, peak_conc, slope, y_int, rsq, decay_length, df_peak_processed, df_decay)
    return output
