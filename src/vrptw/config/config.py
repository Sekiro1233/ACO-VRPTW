class Config:
    # 算法默认参数
    DEFAULT_PARAMS = {
        'n_ants': 50,        # 蚂蚁数量
        'alpha': 2.0,        # 信息素重要程度因子（增加以加强历史经验的影响）
        'beta': 5.0,         # 启发函数重要程度因子（增加以更注重距离因素）
        'gamma': 3.0,        # 时间窗口宽度影响因子（增加以更好处理时间窗约束）
        'delta': 4.0,        # 等待时间影响因子（增加以减少等待时间）
        'r0': 0.6,          # 状态转移规则参数（增加以加强局部搜索）
        'rho': 0.1,         # 信息素挥发系数（减小以保持更多历史信息）
        'q': 10.0,          # 信息素增加强度系数（增加以强化好的路径）
        'max_iter': 100,     # 最大迭代次数
        'v_num': 25,        # 最大车辆数
        'cap': 200          # 车辆最大装载量
    }
    
    # C类问题（聚类分布）的推荐参数
    C_TYPE_PARAMS = {
        'n_ants': 50,        # 蚂蚁数量
        'alpha': 1.0,        # 信息素重要程度因子
        'beta': 3.0,         # 启发函数重要程度因子
        'gamma': 2.0,        # 时间窗口宽度影响因子
        'delta': 3.0,        # 等待时间影响因子
        'r0': 0.5,          # 状态转移规则参数
        'rho': 0.85,        # 信息素挥发系数
        'q': 5.0,           # 信息素增加强度系数
    }
    
    # R类问题（随机分布）的推荐参数
    R_TYPE_PARAMS = {
        'n_ants': 50,        # 蚂蚁数量
        'alpha': 2.0,        # 信息素重要程度因子
        'beta': 5.0,         # 启发函数重要程度因子
        'gamma': 3.0,        # 时间窗口宽度影响因子
        'delta': 4.0,        # 等待时间影响因子
        'r0': 0.6,          # 状态转移规则参数
        'rho': 0.1,         # 信息素挥发系数
        'q': 10.0,          # 信息素增加强度系数
    }
    
    # RC类问题（混合分布）的推荐参数
    RC_TYPE_PARAMS = {
        'n_ants': 50,        # 蚂蚁数量
        'alpha': 1.5,        # 信息素重要程度因子（平衡历史经验）
        'beta': 4.0,         # 启发函数重要程度因子（平衡距离因素）
        'gamma': 2.5,        # 时间窗口宽度影响因子（适中的时间窗约束）
        'delta': 3.5,        # 等待时间影响因子（适中的等待时间权重）
        'r0': 0.55,         # 状态转移规则参数（平衡探索和利用）
        'rho': 0.3,         # 信息素挥发系数（中等程度的信息素保持）
        'q': 7.5,           # 信息素增加强度系数（适中的强化程度）
    }
    
    @staticmethod
    def get_params(custom_params=None, problem_type='R'):
        """
        获取算法参数，允许自定义参数覆盖默认参数
        problem_type: 'C' 表示聚类问题，'R' 表示随机分布问题，'RC' 表示混合分布问题
        """
        # 根据问题类型选择基础参数
        if problem_type == 'C':
            params = Config.C_TYPE_PARAMS.copy()
        elif problem_type == 'RC':
            params = Config.RC_TYPE_PARAMS.copy()
        else:
            params = Config.R_TYPE_PARAMS.copy()
            
        # 添加通用参数
        params.update({
            'max_iter': Config.DEFAULT_PARAMS['max_iter'],
            'v_num': Config.DEFAULT_PARAMS['v_num'],
            'cap': Config.DEFAULT_PARAMS['cap']
        })
        
        # 如果有自定义参数，覆盖默认值
        if custom_params:
            params.update(custom_params)
            
        return params