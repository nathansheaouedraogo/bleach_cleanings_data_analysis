import numpy as np
import pandas as pd
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
    ax.scatter(df_decay['minutes'], df_decay['ln_pm_conc'], color='k')
    ax.plot(df_decay['minutes'], df_decay['best_fit'], 'k-')
    
        
    # eqn
    y_int_str = str(np.around(y_int, sig_figs))
    if y_int_str[0] != '-':
        y_int_str = '+' + y_int_str
    slope_str = str(round(slope, sig_figs)*-1) # NOTE: slope (tau) is shown as a positive value     
    r_sqr_str = str(rsq)
    
    # x-axis
    x_axis_min = df_decay['minutes'].iat[0]
    x_axis_max = df_decay['minutes'].iat[-1]
    ax.set_xlim(x_axis_min, x_axis_max)
    ax.set_xlabel(f'Minutes Since Decay')
    eqn_rsq = r'\begin{align*}y&=\tau\left(x\right)y_int\\{\tau}&=slope{min^{-1}}\\{R^2}&=rsq\end{align*}'.replace('y_int', y_int_str).replace('slope', slope_str).replace('rsq', r_sqr_str)
        
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
        Plots background corrected peak
    """
    
    # convert x data to datetime
    datetime_data = pd.to_datetime(df_peak_processed['datetime']).to_list()
    
    fig, ax = plt.subplots(1, figsize=(8, 4))
    ax.scatter(datetime_data, df_peak_processed['pm_conc'], color='k')
    
    # majorFmt = md.DateFormatter('%H:%M')
    # x-axis
    x_axis_min = datetime_data[0]
    x_axis_max = datetime_data[-1]
    ax.set_xlim(x_axis_min, x_axis_max)
    ax.set_xlabel(r'\textbf{Time} (CST)')
    ax.tick_params(axis='x', bottom=True, top=True, direction='inout')
    
    # y-axis
    ax.tick_params(axis='y', left=True, right=True, direction='inout')
    ax.set_ylabel(r'$\frac{\mu{g}}{m^3}$')
    
    #major locator (4 mins)
    xloc = md.MinuteLocator(byminute=range(0,60), interval = 4)
    ax.xaxis.set_major_locator(xloc)
    
    # minor locator (2mins)
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))    
    
    # # major formatter
    majorFmt = md.DateFormatter('%H:%M')
    fig.autofmt_xdate(which='both')    
    ax.xaxis.set_major_formatter(majorFmt)
    
    return fig
