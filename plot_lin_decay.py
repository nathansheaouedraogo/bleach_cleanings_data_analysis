import numpy as np
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText as at

def plot_lin_decay(df_decay, y_int, slope, rsq, sig_figs=4):
    
    """
    Summary: 
        Plots linearized best fit with fit
    Args: 
        df_decay (_dataframe_): dataframe of linearized decay
        y_int (_float_): float of y-intercept
        slope (_float_): float of slope of fit. displayed as tau. (NOTE: input should be NEGATIVE)
        rsq (_float_): calculated RSQ (NOTE: defaults to 4 decimal places. change rsq_decimals in peak_ops.calculate_decay if needed.)
        sig_figs (_int_, optional): number of sig figs to display on graph. defaults to 4. (NOTE: does NOT affect rsq!)
    Returns:
        fig: figure of linearized decay with fit
    """
    
    fig, ax = plt.subplots(1, figsize=(8, 4))
    ax.scatter(df_decay['decay_time'], df_decay['ln_pm_conc'], color='k')
    ax.line(df_decay['decay_time'], df_decay['best_fit'], color='k--')
    
    # eqn
    y_int_str = str(np.around(y_int, sig_figs)[0])
    if y_int_str[0] != '-':
        y_int_str = '+' + y_int_str
    slope_str = str(np.around(slope, sig_figs)[0]*-1) # NOTE: slope (tau) is shown as a positive value     
    r_sqr_str = str(rsq)
    
    # x-axis
    x_axis_min = df_decay['decay_time'].iat[0]
    x_axis_max = df_decay['decay_time'].iat[-1]
    ax.set_xlim(x_axis_min, x_axis_max)
    while True:
        time_int = simpledialog.askstring(message='please choose time interval of measurements (Hours, Minutes, Seconds)')
        if not time_int:
            messagebox.showerror(f'No label inputted!')
            continue
        elif time_int.lower() == 'hours':
            ax.set_xlabel(f'Hours')
            eqn_rsq = r'\begin{align*}y&=\tau\left(x\right)y_int\\{\tau}&=slope{hr^{-1}}\\{R^2}&=rsq\end{align*}'.replace('y_int', y_int_str).replace('slope', slope_str).replace('rsq', r_sqr_str)
            break
        elif time_int.lower() == 'minutes':
            ax.set_xlabel(f'Minutes')
            eqn_rsq = r'\begin{align*}y&=\tau\left(x\right)y_int\\{\tau}&=slope{min^{-1}}\\{R^2}&=rsq\end{align*}'.replace('y_int', y_int_str).replace('slope', slope_str).replace('rsq', r_sqr_str)
            break
        elif time_int.lower() == 'seconds':
            ax.set_xlabel(f'Seconds')
            eqn_rsq = r'\begin{align*}y&=\tau\left(x\right)y_int\\{\tau}&=slope{s^{-1}}\\{R^2}&=rsq\end{align*}'.replace('y_int', y_int_str).replace('slope', slope_str).replace('rsq', r_sqr_str)
            break
        else:
            messagebox.showerror(f'Improper format, must be hours, minutes, or seconds!')
            continue
    
    # add equation, finish setting up x-axis
    textbox = at(eqn_rsq, loc='upper right')
    ax.add_artist(textbox)    
    ax.tick_params(axis='x', bottom=True, top=True, direction='inout')
    
    # y-axis
    ax.tick_params(axis='y', left=True, right=True, direction='inout')
    ax.set_ylabel(r'$\ln\left(\displaystyle\frac{PM_{conc.}}{PM_{peak}}\right)$')
    return fig
