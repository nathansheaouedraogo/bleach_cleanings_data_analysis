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
    # slope = slope_arr.astype(float)
    # y_int = y_int_arr.astype(float)
    # RSQ = RSQ_arr.astype(float)
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