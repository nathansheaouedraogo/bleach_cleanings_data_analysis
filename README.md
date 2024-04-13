# The experimental_times .json 
For the program to run, you must define a .json file containing identification of each peak. This .json file is organized into nested dictionaries specific for unique datasets. Inside each nested dictionary are 5 linked lists. Each peak has exactly ONE entry in each list, and the index (position) of each list refer to the same peak. For example, index 0 (first position) on all five lists will refer to the exact same peak. However, if there are multiple nested dictionaries (let's say "dict_1" and "dict_2"), the peak referenced by index 0 of dict_1 is different from the peak referenced by index 0 of dict_2. 

#### "condition"
> An identifier for the peak (ex. "illuminated" vs "non-illuminated").\
> Entries do not have to be unique.

#### "peak_start_datetime"
>Format: "YYYY-mm-dd HH:MM:SS" (note: uses 24hr time, tz naive)\
> Start time of the peak. Must be above or equal to background levels

#### "peak_end_datetime"
>Format: "YYYY-mm-dd HH:MM:SS" (note: uses 24hr time, tz naive)\
> End time of the peak. Must be above or equal to background levels

#### "background_start_datetime"
>Format: "YYYY-mm-dd HH:MM:SS" (note: uses 24hr time, tz naive)\
> Start time of the background for the peak. Must be below or equal to peak start/end times

#### "background_end_datetime"
>Format: "YYYY-mm-dd HH:MM:SS" (note: uses 24hr time, tz naive)\
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
3. Copy and paste the dictionary from the "COPY ME" heading into this file. Each nested dictionary should correspond to one dataset. Add or remove as nessecary. Please note: empty dictionaries will BREAK the program, make sure to remove ALL empty or partially-filled dictionaries.

4. On the graph, take note of a range which is a good APPROXIMATION of the background and append the start to
'background_start_datetime' and 'background_end_datetime' The values of the background are calculated as a mean.  
Date values MUST BE THE FOLLOWING FORMAT: 'yyyy-mm-dd HH:MM:SS', where time is in 24hrs.

5. Note the EXACT start AND end times of your peak and enter them in 'peak_start_datetime' and 'peak_end_datetime'. 
Date values MUST be the same format as in step 3. For the program to run as intended, 
background levels must be BELOW ALL VALUES in the decay! Worst case is the program runs and you get back faulty data, best case is the program crashes. Be careful and check the outputs!!

6. When running the program, you will be prompted to open a file inside this directory. Select the file you just created, and fill out all the values. Remember to have correct syntax! 



## COPY ME

Add as many dicts as you want. Use proper JAVA syntax: encase strings with " " (unlike python, single ' ' are illegal in java) and remove all trailing commas (unlike python trailing ','  illegal if not followed by another entry). Rename "dict_1" to whatever identifier you wish for the dataset and you may also change "condition" without worrying about breaking the code, renaming anything else  will cause errors.  Finally, adding or removing any key/value pairs inside nested dictionaries will break the code.

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
