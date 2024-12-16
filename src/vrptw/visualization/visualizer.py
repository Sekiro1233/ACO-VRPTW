import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict

class Visualizer:
    def __init__(self, problem_data: Dict):
        self.problem_data = problem_data
        
    def plot_convergence(self, costs: List[float]):
        """绘制收敛曲线"""
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(costs) + 1), costs, 'b-')
        plt.xlabel('Iterations')
        plt.ylabel('Best Cost')
        plt.title('Convergence Curve')
        plt.grid(True)
        plt.show()
    
    def plot_solution(self, vehicles: List[List[int]]):
        """绘制配送路径"""
        plt.figure(figsize=(12, 8))
        
        # 绘制配送中心
        plt.plot(self.problem_data['vertexs'][0, 0], 
                self.problem_data['vertexs'][0, 1], 
                'ks', markersize=10, label='Depot')
        
        # 绘制顾客点
        plt.plot(self.problem_data['customers'][:, 0], 
                self.problem_data['customers'][:, 1], 
                'ro', label='Customers')
        
        # 为每条路径选择不同的颜色
        colors = plt.cm.rainbow(np.linspace(0, 1, len(vehicles)))
        
        # 绘制每条路径
        for route, color in zip(vehicles, colors):
            if not route:
                continue
                
            # 从配送中心到第一个顾客
            plt.plot([self.problem_data['vertexs'][0, 0], 
                     self.problem_data['customers'][route[0]-1, 0]],
                    [self.problem_data['vertexs'][0, 1], 
                     self.problem_data['customers'][route[0]-1, 1]],
                    color=color, alpha=0.6)
            
            # 顾客之间的路径
            for i in range(len(route)-1):
                plt.plot([self.problem_data['customers'][route[i]-1, 0], 
                         self.problem_data['customers'][route[i+1]-1, 0]],
                        [self.problem_data['customers'][route[i]-1, 1], 
                         self.problem_data['customers'][route[i+1]-1, 1]],
                        color=color, alpha=0.6)
            
            # 从最后一个顾客返回配送中心
            plt.plot([self.problem_data['customers'][route[-1]-1, 0], 
                     self.problem_data['vertexs'][0, 0]],
                    [self.problem_data['customers'][route[-1]-1, 1], 
                     self.problem_data['vertexs'][0, 1]],
                    color=color, alpha=0.6)
        
        plt.title('Vehicle Routing Solution')
        plt.legend()
        plt.grid(True)
        plt.show() 