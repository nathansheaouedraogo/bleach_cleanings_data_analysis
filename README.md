# General Overview
This package is designed to analyze data from the Ambilabs 2Win integrating nephelometer. It is highly customizable, and with a few modifications all functions maybe used independently for other applications. As it stands, the intended use is to quickly analyze all peaks in a given dataset and report back important information organized in a simple and easy to follow manner. 


# Setup and General Use
Setting up the program is simple. Simply copy the directory (folder) that this file is in over to your local drive. Download your raw dataset and move it into the "raw_data" folder. This is just here for convenience, you can keep your raw data wherever you want. However you cannot delete the "raw_data" folder or else the program will crash. Next you must define decimals (number of sig figs to display on graph), time_resolution, and timescale. run the module "run_analysis.py". Do NOT modify ANY other modules unless you know what you're doing! After running, you will be prompted to open your raw data file. Please do so. Your dataset will be visualized on a web browser (no internet needed!). This plot is interactive and allows you to zoom into your peaks. You will then be prompted to select the "experimental times" json. Instructions on how to set this up are listed under the "Defining the "experimental times" JSON" heading. 

After selecting your experimental times, the rest is very straight forwards. Input your time resolution and the "scale" it was taken at. The program will create a directory in "processed_data" and will output all analyzed data and graphs into it. 

# Some Notes on Time Resolution
 
The module is naive of the data's time resolution. You must calculate or determine this before analyzing the data. The module reports ALL rates in units of min^-1. You will be prompted to input the "timescale" (unit time) of the resolution along with the "time resolution" (number of measurements per unit time). 

For example, if the instrument sampled every 30 seconds, you have three options: 

1. input 30 for "time resolution" and "seconds" for timescale
2. input 0.5 for "time resolution" and "minutes" for timescale
3. input 1/120 for "time resolution" and "hours" for timescale

This is all easily modifiable if you wish to change to a different scale. If you do make modifications, make sure to refactor the code as this could easily result in wrong data being outputted without any raised flags. 

# Defining the "experimental times" JSON 
For the program to run, you must define a .json file containing identification of each peak. This .json file is organized into nested dictionaries specific for unique datasets. Inside each nested dictionary are 5 linked lists. Each peak has exactly ONE entry in each list, and the index (position) of each list refer to the same peak. For example, index 0 (first position) on all five lists will refer to the exact same peak. However, if there are multiple nested dictionaries (let's say "dict_1" and "dict_2"), the peak referenced by index 0 of dict_1 is different from the peak referenced by index 0 of dict_2. 

#### "condition"
> An identifier for the peak (ex. "illuminated" vs "non-illuminated").\
> Entries do not have to be unique.

#### "peak_start_datetime"
>Format: "yyyy-mm-dd HH:MM:SS" (note: uses 24hr time, tz naive)\
> Start time of the peak. Must be above or equal to background levels

#### "peak_end_datetime"
>Format: "yyyy-mm-dd HH:MM:SS" (note: uses 24hr time, tz naive)\
> End time of the peak. Must be above or equal to background levels

#### "background_start_datetime"
>Format: "yyyy-mm-dd HH:MM:SS" (note: uses 24hr time, tz naive)\
> Start time of the background for the peak. Must be below or equal to peak start/end times

#### "background_end_datetime"
>Format: "yyyy-mm-dd HH:MM:SS" (note: uses 24hr time, tz naive)\
> End time of the background for the peak. Must be below or equal to peak start/end times

## Creating the .json file 

1. Navigate to the experimental_times_dicts folder and create a new file using the following (include whitespaces!): 

    >For experiments run on a single date with unique file names: 
    >yyyy-mm-dd.json
    >For expertients run on a single date with non-unique file names:
    >yyyy-mm-dd - yyyy-mm-dd (x).json (note: 'x' is just a unique integer identifier. replace as needed.)

    >For experiments run on multiple days with unique file names: 
    >yyyy-mm-dd - yyyy-mm-dd.json
    >For experiments run on multiple days with non-unique file names: 
    >yyyy-mm-dd - yyyy-mm-dd (x).json (note: 'x' is just a unique integer identifier. replace as needed.)
2. Load your plotly dataset, zoom in to the desired peak(s).
3. Copy and paste the dictionary from the "COPY ME" heading into this file. Each nested dictionary should correspond to one dataset. Add or remove as nessecary. You may use the "data_dict()" class to modify further down the line as needed. 

4. On the graph, take note of a range which is a good APPROXIMATION of the background and append the start to
'background_start_datetime' and 'background_end_datetime' The values of the background are calculated as a mean.  
Date values MUST BE THE FOLLOWING FORMAT: 'yyyy-mm-dd HH:MM:SS', where time is in 24hrs.

5. Note the EXACT start AND end times of your peak and enter them in 'peak_start_datetime' and 'peak_end_datetime'. 
Date values MUST be the same format as in step 3. For the program to run as intended, 
background levels must be BELOW ALL VALUES in the decay! Worst case is the program runs and you get back faulty data, best case is the program crashes. Be careful and check the outputs!!

6. When running the program, you will be prompted to open a file inside this directory. Select the file you just created, and fill out all the values. Remember to have correct syntax! 



## COPY ME

Add as many dicts as you want. Use proper JAVA syntax: encase strings with " " (unlike python, single ' ' are illegal in java) and remove all trailing commas (unlike python trailing ','  illegal if not followed by another entry). Rename "dict_1" to whatever identifier you wish for the dataset renaming anything else  will cause errors.  Finally, adding or removing any key/value pairs inside nested dictionaries will break the program.

```
{
    "dict_1":{ 
        "condition" : [],
        "peak_start_datetime" : [],
        "peak_end_datetime" : [],
        "background_start_datetime" : [],
        "background_end_datetime" : []
        },
    "dict_2":{ 
        "condition" : [],
        "peak_start_datetime" : [],
        "peak_end_datetime" : [],
        "background_start_datetime" : [],
        "background_end_datetime" : []
        }
    }
```

Happy analyzing!

Nathan Shea Ouedraogo 2024-04-13  :p   
