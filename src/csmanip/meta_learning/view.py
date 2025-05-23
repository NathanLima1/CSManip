from tkinter import Canvas, Label, LabelFrame, StringVar, IntVar, BooleanVar, Entry, Scale, Checkbutton, Button, HORIZONTAL, CENTER
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ..training.training import Training
from ..styles import colors
from ..utils.indicator import get_indicator_code
from ..utils.ml_param import get_parameters_ml
from ..utils.insert_canvas import insert_canvas_toolbar

class View:
    def data_preview(self, pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x):
        self.laf_res = LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=650, y=50)
        Label(self, text='Pontuação (0-100): '+ str(pts) +'pts', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=70)
        media_ea = round(media_ea, 4)
        Label(self, text='Média Erro absoluto: '+ str(media_ea), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=100)
        media_er = round(media_er, 4)
        Label(self, text='Média Erro relativo: '+ str(media_er), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=130)

        Label(self, text='Maior erro absoluto: ' + str(round(maior_ea,4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exat_maior,4)),font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pre_maior, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(menor_ea,4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exat_menor,4)),font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pre_menor, 4)), font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=1200, y=190)

        figura = Figure(figsize=(12,7.3), dpi=100)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_predict, label='Predict', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figura, master=self)
        insert_canvas_toolbar(canvas, self)

    def generate_preview_dt(self):
        prev = Training()
        salvar_m = self.save_model.get()
        
        #cidade = self.get_end(self.data_s.get())
        cidade = self.data_s.get()
        indicator = self.ind_s.get()
        divisao = int(self.por_trei.get())
        criterio = self.criterion_v.get()
        splitter = self.splitter_v.get()
        maxd = int(self.maxd_v.get())             #* Max_depth
        minsams = self.int_float(self.minsam_s_v.get())    #* Min_samples_split
        minsaml = self.int_float(self.minsam_l_v.get())    #* Min_samples_leaf
        minwei = float(self.minweifra_l_v.get())
        maxfe = self.valid_maxf(self.maxfeat_v.get())
        maxleaf = int(self.maxleaf_n.get())
        
        minim = float(self.minimp_dec.get())
        ccp = float(self.ccp_alp_v.get())
        n_tes = int(self.num_teste.get())

        indicator = get_indicator_code(indicator)

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.ArvoreDecisao(cidade, indicator, divisao, criterio, splitter, maxd, minsaml, maxfe, maxleaf, n_tes, minsams, minwei, minim, ccp, salvar_m)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)

    def generate_preview_nn(self):
        prev = Training()
        salvar_m = self.save_model.get()
        
        cidade = self.get_end(self.data_s.get())
        
        indicator = self.ind_s.get()
        indicator = get_indicator_code(indicator)
    
        divisao = int(self.por_trei.get())

        activ = self.activation_v.get()
        solv = self.solver_v.get()
        alph = float(self.alpha_v.get())
        batc = self.batch_size_v.get()
        learn_r = self.learning_rate_v.get()
        learn_r_ini = float(self.learning_rate_init_v.get())
        powt = float(self.power_t_v.get())
        maxit = int(self.max_iter_v.get())
        shuf = self.shuffle_v.get()
        tol = float(self.tol_v.get())
        verb = self.verbose_v.get()
        warms = self.warm_start_v.get()
        moment = float(self.momentum_v.get())
        neste = self.nesterovs_momentum_v.get()
        earlyst = self.early_stopping_v.get()
        valid = float(self.validation_fraction_v.get())
        b1 = float(self.beta_1_v.get())
        b2 = float(self.beta_2_v.get())
        niter = int(self.n_iter_no_change_v.get())
        maxfun = int(self.max_fun_v.get())
        n_teste = int(self.num_teste.get())
        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.RedeNeural(cidade, indicator, divisao, n_teste, activ, solv, alph, batc, learn_r, learn_r_ini, powt, maxit, shuf, tol, verb, warms, moment, neste, earlyst, valid, b1, b2, niter, maxfun, salvar_m)

        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)
  
    def generate_preview_svm(self):
        prev = Training()
        salvar_m = self.save_model.get()
        
        cidade = self.get_end(self.data_s.get())
        
        indicator = self.ind_s.get()
        indicator = get_indicator_code(indicator)
    
        divisao = int(self.por_trei.get())
        n_teste = int(self.num_teste.get())
        kern = self.kernel_v.get()
        degre = self.degree_v.get()
        gam = self.gamma_v.get()
        coef = float(self.coef0_v.get())
        t = float(self.tol_v.get())
        c = float(self.c_v.get())
        eps = float(self.epsilon_v.get())
        shr = self.shrinking_v.get()
        cach = float(self.cache_size_v.get())
        verb = self.verbose_v.get()
        maxi = int(self.maxiter_v.get())


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
            
        indicator = self.ind_s.get()
        indicator = get_indicator_code(indicator)

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = \
            prev.KNeighbors(cidade, indicator, divisao, n_tes, n_neig, algor, leaf_s, pv, n_job, salvar_m)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)
