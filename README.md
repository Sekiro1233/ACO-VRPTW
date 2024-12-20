# ACO-VRPTW

基于蚁群算法(ACO)求解带时间窗的车辆路径问题(VRPTW)的Python实现。

## 项目结构

```
src/vrptw/
├── core/           # 核心算法模块
│   └── aco.py
├── data/          # 数据处理和测试用例
│   ├── data_loader.py
│   ├── c101.txt
│   ├── r101.txt
│   └── rc101.txt
├── utils/         # 工具函数模块
│   └── utils.py
├── visualization/ # 可视化模块
│   └── visualizer.py
└── config/       # 配置模块
    └── config.py
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

程序支持三种类型的问题：C类（聚类分布）、R类（随机分布）和RC类（混合分布）。
每种类型都有其专门优化的参数配置。

1. C类问题（聚类分布，如c101.txt）：
```bash
python main.py --instance c101.txt --type C --ants 50 --iterations 100
```

2. R类问题（随机分布，如r101.txt）：
```bash
python main.py --instance r101.txt --type R --ants 120 --iterations 200
```

3. RC类问题（混合分布，如rc101.txt）：
```bash
python main.py --instance rc101.txt --type RC --ants 150 --iterations 250
```

### 命令行参数说明

- `--instance`: 测试用例文件名（默认：c101.txt）
- `--type`: 问题类型，可选值：C（聚类）、R（随机）、RC（混合）
- `--ants`: 蚂蚁数量（默认：50）
- `--iterations`: 最大迭代次数（默认：100）

### 问题类型及其参数配置

1. C类问题（聚类分布）参数：
   - alpha = 1.0（信息素重要程度）
   - beta = 3.0（启发函数重要程度）
   - gamma = 2.0（时间窗口影响）
   - delta = 3.0（等待时间影响）
   - r0 = 0.5（状态转移规则）
   - rho = 0.85（信息素挥发系数）
   - q = 5.0（信息素增加强度）

2. R类问题（随机分布）参数：
   - alpha = 2.0（更强的历史经验影响）
   - beta = 5.0（更强的距离因素）
   - gamma = 3.0（更强的时间窗约束）
   - delta = 4.0（更强的等待时间影响）
   - r0 = 0.6（加强局部搜索）
   - rho = 0.1（保持更多历史信息）
   - q = 10.0（更强的路径强化）

3. RC类问题（混合分布）参数：
   - alpha = 1.5（平衡历史经验）
   - beta = 4.0（平衡距离因素）
   - gamma = 2.5（适中的时间窗约束）
   - delta = 3.5（适中的等待时间）
   - r0 = 0.55（平衡探索和利用）
   - rho = 0.3（中等信息素保持）
   - q = 7.5（适中的路径强化）

### 运行建议

1. C类问题（聚类分布）：
   - 使用较少的蚂蚁数量（50）
   - 标准迭代次数（100）
   - 较高的信息素挥发率

2. R类问题（随机分布）：
   - 使用较多的蚂蚁数量（120）
   - 较多的迭代次数（200）
   - 保持更多的历史信息

3. RC类问题（混合分布）：
   - 使用最多的蚂蚁数量（150）
   - 最多的迭代次数（250）
   - 平衡的参数配置

## 输出结果

程序运行后会输出：
1. 迭代过程信息
   - 当前迭代次数
   - 最优成本
   - 平均成本

2. 最终结果
   - 使用的车辆数量
   - 总距离
   - 总成本
   - 每辆车的具体配送路径

3. 可视化结果
   - 收敛曲线图：展示算法收敛过程
   - 配送路径图：直观展示最优配送方案

## 注意事项

1. 参数选择建议：
   - C类问题：使用原始参数配置即可
   - R类问题：增加蚂蚁数量和迭代次数，降低信息素挥发率
   - RC类问题：使用最大的蚂蚁数量和迭代次数，采用平衡的参数配置

2. 性能优化：
   - 较大规模问题可适当增加迭代次数和蚂蚁数量
   - 可以根据实际问题特点微调参数
   - 建议先用小规模数据测试参数效果

3. 结果稳定性：
   - 算法具有随机性，每次运行结果可能略有不同
   - 增加迭代次数和蚂蚁数量可提高稳定性
   - 可多次运行取最优结果