import pandas as pd
import numpy as np

class SuperDataFrame(pd.DataFrame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataframes = {}
        
    def __repr__(self):
        return super().__repr__()
    
    def __str__(self):
        return super().__str__()
    
    def add_frame(self, df, name=None):
        if name is None:
            name = len(self.dataframes)
        self.dataframes[name] = df
        
    def get_frame(self, name):
        return self.dataframes[name]
    
    def get_frames(self):
        return self.dataframes
    
    def delete_frame(self, name):
        del self.dataframes[name]