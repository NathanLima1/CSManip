class DTParameter:
    def __init__(self, criterion_v, splitter, maxd_v, minsam_s_v, minsam_l_v,
                 minweifra_l_v, maxfeat_v, maxleaf_n, minimp_dec, ccp_alp_v):
        self.criterion_v = criterion_v
        self.splitter_v = splitter
        self.maxd_v = maxd_v
        self.minsam_s_v = minsam_s_v
        self.minsam_l_v = minsam_l_v
        self.minweifra_l_v = minweifra_l_v
        self.maxfeat_v = maxfeat_v
        self.maxleaf_n = maxleaf_n
        self.minimp_dec = minimp_dec
        self.ccp_alp_v = ccp_alp_v

class BTParameter:
    def __init__(self, criterion_v, splitter, maxd_v, minsam_s_v, minsam_l_v,
                 minweifra_l_v, maxfeat_v, maxleaf_n, minimp_dec, ccp_alp_v, n_estimators):
        self.criterion_v = criterion_v
        self.splitter_v = splitter
        self.maxd_v = maxd_v
        self.minsam_s_v = minsam_s_v
        self.minsam_l_v = minsam_l_v
        self.minweifra_l_v = minweifra_l_v
        self.maxfeat_v = maxfeat_v
        self.maxleaf_n = maxleaf_n
        self.minimp_dec = minimp_dec
        self.ccp_alp_v = ccp_alp_v
        self.n_estimators = n_estimators

class NNParameter:
    def __init__(self, activation_v, solver_v, alpha_v, batch_size_v,
                 learning_rate_v, learning_rate_init_v, power_t_v, max_iter_v,
                 shuffle_v, tol_v, verbose_v, warm_start_v, momentum_v,
                 nesterovs_momentum_v, early_stopping_v, validation_fraction_v,
                 beta_1_v, beta_2_v, n_iter_no_change_v, max_fun_v):
        self.activation_v = activation_v
        self.solver_v = solver_v
        self.alpha_v = alpha_v
        self.batch_size_v = batch_size_v
        self.learning_rate_v = learning_rate_v
        self.learning_rate_init_v = learning_rate_init_v
        self.power_t_v =  power_t_v
        self.max_iter_v = max_iter_v
        self.shuffle_v = shuffle_v
        self.tol_v = tol_v
        self.verbose_v = verbose_v
        self.warm_start_v = warm_start_v
        self.momentum_v = momentum_v
        self.nesterovs_momentum_v = nesterovs_momentum_v
        self.early_stopping_v = early_stopping_v
        self.validation_fraction_v = validation_fraction_v
        self.beta_1_v = beta_1_v
        self.beta_2_v = beta_2_v
        self.n_iter_no_change_v = n_iter_no_change_v
        self.max_fun_v = max_fun_v

class NNeighParameter:
    def __init__(self, n_neighbors_v, algorithm_v, leaf_size_v, p_v, n_jobs_v):
        self.n_neighbors_v = n_neighbors_v
        self.algorithm_v = algorithm_v
        self.leaf_size_v = leaf_size_v
        self.p_v = p_v
        self.n_jobs_v = n_jobs_v

class GPParameter:
    def __init__(self, alpha_gp, n_restarts_op, normalize_y_gp, copy_X_train, rand_state_gp):
        self.alpha_gp = alpha_gp
        self.n_restarts_op = n_restarts_op
        self.normalize_y_gp = normalize_y_gp
        self.copy_X_train = copy_X_train
        self.rand_state_gp = rand_state_gp