import numpy as np
import time
from typing import List, Dict, Tuple
from src.vrptw.utils.utils import VRPTWUtils
from src.vrptw.visualization.visualizer import Visualizer

class ACO:
    def __init__(self, problem_data: Dict, config: Dict):
        """初始化ACO算法"""
        self.problem_data = problem_data
        self.config = config
        self.utils = VRPTWUtils(problem_data, config)
        self.visualizer = Visualizer(problem_data)
        
        # 初始化信息素矩阵和启发函数
        self.cusnum = problem_data['cusnum']
        self.Tau = np.ones((self.cusnum + 1, self.cusnum + 1))
        self.Eta = 1.0 / (problem_data['dist'] + np.eye(len(problem_data['dist'])) * 1e-10)
        
    def select_next_customer(self, current: int, unvisited: List[int], route: List[int]) -> int:
        """选择下一个访问的顾客"""
        if not unvisited:
            return None
        
        # 获取可行的下一个点集合
        next_points = self.next_point_set(route)
        
        # 如果没有可行点，则使用所有未访问点
        if not next_points:
            next_points = unvisited
        
        r = np.random.random()
        
        if r <= self.config['r0']:
            # 贪婪选择
            max_val = -float('inf')
            chosen = None
            for j in next_points:
                wait_time = max(self.utils.calculate_wait_time(route + [j]), 1e-8)
                val = (
                    (self.Tau[current, j] ** self.config['alpha']) *
                    (self.Eta[current, j] ** self.config['beta']) *
                    (1.0 / self.problem_data['width'][j-1] ** self.config['gamma']) *
                    (1.0 / wait_time ** self.config['delta'])
                )
                if val > max_val:
                    max_val = val
                    chosen = j
        else:
            # 轮盘赌选择
            probs = []
            for j in next_points:
                wait_time = max(self.utils.calculate_wait_time(route + [j]), 1e-8)
                prob = (
                    (self.Tau[current, j] ** self.config['alpha']) *
                    (self.Eta[current, j] ** self.config['beta']) *
                    (1.0 / self.problem_data['width'][j-1] ** self.config['gamma']) *
                    (1.0 / wait_time ** self.config['delta'])
                )
                probs.append(prob)
                
            probs = np.array(probs)
            if sum(probs) == 0:
                return np.random.choice(next_points)
            probs = probs / sum(probs)
            chosen = np.random.choice(next_points, p=probs)
        
        return chosen
    
    def next_point_set(self, route: List[int]) -> List[int]:
        """获取可行的下一个访问点集合"""
        unvisited = list(set(range(1, self.cusnum + 1)) - set(route))
        next_points = []
        
        for j in unvisited:
            test_route = route + [j]
            if self.utils.check_constraints(test_route):
                next_points.append(j)
                
        return next_points
    
    def update_pheromone(self, best_solution: List[int], best_cost: float):
        """更新信息素矩阵"""
        # 信息素挥发
        self.Tau = self.Tau * self.config['rho']
        
        if not best_solution:
            return
        
        # 计算增量
        delta_tau = self.config['q'] / best_cost
        
        # 更新最优路径上的信息素
        for i in range(len(best_solution)-1):
            self.Tau[best_solution[i], best_solution[i+1]] += delta_tau
        
        # 最后一个顾客到配送中心的信息素更新
        self.Tau[best_solution[-1], 0] += delta_tau
    
    def run(self) -> Tuple[List[List[int]], float]:
        """运行算法"""
        best_solution = None
        best_cost = float('inf')
        best_vehicles = None
        best_costs = []
        
        start_time = time.time()
        
        for iteration in range(self.config['max_iter']):
            # 构建所有蚂蚁的解
            solutions = []
            costs = []
            all_vehicles = []
            
            for ant in range(self.config['n_ants']):
                # 构建单个蚂蚁的解
                current_solution = []
                unvisited = list(range(1, self.cusnum + 1))
                
                while unvisited:
                    current = current_solution[-1] if current_solution else 0
                    next_customer = self.select_next_customer(current, unvisited, current_solution)
                    if next_customer is None:
                        break
                    current_solution.append(next_customer)
                    unvisited.remove(next_customer)
                    
                # 解码并计算成本
                vehicles, n_vehicles, total_distance = self.utils.decode_solution(current_solution)
                cost = 1000 * n_vehicles + total_distance
                
                solutions.append(current_solution)
                costs.append(cost)
                all_vehicles.append(vehicles)
            
            # 更新最优解
            min_cost_idx = np.argmin(costs)
            if costs[min_cost_idx] < best_cost:
                best_cost = costs[min_cost_idx]
                best_solution = solutions[min_cost_idx]
                best_vehicles = all_vehicles[min_cost_idx]
            
            # 更新信息素
            self.update_pheromone(best_solution, best_cost)
            
            # 记录最优成本
            best_costs.append(best_cost)
            
            # 打印迭代信息
            print(f"\n迭代 {iteration + 1}/{self.config['max_iter']}")
            print(f"最优成本: {best_cost:.2f}")
            print(f"平均成本: {np.mean(costs):.2f}")
        
        end_time = time.time()
        print(f"\n总用时: {end_time - start_time:.2f} 秒")
        
        # 绘制收敛曲线和最优路径
        self.visualizer.plot_convergence(best_costs)
        self.visualizer.plot_solution(best_vehicles)
        
        return best_vehicles, best_cost 