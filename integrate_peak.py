import numpy as np

def integrate_peak(x_data, y_data):
    
    """
    Summary: 
        Function resolves peak based on NUMERIC x and y values
        index[0] is the start of the peak, index [-1] is the end of the peak
    """
    
    
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
    
    skimmed_data = skim_data(x_data, y_data)

    integrated_area = np.trapz(skimmed_data, x_data)
    
    return integrated_area
    
