# General Overview
This package is designed to analyze data from the Ambilabs 2Win integrating nephelometer. It is highly customizable, and with a few modifications all functions maybe used independently for other applications. As it stands, the intended use is to quickly analyze all peaks in a given dataset and report back important information organized in a simple and easy to follow manner. 

The functions and classes may also be used as a simple "first step" in data processing with heavier analysis used down the line or may be implemented in prexisting workflows. 

# Setup and General Use
Please copy all files and folders from this rep onto your local disk. Files with "example" may be deleted. Locate your raw data file and transfer it into the "raw data" folder. Next, please take note of your instruments timescale and time resolution (see: "Some Notes on Time Resolution heading) and input them into the "pm_analysis" function in __RUN_ANALYSIS__.py file. If you need to define your peak/background times, please set "show_raw_peaks=True". Else, set it to False.  

**Before proceeding further please read  Defining the "experimental times" JSON heading**

# Some Notes on Time Resolution
 
The module is naive of the data's time resolution. You must calculate or determine this before analyzing the data. The module reports ALL rates in units of min^-1. You will have to input the "timescale" (unit time) of the resolution along with the "time resolution" (number of measurements per unit time) into the "pm_analysis" function.

For example, if the instrument sampled every 30 seconds, you have three options: 

1. input 30 for "time resolution" and "seconds" for timescale
2. input 0.5 for "time resolution" and "minutes" for timescale
3. input 1/120 for "time resolution" and "hours" for timescale

The function is set up with "60" for time resolution and "seconds" for timescale, meaning the instrument sampled every 60s. 

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
2. If show_raw_peak=True, load your plotly dataset, zoom in to the desired peak(s). Else continue to 3. 
3. Copy and paste the dictionary from the "COPY ME" heading into this file. *Please read this subheading thoroughly before proceeding*

4. Under "condition", add an identifier for the peak. On the graph, take note of a range which is a good APPROXIMATION of the background and and the start to 'background_start_datetime' and 'background_end_datetime' The values of the background are calculated as a mean.  Date values MUST BE THE FOLLOWING FORMAT: 'yyyy-mm-dd HH:MM:SS', where time is in 24hrs.

5. Note the EXACT start AND end times of your peak and enter them in 'peak_start_datetime' and 'peak_end_datetime'. 
Date values MUST be the same format as in step 3. For the program to run as intended, background levels must be BELOW ALL VALUES in the decay! Worst case is the program runs and you get back faulty data, best case is the program crashes. Be careful and check the outputs!!

6. When running the program, you will be prompted to open a file inside this directory. Select the file you just created. 

## COPY ME

Add as many dictionaries as needed, program will be okay with a minimum of one. Use proper JAVA syntax: encase strings with " " (unlike python, single ' ' are illegal in java) and remove all trailing commas (unlike python trailing ','  illegal if not followed by another entry). Rename "dict_1" to whatever identifier you wish for the dataset renaming anything else  will cause errors.  Finally, adding or removing any key/value pairs inside nested dictionaries will break the program.

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

Nathan Shea Ouedraogo 2024-04-14  :p   
