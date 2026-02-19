import matplotlib.pyplot as plt
from ..training.training import Training
from ..utils.indicator import get_indicator_code
from ..utils.ml_param import get_parameters_ml
from ..utils.insert_canvas import insert_canvas_toolbar

class View:
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

    def generate_preview_dt(self):
        prev = Training()
        salvar_m = self.save_model
        
        #cidade = self.get_end(self.data_s.get())
        cidade = self.data_s
        indicator = self.ind_s
        divisao = int(self.por_trei)
        criterio = self.criterion_v
        splitter = self.splitter_v
        maxd = int(self.maxd_v)             #* Max_depth
        minsams = self.int_float(self.minsam_s_v)    #* Min_samples_split
        minsaml = self.int_float(self.minsam_l_v)    #* Min_samples_leaf
        minwei = float(self.minweifra_l_v)
        maxfe = self.valid_maxf(self.maxfeat_v)
        maxleaf = int(self.maxleaf_n)
        
        minim = float(self.minimp_dec)
        ccp = float(self.ccp_alp_v)
        n_tes = int(self.num_teste)

        indicator = get_indicator_code(indicator)

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.decision_tree(cidade, indicator, divisao, criterio, splitter, maxd, minsaml, maxfe, maxleaf, n_tes, minsams, minwei, minim, ccp, salvar_m)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)

    def generate_preview_bt(self):
        prev = Training()
        salvar_m = self.save_model
        
        #cidade = self.get_end(self.data_s.get())
        cidade = self.data_s
        indicator = self.ind_s
        divisao = int(self.por_trei)
        criterio = self.criterion_v
        splitter = self.splitter_v
        maxd = int(self.maxd_v)             #* Max_depth
        minsams = self.int_float(self.minsam_s_v)    #* Min_samples_split
        minsaml = self.int_float(self.minsam_l_v)    #* Min_samples_leaf
        minwei = float(self.minweifra_l_v)
        maxfe = self.valid_maxf(self.maxfeat_v)
        maxleaf = int(self.maxleaf_n)
        
        minim = float(self.minimp_dec)
        ccp = float(self.ccp_alp_v)
        n_tes = int(self.num_teste)
        n_estimators = int(self.n_estimators)

        indicator = get_indicator_code(indicator)

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.decision_tree(cidade, indicator, divisao, criterio, splitter, maxd, minsaml, maxfe, maxleaf, n_tes, minsams, minwei, minim, ccp, salvar_m, n_estimators)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)


    def generate_preview_nn(self):
        prev = Training()
        salvar_m = self.save_model
        
        cidade = self.get_end(self.data_s)
        
        indicator = self.ind_s
        indicator = get_indicator_code(indicator)
    
        divisao = int(self.por_trei)

        activ = self.activation_v
        solv = self.solver_v
        alph = float(self.alpha_v)
        batc = self.batch_size_v
        learn_r = self.learning_rate_v
        learn_r_ini = float(self.learning_rate_init_v)
        powt = float(self.power_t_v)
        maxit = int(self.max_iter_v)
        shuf = self.shuffle_v
        tol = float(self.tol_v)
        verb = self.verbose_v
        warms = self.warm_start_v
        moment = float(self.momentum_v)
        neste = self.nesterovs_momentum_v
        earlyst = self.early_stopping_v
        valid = float(self.validation_fraction_v)
        b1 = float(self.beta_1_v)
        b2 = float(self.beta_2_v)
        niter = int(self.n_iter_no_change_v)
        maxfun = int(self.max_fun_v)
        n_teste = int(self.num_teste)
        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.RedeNeural(cidade, indicator, divisao, n_teste, activ, solv, alph, batc, learn_r, learn_r_ini, powt, maxit, shuf, tol, verb, warms, moment, neste, earlyst, valid, b1, b2, niter, maxfun, salvar_m)

        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)
  
    def generate_preview_svm(self):
        prev = Training()
        salvar_m = self.save_model
        
        cidade = self.get_end(self.data_s)
        
        indicator = self.ind_s
        indicator = get_indicator_code(indicator)
    
        divisao = int(self.por_trei)
        n_teste = int(self.num_teste)
        kern = self.kernel_v
        degre = self.degree_v
        gam = self.gamma_v
        coef = float(self.coef0_v)
        t = float(self.tol_v)
        c = float(self.c_v)
        eps = float(self.epsilon_v)
        shr = self.shrinking_v
        cach = float(self.cache_size_v)
        verb = self.verbose_v
        maxi = int(self.maxiter_v)


        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.SVR(cidade, indicator, divisao, n_teste, kern, degre, gam, coef, t, c, eps, shr, cach, verb, maxi, salvar_m)

        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)
      
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
            
        indicator = self.ind_s
        indicator = get_indicator_code(indicator)

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = \
            prev.KNeighbors(cidade, indicator, divisao, n_tes, n_neig, algor, leaf_s, pv, n_job, salvar_m)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)
