from tkinter import messagebox, simpledialog
import pandas as pd

class user_inputs:
    
    def _innit_(self, version, date, specie, path, msg):
        self.version = version
        self.date = date 
        self.specie = specie
        self.path = path 
        self.msg = msg
    
    @staticmethod
    def date(version=None):
        
        """
        Summary: 
            >>> Prompts user to input date of experiment
        Returns:
            >>> date (_str_): date of exp. (YYYY-MM-DD)
            >>> experiment_number (_int_): number of experiments done 
        """
        while True:
            
            # input date
            date = simpledialog.askstring(version, 'Please input the date of the experiment(s) (YYYY-MM-DD)')
            if date == None:
                input = messagebox.askyesno('Invalid date! Re-input? \n(note: no will discard this entry!)')
                if input == False:
                    return False
                else:
                    continue
            
            # remove whitespaces
            for char in date:
                if char == ' ':
                    del char
            
            # validate date is ISO 8601
            try:
                dt.date.fromisoformat(date)
            except ValueError:
                input = messagebox.showerror('Invalid date!')
                continue
            else:
                while True:
                    
                    # input number of experiments done on date
                    experiment_number = simpledialog.askinteger(version, 'Please input the number of experiments done')
                    
                    # validate input
                    if experiment_number == None:
                        messagebox.showerror('Number of experiments must be inputted inputted!')
                        continue
                    elif experiment_number <= 0:
                        messagebox.showerror(version, 'number of experiments must be greater than zero!')
                        continue 
                    else:
                        break
                
                msg = 'confirm experiment(s): '+ '\n\n' + str(experiment_number) + ' done on ' + date + '\n\n(press "yes" to confirm, "no" to re-input)'
                
                input = messagebox.askyesno(version, msg)
                
                if input == True:
                    return date, experiment_number
                elif input == None: 
                    continue
    
    @staticmethod
    def input_exp_times(version, date, specie):
        
        """
        Summary: 
            >>> Prompts user to input start and end times of experiment.
        
        Args:   
            >>> date (_str_): date of exp. (YYYY-MM-DD)
            >>> specie (_str_): specie analyzed 
        
        Returns:
            >>> exp_start_end [tuple: (_str_, _str_)]: tuple of start time and end time
        """
        
        while True:
            
            # input start and end of experiment
            msg_start = 'Please input the start of the experiment (HH:MM:SS, 24hrs)'
            msg_end = 'Please input the end of the experiment (HH:MM:SS, 24hrs)'            
            
            while True:
                
                exp_start = simpledialog.askstring(version, msg_start)
                
                # remove whtiespaces
                for char in exp_start:
                    if char == ' ':
                        del char
                
                # validate string is ISO 8601 
                try: 
                    pd.to_datetime(date + ' ' + exp_start, format='%Y-%m-%d %H:%M:%S')
                except ValueError: 
                    input = messagebox.askyesno('Invalid input! Re-input?')
                    if input == True:
                        continue 
                    else:
                        return False, False
                else:
                    
                    while True: 
                        
                        exp_end = simpledialog.askstring(version, msg_end)
                        
                        # delete whitespaces
                        for char in exp_start:
                            if char == ' ':
                                del char
                        
                        # validate string is ISO 8601
                        try: 
                            pd.to_datetime(date + ' ' + exp_end, format='%Y-%m-%d %H:%M:%S')
                        except ValueError: 
                            input = messagebox.askyesno('Invalid input! Re-input?')
                            if input == True:
                                continue 
                            else:
                                return False, False
                        else:
                            break
                    break
                    
            # confirm times 
            msg_confirm = 'confirm time of ' + specie + ' experiment was: '+ exp_start + ' to ' + exp_end + ' on '+ date +  '\n(press "yes" to confirm, "no" to re-input, "cancel" to discard)'
            
            input = messagebox.askyesnocancel(version, msg_confirm)
            
            if input == False:
                continue
            
            elif input == True:
                exp_start_end = (exp_start, exp_end)
                return exp_start_end    
            
            elif input == None:
                return False, False
    
    @staticmethod
    def background(version, date):
        
        """
        Summary: 
            >>> Prompts user to input start and end times of background.
        Args:
            >>> date (_str_): date of experiment (YYYY-MM-DD)
        Returns:
            >>> background_start_end [tuple: (_datetime_, _datetime_)]: tuple of start time and end time (YYYY-MM-DD HH:MM:SS; 24hrs)
        """
        
        loop_on = True
        
        while True:
            
            msg_start = 'Please input the start of the background (HH:MM:SS, 24hrs)'
            msg_end = 'Please input the end of the background (HH:MM:SS, 24hrs)'        
            
            while True:
                
                # input background start time
                background_start = simpledialog.askstring(version, msg_start)
                
                # remove whitespaces
                for char in background_start:
                    if char == ' ':
                        del char
                
                # validate string is ISO 8601 
                try:
                    pd.to_datetime(date + ' ' + background_start, format='%Y-%m-%d %H:%M:%S')
                except ValueError:
                    input = messagebox.askyesno('Invalid input! Re-input?')
                    if input == True:
                        continue 
                    else:
                        return False
                else:
                    while True:
                        
                        # input background start time
                        background_end = simpledialog.askstring(version, msg_end)
                        
                        # remove whitespace
                        for char in background_end:
                            if char == ' ':
                                del char
                        
                        # validate string is ISO 8601
                        try:
                            pd.to_datetime(date + ' ' + background_end, format='%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            input = messagebox.askyesno('Invalid input! Re-input?')
                            if input == True:
                                continue 
                            else:
                                return False
                        else:
                            break
                    break
            
            msg_confirm = 'confirm time of background is: ' + background_start + ' to ' + background_end + '\n(press "yes" to confirm, "no" to re-input, "cancel" to discard)'
            input = messagebox.askyesnocancel(version, msg_confirm)
            
            while True:
                
                if input == True:
                    background_start = pd.to_datetime(date + ' ' + background_start)
                    background_end = pd.to_datetime(date + ' ' + background_end)
                    background_start_end = (background_start, background_end)
                    loop_on = False
                    break 
                
                elif input == False:
                    break
                
                elif input == None:
                    msg_confirm_discard = 'Discard this background?' + '\n' + '(Note: raw data will not be deleted)'
                    input_confirm_discard = messagebox.askyesno(version, msg_confirm_discard)
                    
                    while True: 
                        if input_confirm_discard == True:
                            background_start_end = False
                            loop_on = False
                            break
                        else:
                            break
            
            if loop_on == False:
                return background_start_end
    
    @staticmethod
    def decay(version, date):
        
        """
        Summary: 
            >>> Prompts user to input start and end times of decay.
        Args:
            >>> date (_str_): date of experiment (YYYY-MM-DD)
        Returns:
            >>> decay_start_end [tuple: (_datetime_, _datetime_)]: tuple of start time and end time (YYYY-MM-DD HH:MM:SS; 24hrs)
        """
        loop_on = True
        
        while True:
            
            msg_start = 'Please input the start of the decay (HH:MM:SS, 24hrs)'
            msg_end = 'Please input the end of the decay (HH:MM:SS, 24hrs)'        
            
            while True:
                
                # input background start time
                decay_start = simpledialog.askstring(version, msg_start)
                
                # remove whitespace
                for char in decay_start:
                    if char == ' ':
                        del char
                
                # validate string is ISO 8601
                try:
                    pd.to_datetime(date + ' ' + decay_start, format='%Y-%m-%d %H:%M:%S')
                except ValueError:
                    input = messagebox.askyesno('Invalid input! Re-input?')
                    if input == True:
                        continue 
                    else:
                        return False
                
                else:
                    while True:
                        
                        # input background start time
                        decay_end = simpledialog.askstring(version, msg_end)
                        
                        # remove whitespaces
                        for char in decay_end:
                            if char == ' ':
                                del char
                        
                        # validate string is ISO 8601
                        try:
                            pd.to_datetime(date + ' ' + decay_end, format='%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            input = messagebox.askyesno('Invalid input! Re-input?')
                            if input == True:
                                continue 
                            else:
                                return False
                        else:
                            break
                    break
                
            msg_confirm = 'confirm time of decay is: ' + decay_start + ' to ' + decay_end + '\n(press "yes" to confirm, "no" to re-input, "cancel" to discard)'
            input = messagebox.askyesnocancel(version, msg_confirm)
            
            while True:
                
                if input == True:
                    decay_start = pd.to_datetime(date + ' ' + decay_start)
                    decay_end = pd.to_datetime(date + ' ' + decay_end)
                    decay_start_end = (decay_start, decay_end)
                    loop_on = False
                    break 
                
                elif input == False:
                    break
                
                elif input == None:
                    msg_confirm_discard = 'Discard this decay?' + '\n' + '(Note: raw data will not be deleted)'
                    input_confirm_discard = messagebox.askyesno(version, msg_confirm_discard)
                    
                    while True: 
                        if input_confirm_discard == True:
                            decay_start_end = False
                            loop_on = False
                            break
                        else:
                            break
            
            if loop_on == False:
                return decay_start_end
    
    @staticmethod
    def timezone_offset(version=None):
        
        """
        Summary:
            Valid inputs are any string of a number. +ve and -ve characters are allowed. (eg: -10.13; +10.31; 333.23)
            >>> Prompts user to input instrument's timezone offset from desired timezone.
            >>> Offset can be float or integer. 
            >>> NOTE: FUNCTION IS TIMEZONE NAIVE!
        Returns: 
            >>> timezone_offset (_timedelta_): instrument timezone_offset (note: False can be used in place of 0 :p)
        """
        
        input_offset = messagebox.askyesno(version, 'Input timezone correction?')
        
        if input_offset == True:
            
            while True:
                
                re_input = False
                offset_str = simpledialog.askstring(version, "Please input instrument's offset from desired timezone")
                
                # decimal, negative, positive, char counters
                decimal = 0
                neg = 0
                pos = 0
                
                # if char is not a digit, decimal ('.'and ','), +ve ('+'), -ve ('-'), string prompt user to re-input
                for i in range(len(offset_str)):
                    
                    if offset_str[i] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '.', ',', '-', '+']:
                        messagebox.showwarning(version, 'input cannot contain non-digit charcters!')
                        re_input = True 
                        break 
                    
                    # check that if char contains decimal char, it contains EXACTLY one decimal char
                    if offset_str[i] in ['.', ',']:
                        decimal += 1
                        if decimal > 1:
                            messagebox.showwarning(version, 'input cannot contain more than one decimal places!')
                            re_input = True 
                            break
                    
                    # check that if str contains -ve char, it contains EXACTLY one -ve char at the front!
                    if offset_str[i] == '-':
                        if pos != 0:
                            messagebox.showwarning(version, 'input cannot contain positive and negative characters!')
                            re_input = True 
                            break
                        if i != 0 : 
                            messagebox.showwarning(version, 'negative character must be at the begining of the input!')
                            re_input = True 
                            break
                        neg += 1
                        if neg > 1:
                            messagebox.showwarning(version, 'input cannot contain more than one negative character!')
                            re_input = True 
                            break
                
                    # check that if str contains +ve char, it contains EXACTLY one +ve char at the front!
                    if offset_str[i] == '+':
                        if pos != 0:
                            messagebox.showwarning(version, 'input cannot contain negative and positive characters!')
                            re_input = True 
                            break
                        if i != 0 : 
                            messagebox.showwarning(version, 'positive character must be at the begining of the input!')
                            re_input = True 
                            break
                        pos += 1
                        if pos > 1:
                            messagebox.showwarning(version, 'input cannot contain more than one negative character!')
                            re_input = True 
                            break
                
                if re_input == True: 
                    continue 
                
                # input timezone offset 
                if decimal == 1:
                    timezone_offset_num = float(offset_str)
                    break
                else:
                    timezone_offset_num = int(offset_str)
                    break
            
            if timezone_offset_num == 0:
                timezone_offset = dt.timedelta(hours=False)
            else:
                
                # calculate offset hours, minutes, seconds 
                timezone_offset_sec = timezone_offset_num * 3600
                tz_hours, remainder = divmod(timezone_offset_sec, 3600)
                tz_mins, tz_secs = divmod(remainder, 60)
                timezone_offset = dt.timedelta(hours=tz_hours, minutes=tz_mins, seconds=round(tz_secs))
        
        else:
            timezone_offset = dt.timedelta(hours=False)
        
        return timezone_offset 
    
    