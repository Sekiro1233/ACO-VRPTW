import numpy as np
from scipy.spatial.distance import pdist, squareform
import os

class DataLoader:
    def __init__(self, data_file: str):
        self.data_file = os.path.join(os.path.dirname(__file__), data_file)
        
    def load_data(self):
        """加载并处理VRPTW问题数据"""
        data = np.loadtxt(self.data_file)
        
        problem_data = {
            'E': data[0, 4],  # 配送中心时间窗开始时间
            'L': data[0, 5],  # 配送中心时间窗结束时间
            'vertexs': data[:, 1:3],  # 所有点的坐标x和y
            'customers': data[1:, 1:3],  # 顾客坐标
            'cusnum': len(data[1:, 1:3]),  # 顾客数
            'demands': data[1:, 3],  # 需求量
            'a': data[1:, 4],  # 顾客时间窗开始时间
            'b': data[1:, 5],  # 顾客时间窗结束时间
            'width': data[1:, 5] - data[1:, 4],  # 顾客的时间窗宽度
            's': data[1:, 6],  # 客户点的服务时间
        }
        
        # 计算距离矩阵
        h = pdist(problem_data['vertexs'])
        problem_data['dist'] = squareform(h)
        
        return problem_data 