def scale_measurements(input, time_resolution, timescale, decimals=None, convert=True):
    """
    Summary:
        Scales evenly spaced timeseries data from unitless indices to minutes. 
        
    Args:
        input (_int_, _float_): input to be converted 
        time_resolution (_float_): time resolution of data, units specified by timescale
        timescale (_str_): 'seconds' -> convert from seconds to minutes; 1 -> to minutes; 2 -> hours to minutes 
        decimals (_int_): sets number of sig figs to display on graph. If set to None will NOT round off decimals (recommended)
        convert (bool, optional): If set to false will NOT convert. Defaults to True (recommended)
        
    Returns:
        output: converted input to units of per hour
    """
    if not convert: 
        return input 
    else:
        if timescale.lower() == 'seconds': 
            output = (time_resolution/60) * input
        if timescale.lower() == 'minutes': 
            output = time_resolution * input
        if timescale.lower() == 'hours': 
            output = (time_resolution*60) * input
    if decimals: 
        output = round(output, decimals)
    return output 