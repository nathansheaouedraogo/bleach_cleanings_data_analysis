## module processes peaks and returns all data 

import peak_ops

def process_peak(experimental_dict, i, df_wide, time_resolution, timescale):
    """
    Resolves inputted peak based on values from experimental_dict. 
    Outputs all operations and calculations done on peak. 

    Args:
        experimental_dict (_dict_): user inputted background, peak start/end times
        i (_int_): iterator to keep track of peak
        df_wide (_dataframe_): dataframe of experiment
        time_resolution (_float_): #measurements/timescale
        timescale (_str_): 'seconds', 'minutes', 'hours'

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
    peak_start_index, peak_end_index, background_start_index, background_end_index = peak_ops.load_peak(experimental_dict, i, df_wide)
    background_value = peak_ops.background(background_start_index, background_end_index, df_wide)
    df_peak_processed = peak_ops.subtract_background(df_wide, peak_start_index, peak_end_index, background_value)
    peak_conc, peak_area = peak_ops.calculate_peak_area_and_conc(df_peak_processed)
    decay_length, slope, y_int, rsq, df_decay = peak_ops.calculate_decay(df_peak_processed, time_resolution, timescale)
    
    output = (peak_area, peak_conc, slope, y_int, decay_length, rsq, df_peak_processed, df_decay)
    
    return output
