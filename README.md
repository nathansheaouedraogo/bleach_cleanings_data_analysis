# General Overview
This library is designed to analyze  particulate matter data calculated by the Ambilabs 2WIN Integrating Nephelometer's PM estimate channel. It is highly customizable, and with a few modifications all functions maybe used independently for other applications or new functionality may be added as needed. As it stands, the intended use is to quickly analyze all peaks in a given set of experiments and report back important information organized in a simple and easy to follow manner.
The functions and classes may also be used as a simple "first step" in data processing with heavier analysis used down the line or may be implemented in prexisting workflows.

# Setup and General Use
Please copy all files and folders from this rep into a directory (folder, dir) on your local drive. Create a folder named "processed_data" in the same location as the files you copied (do not copy quotes or add any whitespaces). Files with "example" may be deleted. Locate your raw data file and transfer it into the "raw data" folder. Next, please take note of your instruments timescale and time resolution (see: "Some Notes on Time Resolution heading) and input them into the "pm_analysis" function in "__RUN_ANALYSIS__".py file. If you need to define your peak/background times or would like to view the dataset, please set "show_raw_peaks=True". Else, set it to False. Setting to true will open an interactive plot of your dataset. Setting the argument to false will not affect data analysis.

***Before proceeding further please familiarize yourself with the information below***

# Some Notes on Time Resolution
This library is naive of the data's time resolution: **it will accept what you input as the accurate time resolution of the measurements.**

You will have to input the "timescale" (unit time) of the resolution along with the "time resolution" (number of measurements per unit time) into the "pm_analysis" function. For example, if the instrument sampled every 30 seconds, you have three options:
1. input 30 for "time resolution" and "seconds" for timescale
2. input 0.5 for "time resolution" and "minutes" for timescale
3. input 1/120 for "time resolution" and "hours" for timescale

The function is set up with "60" for time resolution and "seconds" for timescale, meaning the instrument sampled every 60 seconds.

**You must change these arguments to reflect the time resolution of your measurements**

Use the initial settings for analyzing provided example files. You may change them to equivalent entries (ex: set time resolution to 1 and time scale to "minutes" **or** set time resolution to 1/60 and time scale to "hours"). 

This functionality is easily modifiable if you wish to change to a different scale (ex: from units of per minute to per hour). To do this you must modify the function in "time_wrangling.py". If you do make these modifications, make sure to refactor the code as this could easily result in wrong data being outputted without any raised flags (eg: df_decay['minutes'] column should be renamed to reflect the new scale). 

# Defining the "experimental times" JSON 
For the program to run, you must define a .json file containing identification of each peak. This .json file is organized into nested dictionaries specific for each set of experiments in your dataset. Inside each nested dictionary are 5 linked lists. Each peak has exactly ONE entry in each list, and the index (position) of each list refer to the same peak. For example, index 0 (first position) on all five lists will refer to the exact same peak. However, if there are multiple nested dictionaries (let's say "dict_1" and "dict_2"), the peak referenced by index 0 of dict_1 is different from the peak referenced by index 0 of dict_2.

 ***Plotly does not show trailing zeros but the program will crash if you do not add them ( eg:*** yyyy-mm-dd 12:00 ***must be inputted as*** yyyy-mm-dd 12:00:00 ***).***

#### "condition"
> An identifier for the peak (ex. "illuminated" vs "non-illuminated").
> 
> Entries do not have to be unique.
#### "peak_start_datetime"
>*Format: "yyyy-mm-dd HH:MM:SS" (note: uses 24hr time, tz naive)*
>
> Start time of the peak. Must be above or equal to background levels
#### "peak_end_datetime"
>*Format: "yyyy-mm-dd HH:MM:SS" (note: uses 24hr time, tz naive)*
>
> End time of the peak. Must be above or equal to background levels.
#### "background_start_datetime"
>*Format: "yyyy-mm-dd HH:MM:SS" (note: uses 24hr time, tz naive)*
>
> Start time of the background for the peak. Mean background values must be below or equal to peak start and peak end values.
#### "background_end_datetime"
>*Format: "yyyy-mm-dd HH:MM:SS" (note: uses 24hr time, tz naive)*
>
> End time of the background for the peak. Mean background values must be below or equal to peak start and peak end values.
## Creating the .json file 
1. Navigate to the experimental_times_dicts folder and create a new file using the following (include whitespaces!):

    >For experiments run on a single date with unique file names:
    > 
    >yyyy-mm-dd.json
    >
    >For expertients run on a single date with non-unique file names:
    >
    >yyyy-mm-dd - yyyy-mm-dd (x).json
    >
    >For experiments run on multiple days with unique file names:
    >
    >yyyy-mm-dd - yyyy-mm-dd.json
    >
    >For experiments run on multiple days with non-unique file names:
    >
    >yyyy-mm-dd - yyyy-mm-dd (x).json
    >
2. If show_raw_peak=True, the program will launch an interactive graph of your entire raw dataset. Use this to identify the desired peak(s) and associated start/end times. Else continue to 3.
3. Copy and paste the dictionary from the "COPY ME" heading into the file created in step 1. *Please read COPY ME thoroughly before proceeding.*
4. Under "condition", add an identifier for the peak. On the graph, take note of a range which is a good APPROXIMATION of the background and add the start to 'background_start_datetime' and the end to 'background_end_datetime'. The background value is calculated as the mean concentration between these two points.
5. Note the start and end times of your peak and enter them in 'peak_start_datetime' and 'peak_end_datetime'. For the program to run as intended, mean background levels must be BELOW ALL VALUES in the decay! Worst case is the program runs and you get back faulty data, best case is the program crashes. Be careful and check the output log (output.log file in 'processed_data' directory or consol output).
6. When running the program, you will be prompted to open a file containing your experimental times. Select the file you just created.

## COPY ME

**Add as many nested dictionaries as needed, program will run with a minimum of one nested dictionary. All nested dictionaries must be nested inside a *single* parent dictionairy even if you only input one.**

**All values must be strings and datetime strings must include trailing seconds (ie: yyyy-mm-dd HH:MM:SS).**

***Use proper JAVA syntax:*** encase strings with double " " hyphens (unlike python, single ' ' hyphens are illegal in java) and remove all trailing commas (unlike python trailing ',' after the last entry are illegal). Renaming the nested dictionaries will not cause any errors (***it's highly reccomended you do so***) nor will removing dict_2 or adding additional nested dicts (***make sure to add or delete the trailing comma(s)!***).

**Do not rename or modify *anything* inside the nested dictionaries unless you know what you're doing.**

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

Nathan Shea Ouedraogo 2024-04-15  :p   
