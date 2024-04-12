import pandas as pd
import plotly.express as px  
import file_management as fm
import integrate_peak 
import numpy as np
from tkinter import messagebox
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.ticker import AutoMinorLocator
from matplotlib.offsetbox import AnchoredText as at
import lin_reg

# update matplotlib paras to use stix font and tex notation
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.family'] = 'stixgeneral'
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'


experiment_date = fm.input_date_of_experiment()

# create dirs in 'processed_data', return path
processed_data_path = fm.create_processed_data_dir(experiment_date)
print(processed_data_path)
exit()

# load raw data 
raw_data_path = fm.select_raw_data()
print(raw_data_path)
exit()
# file_path = r'C:\Users\Nathan\OneDrive - University of Saskatchewan\HAVOC\bleach_lab_cleanings\2 2024-01-31 - 2024-03-30.csv'

# load df
df_wide = pd.read_csv(raw_data_path)
df_wide = df_wide[['Timestamp', 'PM Estimate']]
df_wide.reset_index(drop=True, inplace=True)
df_wide.rename(columns={
    'Timestamp':'datetime', 
    'PM Estimate':'pm_conc'}, 
    inplace=True)

# convert to long data frame, show on plotly 
df_long=pd.melt(df_wide, id_vars=['datetime'], value_vars=['pm_conc'])
fig = px.line(df_long, x='datetime', y='value', color='variable')
fig.show()

messagebox.showinfo(message='Please fill out experimental data dictionary')
# load experimental data
experimental_data_dict = fm.load_experimental_data_dict()



# DO NOT FILL -> program fills this out  !
resolved_peaks_dict = {
    'bleachings_with_airfresh' : {
        'condition' : [],
        'peak_area' : [],
        'peak_concentration' : [],
        'reg_paras' : {
            'negative_decay' : [],
            'ln_A' : [],
            'decay_length' : [],
            'RSQ' : []
        }
    },
    'bleachings_without_airfresh' : {
        'condition' : [],
        'peak_area' : [],
        'peak_concentration' : [],
        'reg_paras' : {
            'negative_decay' : [],
            'ln_A' : [],
            'decay_length' : [],
            'RSQ' : []
        }
    },
}

# 
while True:
    input = messagebox.askyesnocancel(title=None, message='Are all times inputted?')
    if input == True: 
        break 
    elif input == False: 
        continue
    else: 
        messagebox.showerror(None, 'Fatal Error: \n\n Cancelled processing experiments')
        print(f'\nprocess finished with exit code 1 (Cancelled processing experiments)\n')
        exit()

df_corrected = pd.DataFrame()


print(f'\nProcessing experiment(s) done on {date}')


# this will be the dictionairy used for processing. feel free to change it when needed!
dict = experimental_data_dict['bleachings_with_airfresh']

# air freshener
for i in range(len(dict['bleachings_with_airfresh']['peak_start_datetime'])):
    
    
    # select peak range
    peak_start_time = dict['bleachings_with_airfresh']['peak_start_datetime'][i]
    peak_start_index =df_wide.index[df_wide['datetime'] == peak_start_time][0]
    peak_end_time = dict['bleachings_with_airfresh']['peak_end_datetime'][i]
    peak_end_index = df_wide.index[df_wide['datetime']==peak_end_time][0]
    
    # select background values 
    background_start_time = dict['bleachings_with_airfresh']['background_start_datetime'][i]
    background_start_index =df_wide.index[df_wide['datetime'] == background_start_time][0]
    background_end_time = dict['bleachings_with_airfresh']['background_end_datetime'][i]
    background_end_index =df_wide.index[df_wide['datetime'] == background_end_time][0]
    
    # background
    background = df_wide.iloc[background_start_index:background_end_index+1]['pm_conc'].mean()
    
    # filter df
    df_peak_processed = df_wide.iloc[peak_start_index:peak_end_index+1]
    df_peak_processed.reset_index(inplace=True,drop=True)

    # background correct pm_conc, truncate to peak
    df_peak_processed['pm_conc'] -= background
    df_peak_processed.pm_conc = df_peak_processed.pm_conc.round(decimals=2)
    
    print(f'\nProcessed df:')
    print(df_peak_processed)
    # append to df_corrected
    df_corrected = pd.concat([df_corrected, df_peak_processed], ignore_index=True, copy=False)
    print(f'\nCorrected df:')
    print(df_corrected)

    # calculate length of decay
    elapsed_time = []
    for idx in range(len(df_peak_processed['datetime'])):
        elapsed_time.append(idx)
    
    # tangent skim, resolve area and peak
    area, peak = integrate_peak.integrate_peak(elapsed_time, df_peak_processed['pm_conc'].to_list())
    
    # filter df_peak_processed to decay
    peak_conc = df_peak_processed.pm_conc.max()
    decay_start_index = df_peak_processed.index[df_peak_processed['pm_conc'] == peak_conc][0]
    print(max(df_peak_processed.index))
    print(df_peak_processed['pm_conc'][decay_start_index])
    
    df_decay = df_peak_processed.iloc[decay_start_index:max(df_peak_processed.index)+1]
    df_decay.reset_index(inplace=True, drop=True)
    
    # linearize decay
    df_decay['ln_pm_conc'] = lin_reg.linearized(df_decay.pm_conc.to_list())
    df_decay['decay_time'] = [idx for idx in df_decay.index]
    
    # convert 
    
    # set x data, y data
    x_data = df_decay['decay_time'].to_numpy().reshape(-1,1)
    y_data = df_decay['ln_pm_conc'].to_numpy().reshape(-1,1)

    # calculate regression
    slope, y_int, rsq = lin_reg.regression(x_data, y_data)

    # update resolved_peaks_dict
    resolved_peaks_dict['bleachings_with_airfresh']['condition'].append(experimental_data_dict['bleachings_with_airfresh']['condition'][i]) 
    resolved_peaks_dict['bleachings_with_airfresh']['peak_area'].append(float(area))
    resolved_peaks_dict['bleachings_with_airfresh']['peak_concentration'].append(float(peak))
    resolved_peaks_dict['bleachings_with_airfresh']['reg_paras']['negative_decay'].append(float(slope))
    resolved_peaks_dict['bleachings_with_airfresh']['reg_paras']['ln_A'].append(float(y_int))
    resolved_peaks_dict['bleachings_with_airfresh']['reg_paras']['decay_length'].append(int(len(df_decay.index)))
    resolved_peaks_dict['bleachings_with_airfresh']['reg_paras']['RSQ'].append(float(rsq))
    
    fig, ax = plt.subplots(1, figsize=(8, 4))
    ax.scatter(df_decay['decay_time'], df_decay['ln_pm_conc'], color='k')
    
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    
    # eqn
    y_int_str = str(np.around(y_int, 4)[0])
    slope_str = str(np.around(slope, 4)[0]*-1) # NOTE: tau is shown as a positive value     
    r_sqr_str = str(rsq)
    
    eqn_rsq = r'\begin{align*}y&=\tau\left(x\right)y_int\\{\tau}&=slope{min^{-1}}\\{R^2}&=rsq\end{align*}'.replace('y_int', y_int_str).replace('slope', slope_str).replace('rsq', r_sqr_str)
    textbox = at(eqn_rsq, loc='upper right')
    ax.add_artist(textbox)    
    # x-axis
    x_axis_min = df_decay['decay_time'].iat[0]
    x_axis_max = df_decay['decay_time'].iat[-1]
    ax.set_xlim(x_axis_min, x_axis_max)
    ax.set_xlabel(r'Minutes')
    ax.tick_params(axis='x', bottom=True, top=True, direction='inout')

    # y-axis
    ax.tick_params(axis='y', left=True, right=True, direction='inout')
    ax.set_ylabel(r'$\ln\left(\displaystyle\frac{PM_{conc.}}{PM_{peak}}\right)$')
    
    fig_name = f'decay_{i+1}_with_air_fresh.png'
    fig.savefig(fig_name, bbox_inches='tight',dpi=600)
    
# plotly plot
df_corrected_wide=pd.melt(df_corrected, id_vars=['datetime'], value_vars=['pm_conc'])
fig = px.line(df_corrected_wide, x='datetime', y='value', color='variable')
fig.update_layout(
    yaxis_title=r'$\text{PM Concentration} \left(\displaystyle\frac{\mu{g}}{m^3}\right)$',
    xaxis_title=r'Time (CST)'
)
fig.show()

df_corrected.to_csv('bleachings_with_airfresh.csv', index=False)

# convert to datetime
df_corrected['datetime'] = pd.to_datetime(df_corrected['datetime'])

# plot!
fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(df_corrected['datetime'], df_corrected['pm_conc'], color='k')

# x-axis
x_axis_min = df_corrected['datetime'].iat[0]
x_axis_max = df_corrected['datetime'].iat[-1]
ax.set_xlim(x_axis_min, x_axis_max)
ax.set_xlabel(r'\textbf{Time} (CST)')
ax.tick_params(axis='x', bottom=True, top=True, direction='inout')

# y-axis
ax.tick_params(axis='y', left=True, right=True, direction='inout')
ax.set_ylabel(r'\textbf{PM Concentration} $\left(\mu{g}{m}^{-3}\right)$')

## highlight illuminated conditions
ax.axvspan(pd.to_datetime(experimental_data_dict['bleachings_with_airfresh']['peak_start_datetime'][0]), 
        pd.to_datetime(experimental_data_dict['bleachings_with_airfresh']['peak_end_datetime'][0]), color='yellow', 
        alpha=0.5)

ax.axvspan(pd.to_datetime(experimental_data_dict['bleachings_with_airfresh']['peak_start_datetime'][2]),
        pd.to_datetime(experimental_data_dict['bleachings_with_airfresh']['peak_end_datetime'][2]), 
        color='yellow', 
        alpha=0.5)

## highlight dark conditions
ax.axvspan(pd.to_datetime(experimental_data_dict['bleachings_with_airfresh']['peak_start_datetime'][1]), 
        pd.to_datetime(experimental_data_dict['bleachings_with_airfresh']['peak_end_datetime'][1]), 
        color='orange', 
        alpha=0.5)

# major locator (1hr)
xloc=md.HourLocator(interval = 1)
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
fig.show()
fig.savefig('bleach_cleanings_with_airfresh.png', bbox_inches='tight', dpi=600)
del fig, df_corrected, ax, df_peak_processed


df_corrected = pd.DataFrame()

# no air freshener
for i in range(len(experimental_data_dict['bleachings_without_airfresh']['peak_start_datetime'])):
    
    
    # select peak range
    peak_start_time = experimental_data_dict['bleachings_without_airfresh']['peak_start_datetime'][i]
    peak_start_index =df_wide.index[df_wide['datetime'] == peak_start_time][0]
    peak_end_time = experimental_data_dict['bleachings_without_airfresh']['peak_end_datetime'][i]
    peak_end_index = df_wide.index[df_wide['datetime']==peak_end_time][0]
    
    # select background values 
    background_start_time = experimental_data_dict['bleachings_without_airfresh']['background_start_datetime'][i]
    background_start_index =df_wide.index[df_wide['datetime'] == background_start_time][0]
    background_end_time = experimental_data_dict['bleachings_without_airfresh']['background_end_datetime'][i]
    background_end_index =df_wide.index[df_wide['datetime'] == background_end_time][0]
    
    # background
    background = df_wide.iloc[background_start_index:background_end_index+1]['pm_conc'].mean()
    
    # filter df
    df_peak_processed = df_wide.iloc[peak_start_index:peak_end_index+1]
    df_peak_processed.reset_index(inplace=True,drop=True)

    # background correct pm_conc, truncate to peak
    df_peak_processed['pm_conc'] -= background
    df_peak_processed.pm_conc = df_peak_processed.pm_conc.round(decimals=2)
    
    print(f'\nProcessed df:')
    print(df_peak_processed)
    # append to df_corrected
    df_corrected = pd.concat([df_corrected, df_peak_processed], ignore_index=True, copy=False)
    print(f'\nCorrected df:')
    print(df_corrected)

    # calculate length of decay
    elapsed_time = []
    for idx in range(len(df_peak_processed['datetime'])):
        elapsed_time.append(idx)
    
    # tangent skim, resolve area and peak
    area, peak = integrate_peak.integrate_peak(elapsed_time, df_peak_processed['pm_conc'].to_list())
    
    # filter df_peak_processed to decay
    peak_conc = df_peak_processed.pm_conc.max()
    decay_start_index = df_peak_processed.index[df_peak_processed['pm_conc'] == peak_conc][0]
    print(max(df_peak_processed.index))
    print(df_peak_processed['pm_conc'][decay_start_index])
    
    df_decay = df_peak_processed.iloc[decay_start_index:max(df_peak_processed.index)+1]
    df_decay.reset_index(inplace=True, drop=True)
    
    # linearize decay
    df_decay['ln_pm_conc'] = lin_reg.linearized(df_decay.pm_conc.to_list())
    df_decay['decay_time'] = [idx for idx in df_decay.index]
    
    # convert 
    
    # set x data, y data
    x_data = df_decay['decay_time'].to_numpy().reshape(-1,1)
    y_data = df_decay['ln_pm_conc'].to_numpy().reshape(-1,1)

    # calculate regression
    slope, y_int, rsq = lin_reg.regression(x_data, y_data)

    # update resolved_peaks_dict
    resolved_peaks_dict['bleachings_without_airfresh']['condition'].append(experimental_data_dict['bleachings_without_airfresh']['condition'][i]) 
    resolved_peaks_dict['bleachings_without_airfresh']['peak_area'].append(float(area))
    resolved_peaks_dict['bleachings_without_airfresh']['peak_concentration'].append(float(peak))
    resolved_peaks_dict['bleachings_without_airfresh']['reg_paras']['negative_decay'].append(float(slope))
    resolved_peaks_dict['bleachings_without_airfresh']['reg_paras']['ln_A'].append(float(y_int))
    resolved_peaks_dict['bleachings_without_airfresh']['reg_paras']['decay_length'].append(int(len(df_decay.index)))
    resolved_peaks_dict['bleachings_without_airfresh']['reg_paras']['RSQ'].append(float(rsq))
    
    fig, axs = plt.subplots(1, figsize=(8, 4))
    axs.scatter(df_decay['decay_time'], df_decay['ln_pm_conc'], color='k')
    
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    
    # eqn
    y_int_str = str(np.around(y_int, 4)[0])
    slope_str = str(np.around(slope, 4)[0]*-1) # NOTE: tau is shown as a positive value     
    r_sqr_str = str(rsq)
    eqn_rsq = r'\begin{align*}y&=\tau\left(x\right)y_int\\{\tau}&=slope{min^{-1}}\\{R^2}&=rsq\end{align*}'.replace('y_int', y_int_str).replace('slope', slope_str).replace('rsq', r_sqr_str)
    textbox = at(eqn_rsq, loc='upper right')
    axs.add_artist(textbox)    

    # x-axis
    x_axis_min = df_decay['decay_time'].iat[0]
    x_axis_max = df_decay['decay_time'].iat[-1]
    axs.set_xlim(x_axis_min, x_axis_max)
    axs.set_xlabel(r'Minutes')
    axs.tick_params(axis='x', bottom=True, top=True, direction='inout')

    # y-axis
    axs.tick_params(axis='y', left=True, right=True, direction='inout')
    axs.set_ylabel(r'$\ln\left(\displaystyle\frac{PM_{conc.}}{PM_{peak}}\right)$')
    
    fig_name = f'decay_{i+1}_without_air_fresh.png'
    fig.savefig(fig_name, bbox_inches='tight',dpi=600)


df_corrected.to_csv('bleachings_without_airfresh.csv', index=False)

# convert to datetime
df_corrected['datetime'] = pd.to_datetime(df_corrected['datetime'])

# plotly plot
df_corrected_wide=pd.melt(df_corrected, id_vars=['datetime'], value_vars=['pm_conc'])
fig = px.line(df_corrected_wide, x='datetime', y='value', color='variable')
fig.update_layout(
    yaxis_title=r'$\text{PM Concentration} \left(\displaystyle\frac{\mu{g}}{m^3}\right)$',
    xaxis_title=r'Time (CST)'
)
fig.show()

# plot!
fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(df_corrected['datetime'], df_corrected['pm_conc'], color='k')

# x-axis
x_axis_min = df_corrected['datetime'].iat[0]
x_axis_max = df_corrected['datetime'].iat[-1]
ax.set_xlim(x_axis_min, x_axis_max)
ax.set_xlabel(r'\textbf{Time} (CST)')
ax.tick_params(axis='x', bottom=True, top=True, direction='inout')

# y-axis
ax.tick_params(axis='y', left=True, right=True, direction='inout')
ax.set_ylabel(r'\textbf{PM Concentration} $\left(\mu{g}{m}^{-3}\right)$')

## highlight illuminated conditions
ax.axvspan(pd.to_datetime(experimental_data_dict['bleachings_without_airfresh']['peak_start_datetime'][0]), 
        pd.to_datetime(experimental_data_dict['bleachings_without_airfresh']['peak_end_datetime'][0]), color='yellow', 
        alpha=0.5)

ax.axvspan(pd.to_datetime(experimental_data_dict['bleachings_without_airfresh']['peak_start_datetime'][2]),
        pd.to_datetime(experimental_data_dict['bleachings_without_airfresh']['peak_end_datetime'][2]), 
        color='yellow', 
        alpha=0.5)

## highlight dark conditions
ax.axvspan(pd.to_datetime(experimental_data_dict['bleachings_without_airfresh']['peak_start_datetime'][1]), 
        pd.to_datetime(experimental_data_dict['bleachings_without_airfresh']['peak_end_datetime'][1]), 
        color='orange', 
        alpha=0.5)

# major locator (1hr)
xloc=md.HourLocator(interval = 1)
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
fig.show()
fig.savefig('bleach_cleanings_without_airfresh.png', bbox_inches='tight', dpi=600)
del fig, df_corrected, ax, df_peak_processed



# dump resolved dict
file_name = 'resolved_peaks_dict.txt'
fm.dump_dict(resolved_peaks_dict, file_name)
