import numpy as np
from sklearn.linear_model import LinearRegression as lm 

def linearized(y_data, peak=None):
    
    """
    Summary: 
        Function will linearize inputted data      
        
        Normalization of Data: 
            lin_y_data = ln(y_data[i]/max(y_data))
        
        NOTE: function sets any value <= 0 to zero! 
    Args:
        >>> y_data (_array_): array like numerical data to be linearized 
        >>> peak (_int_, _float_): user defined the peak concentration. If set to none, will pick first index.
        
    Returns: 
        >>> lin_y_data (_array_): normalized y_data
    """
    
    # user warnings
    for val in y_data: 
        if val <= 0: 
            print(f'\ninvalid value at index {y_data.index(val)}, replacing with 0')
    
    if peak: 
        peak_conc = peak
    else: 
        peak_conc = y_data[0]
    
    
    # apply log normalization 
    ln_y_data = [np.log(conc_i/peak_conc).astype(np.float) for conc_i in y_data]    
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
    slope_arr, y_int_arr, RSQ_arr = lin_reg.coef_[0], lin_reg.intercept_, round(lin_reg.score(x_data, y_data), rsq_decimals)
    slope = slope_arr.astype(np.float)
    y_int = y_int_arr.astype(np.float)
    RSQ = RSQ_arr.astype(np.float)
    return slope, y_int, RSQ
