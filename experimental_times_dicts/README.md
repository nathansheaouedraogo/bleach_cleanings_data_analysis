## READ THIS BEFORE PROCEEDING ##

This dictionary accepts 2 sets of 5 linked lists as default. Therefore index[0] for condition, peak_start_datetime, etc...
all refer to the SAME PEAK. You can add or remove nested dictionaries it will not affect the program! 

Potential warning:
Currently, the program assumes 2 conditions present (ie illuminated, non-illuminated) but this is only used when automatic highlighting of peaks is turned on. This feature has not been implimented yet. 

You may rename nested dictionaries to whatever you want, however you CANNOT rename any of the keys. Doing so will break the code unless you modify ALL key/value pairs!

This is not the EXACT experimental times, rather it is what you observe AFTER running in plotly. Please note this as choosing the times will affect the area, peak concentration, and decay constant! 

Finally: DO NOT RENAME THE DIRECTORY OR THE PROGRAM WILL CRASH!!!

## STEPS ## 

1. Navigate to 'experimental_times_dicts and create a new .txt file named EXACTLY as followed (yes including whitespaces!): 'yyyy-mm-dd - yyyy-mm-dd'. You may omit the second date and all whitespaces if your experiments only spanned a single day. Copy and paste the dictionary under the 'COPY ME' heading below into this text file. As mentioned above, you may rename the nested dictionaries, add more entries, or remove any without worry. EMPTY DICTIONARIES WILL BREAK THE CODE! Remove all empty dictionaries before proceeding. Once you are done, please fill out the conditions of each expected peak (you can modify later on as well).

2. Load your plotly dataset, zoom in to the desired peak(s)

3. On the graph, take note of a range which is a good APPROXIMATION of the background and append the start to
'background_start_datetime' and 'background_end_datetime' The values of the background are calculated as a mean.  
Date values MUST BE THE FOLLOWING FORMAT: 'yyyy-mm-dd HH:MM:SS', where time is in 24hrs.

4. Note the EXACT start AND end times of your peak and enter them in 'peak_start_datetime' and 'peak_end_datetime'. 
Date values MUST be the same format as in step 3. For the program to run as intended, 
background levels must be BELOW ALL VALUES in the decay! Worst case is the program runs and you get back faulty data, best case is the program crashes. Be careful and check the outputs!!

5. When running the program, you will be prompted to open a file inside this directory. Select the file you just created, and fill out all the values. Remember to have correct syntax! 

Happy analyzing!

Nathan Shea Ouedraogo 2024-04-11  :p   

## COPY ME ##

```

experimental_data_dict = {

    # input times for bleachings with air freshener
    'bleachings_with_airfresh':{ # note: you may rename this to whatever identifier you wish. will not affect code!

        # refers to lighting condition of a specific peak (or any other identifier you want)
        'condition' : [],

        # start of the peak of interest
        'peak_start_datetime' : [],

        # end of the peak of interest
        'peak_end_datetime' : [],

        # start of the background
        'background_start_datetime' : [],
        
        # end of the background
        'background_end_datetime' : [],
        },
    
    
    # input times for bleachings without air freshener
    'bleachings_without_airfresh':{ # note: you may rename this to whatever identifier you wish. will not affect code!

        # refers to lighting condition of a specific peak (or any other identifier you want)
        'condition' : [],

        # start of the peak of interest
        'peak_start_datetime' : [],

        # end of the peak of interest
        'peak_end_datetime' : [],

        # start of the background
        'background_start_datetime' : [],
        
        # end of the background
        'background_end_datetime' : [],
        },
    }
```
