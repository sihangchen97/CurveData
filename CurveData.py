import numpy as np

class CurveData:

    def __init__(self, data_len, curve_names=[]):
        if type(curve_names)!=list:
            curve_names = list(curve_names)
        self._data_len = data_len
        self._curve_names = [name.lower() for name in curve_names]
        self._curve_data = np.zeros((data_len,len(self._curve_names)), dtype=float)
    
    def data_len(self):
        return self._data_len

    def update_curve(self, name, data, b_add=False):
        name = name.lower()
        if data.shape[0]!=self._data_len:
            return "curve length not match"
        if not str(data.dtype).startswith("float"):
            return "curve data type is not float"
        if name in self._curve_names:
            index = self._curve_names.index(name)
            self._curve_data[:, index] = data
        elif b_add:
            self._curve_names.append(name)
            self._curve_data = np.column_stack((self._curve_data,data))
        else:
            return "curve name not found"
    
    def update_curves(self, curves, b_add=False):
        for i in range(len(curves._curve_names)):
            self.update_curve(curves._curve_names[i], curves._curve_data[:,i], b_add)
    
    def remove_curve(self, name):
        self.remove_curves([name])

    def remove_curves(self, names):
        indexs = [self._curve_names.index(name) if name in self._curve_names else -1 for name in names]
        indexs.remove(-1)
        indexs.sort(reverse=-1)
        for index in indexs:
            del self._curve_data[index]
        self._curve_data = np.delete(self._curve_data, indexs, axis=1)
