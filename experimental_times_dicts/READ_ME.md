## READ THIS BEFORE PROCEEDING ##

This dictionary accepts 2 sets of 5 linked lists. Therefore index[0] for condition, peak_start_datetime, etc...
all refer to the SAME PEAK. 

This is not the EXACT experimental times, rather it is 
what you observe AFTER running in plotly. Please note this as this will affect the area, peak concentration, 
and decay constant! 

Finally: DO NOT RENAME THE DIRECTORY OR THE PROGRAM WILL CRASH!!!

## STEPS ## 

1. Create a new .txt file named EXACTLY as followed: 'yyyy-mm-dd - yyyy-mm-dd'. You may omit the second date
entry if your experiments only spanned a single day. Copy and paste the dictionary under the 'COPY ME' heading below.

2. Load your plotly dataset, zoom in to the desired peak(s)


3. On the graph, take note of a range which is a good APPROXIMATION of the background and append the start to
'background_start_datetime' and 'background_end_datetime' The values of the background are calculated as a mean.  
Date values MUST BE THE FOLLOWING FORMAT: 'yyyy-mm-dd HH:MM:SS', where time is in 24hrs.

4. Note the EXACT start AND end times of your peak and enter them in 'peak_start_datetime' and 'peak_end_datetime'. 
Date values MUST be the same format as in step 3. For the program to run as intended, 
background levels must be BELOW ALL VALUES in the decay!

5. When running the program, you will be prompted to open a file inside this directory. Select the file you just created! Have fun :-)
-Nathan Ouedraogo 2024-04-11   

## COPY ME ##

{
experimental_data_dict = {

    # input times for bleachings with air freshener
    'bleachings_with_airfresh':{ 

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
    'bleachings_without_airfresh':{ 

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
}
