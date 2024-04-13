import numpy as np
from tkinter import messagebox, simpledialog
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.ticker import AutoMinorLocator
from matplotlib.offsetbox import AnchoredText as at

# update matplotlib paras to use stix font and tex notation
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.family'] = 'stixgeneral'
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'


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

def plot_peak(df_peak_processed):
    """
    Summary: 
        Plots background corrected peak in 5 minute intervals
    """
    
    fig, ax = plt.subplots(1, figsize=(8, 4))
    ax.line(df_peak_processed['datetime'])
    
    # x-axis
    x_axis_min = df_peak_processed['datetime'].iat[0]
    x_axis_max = df_peak_processed['datetime'].iat[-1]
    ax.set_xlim(x_axis_min, x_axis_max)
    ax.set_xlabel(r'\textbf{Time} (CST)')
    ax.tick_params(axis='x', bottom=True, top=True, direction='inout')
    
        # major locator (1hr)
    xloc=md.MinuteLocator(interval = 5)
    ax.xaxis.set_major_locator(xloc)

    # major formatter
    majorFmt = md.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(majorFmt)

    # minor locator (15mins)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which='minor', length=5, width=1,)

    # auto-format
    fig.autofmt_xdate()

    fig.autofmt_xdate(which='both')
    
    return fig
