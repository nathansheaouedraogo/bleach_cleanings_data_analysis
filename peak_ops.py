## Module performs calculations and data wrangling on peaks
## does all the heavy lifting. decided to move it outside of process_peak module 
## lin_reg and integrate_peak modules moved here as well to clean up code

from time_wrangling import scale_measurements 
import numpy as np
from sklearn.linear_model import LinearRegression as lm 

def linearized(y_data, peak=None, log_file=None):
    
    """
    Summary: 
        Function will linearize inputted data      
        
        Normalization of Data: 
            lin_y_data = ln(y_data[i]/max(y_data))
        
        !WARNING!: any value after background correction less than zero is set to 0 automatically
    Args:
        >>> y_data (_array_): array like numerical data to be linearized 
        >>> peak (_int_, _float_, opt): user defined the peak concentration. If set to none, will pick first index.
        >>> log_file (_list_, opt): log file from fm.track_log() class. defaulted to None.
    Returns: 
        >>> lin_y_data (_array_): normalized y_data
    """
    
    # user warnings
    for val in y_data: 
        if val <= 0: 
            message_1 = f'\nWARNING: invalid value {val} at index {y_data.index(val)}, replacing with 0'
            if log_file: 
                log_file.add_line(message_1)
            print(message)

    # if user selected peak exisits, set as peak. else, select first index in list. 
    if peak: 
        peak_conc = peak
    else: 
        peak_conc = y_data[0]
    
    
    # apply log normalization 
    ln_y_data = [np.log(conc_i/peak_conc).astype(float) for conc_i in y_data]    
    return ln_y_data

def regression(x_data, y_data, rsq_decimals=4):
    
    """
    Summary: 
        Function calculates a linear regression on x_data and y_data
    Args:
    
        x_data (_array_): array like numerical data
        y_data (_array_): array like numerical data
        rsq_decimals (_int_): sets decimals of RSQ. default to 4. 
    
    Returns: 
        slope, y_int, RSQ
    """
    
    # apply linear regression 
    lin_reg = lm().fit(x_data, y_data)
    slope, y_int, RSQ = lin_reg.coef_[0][0], lin_reg.intercept_[0], round(lin_reg.score(x_data, y_data), rsq_decimals)
    return slope, y_int, RSQ

def residuals(y_data, y_fit):
    """
    Summary: 
        Function calculates the residuals between fit and data
    Args:
    
        y_data (_array_): array like numerical data of  measured data
        y_fit (_array_): array like numerical data of  calculated data
    
    Returns: 
        residuals (_array_): list of residuals
    """
    
    residuals = []
    for i in range(len(y_data)):
        residuals.append(y_data[i]-y_fit[i])
    return residuals

def tangent_line(x_left, x_right, y_right, y_left): 
    """
    Summary:
        Function fits a tangent line between two points 
        at the edge of a peak.
    Args:
        x_left (numeric)  : left most x value. must be numeric. 
        x_right (numeric) : right most x value. must be numeric.
        y_left (numeric)  : left most y value. must be numeric. 
        y_right (numeric) : right most y value. must be numeric.
        
    Returns:
        slope (_float_), y_int (_float_): fitting paras of tangent line
    """
    
    tangent_line = np.polyfit([x_right, x_left], [y_right, y_left], 1)
    slope = tangent_line[0]
    y_int = tangent_line[1]
    return slope, y_int

def skim_data(x_data, y_data):
        
    """
    Summary: 
        Function 'skims' values based on calculated tangent line. 
        Calculated tangent line taken to be the 'baseline'. 
        Returns corrected y-values. 
    """
    
    slope, y_int = tangent_line(x_data[0], x_data[-1], y_data[0], y_data[-1])
    skimmed_points = []
    for i in range(len(x_data)):
        y_skimmed = y_data[i] - (slope*x_data[i] + y_int)
        skimmed_points.append(y_skimmed)
    return skimmed_points 

def integrate_peak(x_data, y_data):
    
    """
    Summary: 
        Function resolves peak based on NUMERIC x and y values
        index[0] is the start of the peak, index [-1] is the end of the peak
    """
    
    skimmed_data = skim_data(x_data, y_data)

    integrated_area = np.trapz(skimmed_data, x_data)
    
    return integrated_area
    
def load_peak(experimental_dict, i, df_wide):
    
    """
    i is the index of the experiment and df_wide is the experimental dataframe
    Experiment 1 = idx[0], exp 2 = idx[1], etc...
    Returns indices of times
    """
    
    ## SELECT TIMES ##
    # select peak range
    peak_start_time = experimental_dict['peak_start_datetime'][i]
    peak_end_time = experimental_dict['peak_end_datetime'][i]
    
    # select background values 
    background_start_time = experimental_dict['background_start_datetime'][i]
    background_end_time = experimental_dict['background_end_datetime'][i]
    
    ## SELECT INDICES ##
    # return indices of dataframe, print values
    peak_start_index = df_wide.index[df_wide['datetime'] == peak_start_time][0]
    peak_end_index = df_wide.index[df_wide['datetime']==peak_end_time][0]
    background_start_index =df_wide.index[df_wide['datetime'] == background_start_time][0]
    background_end_index =df_wide.index[df_wide['datetime'] == background_end_time][0]
    
    return peak_start_index, peak_end_index, background_start_index, background_end_index
    
def background(background_start_index, background_end_index, df_wide):
    """
    Calculates background concentration
    """
    background = df_wide.iloc[background_start_index:background_end_index+1]['pm_conc'].mean()
    return background

def subtract_background(df_wide, peak_start_index, peak_end_index, background_value):
    
    """
    Filters df_wide down to selected peak range and corrects for background value
    Processes area, peak, (and returns them!)
    Defaults to rounding background to 2 decimals. Can be changed!
    """
    
    # filter df
    df_peak_processed = df_wide.iloc[peak_start_index:peak_end_index+1]
    df_peak_processed.reset_index(inplace=True,drop=True)

    # background correct pm_conc, truncate to peak
    df_peak_processed['pm_conc'] -= background_value
    
    return df_peak_processed

def calculate_peak_area_and_conc(df_peak_processed):
    """
    Processes area, peak, (and returns them!)
    """
    # calculate peak concentration 
    elapsed_time = []
    for idx in range(len(df_peak_processed['datetime'])):
        elapsed_time.append(idx)
    peak_conc = df_peak_processed.pm_conc.max()
    peak_area = integrate_peak(elapsed_time, df_peak_processed['pm_conc'].to_list())
    return peak_conc, peak_area 

def calculate_decay(df_peak_processed, time_resolution, timescale, rsq_decimals=4, peak=None, log_file=None):
    
    """
    Summary:
        Linearizes decay and calculates fit (including residuals)
        RSQ is defaulted to 4 decimals, change if wanted    
    Args: 
        df_peak_processed (_dataframe_): background corrected dataframe of peak
        time_resolution (_numeric_): time resolution of measurements
        timescale (_str_): units of time resolution
        rsq_decimals (_int_): defaulted to round rsq to 4 decimals
        peak (_int_, _float_, opt): user defined the peak concentration. If set to none, will pick first index.
        log_file (_list_, opt): log file from fm.track_log() class. defaulted to None.
    Returns: 
        max(df_decay['minutes']) (_numeric_): length of decay in minutes
        slope (_numeric_): slope of fit in units of [conc]/min (can be changed by modifying 'time_wrangling.scale_measurements()')
        y_int (_numeric_): y-intercept of fit
        round(rsq, rsq_decimals) (_numeric_): calculated r^2 of fit, rounded to 'rsq_decimals'
        df_decay (_dataframe_): linearized decay data
    """
    
    # filter dataframe to decay
    peak_concentration = df_peak_processed['pm_conc'].max()
    peak_concentration_index = df_peak_processed.index[df_peak_processed['pm_conc'] == peak_concentration][0]
    df_decay = df_peak_processed.iloc[peak_concentration_index:df_peak_processed.index.max() + 1]
    df_decay.reset_index(inplace=True, drop=True)
        
    # linearize decays
    df_decay['ln_pm_conc'] = linearized(df_decay.pm_conc.to_list(), peak, log_file)
    
    # each index coresponds to 1 measurement
    # code below converts the index to appropriate timestamp in minutes
    # NOTE: code may be modified to change scale to units of per second or per hour
    df_decay['minutes'] = [scale_measurements(idx, time_resolution, timescale) for idx in df_decay.index]
        
    # set x data, y data
    x_data = df_decay['minutes'].to_numpy().reshape(-1,1)
    y_data = df_decay['ln_pm_conc'].to_numpy().reshape(-1,1)
    
    # calculate regression
    slope, y_int, rsq = regression(x_data, y_data)
    
    # calculate linear fit
    df_decay['best_fit'] = [slope*x+y_int for x in df_decay['minutes']]
    
    # calculate residuals
    df_decay['residuals'] = residuals(df_decay['ln_pm_conc'].to_list(), df_decay['best_fit'].to_list())
    
    # reorder dataframe columns 
    #! BE VIGILANT IN TYPING COLUMN TITLES! Misspelling column names will result in column of NaNs (and no flagged error!)
    ordered_columns = ['datetime', 'minutes', 'pm_conc', 'ln_pm_conc', 'best_fit', 'residuals']
    df_decay = df_decay.reindex(columns=ordered_columns)
    return df_decay['minutes'].max(), slope, y_int, round(rsq, rsq_decimals), df_decay

