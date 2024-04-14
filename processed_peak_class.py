## data_dict creates a dictionary used in 'pm_analysis
## allows greater abstraction to prevent modification of dictionary by user
## if you know what you're doing, you may add keys or functionalities and add more functions
## as it stands, this compartmentalizes dictionary instances and also cleans up code   

from file_management import dump_dict as dump

class data_dict():
    def __init__ (self):
        """
        Initializes empty dictionary 
        """
        self.dict = {}
    def add_to(self, dict_name):
        """
        Adds empty nested dictionary with name 'dict_name'
        """
        self.dict[dict_name] =  {
                "condition" : [],
                "peak_area" : [],
                "peak_concentration" : [],
                "negative_decay_constant" : [],
                "decay_y_int" : [],
                "decay_rsq" : [],
                "decay_length_minutes": []
                }
        return 
    
    def return_dict(self):
        """
        returns dictionary
        """
        return self.dict
    
    def at_index(self, idx, key):
        """
        Returns dictionary at specific index
        
        Args:
            idx (_int_): index 
            key (_str_): key
        """
        
        dict = {
                key : {
                    "condition" : self.dict["condition"][idx],
                    "peak_area" : self.dict["peak_area"][idx],
                    "peak_concentration" : self.dict["peak_concentration"][idx],
                    "negative_decay_constant" : self.dict["negative_decay_const"][idx],
                    "decay_y_int" : self.dict["decay_y_int"][idx],
                    "decay_rsq" : self.dict["decay_RSQ"][idx],
                    "decay_length_minutes": self.dict["decay_length_minutes"][idx]
                }
            }
        return dict
    
    def return_dicts(self):
        """
        Returns list of nested dictionaries
        """
        return self.dict.keys()
    
    def return_value(self, key, value):
        """
        returns value at specific key value pair
        """
        return self.dict[key][value]
    
    def append_condition(self, dict_name, data):
        """
        Appends to condition key
        Args:
            dict_name (_any_): name of sub dictionary
            data (_any_): data to be appended
        """
        self.dict[dict_name]['condition'].append(data)
    
    def append_peak_area(self, dict_name, data):
        """
        Appends to peak area key
        Args:
            dict_name (_any_): name of sub dictionary
            data (_any_): data to be appended
        """
        self.dict[dict_name]['append_peak_area'].append(data)
    
    def append_peak_concentration(self, dict_name, data):
        """
        Appends to peak concentration key
        Args:
            dict_name (_any_): name of sub dictionary
            data (_any_): data to be appended
        """
        self.dict[dict_name]['peak_concentration'].append(data)
    
    def append_negative_decay_constant(self, dict_name, data):
        """
        Appends to negative_decay_constant key
        Args:
            dict_name (_any_): name of sub dictionary
            data (_any_): data to be appended
        """
        self.dict[dict_name]['negative_decay_constant'].append(data)
    
    def append_decay_y_int(self, dict_name, data):
        """
        Appends to decay_y_int key
        Args:
            dict_name (_any_): name of sub dictionary
            data (_any_): data to be appended
        """
        self.dict[dict_name]['decay_y_int'].append(data)
    
    def append_decay_rsq(self, dict_name, data):
        """
        Appends to decay_rsq key
        Args:
            dict_name (_any_): name of sub dictionary
            data (_any_): data to be appended
        """
        self.dict[dict_name]['decay_rsq'].append(data)
    
    def append_decay_length_minutes(self, dict_name, data):
        """
        Appends to decay_length_minutes key
        Args:
            dict_name (_any_): name of sub dictionary
            data (_any_): data to be appended
        """
        self.dict[dict_name]['decay_length_minutes'].append(data)
    
    def is_invalid(self):
        """
        Returns True if length of keys in sub dicts are
        not identical. Returns None if valid.
        """
        for dict in self.dict.return_dicts():
            is_valid = (
                len(dict['condition']) == len(dict['peak_area'])
                == len(dict['peak_concentration']) == len(dict['negative_decay_constant'])
                == len(dict['decay_y_int']) == len(dict['decay_rsq'])
                == len(dict['decay_length_minutes']) == len(dict['decay_length_minutes'])
            )
            if not is_valid:
                return True 
    
    def dump_json(self, file_name, parent_dir_path):
        """ 
        Dumps json of dictionary to specified path
        """
        dump(self.dict, file_name, parent_dir_path)