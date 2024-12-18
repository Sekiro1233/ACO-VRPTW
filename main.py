from src.vrptw.data.data_loader import DataLoader
from src.vrptw.config.config import Config
from src.vrptw.core.aco import ACO
import os
import argparse

def run_vrptw(data_file: str, custom_params: dict = None, problem_type: str = 'R'):
    """运行VRPTW算法"""
    # 加载数据
    data_loader = DataLoader(data_file)
    problem_data = data_loader.load_data()
    
    # 获取配置参数
    config = Config.get_params(custom_params, problem_type)
    
    # 创建并运行ACO算法
    aco = ACO(problem_data, config)
    best_vehicles, best_cost, total_distance = aco.run()
    
    # 输出结果
    print(f"\n测试用例: {data_file}")
    print("\n最终结果:")
    print(f"使用车辆数: {len(best_vehicles)}")
    print(f"总距离: {total_distance:.2f}")
    print(f"总成本: {best_cost:.2f}")
    print("\n具体路径:")
    for i, route in enumerate(best_vehicles):
        print(f"车辆 {i+1}: {route}")
    
    return best_vehicles, best_cost, total_distance

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='VRPTW求解器')
    parser.add_argument('--instance', type=str, default='c101.txt',
                      help='测试用例文件名 (默认: c101.txt)')
    parser.add_argument('--ants', type=int, default=50,
                      help='蚂蚁数量 (默认: 50)')
    parser.add_argument('--iterations', type=int, default=100,
                      help='最大迭代次数 (默认: 100)')
    parser.add_argument('--type', type=str, choices=['C', 'R', 'RC'], default='R',
                      help='问题类型: C-聚类分布, R-随机分布, RC-混合分布 (默认: R)')
    
    args = parser.parse_args()
    
    # 自定义参数
    custom_params = {
        'n_ants': args.ants,
        'max_iter': args.iterations
    }
    
    # 运行算法
    run_vrptw(args.instance, custom_params, args.type)

if __name__ == "__main__":
    main() 