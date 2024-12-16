from typing import List, Dict

class VRPTWUtils:
    def __init__(self, problem_data: Dict, config: Dict):
        self.problem_data = problem_data
        self.config = config
        
    def check_constraints(self, route: List[int]) -> bool:
        """检查路径是否满足约束条件"""
        if not route:
            return True
            
        # 检查载重约束
        total_demand = sum(self.problem_data['demands'][j-1] for j in route)
        if total_demand > self.config['cap']:
            return False
            
        # 检查时间窗约束
        current_time = 0
        current_pos = 0
        
        for j in route:
            travel_time = self.problem_data['dist'][current_pos, j]
            arrival_time = current_time + travel_time
            
            # 如果到达时间晚于时间窗结束时间
            if arrival_time > self.problem_data['b'][j-1]:
                return False
                
            # 更新服务开始时间
            service_time = max(arrival_time, self.problem_data['a'][j-1])
            current_time = service_time + self.problem_data['s'][j-1]
            current_pos = j
            
        # 检查返回配送中心时间约束
        return_time = current_time + self.problem_data['dist'][current_pos, 0]
        return return_time <= self.problem_data['L']
    
    def calculate_wait_time(self, route: List[int]) -> float:
        """计算到达最后一个顾客的等待时间"""
        if not route:
            return 0
            
        current_time = 0
        current_pos = 0
        
        for j in route:
            travel_time = self.problem_data['dist'][current_pos, j]
            arrival_time = current_time + travel_time
            wait_time = max(0, self.problem_data['a'][j-1] - arrival_time)
            current_time = max(arrival_time, self.problem_data['a'][j-1]) + self.problem_data['s'][j-1]
            current_pos = j
            
        return wait_time
    
    def decode_solution(self, route: List[int]) -> tuple:
        """将路径解码为可行解"""
        if not route:
            return [], 0, 0
            
        vehicles = []
        current_route = []
        current_time = 0
        current_pos = 0
        
        for j in route:
            test_route = current_route + [j]
            if self.check_constraints(test_route):
                current_route.append(j)
            else:
                if current_route:
                    vehicles.append(current_route)
                current_route = [j]
                current_time = 0
                current_pos = 0
                
        if current_route:
            vehicles.append(current_route)
            
        # 计算总距离和使用车辆数
        total_distance = 0
        for route in vehicles:
            if not route:
                continue
            total_distance += self.problem_data['dist'][0, route[0]]
            for i in range(len(route)-1):
                total_distance += self.problem_data['dist'][route[i], route[i+1]]
            total_distance += self.problem_data['dist'][route[-1], 0]
            
        return vehicles, len(vehicles), total_distance