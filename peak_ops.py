## Module performs calculations and data wrangling on peaks
## does all the heavy lifting. decided to move it outside of process_peak module 
## in order to make it easier to fix and more modular 
import integrate_peak 
import lin_reg
from time_wrangling import scale_measurements 

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
    
    # output message 
    print(f'\n\n~~~Loading experiment {i+1}~~~')
    print(f'\n            Condition:    {experimental_dict["condition"][i]}')
    print(f'\n      Peak Start Time:    {peak_start_time}')
    print(f'\n      Peak Start Time:    {peak_end_time}')
    print(f'\nBackground Start Time:    {background_start_time}')
    print(f'\n  Background End Time:    {background_end_time}')
    
    return peak_start_index, peak_end_index, background_start_index, background_end_index
    
def background(background_start_index, background_end_index, df_wide):
    
    """
    Calculates background concentration
    """
    
    print(f'\n\n~~~Calculating Background~~~')
    background = df_wide.iloc[background_start_index:background_end_index+1]['pm_conc'].mean()
    print(f'\n           Background:    {background}')
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
    peak_area = integrate_peak.integrate_peak(elapsed_time, df_peak_processed['pm_conc'].to_list())
    
    # output message
    print(f'\n\n~~~Calculating Peak Area\Conc.~~~')
    print(f'\n            Peak Area:    {peak_area}')
    print(f'\n            Peak Conc:    {peak_conc}')
    
    return peak_conc, peak_area 

def calculate_decay(df_peak_processed, time_resolution, timescale, rsq_decimals=4):
    
    """
    Summary:
        Linearizes decay and calculates fit. 
        Returns number of measurements in decay, slope, y_int, rsq, and linearized dataset
        Units are in terms of measurements per hour
        NOTE: rsq_decimals defaults to 4 decimal places. Change if wanted!   
    Args: 
        df_peak_processed (_dataframe_): background corrected dataframe of peak
        time_resolution (_numeric_): time resolution of measurements
        timescale (_str_): units of time resolution
        rsq_decimals (_int_): defaulted to round rsq to 4 decimals
    Returns: 
        max(df_decay['minutes']) (_numeric_): length of decay in minutes
        slope (_numeric_): slope of fit in units of [conc]/min (can be changed by modifying 'time_wrangling.scale_measurements()')
        y_int (_numeric_): y-intercept of fit
        round(rsq, rsq_decimals) (_numeric_): calculated r^2 of fit, rounded to 'rsq_decimals'
        df_decay (_dataframe_): linearized decay data
        
    """
    
    # filter dataframe to decay
    df_decay = df_peak_processed.iloc[df_peak_processed.index.min():df_peak_processed.index.max() + 1]
    df_decay.reset_index(inplace=True, drop=True)
    
    print(f'\n\n~~~Calculating Linearized Decay Params~~~')
    
    # linearize decays
    df_decay['ln_pm_conc'] = lin_reg.linearized(df_decay.pm_conc.to_list())
    
    # each index coresponds to 1 measurement
    # code below converts the index to appropriate timestamp in minutes
    # NOTE: code may be modified to change scale to units of per second or per hour
    df_decay['minutes'] = [scale_measurements(idx, time_resolution, timescale) for idx in df_decay.index]
    print(f'           decay length:    {df_decay["minutes"].max()} minutes')
    
    # set x data, y data
    x_data = df_decay['minutes'].to_numpy().reshape(-1,1)
    y_data = df_decay['ln_pm_conc'].to_numpy().reshape(-1,1)
    
    # calculate regression
    slope, y_int, rsq = lin_reg.regression(x_data, y_data)
    
    # calculate linear fit
    df_decay['best_fit'] = [slope*x+y_int for x in df_decay['minutes']]
    
    print(f'                  slope:    {slope}')
    print(f'                  y_int:    {y_int}')
    print(f'                  r_sqr:    {rsq}')
    
    return df_decay['minutes'].max(), slope, y_int, round(rsq, rsq_decimals), df_decay

