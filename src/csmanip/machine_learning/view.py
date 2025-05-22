import os
import pyscreenshot
from training.training import Training
from tkinter import Label, LabelFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from machine_learning import decision_trees
from machine_learning import nearest_neighbors
from machine_learning import neural_network
from machine_learning import gaussian_process
from machine_learning import support_vector
from styles import colors
from utils.indicator import get_indicator_code
from utils.ml_param import get_parameters_ml
from utils.insert_canvas import insert_canvas_toolbar 

class View():
    def save_parameter(self):
        #salvar_paramt
        img = pyscreenshot.grab(bbox=(0, 25, 1920, 1040))
        img.show()

        path = os.path.join(os.getcwd(), 'teste.png')  # Caminho atual
        img.save(path)

    def data_preview(self, score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis):
        self.laf_res = LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=650, y=50)
        Label(self, text='Pontuação (0-100): ' + str(score) + 'pts', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=70)
        mean_abs_error = round(mean_abs_error, 4)
        Label(self, text='Média Erro absoluto: ' + str(mean_abs_error), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=100)
        mean_rel_error = round(mean_rel_error, 4)
        Label(self, text='Média Erro relativo: ' + str(mean_rel_error), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=130)

        Label(self, text='Maior erro absoluto: ' + str(round(max_abs_error, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exact_max, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pred_max, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(min_abs_error, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exact_min, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pred_min, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=1200, y=190)

        figure = Figure(figsize=(12, 7.3), dpi=100)
        plot_r = figure.add_subplot(111)
        plot_r.plot(x_axis, y_exact, label='Exato', color='green')
        plot_r.plot(x_axis, y_pred, label='Predict', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figure, master=self)
        insert_canvas_toolbar(canvas, self)

    def generate_preview_dt(self):
        prev = Training()
        save_model_flag = self.save_model.get()

        # city = self.get_end(self.data_s.get())
        city = self.data_s.get()
        indicator = self.ind_s.get()
        split_percentage = int(self.por_trei.get())
        criterion = self.criterion_v.get()
        splitter = self.splitter_v.get()
        max_depth = int(self.maxd_v.get())
        min_samples_split = self.int_float(self.minsam_s_v.get())
        min_samples_leaf = self.int_float(self.minsam_l_v.get())
        min_weight_fraction_leaf = float(self.minweifra_l_v.get())
        max_features = self.valid_maxf(self.maxfeat_v.get())
        max_leaf_nodes = int(self.maxleaf_n.get())
        
        min_impurity_decrease = float(self.minimp_dec.get())
        ccp_alpha = float(self.ccp_alp_v.get())
        n_tests = int(self.num_teste.get())

        indicator = get_indicator_code(indicator)

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.decision_tree(
            city, indicator, split_percentage, criterion, splitter, max_depth,
            min_samples_leaf, max_features, max_leaf_nodes, n_tests, min_samples_split,
            min_weight_fraction_leaf, min_impurity_decrease, ccp_alpha, save_model_flag
        )
        self.data_prev(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )

    def generate_preview_nn(self):
        prev = Training()
        save_model_flag = self.save_model.get()

        city = self.get_end(self.data_s.get())

        indicator = self.ind_s.get()
        
        indicator = get_indicator_code(indicator)

        split_percentage = int(self.por_trei.get())

        activation = self.activation_v.get()
        solver = self.solver_v.get()
        alpha = float(self.alpha_v.get())
        batch_size = self.batch_size_v.get()
        learning_rate = self.learning_rate_v.get()
        learning_rate_init = float(self.learning_rate_init_v.get())
        power_t = float(self.power_t_v.get())
        max_iter = int(self.max_iter_v.get())
        shuffle = self.shuffle_v.get()
        tol = float(self.tol_v.get())
        verbose = self.verbose_v.get()
        warm_start = self.warm_start_v.get()
        momentum = float(self.momentum_v.get())
        nesterovs_momentum = self.nesterovs_momentum_v.get()
        early_stopping = self.early_stopping_v.get()
        validation_fraction = float(self.validation_fraction_v.get())
        beta_1 = float(self.beta_1_v.get())
        beta_2 = float(self.beta_2_v.get())
        n_iter_no_change = int(self.n_iter_no_change_v.get())
        max_fun = int(self.max_fun_v.get())
        n_tests = int(self.num_teste.get())

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.neural_network(
            city, indicator, split_percentage, n_tests, activation, solver, alpha, batch_size,
            learning_rate, learning_rate_init, power_t, max_iter, shuffle, tol, verbose,
            warm_start, momentum, nesterovs_momentum, early_stopping, validation_fraction,
            beta_1, beta_2, n_iter_no_change, max_fun, save_model_flag
        )

        self.data_prev(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )

    def generate_preview_svm(self):
        prev = Training()
        save_model_flag = self.save_model.get()

        city = self.get_end(self.data_s.get())

        indicator = self.ind_s.get()
        indicator = get_indicator_code(indicator)

        split_percentage = int(self.por_trei.get())
        n_tests = int(self.num_teste.get())
        kernel = self.kernel_v.get()
        degree = self.degree_v.get()
        gamma = self.gamma_v.get()
        coef0 = float(self.coef0_v.get())
        tol = float(self.tol_v.get())
        c_param = float(self.c_v.get())
        epsilon = float(self.epsilon_v.get())
        shrinking = self.shrinking_v.get()
        cache_size = float(self.cache_size_v.get())
        verbose = self.verbose_v.get()
        max_iter = int(self.maxiter_v.get())

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.support_vector_regression(
            city, indicator, split_percentage, n_tests, kernel, degree, gamma, coef0,
            tol, c_param, epsilon, shrinking, cache_size, verbose, max_iter, save_model_flag
        )

        self.data_prev(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )

    def generate_preview_kn(self):
        prev = Training()
        save_model_flag = self.save_model.get()

        city = self.get_end(self.data_s.get())
        n_tests = int(self.num_teste.get())
        split_percentage = int(self.por_trei.get())
        n_neighbors = self.n_neighbors_v.get()
        algorithm = self.algorithm_v.get()
        leaf_size = self.leaf_size_v.get()
        p_value = self.p_v.get()
        n_jobs = self.n_jobs_v.get()

        if n_jobs.isdigit() == True:
            n_jobs = int(n_jobs)

        indicator = self.ind_s.get()
        indicator = get_indicator_code(indicator)

        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.KNeighbors(
            city, indicator, split_percentage, n_tests, n_neighbors, algorithm, leaf_size, p_value, n_jobs, save_model_flag
        )

        self.data_prev(
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max,
            min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis
        )

    def generate_preview_Kn(self):
        prev = Training()
        parameters = get_parameters_ml(self)

        cidade = parameters["cidade"]
        salvar_m = parameters["save_model"]
        n_tes = parameters["num_testes"]
        divisao = parameters["porcentagem_treinamento"]
        n_neig = parameters["n_neighbors"]
        algor = parameters["algorithm"]
        leaf_s = parameters["leaf_size"]
        pv = parameters["p_v"]
        n_job = parameters["n_jobs"]
            
        indicador = self.ind_s.get()
        indicator = get_indicator_code(indicator)

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.KNeighbors(cidade, indicador, divisao, n_tes, n_neig, algor, leaf_s, pv, n_job, salvar_m)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)

    def generate_param(self):
        opcao = self.ml_selected.get()
        if opcao == 'Decision Trees':
            decision_trees.generate_param(self)
        elif opcao == 'Neural network':
            neural_network.generate_param(self)
        elif opcao == 'Nearest Neighbors':
            nearest_neighbors.generate_param(self)
        elif opcao == 'Support Vector':
            support_vector.generate_param(self)
        elif opcao == 'Gaussian Process':
            gaussian_process.generate_param(self)