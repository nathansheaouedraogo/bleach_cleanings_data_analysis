## module processes peaks and returns all data 

import peak_ops
resolved_peaks_dict = {
                'condition' : [],
                'peak_area' : [],
                'peak_concentration' : [],
                'linearized_decay_fit' : {
                    'negative_decay_const' : [],
                    'ln_A' : [],
                    'RSQ' : []
                }
            }

def process_peak(experimental_dict, i, df_wide, decimals=2):
    """
    Resolves inputted peak based on values from experimental_dict

    Args:
        experimental_dict (_dict_): user inputted background, peak start/end times
        i (_int_): iterator to keep track of peak
        df_wide (_dataframe_): dataframe of experiment
        decimals (int, optional): sets sigfigs. Defaults to 2.

    Returns:
                peak_conc (_float_): background-corrected maximum concentration measured
                peak_area (_float_): area of peak based on start/end times
        num_of_measurements (_int_): number of measurements taken during decay
                    slope (_float_): slope of linearized decay fit
                    y_int (_float_): y_int of linearized decay fit
                    rsq   (_float_): rsq of linearized decay fit
    """
    peak_start_index, peak_end_index, background_start_index, background_end_index = peak_ops.load_peak(experimental_dict, i, df_wide)
    background_value = peak_ops.background(background_start_index, background_end_index, df_wide)
    df_peak_processed = peak_ops.subtract_background(df_wide, peak_start_index, peak_end_index, background_value, decimals)
    peak_conc, peak_area = peak_ops.calculate_peak_area_and_conc(df_peak_processed, decimals)
    num_of_measurements, slope, y_int, rsq = peak_ops.calculate_decay(df_peak_processed)
    
    return peak_conc, peak_area, num_of_measurements, slope, y_int, rsq
