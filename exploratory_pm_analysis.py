import pandas as pd
import plotly.express as px  
import datetime as dt
import file_management as fm
import user_inputs as input
from tkinter import messagebox


# load files
for file in fm.select_file(fm.parent_dir()):
    
    # load df
    df_wide = pd.read_csv(file)
    df_wide = df_wide[['Timestamp', 'PM Estimate', 'Angstrom Exponent']]
    df_wide.reset_index(drop=True, inplace=True)
    df_wide.rename(columns={
        'Timestamp':'datetime', 
        'PM Estimate':'pm_conc', 
        'Angstrom Exponent':'angstrom_exp'}, 
        inplace=True)
    
    # convert to long data frame
    df_long=pd.melt(df_wide, id_vars=['datetime'], value_vars=['pm_conc', 'angstrom_exp'])
    fig = px.line(df_long, x='datetime', y='value', color='variable')
    fig.show()