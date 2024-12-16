class Config:
    # 算法默认参数
    DEFAULT_PARAMS = {
        'n_ants': 50,        # 蚂蚁数量
        'alpha': 1.0,        # 信息素重要程度因子
        'beta': 3.0,         # 启发函数重要程度因子
        'gamma': 2.0,        # 时间窗口宽度影响因子
        'delta': 3.0,        # 等待时间影响因子
        'r0': 0.5,          # 状态转移规则参数
        'rho': 0.85,        # 信息素挥发系数
        'q': 5.0,           # 信息素增加强度系数
        'max_iter': 100,     # 最大迭代次数
        'v_num': 25,        # 最大车辆数
        'cap': 200          # 车辆最大装载量
    }
    
    @staticmethod
    def get_params(custom_params=None):
        """
        获取算法参数，允许自定义参数覆盖默认参数
        """
        params = Config.DEFAULT_PARAMS.copy()
        if custom_params:
            params.update(custom_params)
        return params 