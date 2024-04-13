from file_management import dump_dict as dump

class data_dict():
    def __init__ (self):
        """
        Initializes empty dictionary 
        """
        self.dict = {}
    def add_to(self, dict_name):
        """
        Adds nested dictionary
        """
        self.dict[dict_name] =  {
                "condition" : [],
                "peak_area" : [],
                "peak_concentration" : [],
                "linearized_decay_fit" : {
                    "negative_decay_const" : [],
                    "ln_A" : [],
                    "RSQ" : [],
                    "num_of_measurements": []
                }
            }

    def return_dict(self):
        """
        returns dictionary
        """
        return self.dict
    def at_index(self, idx, key):
        """
        Returns dictionary at specific index if it exists. 
        
        Args:
            idx (_int_): index 
            key (_str_): key
        """
        
        dict = {
                key : {
                    "condition" : self.dict["condition"][idx],
                    "peak_area" : self.dict["peak_area"][idx],
                    "peak_concentration" : self.dict["peak_concentration"][idx],
                    "linearized_decay_fit" : {
                        "negative_decay_const" : self.dict["peak_concentration"][idx],
                        "ln_A" : self.dict["peak_concentration"][idx],
                        "RSQ" : self.dict["peak_concentration"][idx]
                    }
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
    def append_value(self, dict_name, key_name, data):
        self.dict[dict_name][key_name].append(data)
    def append_value_to_fit_params(self, dict_name, param, data):
        self.dict[dict_name]["linearized_decay_fit"][param].append(data)
    def dump_dict(self, file_name, parent_dir_path):
        """ 
        Dumps dictionary to specified location
        """
        dump(self.dict, file_name, parent_dir_path)