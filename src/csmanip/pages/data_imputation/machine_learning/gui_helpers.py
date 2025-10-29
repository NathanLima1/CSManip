import tkinter as tk
from tkinter import ttk, StringVar, IntVar, BooleanVar

class SVMParameterFrame(ttk.Frame):
    """
    Frame com parâmetros para Support Vector Machine (Regression).
    """
    def __init__(self, master):
        super().__init__(master)

        # Configura as colunas da grade para expandirem igualmente
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")

        self._create_widgets()

    def _create_widgets(self):
        # --- Linha 0: Kernel e Degree ---
        ttk.Label(self, text='Kernel:').grid(row=0, column=0, sticky="w", padx=5)
        self.kernel_v = StringVar(value='rbf')
        lista_ker = ['linear', 'poly', 'rbf', 'sigmoid']
        ttk.Combobox(self, values=lista_ker, textvariable=self.kernel_v, state='readonly').grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='Degree (int, para poly):').grid(row=0, column=1, sticky="w", padx=5)
        self.degree_v = IntVar(value=3)
        ttk.Entry(self, textvariable=self.degree_v, justify=tk.CENTER).grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 2: Gamma e Coef0 ---
        ttk.Label(self, text='Gamma ("scale", "auto", float):').grid(row=2, column=0, sticky="w", padx=5)
        self.gamma_v = StringVar(value='scale')
        ttk.Entry(self, textvariable=self.gamma_v, justify=tk.CENTER).grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='Coef0 (float, para poly/sigmoid):').grid(row=2, column=1, sticky="w", padx=5)
        self.coef0_v = StringVar(value='0.0')
        ttk.Entry(self, textvariable=self.coef0_v, justify=tk.CENTER).grid(row=3, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 4: Tol e C ---
        ttk.Label(self, text='Tol (float):').grid(row=4, column=0, sticky="w", padx=5)
        self.tol_v = StringVar(value='0.001')
        ttk.Entry(self, textvariable=self.tol_v, justify=tk.CENTER).grid(row=5, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='C (float, Regularization):').grid(row=4, column=1, sticky="w", padx=5)
        self.c_v = StringVar(value='1.0')
        ttk.Entry(self, textvariable=self.c_v, justify=tk.CENTER).grid(row=5, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 6: Epsilon e Shrinking ---
        ttk.Label(self, text='Epsilon (float):').grid(row=6, column=0, sticky="w", padx=5)
        self.epsilon_v = StringVar(value='0.1')
        ttk.Entry(self, textvariable=self.epsilon_v, justify=tk.CENTER).grid(row=7, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='Shrinking (Bool):').grid(row=6, column=1, sticky="w", padx=5)
        self.shrinking_v = BooleanVar(value=True)
        ttk.Checkbutton(self, variable=self.shrinking_v, onvalue=True, offvalue=False).grid(row=7, column=1, sticky="w", padx=5, pady=(0, 10))

        # --- Linha 8: Cache Size e Verbose ---
        ttk.Label(self, text='Cache_size (MB, float):').grid(row=8, column=0, sticky="w", padx=5)
        self.cache_size_v = StringVar(value='200')
        ttk.Entry(self, textvariable=self.cache_size_v, justify=tk.CENTER).grid(row=9, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='Verbose (Bool):').grid(row=8, column=1, sticky="w", padx=5)
        self.verbose_v = BooleanVar(value=False)
        ttk.Checkbutton(self, variable=self.verbose_v, onvalue=True, offvalue=False).grid(row=9, column=1, sticky="w", padx=5, pady=(0, 10))

        # --- Linha 10: Max Iter ---
        ttk.Label(self, text='Max_iter (int, -1 for no limit):').grid(row=10, column=0, sticky="w", padx=5)
        self.maxiter_v = IntVar(value=-1)
        ttk.Entry(self, textvariable=self.maxiter_v, justify=tk.CENTER).grid(row=11, column=0, sticky="ew", padx=5, pady=(0, 10))

class NNeighParameterFrame(ttk.Frame):
    """
    Frame com parâmetros para Nearest Neighbors.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        
        self._create_widgets()

    def _create_widgets(self):
        # --- Linha 0 ---
        ttk.Label(self, text='N_neighbors (int):').grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(self, text='Algorithm:').grid(row=0, column=1, sticky="w", padx=5)
        
        self.n_neighbors_v = IntVar(value=5)
        ttk.Entry(self, textvariable=self.n_neighbors_v, justify=tk.CENTER).grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 10))

        self.algorithm_v = StringVar(value='auto')
        lista_alg = ['auto', 'ball_tree', 'kd_tree', 'brute']
        ttk.Combobox(self, values=lista_alg, textvariable=self.algorithm_v, state='readonly').grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 2 ---
        ttk.Label(self, text='Leaf_size (int):').grid(row=2, column=0, sticky="w", padx=5)
        ttk.Label(self, text='P (int):').grid(row=2, column=1, sticky="w", padx=5)

        self.leaf_size_v = IntVar(value=30)
        ttk.Entry(self, textvariable=self.leaf_size_v, justify=tk.CENTER).grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 10))

        self.p_v = IntVar(value=2)
        ttk.Entry(self, textvariable=self.p_v, justify=tk.CENTER).grid(row=3, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 4 ---
        ttk.Label(self, text='N_jobs (int / "None"):').grid(row=4, column=0, sticky="w", padx=5)
        self.n_jobs_v = StringVar(value='-1')
        ttk.Entry(self, textvariable=self.n_jobs_v, justify=tk.CENTER).grid(row=5, column=0, sticky="ew", padx=5, pady=(0, 10))

class GPParameterFrame(ttk.Frame):
    """
    Frame com parâmetros para Gaussian Process.
    Usa .grid() e herda de ttk.Frame.
    """
    def __init__(self, master):
        super().__init__(master)
        
        # Configura as colunas da grade para expandirem igualmente
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        
        self._create_widgets()

    def _create_widgets(self):
        # --- Linha 0 ---
        ttk.Label(self, text='Alpha (float):').grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(self, text='N_restart_optimizer (int):').grid(row=0, column=1, sticky="w", padx=5)

        self.alpha_gp = StringVar(value='0.0000000001')
        ttk.Entry(self, textvariable=self.alpha_gp, justify=tk.CENTER).grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 10))

        self.n_restarts_op = IntVar(value=0)
        ttk.Entry(self, textvariable=self.n_restarts_op, justify=tk.CENTER).grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 2 ---
        ttk.Label(self, text='Normalize_y (Bool 1/0):').grid(row=2, column=0, sticky="w", padx=5)
        ttk.Label(self, text='Kernel type:').grid(row=2, column=1, sticky="w", padx=5)

        self.normalize_y_gp = BooleanVar(value=0)
        ttk.Entry(self, textvariable=self.normalize_y_gp, justify=tk.CENTER).grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 10))

        self.kernel_type = StringVar(value='RBF')
        ttk.Combobox(self, textvariable=self.kernel_type, values=["RBF", "Matern", "DotProduct", "RationalQuadratic"], state='readonly').grid(row=3, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Frame para Parâmetros de Kernel ---
        kernel_frame = ttk.LabelFrame(self, text="Parâmetros de Kernel Específicos")
        kernel_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=10)
        kernel_frame.grid_columnconfigure(0, weight=1)
        kernel_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(kernel_frame, text='length_scale (float):').grid(row=0, column=0, sticky="w", padx=5)
        self.length_scale = StringVar(value='1.0')
        ttk.Entry(kernel_frame, textvariable=self.length_scale, justify=tk.CENTER).grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))
        
        ttk.Label(kernel_frame, text='nu (Matern):').grid(row=0, column=1, sticky="w", padx=5)
        self.nu = StringVar(value='1.5')
        ttk.Entry(kernel_frame, textvariable=self.nu, justify=tk.CENTER).grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 5))

        ttk.Label(kernel_frame, text='sigma_0 (DotProduct):').grid(row=2, column=0, sticky="w", padx=5)
        self.sigma_0 = StringVar(value='1.0')
        ttk.Entry(kernel_frame, textvariable=self.sigma_0, justify=tk.CENTER).grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 5))

        ttk.Label(kernel_frame, text='alpha (RationalQuadratic):').grid(row=2, column=1, sticky="w", padx=5)
        self.alpha_rq = StringVar(value='1.0')
        ttk.Entry(kernel_frame, textvariable=self.alpha_rq, justify=tk.CENTER).grid(row=3, column=1, sticky="ew", padx=5, pady=(0, 5))


class BaggingTParameterFrame(ttk.Frame):
    """
    Frame com parâmetros para Bagging Trees.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        
        self._create_widgets()

    def _create_widgets(self):
        # --- Linha 0 ---
        ttk.Label(self, text='Criterion:').grid(row=0, column=0, sticky="w", padx=5)
        self.criterion_v = StringVar(value="absolute_error")
        lista_cri = ["squared_error", "friedman_mse", "absolute_error", "poisson"]
        ttk.Combobox(self, values=lista_cri, textvariable=self.criterion_v, state='readonly').grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='Splitter:').grid(row=0, column=1, sticky="w", padx=5)
        self.splitter_v = StringVar(value="random")
        lista_spl = ["best", "random"]
        ttk.Combobox(self, values=lista_spl, textvariable=self.splitter_v, state='readonly').grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 2 ---
        ttk.Label(self, text="Max_depth (int):").grid(row=2, column=0, sticky="w", padx=5)
        self.maxd_v = StringVar(value="22")
        ttk.Entry(self, textvariable=self.maxd_v, justify=tk.CENTER).grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text="Min_samples_split (int):").grid(row=2, column=1, sticky="w", padx=5)
        self.minsam_s_v = IntVar(value=6)
        ttk.Entry(self, textvariable=self.minsam_s_v, justify=tk.CENTER).grid(row=3, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 4 ---
        ttk.Label(self, text="Min_samples_leaf (int):").grid(row=4, column=0, sticky="w", padx=5)
        self.minsam_l_v = IntVar(value=5)
        ttk.Entry(self, textvariable=self.minsam_l_v, justify=tk.CENTER).grid(row=5, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text="Min_weight_fraction_leaf (float):").grid(row=4, column=1, sticky="w", padx=5)
        self.minweifra_l_v = StringVar(value="0.0")
        ttk.Entry(self, textvariable=self.minweifra_l_v, justify=tk.CENTER).grid(row=5, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 6 ---
        ttk.Label(self, text="Max_features (int/float/'sqrt'/'log2'):").grid(row=6, column=0, sticky="w", padx=5)
        self.maxfeat_v = StringVar(value="sqrt")
        ttk.Entry(self, textvariable=self.maxfeat_v, justify=tk.CENTER).grid(row=7, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text="Max_leaf_nodes (int):").grid(row=6, column=1, sticky="w", padx=5)
        self.maxleaf_n = StringVar(value="10")
        ttk.Entry(self, textvariable=self.maxleaf_n, justify=tk.CENTER).grid(row=7, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 8 ---
        ttk.Label(self, text="Min_impurity_decrease (float):").grid(row=8, column=0, sticky="w", padx=5)
        self.minimp_dec = StringVar(value="0.0")
        ttk.Entry(self, textvariable=self.minimp_dec, justify=tk.CENTER).grid(row=9, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text="Ccp_alpha (float >= 0.0):").grid(row=8, column=1, sticky="w", padx=5)
        self.ccp_alp_v = StringVar(value="0.001")
        ttk.Entry(self, textvariable=self.ccp_alp_v, justify=tk.CENTER).grid(row=9, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 10 (Específico do Bagging) ---
        ttk.Label(self, text='N_Estimators (int):').grid(row=10, column=0, sticky="w", padx=5)
        self.n_estimators = IntVar(value=10)
        ttk.Entry(self, textvariable=self.n_estimators, justify=tk.CENTER).grid(row=11, column=0, sticky="ew", padx=5, pady=(0, 10))


class DTParameterFrame(ttk.Frame):
    """
    Frame com parâmetros para Decision Trees.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        
        self._create_widgets()

    def _create_widgets(self):
        # --- Linha 0 ---
        ttk.Label(self, text='Criterion:').grid(row=0, column=0, sticky="w", padx=5)
        self.criterion_v = StringVar(value="absolute_error")
        lista_cri = ["squared_error", "friedman_mse", "absolute_error", "poisson"]
        ttk.Combobox(self, values=lista_cri, textvariable=self.criterion_v, state='readonly').grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='Splitter:').grid(row=0, column=1, sticky="w", padx=5)
        self.splitter_v = StringVar(value="random")
        lista_spl = ["best", "random"]
        ttk.Combobox(self, values=lista_spl, textvariable=self.splitter_v, state='readonly').grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 2 ---
        ttk.Label(self, text="Max_depth (int):").grid(row=2, column=0, sticky="w", padx=5)
        self.maxd_v = StringVar(value="22")
        ttk.Entry(self, textvariable=self.maxd_v, justify=tk.CENTER).grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text="Min_samples_split (int):").grid(row=2, column=1, sticky="w", padx=5)
        self.minsam_s_v = IntVar(value=6)
        ttk.Entry(self, textvariable=self.minsam_s_v, justify=tk.CENTER).grid(row=3, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 4 ---
        ttk.Label(self, text="Min_samples_leaf (int):").grid(row=4, column=0, sticky="w", padx=5)
        self.minsam_l_v = IntVar(value=5)
        ttk.Entry(self, textvariable=self.minsam_l_v, justify=tk.CENTER).grid(row=5, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text="Min_weight_fraction_leaf (float):").grid(row=4, column=1, sticky="w", padx=5)
        self.minweifra_l_v = StringVar(value="0.0")
        ttk.Entry(self, textvariable=self.minweifra_l_v, justify=tk.CENTER).grid(row=5, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 6 ---
        ttk.Label(self, text="Max_features (int/float/'sqrt'/'log2'):").grid(row=6, column=0, sticky="w", padx=5)
        self.maxfeat_v = StringVar(value="sqrt")
        ttk.Entry(self, textvariable=self.maxfeat_v, justify=tk.CENTER).grid(row=7, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text="Max_leaf_nodes (int):").grid(row=6, column=1, sticky="w", padx=5)
        self.maxleaf_n = StringVar(value="10")
        ttk.Entry(self, textvariable=self.maxleaf_n, justify=tk.CENTER).grid(row=7, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 8 ---
        ttk.Label(self, text="Min_impurity_decrease (float):").grid(row=8, column=0, sticky="w", padx=5)
        self.minimp_dec = StringVar(value="0.0")
        ttk.Entry(self, textvariable=self.minimp_dec, justify=tk.CENTER).grid(row=9, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text="Ccp_alpha (float >= 0.0):").grid(row=8, column=1, sticky="w", padx=5)
        self.ccp_alp_v = StringVar(value="0.001")
        ttk.Entry(self, textvariable=self.ccp_alp_v, justify=tk.CENTER).grid(row=9, column=1, sticky="ew", padx=5, pady=(0, 10))

class NNParameterFrame(ttk.Frame):
    """
    Frame com parâmetros para Neural Network.
    """
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")

        self._create_widgets()

    def _create_widgets(self):
        # --- Linha 0 ---
        ttk.Label(self, text='Activation:').grid(row=0, column=0, sticky="w", padx=5)
        self.activation_v = StringVar(value='relu')
        ttk.Combobox(self, values=['identity', 'logistic', 'tanh', 'relu'],
                     textvariable=self.activation_v, state='readonly').grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='Solver:').grid(row=0, column=1, sticky="w", padx=5)
        self.solver_v = StringVar(value='adam')
        lista_sol = ['lbfgs', 'sgd', 'adam']
        ttk.Combobox(self, values=lista_sol, textvariable=self.solver_v, state='readonly').grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 2 ---
        ttk.Label(self, text='Alpha (float):').grid(row=2, column=0, sticky="w", padx=5)
        self.alpha_v = StringVar(value='0.0001')
        ttk.Entry(self, textvariable=self.alpha_v, justify=tk.CENTER).grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='Batch_size (int / "auto"):').grid(row=2, column=1, sticky="w", padx=5)
        self.batch_size_v = StringVar(value='auto')
        ttk.Entry(self, textvariable=self.batch_size_v, justify=tk.CENTER).grid(row=3, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 4 ---
        ttk.Label(self, text="Learning_rate:").grid(row=4, column=0, sticky="w", padx=5)
        self.learning_rate_v = StringVar(value='constant')
        lista_learn = ['constant', 'invscaling', 'adaptive']
        ttk.Combobox(self, values=lista_learn, textvariable=self.learning_rate_v, state='readonly').grid(row=5, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='Learning_rate_init (float):').grid(row=4, column=1, sticky="w", padx=5)
        self.learning_rate_init_v = StringVar(value='0.001')
        ttk.Entry(self, textvariable=self.learning_rate_init_v, justify=tk.CENTER).grid(row=5, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 6 ---
        ttk.Label(self, text='Power_t (float):').grid(row=6, column=0, sticky="w", padx=5)
        self.power_t_v = StringVar(value='0.5')
        ttk.Entry(self, textvariable=self.power_t_v, justify=tk.CENTER).grid(row=7, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='Max_iter (int):').grid(row=6, column=1, sticky="w", padx=5)
        self.max_iter_v = StringVar(value='200')
        ttk.Entry(self, textvariable=self.max_iter_v, justify=tk.CENTER).grid(row=7, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 8 ---
        ttk.Label(self, text='Shuffle (Bool 1/0):').grid(row=8, column=0, sticky="w", padx=5)
        self.shuffle_v = BooleanVar(value=True)
        # Usando Checkbutton para BooleanVar
        ttk.Checkbutton(self, variable=self.shuffle_v, onvalue=True, offvalue=False).grid(row=9, column=0, sticky="w", padx=5, pady=(0, 10))

        ttk.Label(self, text='Tol (float):').grid(row=8, column=1, sticky="w", padx=5)
        self.tol_v = StringVar(value='0.0001')
        ttk.Entry(self, textvariable=self.tol_v, justify=tk.CENTER).grid(row=9, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 10 ---
        ttk.Label(self, text='Verbose (Bool 1/0):').grid(row=10, column=0, sticky="w", padx=5)
        self.verbose_v = BooleanVar(value=False)
        ttk.Checkbutton(self, variable=self.verbose_v, onvalue=True, offvalue=False).grid(row=11, column=0, sticky="w", padx=5, pady=(0, 10))

        ttk.Label(self, text='Warm_start (Bool 1/0):').grid(row=10, column=1, sticky="w", padx=5)
        self.warm_start_v = BooleanVar(value=False)
        ttk.Checkbutton(self, variable=self.warm_start_v, onvalue=True, offvalue=False).grid(row=11, column=1, sticky="w", padx=5, pady=(0, 10))

        # --- Linha 12 ---
        ttk.Label(self, text='Momentum (float):').grid(row=12, column=0, sticky="w", padx=5)
        self.momentum_v = StringVar(value='0.9')
        ttk.Entry(self, textvariable=self.momentum_v, justify=tk.CENTER).grid(row=13, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='Nesterovs_momentum (Bool 1/0):').grid(row=12, column=1, sticky="w", padx=5)
        self.nesterovs_momentum_v = BooleanVar(value=True)
        ttk.Checkbutton(self, variable=self.nesterovs_momentum_v, onvalue=True, offvalue=False).grid(row=13, column=1, sticky="w", padx=5, pady=(0, 10))

        # --- Linha 14 ---
        ttk.Label(self, text='Early_stopping (Bool 1/0):').grid(row=14, column=0, sticky="w", padx=5)
        self.early_stopping_v = BooleanVar(value=False)
        ttk.Checkbutton(self, variable=self.early_stopping_v, onvalue=True, offvalue=False).grid(row=15, column=0, sticky="w", padx=5, pady=(0, 10))

        ttk.Label(self, text='Validation_fraction (float):').grid(row=14, column=1, sticky="w", padx=5)
        self.validation_fraction_v = StringVar(value='0.1')
        ttk.Entry(self, textvariable=self.validation_fraction_v, justify=tk.CENTER).grid(row=15, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 16 ---
        ttk.Label(self, text='Beta_1 (float):').grid(row=16, column=0, sticky="w", padx=5)
        self.beta_1_v = StringVar(value='0.9')
        ttk.Entry(self, textvariable=self.beta_1_v, justify=tk.CENTER).grid(row=17, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='Beta_2 (float):').grid(row=16, column=1, sticky="w", padx=5)
        self.beta_2_v = StringVar(value='0.999')
        ttk.Entry(self, textvariable=self.beta_2_v, justify=tk.CENTER).grid(row=17, column=1, sticky="ew", padx=5, pady=(0, 10))

        # --- Linha 18 ---
        ttk.Label(self, text='N_iter_no_change (int):').grid(row=18, column=0, sticky="w", padx=5)
        self.n_iter_no_change_v = StringVar(value='10')
        ttk.Entry(self, textvariable=self.n_iter_no_change_v, justify=tk.CENTER).grid(row=19, column=0, sticky="ew", padx=5, pady=(0, 10))

        ttk.Label(self, text='max_fun (int):').grid(row=18, column=1, sticky="w", padx=5)
        self.max_fun_v = StringVar(value='15000')
        ttk.Entry(self, textvariable=self.max_fun_v, justify=tk.CENTER).grid(row=19, column=1, sticky="ew", padx=5, pady=(0, 10))