import numpy as np
from .utils import str2float

class CurveData:

    def __init__(self, frame_num = 0, fps=30.0, curve_names=[]):
        if type(curve_names)!=list:
            curve_names = list(curve_names)
        self._fps = fps
        self._frame_num = frame_num
        self._curve_names = curve_names
        self._curve_data = np.zeros((self._frame_num,len(self._curve_names)))
    
    @property
    def fps(self):
        return self._fps
    @property
    def frame_num(self):
        return self._frame_num
    @property
    def curve_num(self):
        return len(self._curve_names)
    @property
    def curve_names(self):
        return self._curve_names
    @property
    def curve_data(self):
        return self._curve_data
    @property
    def curves_dict(self):
        return {name: self._curve_data[:,i] for i,name in enumerate(self._curve_names)}
    @property
    def is_valid(self):
        return self.frame_num!=0 and len(self.curve_names)!=0 and np.sum(self.curve_data)!=0
    
    def curve_index(self, name, ignore_case=True):
        curve_names = self.curve_names
        if ignore_case:
            name = name.lower()
            curve_names = [c.lower() for c in curve_names]
        return curve_names.index(name) if name in curve_names else -1
    
    def curve(self, name, ignore_case=True):
        index = self.curve_index(name, ignore_case)
        return self._curve_data[:,index] if index!=-1 else np.zeros((self.frame_num))
    
    @classmethod
    def load_from_csv(self, csv_file):
        try:
            with open(csv_file, 'r') as f:
                data = [line[:-1].split(",") for line in f.readlines()]
                t = self(frame_num = len(data)-1, curve_names=data[0])
                print(t.curve_num, t.frame_num)
                for i in range(t.frame_num):
                    for j in range(t.curve_num):
                        t._curve_data[i][j] = str2float(data[i+1][j])
                return t
        except:
            return self()
    
    @classmethod
    def load_from_npz(self, npz_file):
        try:
            data = dict(np.load(npz_file))
            keys = [k for k in data.keys() if k[0]!="_"]
            frame_num = len(data[keys[0]])
            t = self(frame_num = frame_num, curve_names=keys)
            for i,k in enumerate(keys):
                for j in range(t.frame_num):
                    t._curve_data[j][i] = str2float(data[k][j])
            return t
        except:
            return self()
    
    def save_to_npz(self, npz_file):
        try:
            assert self.is_valid
            np.savez(npz_file, _fps=self.fps, _frame_num=self.frame_num, **self.curves_dict)
        except:
            raise ValueError("Cannot save Invalid Curve Data")
    
    def update_curve(self, name, data, ignore_case=True, add=False):
        if data.shape[0]!=self.frame_num:
            raise ValueError("Curve Length Not Match")
        index = self.curve_index(name, ignore_case)
        if index!=-1:
            self._curve_data[:, index] = data
        elif add:
            self.curve_names.append(name)
            self._curve_data = np.column_stack((self._curve_data, data))
       
    def update_curves(self, curves, ignore_case=True, add=False):
        for k, v in curves.curves_dict.items():
            self.update_curve(k, v, ignore_case, add)
    
    def remove_curve(self, name, ignore_case=True):
        self.remove_curves([name], ignore_case)

    def remove_curves(self, names, ignore_case=True):
        indexs = [self.curve_index(name, ignore_case) for name in names]
        indexs.remove(-1)
        indexs.sort(reverse=True)
        for index in indexs:
            del self._curve_data[index]
        self._curve_data = np.delete(self._curve_data, indexs, axis=1)
