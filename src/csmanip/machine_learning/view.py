import os
import pyscreenshot
from ..training.training import Training
from tkinter import Label, LabelFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from . import decision_trees
from . import bagging_trees
from . import support_vector
from . import neural_network
from . import gaussian_process
from . import nearest_neighbors
from ..styles import colors
from ..utils.indicator import get_indicator_code
from ..utils.insert_canvas import insert_canvas_toolbar 

class View():
    def save_parameter(self):
        #salvar_paramt
        img = pyscreenshot.grab(bbox=(0, 25, 1920, 1040))
        img.show()

        path = os.path.join(os.getcwd(), 'teste.png')  # Caminho atual
        img.save(path)

    def data_preview(self, master, score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis):
        master.laf_res = LabelFrame(master, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=650, y=50)
        Label(master, text='Pontuação (0-100): ' + str(score) + 'pts', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=70)
        mean_abs_error = round(mean_abs_error, 4)
        Label(master, text='Média Erro absoluto: ' + str(mean_abs_error), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=100)
        mean_rel_error = round(mean_rel_error, 4)
        Label(master, text='Média Erro relativo: ' + str(mean_rel_error), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=130)

        Label(master, text='Maior erro absoluto: ' + str(round(max_abs_error, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=160)
        Label(master, text="Valor exato do maior EA: " + str(round(exact_max, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=940, y=160)
        Label(master, text="Predict do maior EA: " + str(round(pred_max, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=1200, y=160)

        Label(master, text='Menor erro absoluto: ' + str(round(min_abs_error, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=190)
        Label(master, text="Valor exato do menor EA: " + str(round(exact_min, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=940, y=190)
        Label(master, text="Predict do menor EA: " + str(round(pred_min, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=1200, y=190)

        figure = Figure(figsize=(12, 7.3), dpi=100)
        plot_r = figure.add_subplot(111)
        plot_r.plot(x_axis, y_exact, label='Exato', color='green')
        plot_r.plot(x_axis, y_pred, label='Predict', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperature(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figure, master=master)
        insert_canvas_toolbar(canvas, master)

    def generate_preview_dt(self, master):
        prev = Training()
        save_model_flag = master.save_model.get()

        # city = master.get_end(master.data_s.get())
        city = master.data_s.get()
        indicator = master.ind_s.get()
        split_percentage = int(master.por_trei.get())
        criterion = master.param_frame.criterion_v.get()
        splitter = master.param_frame.splitter_v.get()
        max_depth = int(master.param_frame.maxd_v.get())
        min_samples_split = master.int_float(master.param_frame.minsam_s_v.get())
        min_samples_leaf = master.int_float(master.param_frame.minsam_l_v.get())
        min_weight_fraction_leaf = float(master.param_frame.minweifra_l_v.get())
        max_features = master.valid_maxf(master.param_frame.maxfeat_v.get())
        max_leaf_nodes = int(master.param_frame.maxleaf_n.get())

        print("Max features ", max_features)
        
        min_impurity_decrease = float(master.param_frame.minimp_dec.get())
        ccp_alpha = float(master.param_frame.ccp_alp_v.get())
        n_tests = int(master.num_teste.get())

        indicator = get_indicator_code(indicator)

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.decision_tree(
            city, indicator, split_percentage, criterion, splitter, max_depth,
            min_samples_leaf, max_features, max_leaf_nodes, n_tests, min_samples_split,
            min_weight_fraction_leaf, min_impurity_decrease, ccp_alpha, save_model_flag
        )
        master.data_preview(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )

    def generate_preview_bt(self, master):
        prev = Training()
        save_model_flag = master.save_model.get()

        # city = master.get_end(master.data_s.get())
        city = master.data_s.get()
        indicator = master.ind_s.get()
        split_percentage = int(master.por_trei.get())
        criterion = master.param_frame.criterion_v.get()
        splitter = master.param_frame.splitter_v.get()
        max_depth = int(master.param_frame.maxd_v.get())
        min_samples_split = master.int_float(master.param_frame.minsam_s_v.get())
        min_samples_leaf = master.int_float(master.param_frame.minsam_l_v.get())
        min_weight_fraction_leaf = float(master.param_frame.minweifra_l_v.get())
        max_features = master.valid_maxf(master.param_frame.maxfeat_v.get())
        max_leaf_nodes = int(master.param_frame.maxleaf_n.get())

        print("Max features ", max_features)
        
        min_impurity_decrease = float(master.param_frame.minimp_dec.get())
        ccp_alpha = float(master.param_frame.ccp_alp_v.get())
        n_tests = int(master.num_teste.get())
        n_estimators = int(master.n_estimators.get())

        indicator = get_indicator_code(indicator)

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.bagging_trees(
            city, indicator, split_percentage, criterion, splitter, max_depth,
            min_samples_leaf, max_features, max_leaf_nodes, n_tests, min_samples_split,
            min_weight_fraction_leaf, min_impurity_decrease, ccp_alpha, save_model_flag
        )
        master.data_preview(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )

    def generate_preview_nn(self, master):
        prev = Training()
        save_model_flag = master.save_model.get()

        city = master.get_end(master.data_s.get())

        indicator = master.ind_s.get()
        
        indicator = get_indicator_code(indicator)

        split_percentage = int(master.por_trei.get())

        activation = master.param_frame.activation_v.get()
        solver = master.param_frame.solver_v.get()
        alpha = float(master.param_frame.alpha_v.get())
        batch_size = master.param_frame.batch_size_v.get()
        learning_rate = master.param_frame.learning_rate_v.get()
        learning_rate_init = float(master.param_frame.learning_rate_init_v.get())
        power_t = float(master.param_frame.power_t_v.get())
        max_iter = int(master.param_frame.max_iter_v.get())
        shuffle = master.param_frame.shuffle_v.get()
        tol = float(master.param_frame.tol_v.get())
        verbose = master.param_frame.verbose_v.get()
        warm_start = master.param_frame.warm_start_v.get()
        momentum = float(master.param_frame.momentum_v.get())
        nesterovs_momentum = master.param_frame.nesterovs_momentum_v.get()
        early_stopping = master.param_frame.early_stopping_v.get()
        validation_fraction = float(master.param_frame.validation_fraction_v.get())
        beta_1 = float(master.param_frame.beta_1_v.get())
        beta_2 = float(master.param_frame.beta_2_v.get())
        n_iter_no_change = int(master.param_frame.n_iter_no_change_v.get())
        max_fun = int(master.param_frame.max_fun_v.get())
        n_tests = int(master.num_teste.get())

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
        save_model_flag = master.save_model.get()

        city = master.get_end(master.data_s.get())

        indicator = master.ind_s.get()
        indicator = get_indicator_code(indicator)

        split_percentage = int(master.por_trei.get())
        n_tests = int(master.num_teste.get())
        kernel = master.kernel_v.get()
        degree = master.degree_v.get()
        gamma = master.gamma_v.get()
        coef0 = float(master.coef0_v.get())
        tol = float(master.tol_v.get())
        c_param = float(master.c_v.get())
        epsilon = float(master.epsilon_v.get())
        shrinking = master.shrinking_v.get()
        cache_size = float(master.cache_size_v.get())
        verbose = master.verbose_v.get()
        max_iter = int(master.maxiter_v.get())

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.support_vector_regression(
            city, indicator, split_percentage, n_tests, kernel, degree, gamma, coef0,
            tol, c_param, epsilon, shrinking, cache_size, verbose, max_iter, save_model_flag
        )

        master.data_preview(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )

    def generate_preview_GP(self, master):
        prev = Training()
        save_model_flag = master.save_model.get()

        city = master.get_end(master.data_s.get())
        n_tests = int(master.num_teste.get())
        split_percentage = int(master.por_trei.get())
        alpha_gp = master.param_frame.alpha_gp.get()
        kernel_type = master.kernel_type.get()
        normalize_y_gp = master.param_frame.normalize_y_gp.get()
        lenght_scale = master.param_frame.lenght_scale.get()
        nu = master.param_frame.nu.get()
        sigma_0 = master.param_frame.sigma_0.get()
        alpha_rq = master.param_frame.alpha_rq.get()
        n_restarts_op = master.param_frame.n_restarts_op.get()

        indicator = master.ind_s.get()
        indicator = get_indicator_code(indicator)

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.gaussian_process_regression(
            city, indicator, split_percentage, n_tests, kernel_type, lenght_scale, 
            nu, sigma_0, alpha_rq, alpha_gp, n_restarts_op, normalize_y_gp, save_model_flag
        )

        master.data_preview(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )


    def generate_preview_kn(self, master):
        prev = Training()
        save_model_flag = master.save_model.get()

        city = master.get_end(master.data_s.get())
        n_tests = int(master.num_teste.get())
        split_percentage = int(master.por_trei.get())
        n_neighbors = master.param_frame.n_neighbors_v.get()
        algorithm = master.param_frame.algorithm_v.get()
        leaf_size = master.param_frame.leaf_size_v.get()
        p_value = master.param_frame.p_v.get()
        n_jobs = master.param_frame.n_jobs_v.get()

        if n_jobs.isdigit() == True:
            n_jobs = int(n_jobs)

        indicator = master.ind_s.get()
        indicator = get_indicator_code(indicator)

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.KNeighbors(
            city, indicator, split_percentage, n_tests, n_neighbors, algorithm, leaf_size, p_value, n_jobs, save_model_flag
        )

        master.data_preview(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )

    def generate_param(self, master):
        opcao = master.ml_selected.get()
        if opcao == 'Decision Trees':
            decision_trees.generate_param(master)
        elif opcao == 'Bagged Trees':
            bagging_trees.generate_param(master)
        elif opcao == 'Neural network':
            neural_network.generate_param(master)
        elif opcao == 'Nearest Neighbors':
            nearest_neighbors.generate_param(master)
        elif opcao == 'Support Vector':
            support_vector.generate_param(master)
        elif opcao == 'Gaussian Process':
            gaussian_process.generate_param(master)