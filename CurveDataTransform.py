import numpy as np
from .CurveData import CurveData
from .utils import array_get_index, str2float

class CurveDataTransform:
    def __init__(self, input_curve_names=[], output_curve_names=[]):
        self._input_curve_names = input_curve_names
        self._output_curve_names = output_curve_names
        self._transform_matrix = np.zeros((len(self._input_curve_names), len(self._output_curve_names)), dtype=float)
    
    @classmethod
    def load_from_opt_csv(self, csv_file):
        input_curve_names = []
        output_curve_names = []
        operations = []
        try:
            with open(csv_file, 'r') as f:
                srcData = [line[:-1].split(",") for line in f.readlines()]
                for src in srcData:
                    output_index = array_get_index(output_curve_names, src[0], add=True)
                    for i in range(2, len(src),2):
                        input_index = array_get_index(input_curve_names, src[i-1], add=True)
                        operations.append((input_index, output_index, str2float(src[i])))
        except:
            raise ValueError(csv_file + " csv_file not support")
        transfrom = self(input_curve_names, output_curve_names)
        for input_index, output_index, value in operations:
            transfrom._transform_matrix[input_index, output_index] = value
        return transfrom

    def apply(self, curves):
        data_len = curves.data_len()
        input_curves = CurveData(data_len, self._input_curve_names)
        input_curves.update_curves(curves)

        output_curves = CurveData(data_len, self._output_curve_names)
        output_curves._curve_data = input_curves._curve_data.dot(self._transform_matrix)

        return output_curves
