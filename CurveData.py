import numpy as np
from .utils import str2float

class CurveData:

    def __init__(self, data_len, curve_names=[]):
        if type(curve_names)!=list:
            curve_names = list(curve_names)
        self._data_len = data_len
        self._curve_names = curve_names
        self._curve_data = np.zeros((data_len,len(self._curve_names)), dtype=float)
    
    @classmethod
    def load_from_csv(self, csv_file):
        try:
            with open(csv_file, 'r') as f:
                data = [line[:-1].split(",") for line in f.readlines()]
                data_len = len(data)-1

                curve_data = self(data_len, data[0])
                for i in range(data_len):
                    for j in range(len(curve_data._curve_names)):
                        curve_data._curve_data[i][j] = str2float(data[i+1][j])
                return curve_data
        except:
            return self(0)
    
    @property
    def data_len(self):
        return self._data_len
    
    @property
    def curve_names(self):
        return self._curve_names
    
    @property
    def curves_dict(self):
        return {name: self._curve_data[:,i] for i,name in enumerate(self._curve_names)}
    
    @property
    def curve(self, name, ignore_case=True):
        index = self.curve_index(name, ignore_case)
        return self._curve_data[:,index] if index!=-1 else np.zeros((self.data_len))

    def curve_index(self, name, ignore_case=True):
        curve_names = self.curve_names
        if ignore_case:
            name = name.lower()
            curve_names = [c.lower() for c in curve_names]
        return curve_names.index(name) if name in curve_names else -1

    def update_curve(self, name, data, b_add=False):
        if data.shape[0]!=self.data_len:
            return "curve length not match"
        if not str(data.dtype).startswith("float"):
            return "curve data type is not float"
        index = self.curve_index(name)
        if index!=-1:
            self._curve_data[:, index] = data
        elif b_add:
            self.curve_names.append(name)
            self._curve_data = np.column_stack((self._curve_data, data))
        else:
            return "curve name not found"
    
    def update_curves(self, curves, b_add=False):
        for k, v in curves.curves_dict.items():
            self.update_curve(k, v, b_add)
    
    def remove_curve(self, name):
        self.remove_curves([name])

    def remove_curves(self, names):
        indexs = [self.curve_index(name) for name in names]
        indexs.remove(-1)
        indexs.sort(reverse=True)
        for index in indexs:
            del self._curve_data[index]
        self._curve_data = np.delete(self._curve_data, indexs, axis=1)
