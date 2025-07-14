import os
import pyscreenshot
from ..training.training import Training
from tkinter import Label, LabelFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from . import decision_trees
from . import bagging_trees
from . import support_vector
from . import neural_network
from . import gaussian_process
from . import nearest_neighbors
from ..styles import colors
from ..utils.indicator import get_indicator_code
from ..utils.ml_param import get_parameters_ml
from ..utils.insert_canvas import insert_canvas_toolbar 

class View():
    def save_parameter(self):
        #salvar_paramt
        img = pyscreenshot.grab(bbox=(0, 25, 1920, 1040))
        img.show()

        path = os.path.join(os.getcwd(), 'teste.png')  # Caminho atual
        img.save(path)

    def data_preview(self, score, mean_abs_error, mean_rel_error,
                 max_abs_error, exact_max, pred_max,
                 min_abs_error, exact_min, pred_min,
                 y_exact, y_pred, x_axis):
    
        print("\n--- Preview dos Resultados ---")
        print(f"Pontuação (0-100): {score} pts")
        print(f"Média Erro Absoluto: {round(mean_abs_error, 4)}")
        print(f"Média Erro Relativo: {round(mean_rel_error, 4)}")
        print(f"Maior Erro Absoluto: {round(max_abs_error, 4)}")
        print(f"  Valor Exato do Maior EA: {round(exact_max, 4)}")
        print(f"  Previsão do Maior EA: {round(pred_max, 4)}")
        print(f"Menor Erro Absoluto: {round(min_abs_error, 4)}")
        print(f"  Valor Exato do Menor EA: {round(exact_min, 4)}")
        print(f"  Previsão do Menor EA: {round(pred_min, 4)}")

        # Gerar gráfico com matplotlib puro
        plt.figure(figsize=(12, 7.3))
        plt.plot(x_axis, y_exact, label='Exato', color='green')
        plt.plot(x_axis, y_pred, label='Predict', color='red')
        plt.legend()
        plt.grid(True)
        plt.ylabel("Temperature(°C)")
        plt.xlabel("Comparações")
        plt.title("Comparação entre valores exatos e preditos")
        plt.show()

    def generate_preview_dt(self, master):
        prev = Training()
        save_model_flag = master.save_model

        # city = master.get_end(master.data_s.get())
        city = master.data_s
        indicator = master.ind_s
        split_percentage = int(master.por_trei)
        criterion = master.param_frame.criterion_v
        splitter = master.param_frame.splitter_v
        max_depth = int(master.param_frame.maxd_v)
        min_samples_split = master.int_float(master.param_frame.minsam_s_v)
        min_samples_leaf = master.int_float(master.param_frame.minsam_l_v)
        min_weight_fraction_leaf = float(master.param_frame.minweifra_l_v)
        max_features = master.valid_maxf(master.param_frame.maxfeat_v)
        max_leaf_nodes = int(master.param_frame.maxleaf_n)

        min_impurity_decrease = float(master.param_frame.minimp_dec)
        ccp_alpha = float(master.param_frame.ccp_alp_v)
        n_tests = int(master.num_teste)

        indicator = get_indicator_code(indicator)

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.decision_tree(
            city, indicator, split_percentage, criterion, splitter, max_depth,
            min_samples_leaf, max_features, max_leaf_nodes, n_tests, min_samples_split,
            min_weight_fraction_leaf, min_impurity_decrease, ccp_alpha, save_model_flag
        )
        self.data_preview(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )
    
    def generate_preview_bt(self, master):
        prev = Training()
        save_model_flag = master.save_model

        # city = master.get_end(master.data_s.get())
        city = master.data_s
        indicator = master.ind_s
        split_percentage = int(master.por_trei)
        criterion = master.param_frame.criterion_v
        splitter = master.param_frame.splitter_v
        max_depth = int(master.param_frame.maxd_v)
        min_samples_split = master.int_float(master.param_frame.minsam_s_v)
        min_samples_leaf = master.int_float(master.param_frame.minsam_l_v)
        min_weight_fraction_leaf = float(master.param_frame.minweifra_l_v)
        max_features = master.valid_maxf(master.param_frame.maxfeat_v)
        max_leaf_nodes = int(master.param_frame.maxleaf_n)

        min_impurity_decrease = float(master.param_frame.minimp_dec)
        ccp_alpha = float(master.param_frame.ccp_alp_v)
        n_tests = int(master.num_teste)
        n_estimators = int(master.n_estimators)

        indicator = get_indicator_code(indicator)

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.bagging_trees(
            city, indicator, split_percentage, criterion, splitter, max_depth,
            min_samples_leaf, max_features, max_leaf_nodes, n_tests, min_samples_split,
            min_weight_fraction_leaf, min_impurity_decrease, ccp_alpha, save_model_flag, n_estimators
        )
        self.data_preview(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )

    def generate_preview_nn(self, master):
        prev = Training()
        save_model_flag = master.save_model

        city = master.get_end(master.data_s)

        indicator = master.ind_s
        
        indicator = get_indicator_code(indicator)

        split_percentage = int(master.por_trei)

        activation = master.param_frame.activation_v
        solver = master.param_frame.solver_v
        alpha = float(master.param_frame.alpha_v)
        batch_size = master.param_frame.batch_size_v
        learning_rate = master.param_frame.learning_rate_v
        learning_rate_init = float(master.param_frame.learning_rate_init_v)
        power_t = float(master.param_frame.power_t_v)
        max_iter = int(master.param_frame.max_iter_v)
        shuffle = master.param_frame.shuffle_v
        tol = float(master.param_frame.tol_v)
        verbose = master.param_frame.verbose_v
        warm_start = master.param_frame.warm_start_v
        momentum = float(master.param_frame.momentum_v)
        nesterovs_momentum = master.param_frame.nesterovs_momentum_v
        early_stopping = master.param_frame.early_stopping_v
        validation_fraction = float(master.param_frame.validation_fraction_v)
        beta_1 = float(master.param_frame.beta_1_v)
        beta_2 = float(master.param_frame.beta_2_v)
        n_iter_no_change = int(master.param_frame.n_iter_no_change_v)
        max_fun = int(master.param_frame.max_fun_v)
        n_tests = int(master.num_teste)

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.neural_network(
            city, indicator, split_percentage, n_tests, activation, solver, alpha, batch_size,
            learning_rate, learning_rate_init, power_t, max_iter, shuffle, tol, verbose,
            warm_start, momentum, nesterovs_momentum, early_stopping, validation_fraction,
            beta_1, beta_2, n_iter_no_change, max_fun, save_model_flag
        )

        master.data_preview(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )

    def generate_preview_svm(self, master):
        prev = Training()
        save_model_flag = master.save_model

        city = master.get_end(master.data_s)

        indicator = master.ind_s
        indicator = get_indicator_code(indicator)

        split_percentage = int(master.por_trei)
        n_tests = int(master.num_teste)
        kernel = master.kernel_v
        degree = master.degree_v
        gamma = master.gamma_v
        coef0 = float(master.coef0_v)
        tol = float(master.tol_v)
        c_param = float(master.c_v)
        epsilon = float(master.epsilon_v)
        shrinking = master.shrinking_v
        cache_size = float(master.cache_size_v)
        verbose = master.verbose_v
        max_iter = int(master.maxiter_v)

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.support_vector_regression(
            city, indicator, split_percentage, n_tests, kernel, degree, gamma, coef0,
            tol, c_param, epsilon, shrinking, cache_size, verbose, max_iter, save_model_flag
        )

        master.data_preview(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )

    def generate_preview_kn(self, master):
        prev = Training()
        save_model_flag = master.save_model

        city = master.get_end(master.data_s)
        n_tests = int(master.num_teste)
        split_percentage = int(master.por_trei)
        n_neighbors = master.param_frame.n_neighbors_v
        algorithm = master.param_frame.algorithm_v
        leaf_size = master.param_frame.leaf_size_v
        p_value = master.param_frame.p_v
        n_jobs = master.param_frame.n_jobs_v

        if n_jobs.isdigit() == True:
            n_jobs = int(n_jobs)

        indicator = master.ind_s
        indicator = get_indicator_code(indicator)

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.KNeighbors(
            city, indicator, split_percentage, n_tests, n_neighbors, algorithm, leaf_size, p_value, n_jobs, save_model_flag
        )

        master.data_preview(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )

    def generate_param(self, master, option):
        if option == 'Decision Trees':
            decision_trees.generate_param(master)
        elif option == 'Bagged Trees':
            bagging_trees.generate_param(master)
        elif option == 'Neural network':
            neural_network.generate_param(master)
        elif option == 'Nearest Neighbors':
            nearest_neighbors.generate_param(master)
        elif option == 'Support Vector':
            support_vector.generate_param(master)
        elif option == 'Gaussian Process':
            gaussian_process.generate_param(master)