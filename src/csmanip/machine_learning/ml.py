"""Module for the machine learning without interface.

This module creates a window with options for selecting different 
Machine Learning algorithms and integrates functionalities such as
parameter selection, data preview, and result visualization.
"""

from tkinter import Toplevel
from .ml_view import View
from .utils import *
from .ml_helpers import *
from ..data_processing.data_processing import DataProcessing

class Ml:
    def __init__(self):
        self.list_ml = ['Decision Trees',
                     'Neural network',
                     'Nearest Neighbors',
                     'Support Vector',
                     'Gaussian Process']
        
        self.list_ind = ["Precipitation", 'Maximum temperature', 'Minimum temperature']
        self.list_dt = ['Target city', 'Neighbor A', 'Neighbor B', 'Neighbor C']
        
        self.data_s = "Target_city"
        self.ind_s = "Maximum temperature"
        

    def int_float(self, value):
        """
        Try to return a int value, if it can't, returns a float value
        """
        try:
            return int(value)
        except:
            return float(value)

    def valid_maxf(self, value):
        """
        Returnes the correct type of a received value
        """
        if value.isdigit() == True:
            value = int(value)
        elif value.isalnum() == True and value.isdigit() == False:
            value = str(value)
        elif value.isalnum() == False and value.isdigit() == False and value.isalpha() == False:
            value = float(value)

        return value

    def save_parameter(self):
        v = View
        return v.save_parameter()

    def data_preview(self, score, mean_abs_error, mean_rel_error, max_abs_error, exact_max,
                     pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis):
        v = View()
        v.data_preview(score, mean_abs_error, mean_rel_error, max_abs_error, exact_max,
                       pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis)

    def get_end(self, city):
        treatment = DataProcessing()
        return treatment.get_file_path(city)

    def generate_preview_dt(self):
        v = View()
        v.generate_preview_dt(self)
    
    def generate_preview_bt(self):
        v = View()
        v.generate_preview_bt(self)

    def generate_preview_nn(self):
        v = View()
        v.generate_preview_nn(self)

    def generate_preview_svm(self):
        v = View()
        v.generate_preview_svm(self)

    def generate_preview_kn(self):
        v = View()
        v.generate_preview_kn(self)

    def decision_tree(self, criterion_v="squared_error", splitter="best", maxd_v='10',
                      minsam_s_v=2, minsam_l_v=50, minweifra_l_v='0.0', maxfeat_v="sqrt",
                      maxleaf_n='10', minimp_dec='0.0', ccp_alp_v='0.0', 
                      por_trei=70, num_teste=5,save_model=False):
        
        list_cri = ["squared_error", "friedman_mse", "absolute_error", "poisson"]
        if criterion_v not in list_cri:
            raise ValueError(f"Selected criterion_v is not compatible. "
            f"Please try one of the following options: 'squared_error', 'friedman_mse', 'absolute_error', 'poisson'.")
        
        list_spl = ['best', 'random']
        if splitter not in list_spl:
            raise ValueError(f"Selected splitter is not compatible. "
                             f"Please try one of the following options: 'best', 'random'")
        
        list_maxfeat_v = ['int', 'float', 'sqrt', 'log2']
        if maxfeat_v not in list_maxfeat_v:
            raise ValueError(f"Selected maxfeat_v is not compatible. "
                             f"Please try one of the following options: 'int', 'float', 'sqrt', 'log2'")
        
        self.param_frame = DTParameter(criterion_v, splitter, maxd_v, minsam_s_v, minsam_l_v,
                                       minweifra_l_v, maxfeat_v, maxleaf_n, minimp_dec, ccp_alp_v)
        self.por_trei = por_trei
        self.num_teste = num_teste
        self.save_model = save_model
        self.generate_preview_dt()

    def bagged_trees(self, criterion_v="squared_error", splitter="best", maxd_v='10',
                      minsam_s_v=2, minsam_l_v=50, minweifra_l_v='0.0', maxfeat_v="sqrt",
                      maxleaf_n='10', minimp_dec='0.0', ccp_alp_v='0.0', 
                      por_trei=70, num_teste=5,save_model=False, n_estimators=10):
        
        list_cri = ["squared_error", "friedman_mse", "absolute_error", "poisson"]
        if criterion_v not in list_cri:
            raise ValueError(f"Selected criterion_v is not compatible. "
            f"Please try one of the following options: 'squared_error', 'friedman_mse', 'absolute_error', 'poisson'.")
        
        list_spl = ['best', 'random']
        if splitter not in list_spl:
            raise ValueError(f"Selected splitter is not compatible. "
                             f"Please try one of the following options: 'best', 'random'")
        
        list_maxfeat_v = ['int', 'float', 'sqrt', 'log2']
        if maxfeat_v not in list_maxfeat_v:
            raise ValueError(f"Selected maxfeat_v is not compatible. "
                             f"Please try one of the following options: 'int', 'float', 'sqrt', 'log2'")
        
        self.param_frame = BTParameter(criterion_v, splitter, maxd_v, minsam_s_v, minsam_l_v,
                                       minweifra_l_v, maxfeat_v, maxleaf_n, minimp_dec, ccp_alp_v, n_estimators)
        self.por_trei = por_trei
        self.num_teste = num_teste
        self.save_model = save_model
        self.n_estimators = n_estimators
        self.generate_preview_bt()

    def neural_network(self, activation_v='relu', solver_v='adam', alpha_v='0.0001',
                       batch_size_v='auto', learning_rate_v='constant', learning_rate_init_v='0.001',
                       power_t_v='0.5', max_iter_v='200', shuffle_v=True, tol_v='0.0001',
                       verbose_v=False, warm_start_v=False, momentum_v='0.9', nesterovs_momentum_v=True,
                       early_stopping_v=False, validation_fraction_v='0.1', beta_1_v='0.9',
                       beta_2_v='0.999', n_iter_no_change_v='10', max_fun_v='15000', por_trei=70,
                       num_teste=5, save_model=False):
        
        list_activation_v = ['identity', 'logistic', 'tanh', 'relu']
        if activation_v not in list_activation_v:
            raise ValueError(f"Selected activation_v is not compatible. "
                             f"Please try one of the following options: 'identity', 'logistic', 'tanh', 'relu'")
        
        list_solver = ['lbfgs', 'sgd', 'adam']
        if solver_v not in list_solver:
            raise ValueError(f"Selected solver_v is not compatible. "
                             f"Please try one of the following options: 'lbfgs', 'sgd', 'adam'")
        
        list_batch_size = ['int', 'auto']
        if batch_size_v not in list_batch_size:
            raise ValueError(f"Selected batch_size_v is not compatible. "
                             f"Please try one of the following options: 'int', 'auto'")
        
        list_learn = ['constant', 'invscaling', 'adaptive']
        if learning_rate_v not in list_learn:
            raise ValueError(f"Selected learning_rate_v is not compatible. "
                             f"Please try one of the following options: 'constant', 'invscaling', 'adaptive'")

        self.param_frame = NNParameter(activation_v, solver_v, alpha_v, batch_size_v,
                 learning_rate_v, learning_rate_init_v, power_t_v, max_iter_v,
                 shuffle_v, tol_v, verbose_v, warm_start_v, momentum_v,
                 nesterovs_momentum_v, early_stopping_v, validation_fraction_v,
                 beta_1_v, beta_2_v, n_iter_no_change_v, max_fun_v)
        
        self.save_model = save_model
        self.num_teste = num_teste
        self.por_trei = por_trei
        self.generate_preview_nn()

    def nearest_neighbors(self, n_neighbors_v=5, algorithm_v='auto', leaf_size_v=30,
                          p_v=2, n_jobs_v='5', por_trei=70, num_teste=5, save_model=False):
        
        list_alg = ['auto', 'ball_tree', 'kd_tree', 'brute']
        if algorithm_v not in list_alg:
            raise ValueError(f"Selected algorithm_v is not compatible. "
                             f"Please try one of the following options: 'auto', 'ball_tree', 'kd_tree', 'brute'")
        self.param_frame = NNeighParameter(n_neighbors_v, algorithm_v, leaf_size_v, p_v, n_jobs_v)

        self.save_model = save_model
        self.num_teste = num_teste
        self.por_trei = por_trei
        self.generate_preview_kn()

    def support_vector(self, kernel_v='rbf', degree_v=3, gamma_v='scale', coef0_v='0.0',
                       tol_v='0.001', c_v='1.0', epsilon_v='0.1', shrinking_v=True,
                       cache_size_v='200', verbose_v=False, maxiter_v=-1, por_trei=70,
                       num_teste=5, save_model=False):
        list_kernel = ['linear', 'poly', 'rbf', 'sigmoid']
        if kernel_v not in list_kernel:
            raise ValueError(f"Selected kernel_v is not compatible. "
                             f"Please try one of the following options: 'linear', 'poly', 'rbf', 'sigmoid'")
        
        self.kernel_v = kernel_v
        self.degree_v = degree_v
        list_gamma = ['scale', 'auto', 'float']
        if gamma_v not in list_gamma:
            raise ValueError(f"Selected algorithm_v is not compatible. "
                             f"Please try one of the following options: 'auto', 'sacle', 'float'")
        
        self.gamma_v = gamma_v
        self.coef0_v = coef0_v
        self.tol_v = tol_v
        self.c_v = c_v
        self.epsilon_v = epsilon_v
        self.shrinking_v = shrinking_v
        self.cache_size_v = cache_size_v
        self.verbose_v = verbose_v
        self.maxiter_v = maxiter_v
        self.por_trei = por_trei
        self.num_teste = num_teste
        self.save_model = save_model
        self.generate_preview_svm()

    def gaussian_process(self, alpha_gp='0.0000000001', n_restarts_op=0,
                         normalize_y_gp=False, copy_X_train=False, rand_state_gp='None',
                         por_trei=70, num_teste=5, save_model=False):
        self.param_frame = GPParameter(alpha_gp, n_restarts_op, normalize_y_gp, copy_X_train, rand_state_gp)
        self.por_trei = por_trei
        self.num_teste = num_teste
        self.save_model = save_model
        self.generate_preview_svm()