import tkinter as tk
from tkinter import ttk, messagebox as msg, filedialog
from tkinter.scrolledtext import ScrolledText
import typing
import os
import sys
import optuna
import functools
import logging
from ...tooltip import CreateToolTip
import threading
import json

from ....training.training import Training
from ....utils.indicator import get_indicator_code 
from .optuna_popup import OptunaPopup

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

if typing.TYPE_CHECKING:
    from ...start_page import StartPage 
    from .gui_helpers import DTParameterFrame, BaggingTParameterFrame, NNParameterFrame, NNeighParameterFrame, SVMParameterFrame, GPParameterFrame

class TextHandler(logging.Handler):
    """
    Classe customizada para redirecionar logs para um widget ScrolledText do Tkinter.
    """
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.see(tk.END)
        
        self.text_widget.after(0, append)

class MachineLearningPage(ttk.Frame):
    """Tela para treinamento e visualização de modelos de Machine Learning."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        i18n = controller.i18n

        # --- Variáveis de Controle ---
        self.split_var = tk.StringVar(value="70")
        self.tests_var = tk.StringVar(value="10")
        self.save_model_var = tk.BooleanVar(value=False)
        self.optuna_trials_var = tk.StringVar(value="10")
        self.current_param_frame = None

        # --- Frame Superior ---
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        self.back_button = ttk.Button(top_frame, text="", command=self.go_to_previous_page)
        self.back_button.pack(side=tk.LEFT)
        self.page_title = ttk.Label(top_frame, text="", font=("Verdana", 16, "bold"))
        self.page_title.pack(side=tk.LEFT, expand=True)

        # --- Layout Principal ---
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_container.grid_columnconfigure(0, weight=1, minsize=300)
        main_container.grid_columnconfigure(1, weight=3)
        main_container.grid_rowconfigure(0, weight=1)

        # --- PAINEL ESQUERDO ---
        left_panel_base = ttk.Frame(main_container)
        left_panel_base.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_panel_base.grid_rowconfigure(0, weight=1)
        left_panel_base.grid_columnconfigure(0, weight=1)

        self.canvas_left = tk.Canvas(left_panel_base)
        self.canvas_left.grid(row=0, column=0, sticky="nsew")

        scrollbar_left = ttk.Scrollbar(left_panel_base, orient="vertical", command=self.canvas_left.yview)
        scrollbar_left.grid(row=0, column=1, sticky="ns")
        self.canvas_left.configure(yscrollcommand=scrollbar_left.set)

        self.scrollable_frame_left = ttk.Frame(self.canvas_left)

        self.canvas_left.create_window((0, 0), window=self.scrollable_frame_left, anchor="nw")

        self.scrollable_frame_left.bind(
            "<Configure>",
            lambda e: self.canvas_left.configure(
                scrollregion=self.canvas_left.bbox("all")
            )
        )

        self.canvas_left.bind_all("<MouseWheel>", self._on_mousewheel) # Linux/Windows
        self.canvas_left.bind_all("<Button-4>", self._on_mousewheel) # Linux scroll up
        self.canvas_left.bind_all("<Button-5>", self._on_mousewheel) # Linux scroll down

        # --- Configurações Gerais ---
        general_frame = ttk.LabelFrame(self.scrollable_frame_left, text="")
        general_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        self.general_frame_label = general_frame

        self.data_label = ttk.Label(general_frame, text="")
        self.data_label.pack(anchor="w", padx=5)
        self.data_combo = ttk.Combobox(general_frame, state="readonly", values=["Target", "Neighbor A", "Neighbor B", "Neighbor C"])
        self.data_combo.pack(fill=tk.X, padx=5, pady=(0, 5))
        self.data_combo_hint = CreateToolTip(self.data_combo, text=i18n.get('data_MaL_hint'))

        self.indicator_label = ttk.Label(general_frame, text="")
        self.indicator_label.pack(anchor="w", padx=5)
        self.indicator_combo = ttk.Combobox(general_frame, state="readonly", values=["Precipitation", "Maximum temperature", "Minimum temperature"])
        self.indicator_combo.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.indicator_combo_hint = CreateToolTip(self.indicator_combo, text=i18n.get('param_MaL_hint'))

        self.training_percentage_label = ttk.Label(general_frame, text="")
        self.training_percentage_label.pack(anchor="w", padx=5)
        self.split_entry = ttk.Entry(general_frame, textvariable=self.split_var)
        self.split_entry.pack(fill=tk.X, padx=5, pady=(0, 5))
        self.split_entry_hint = CreateToolTip(self.split_entry, text=i18n.get('train_percent_MaL_hint'))

        self.number_tests_label = ttk.Label(general_frame, text="")
        self.number_tests_label.pack(anchor="w", padx=5)
        self.tests_entry = ttk.Entry(general_frame, textvariable=self.tests_var)
        self.tests_entry.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.tests_entry_hint = CreateToolTip(self.tests_entry, text=i18n.get('number_tests_MaL_hint'))

        self.save_model_check = ttk.Checkbutton(general_frame, text="", variable=self.save_model_var)
        self.save_model_check.pack(anchor="w", padx=5, pady=(0, 5))

        # --- Seleção do Modelo ---
        model_frame = ttk.LabelFrame(self.scrollable_frame_left, text="")
        model_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        self.model_frame_label = model_frame

        self.model_label = ttk.Label(model_frame, text="")
        self.model_label.pack(anchor="w", padx=5)
        model_list = ['Decision Trees', 'Bagged Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        self.ml_combo = ttk.Combobox(model_frame, state="readonly", values=model_list)
        self.ml_combo.pack(fill=tk.X, padx=5, pady=(0, 5))
        self.ml_combo_hint = CreateToolTip(self.ml_combo, text=i18n.get('model_MaL_hint'))
        self.ml_combo.bind("<<ComboboxSelected>>", self.generate_param_ui)

        # --- Parâmetros do Modelo ---
        self.param_container = ttk.LabelFrame(self.scrollable_frame_left, text="")
        self.param_container.pack(fill=tk.X, pady=(0, 10), padx=5)

        """
        self.optuna_trials_label = ttk.Label(self.scrollable_frame_left, text="")
        self.optuna_trials_label.pack(anchor="w", padx=5, pady=(10, 0))

        self.optuna_trials_entry = ttk.Entry(self.scrollable_frame_left, textvariable=self.optuna_trials_var)
        self.optuna_trials_entry.pack(fill=tk.X, padx=5, pady=(0, 5))
        self.optuna_trials_hint = CreateToolTip(self.optuna_trials_entry, text=i18n.get("optuna_trials_MaL_hint"))
        """
        self.optuna_btn = ttk.Button(self.scrollable_frame_left, 
                                     text="", 
                                     command=self.run_optuna_optimization)
        self.optuna_btn.pack(fill=tk.X, pady=(10, 0), padx=5)
        self.optuna_btn_hint = CreateToolTip(self.optuna_btn, text=i18n.get('optuna_MaL_hint'))

        manage_frame = ttk.Frame(self.scrollable_frame_left)
        manage_frame.pack(fill=tk.X, pady=5, padx=5)

        self.btn_save_params = ttk.Button(manage_frame, text="Salvar Params", command=self.save_hyperparameters)
        self.btn_save_params.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        
        self.btn_save_params.config(state="disabled") 

        self.btn_load_params = ttk.Button(manage_frame, text="Carregar Params", command=self.load_hyperparameters)
        self.btn_load_params.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))

        self.last_best_params = None

        # --- Executar ---
        self.run_btn = ttk.Button(self.scrollable_frame_left, text="", command=self.run_model_preview)
        self.run_btn.pack(fill=tk.X, pady=10, padx=5)
        self.run_btn_hint = CreateToolTip(self.run_btn  , text=i18n.get('generate_prev_MaL_hint'))

        # --- PAINEL DIREITO ---
        self.right_panel = ttk.Frame(main_container, relief="solid", borderwidth=1)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self.update_texts() # Chama para definir os textos iniciais

    def _on_mousewheel(self, event):
        """Função para habilitar scroll com a roda do mouse."""
        # Determina a direção e a quantidade do scroll
        if event.num == 4 or event.delta > 0: # Linux scroll up ou Windows/macOS scroll up
            self.canvas_left.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0: # Linux scroll down ou Windows/macOS scroll down
            self.canvas_left.yview_scroll(1, "units")

    def go_to_previous_page(self):
        """Importa e navega para a página anterior."""
        from ..imputation_techniques_page import ImputationTechniquesPage
        self.controller.show_frame(ImputationTechniquesPage)

    def _clear_panel(self, panel):
        """Remove todos os widgets de um painel."""
        for widget in panel.winfo_children():
            widget.destroy()

    def update_texts(self):
        """Atualiza os textos estáticos da tela."""
        i18n = self.controller.i18n
        self.back_button.config(text=i18n.get('back_btn'))
        self.page_title.config(text=i18n.get('ml_page_title'))
        self.general_frame_label.config(text=i18n.get('general_settings_label'))
        self.save_model_check.config(text=i18n.get('save_model_label'))
        self.model_frame_label.config(text=i18n.get('model_selection_label'))
        self.param_container.config(text=i18n.get('model_parameters_label'))
        self.run_btn.config(text=i18n.get('run_prediction_btn'))
        self.data_label.config(text=i18n.get('data_label'))
        self.indicator_label.config(text=i18n.get('parameter_label'))
        self.model_label.config(text=i18n.get('model_label'))
        self.number_tests_label.config(text=i18n.get('number_tests_label'))
        self.training_percentage_label.config(text=i18n.get('training_percentage_label'))
        self.optuna_btn.config(text=i18n.get('param_optimizer_btn'))
        #self.optuna_trials_label.config(text="Número de tentativas")
        self.data_combo_hint.text = i18n.get('data_MaL_hint')
        self.indicator_combo_hint.text = i18n.get('param_MaL_hint')
        self.split_entry_hint.text = i18n.get('train_percent_MaL_hint')
        self.tests_entry_hint.text = i18n.get('number_tests_MaL_hint')
        self.ml_combo_hint.text = i18n.get('model_MaL_hint')
        #self.optuna_trials_hint.text = i18n.get('optuna_trials_MaL_hint')
        self.optuna_btn_hint.text = i18n.get('optuna_MaL_hint')
        self.optuna_btn_hint.text = i18n.get('generate_prev_MaL_hint')

    def _setup_log_view(self):
        """Prepara o painel direito para exibir logs."""
        self._clear_panel(self.right_panel)
        
        lbl = ttk.Label(self.right_panel, text="Progresso da Otimização (Optuna):", font=("Arial", 10, "bold"))
        lbl.pack(anchor="w", padx=10, pady=(10, 5))
        
        log_text = ScrolledText(self.right_panel, state='disabled', height=20)
        log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        return log_text

    def run_optuna_optimization(self):
        model_name = self.ml_combo.get()
        
        if not model_name:
            self.controller.show_translated_message(
                 msg_type='warning',
                 title_key='warning_title',
                 message_key='select_ml_model_msg'
             )
            return
        
        if self._get_common_params() is None:
            return

        OptunaPopup(self, self.controller, callback=self._execute_optuna_optimization)


    def _execute_optuna_optimization(self, n_trials):
        model_name = self.ml_combo.get()
        common_params = self._get_common_params()
        
        objective_mapping = {
            'Decision Trees': self.objective_dt,
            'Bagged Trees': self.objective_bt,
            'Neural network': self.objective_nn,
            'Nearest Neighbors': self.objective_kn,
            'Support Vector': self.objective_svm,
            'Gaussian Process': self.objective_gp,
        }

        base_objective = objective_mapping.get(model_name)
        if base_objective is None:
            return

        log_widget = self._setup_log_view()
        
        optuna.logging.set_verbosity(optuna.logging.INFO)
        optuna_logger = optuna.logging.get_logger("optuna")
        
        handler = TextHandler(log_widget)
        handler.setFormatter(logging.Formatter('%(message)s'))
        optuna_logger.addHandler(handler)

        def run_optimization_thread():
            try:
                objective_func = functools.partial(base_objective, common_params=common_params)
                
                study = optuna.create_study(direction='maximize')
                study.optimize(objective_func, n_trials=n_trials)

                best_params = study.best_params
                best_value = study.best_value

                self.controller.after(0, lambda: self._on_optimization_finished(best_params, best_value, optuna_logger, handler))

            except Exception as e:
                self.controller.after(0, lambda: self.controller.show_translated_message(
                    msg_type='error', 
                    title_key='optimization_error_title', 
                    message_key='optimization_error_msg', 
                    error=str(e)
                ))
                self.controller.after(0, lambda: optuna_logger.removeHandler(handler))

        threading.Thread(target=run_optimization_thread, daemon=True).start()

    def _on_optimization_finished(self, best_params, best_value, logger, handler):
        """Chamado quando a thread termina com sucesso."""
        
        logger.removeHandler(handler)

        self.last_best_params = best_params
        self.btn_save_params.config(state="normal")
        
        self.update_ui_with_params(best_params)

        self.controller.show_translated_message(
            msg_type='info',
            title_key='optimization_complete_title',
            message_key='optimization_complete_msg',
            best_score=f"{best_value:.4f}",
            params=str(best_params)
        )
    def update_ui_with_params(self, best_params):
        """
        Preenche os campos da UI (Entry, Combobox) com os 
        parâmetros do dicionário 'best_params' do Optuna.
        """

        if not self.current_param_frame:
            return
        
        param_map = {
            # Decision Trees / Bagging
            'criterion': 'criterion_v',
            'splitter': 'splitter_v',
            'max_depth': 'maxd_v',
            'min_samples_split': 'minsam_s_v',
            'min_samples_leaf': 'minsam_l_v',
            'min_weight_fraction_leaf': 'minweifra_l_v',
            'max_features': 'maxfeat_v',
            'max_leaf_nodes': 'maxleaf_n',
            'min_impurity_decrease': 'minimp_dec',
            'ccp_alpha': 'ccp_alp_v',
            # Bagging (nomeado diferente para evitar colisão)
            'n_estimators_bag': 'n_estimators', 
            # Neural Network
            'activation': 'activation_v',
            'solver': 'solver_v',
            'alpha': 'alpha_v',
            'batch_size': 'batch_size_v',
            'learning_rate': 'learning_rate_v',
            'learning_rate_init': 'learning_rate_init_v',
            'max_iter': 'max_iter_v',
            'momentum': 'momentum_v',
            # Nearest Neighbors
            'n_neighbors': 'n_neighbors_v',
            'algorithm': 'algorithm_v',
            'leaf_size': 'leaf_size_v',
            'p_value': 'p_v',
            # SVM
            'kernel': 'kernel_v',
            'degree': 'degree_v',
            'gamma': 'gamma_v',
            'c_param': 'c_v',
            'epsilon': 'epsilon_v',
            # Gaussian Process
            'alpha_gp': 'alpha_gp',
            'length_scale': 'length_scale',
            'nu': 'nu',
            'sigma_0': 'sigma_0',
            'alpha_rq': 'alpha_rq',
        }

        for param_name, widget_var_name in param_map.items():
            if param_name in best_params:
                if hasattr(self.current_param_frame, widget_var_name):
                    widget_var = getattr(self.current_param_frame, widget_var_name)
                    widget_var.set(str(best_params[param_name]))
                else:
                    print(f"Aviso: Parâmetro '{param_name}' encontrado, mas UI var '{widget_var_name}' não existe no frame atual.")

    def save_hyperparameters(self):
        """Salva os últimos parâmetros otimizados em um arquivo JSON."""
        if not self.last_best_params:
            return

        model_name = self.ml_combo.get().replace(" ", "_")
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"params_{model_name}.json",
            title="Salvar Hiperparâmetros"
        )

        if file_path:
            try:
                data_to_save = {
                    "model": self.ml_combo.get(),
                    "params": self.last_best_params
                }
                
                with open(file_path, 'w') as f:
                    json.dump(data_to_save, f, indent=4)
                
                msg.showinfo("Sucesso", "Parâmetros salvos com sucesso!")
            except Exception as e:
                msg.showerror("Erro", f"Falha ao salvar arquivo: {str(e)}")

    def load_hyperparameters(self):
        """Carrega parâmetros de um arquivo JSON e preenche a UI."""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Carregar Hiperparâmetros"
        )

        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                if "params" in data:
                    params_to_load = data["params"]
                    model_saved = data.get("model", "Desconhecido")
                    
                    current_model = self.ml_combo.get()
                    if model_saved != "Desconhecido" and model_saved != current_model:
                        confirm = msg.askyesno(
                            "Modelo Diferente", 
                            f"Estes parâmetros foram salvos para '{model_saved}', "
                            f"mas o modelo atual é '{current_model}'.\n\nDeseja carregar mesmo assim?"
                        )
                        if not confirm:
                            return

                else:
                    params_to_load = data

                self.update_ui_with_params(params_to_load)
                
                self.last_best_params = params_to_load
                self.btn_save_params.config(state="normal")

                msg.showinfo("Sucesso", "Parâmetros carregados na interface!")

            except json.JSONDecodeError:
                msg.showerror("Erro", "O arquivo selecionado não é um JSON válido.")
            except Exception as e:
                msg.showerror("Erro", f"Falha ao ler arquivo: {str(e)}")

    def objective_dt(self, trial, common_params):
        """Função objetivo para Decision Trees"""
        city_path, indicator, split_percentage, n_tests, save_model_flag = common_params
        
        criterion = trial.suggest_categorical('criterion', ['squared_error', 'absolute_error'])
        splitter = trial.suggest_categorical('splitter', ['best', 'random'])
        max_depth = trial.suggest_int('max_depth', 5, 50)
        min_samples_split = trial.suggest_int('min_samples_split', 2, 20)
        min_samples_leaf = trial.suggest_int('min_samples_leaf', 1, 20)
        max_features = trial.suggest_float('max_features', 0.5, 1.0)
        
        min_weight_fraction_leaf = 0.0 
        
        min_impurity_decrease = trial.suggest_float('min_impurity_decrease', 0.0, 0.01)
        
        ccp_alpha = trial.suggest_float('ccp_alpha', 1e-5, 0.005, log=True)

        prev = Training()
        score, *_ = prev.decision_tree(
            city_path, indicator, split_percentage, criterion, splitter, max_depth,
            min_samples_leaf, max_features, 
            max_leaf_nodes=None,
            n_tests=n_tests, 
            min_samples_split=min_samples_split,
            min_weight_fraction_leaf=min_weight_fraction_leaf, 
            min_impurity_decrease=min_impurity_decrease, 
            ccp_alpha=ccp_alpha,
            save_model=False
        )
        
        return score
    
    def objective_bt(self, trial, common_params):
        """Função objetivo para Bagged Trees (VERSÃO CORRIGIDA)."""
        city_path, indicator, split_percentage, n_tests, save_model_flag = common_params

        n_estimators = trial.suggest_int('n_estimators_bag', 50, 200, log=True) 

        criterion = trial.suggest_categorical('criterion', ['squared_error', 'absolute_error'])
        max_depth = trial.suggest_int('max_depth', 5, 50)
        min_samples_split = trial.suggest_int('min_samples_split', 2, 20)
        min_samples_leaf = trial.suggest_int('min_samples_leaf', 1, 20)
        max_features = trial.suggest_float('max_features', 0.5, 1.0)
        
        min_weight_fraction_leaf = 0.0
        min_impurity_decrease = trial.suggest_float('min_impurity_decrease', 0.0, 0.01)
        ccp_alpha = trial.suggest_float('ccp_alpha', 1e-5, 0.005, log=True)
        
        prev = Training()
        score, *_ = prev.bagging_trees(
             city_path, indicator, split_percentage, criterion, 
             splitter='best',
             max_depth=max_depth,
             min_samples_leaf=min_samples_leaf, 
             max_features=max_features, 
             max_leaf_nodes=None, 
             n_tests=n_tests, min_samples_split=min_samples_split,
             min_weight_fraction_leaf=min_weight_fraction_leaf, 
             min_impurity_decrease=min_impurity_decrease, 
             ccp_alpha=ccp_alpha, 
             save_model=False,
             n_estimators=n_estimators
        )
        return score
    
    def objective_nn(self, trial, common_params):
        """Função objetivo para Neural Network."""
        city_path, indicator, split_percentage, n_tests, save_model_flag = common_params

        activation = trial.suggest_categorical('activation', ['relu', 'tanh', 'logistic'])
        solver = trial.suggest_categorical('solver', ['adam', 'lbfgs', 'sgd'])
        alpha = trial.suggest_float('alpha', 1e-5, 1e-1, log=True)
        batch_size_str = trial.suggest_categorical('batch_size', ['auto', '50', '100', '200'])
        batch_size = int(batch_size_str) if batch_size_str != 'auto' else 'auto'
        learning_rate = trial.suggest_categorical('learning_rate', ['constant', 'invscaling', 'adaptive'])
        learning_rate_init = trial.suggest_float('learning_rate_init', 1e-4, 1e-2, log=True)
        max_iter = trial.suggest_int('max_iter', 200, 1000)
        momentum = 0.9
        
        if solver == 'sgd':
            momentum = trial.suggest_float('momentum', 0.1, 0.99)
        
        prev = Training()
        score, *_ = prev.neural_network(
             city_path, indicator, split_percentage, n_tests, activation, solver, alpha, batch_size,
             learning_rate, learning_rate_init, power_t=0.5, max_iter=max_iter, shuffle=True, 
             tol=1e-4, verbose=False, warm_start=False, momentum=momentum, 
             nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1,
             beta_1=0.9, beta_2=0.999, n_iter_no_change=10, max_fun=15000, 
             save_model=False
        )
        return score

    def objective_svm(self, trial, common_params):
        """Função objetivo para Support Vector."""
        city_path, indicator, split_percentage, n_tests, save_model_flag = common_params

        kernel = 'rbf'
        c_param = trial.suggest_float('c_param', 1e-2, 1e2, log=True)
        epsilon = trial.suggest_float('epsilon', 1e-3, 1e-1, log=True)
        
        degree = 3
        gamma = trial.suggest_float('gamma', 1e-4, 1.0, log=True)
        
        prev = Training()
        score, *_ = prev.support_vector_regression(
             city_path, indicator, split_percentage, n_tests, kernel, degree, gamma, 
             coef0=0.0, tol=1e-3, C=c_param, epsilon=epsilon, 
             shrinking=True, cache_size=200, verbose=False, max_iter=-1, 
             save_model=False
        )
        return score

    def objective_gp(self, trial, common_params):
        """Função objetivo para Gaussian Process."""
        city_path, indicator, split_percentage, n_tests, save_model_flag = common_params
        
        # Pega o tipo de Kernel selecionado na UI
        kernel_type = self.current_param_frame.kernel_type.get() 
        
        # Otimização de Hiperparâmetros baseada no Kernel
        length_scale = 1.0
        nu = 1.5
        alpha_rq = 1.0
        sigma_0 = 1.0

        # RBF, Matern e RationalQuadratic usam length_scale
        if kernel_type in ['RBF', 'Matern', 'RationalQuadratic']:
            length_scale = trial.suggest_float('length_scale', 1e-2, 1e2, log=True)
        
        if kernel_type == 'Matern':
            nu = trial.suggest_categorical('nu', [0.5, 1.5, 2.5])
            
        if kernel_type == 'RationalQuadratic':
            alpha_rq = trial.suggest_float('alpha_rq', 1e-2, 1e2, log=True)
            
        if kernel_type == 'DotProduct':
            sigma_0 = trial.suggest_float('sigma_0', 1e-2, 10.0, log=True)
        
        # Alpha (Noise) global
        alpha_gp = trial.suggest_float('alpha_gp', 1e-10, 1e-1, log=True)

        prev = Training()
        
        score, *_ = prev.gaussian_process_regression(
             city_path, indicator, split_percentage, n_tests, kernel_type, 
             len_scale=length_scale,
             nu=nu, 
             sigma_0=sigma_0, 
             alpha_rq=alpha_rq,
             alpha_gp=alpha_gp, 
             n_restarts_optimizer=int(self.current_param_frame.n_restarts_op.get()), 
             normalize_y_gp=self.current_param_frame.normalize_y_gp.get(), 
             save_model=False
        )
        return score


    def objective_kn(self, trial, common_params):
        """Função objetivo para Nearest Neighbors (ESPAÇO REDUZIDO)."""
        city_path, indicator, split_percentage, n_tests, save_model_flag = common_params
        
        n_neighbors = trial.suggest_int('n_neighbors', 3, 30)
        
        p_value = trial.suggest_int('p_value', 1, 2) # 1=Manhattan, 2=Euclidean

        algorithm = 'auto'
        leaf_size = 30   

        prev = Training()
        score, *_ = prev.KNeighbors(
             city_path, indicator, split_percentage, n_tests, 
             n_neighbors, 
             algorithm,  
             leaf_size,   
             p_value,     
             n_jobs=-1,
             save_model=False
        )
        return score
    
    def generate_param_ui(self, event=None):
        """Preenche o 'param_container' com os widgets corretos."""
        self._clear_panel(self.param_container)
        self.current_param_frame = None

        opcao = self.ml_combo.get()
        if not opcao: return

        try:
            if opcao == 'Decision Trees':
                from .gui_helpers import DTParameterFrame
                self.current_param_frame = DTParameterFrame(self.param_container)
            elif opcao == 'Bagged Trees':
                from .gui_helpers import BaggingTParameterFrame
                self.current_param_frame = BaggingTParameterFrame(self.param_container)
            elif opcao == 'Neural network':
                from .gui_helpers import NNParameterFrame
                self.current_param_frame = NNParameterFrame(self.param_container)
            elif opcao == 'Nearest Neighbors':
                from .gui_helpers import NNeighParameterFrame
                self.current_param_frame = NNeighParameterFrame(self.param_container)
            elif opcao == 'Support Vector':
                from .gui_helpers import SVMParameterFrame
                self.current_param_frame = SVMParameterFrame(self.param_container)
            elif opcao == 'Gaussian Process':
                from .gui_helpers import GPParameterFrame
                self.current_param_frame = GPParameterFrame(self.param_container)

            if self.current_param_frame:
                self.current_param_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            else:
                 ttk.Label(self.param_container, text=f"UI de parâmetros para '{opcao}' não implementada.").pack()

        except ImportError as e:
             self.controller.show_translated_message(
                 msg_type='error',
                 title_key='import_error_title',
                 message_key='param_ui_import_error_msg',
                 option=opcao,
                 error=str(e)
             )
        except Exception as e:
            self.controller.show_translated_message(
                 msg_type='error',
                 title_key='ui_generate_error_title',
                 message_key='param_ui_generate_error_msg',
                 option=opcao,
                 error=str(e)
             )
            
    def data_preview(self, score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis):
        """Exibe os resultados textuais e o gráfico de comparação no painel direito."""
        # 1. Limpa o painel direito de qualquer conteúdo anterior
        self._clear_panel(self.right_panel)
        i18n = self.controller.i18n

        # --- Frame para os Resultados Textuais ---
        # Cria um LabelFrame DENTRO do self.right_panel
        results_outer_frame = ttk.LabelFrame(self.right_panel, text=i18n.get('results_preview_label'))
        results_outer_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5)) # Pack no topo

        # Frame interno para usar .grid() para alinhar os labels
        results_inner_frame = ttk.Frame(results_outer_frame)
        results_inner_frame.pack(padx=10, pady=10)

        # Configura colunas para o grid interno (label, valor_exato, valor_pred)
        results_inner_frame.grid_columnconfigure(0, weight=1)
        results_inner_frame.grid_columnconfigure(1, weight=1)
        results_inner_frame.grid_columnconfigure(2, weight=1)

        # 2. Cria os Labels para as métricas usando ttk e grid
        ttk.Label(results_inner_frame, text=f"{i18n.get('score_label')}: {score:.2f} pts", font='Arial 11 bold').grid(row=0, column=0, sticky="w", columnspan=3)
        ttk.Label(results_inner_frame, text=f"{i18n.get('mean_abs_error_label')}: {round(mean_abs_error, 4)}", font='Arial 11').grid(row=1, column=0, sticky="w", columnspan=3)
        ttk.Label(results_inner_frame, text=f"{i18n.get('mean_rel_error_label')}: {round(mean_rel_error, 4)}", font='Arial 11').grid(row=2, column=0, sticky="w", columnspan=3)

        # Separador visual
        ttk.Separator(results_inner_frame, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky='ew', pady=5)

        # Maior Erro
        ttk.Label(results_inner_frame, text=f"{i18n.get('max_abs_error_label')}: {round(max_abs_error, 4)}", font='Arial 11').grid(row=4, column=0, sticky="w")
        ttk.Label(results_inner_frame, text=f"{i18n.get('exact_value_label')}: {round(exact_max, 4)}", font='Arial 11').grid(row=4, column=1, sticky="w", padx=10)
        ttk.Label(results_inner_frame, text=f"{i18n.get('prediction_label')}: {round(pred_max, 4)}", font='Arial 11').grid(row=4, column=2, sticky="w", padx=10)

        # Menor Erro
        ttk.Label(results_inner_frame, text=f"{i18n.get('min_abs_error_label')}: {round(min_abs_error, 4)}", font='Arial 11').grid(row=5, column=0, sticky="w")
        ttk.Label(results_inner_frame, text=f"{i18n.get('exact_value_label')}: {round(exact_min, 4)}", font='Arial 11').grid(row=5, column=1, sticky="w", padx=10)
        ttk.Label(results_inner_frame, text=f"{i18n.get('prediction_label')}: {round(pred_min, 4)}", font='Arial 11').grid(row=5, column=2, sticky="w", padx=10)

        # --- Criação e Plotagem do Gráfico Matplotlib ---
        figure = Figure(figsize=(10, 6), dpi=100)
        plot_r = figure.add_subplot(111)
        plot_r.plot(x_axis, y_exact, label=i18n.get('exact_plot_label'), color='green')
        plot_r.plot(x_axis, y_pred, label=i18n.get('prediction_plot_label'), color='red')
        plot_r.legend()
        plot_r.grid(True)
        # TODO: Adicionar i18n para os eixos Y e X
        plot_r.set_ylabel("Temperature(°C)")
        plot_r.set_xlabel(i18n.get('comparisons_label'))
        figure.tight_layout() # Ajusta o layout para evitar sobreposições

        # 4. Integração do Matplotlib com Tkinter DENTRO do self.right_panel
        # Cria o Canvas como filho do self.right_panel
        canvas = FigureCanvasTkAgg(figure, master=self.right_panel)
        canvas.draw()

        # Cria a Toolbar como filha do self.right_panel
        toolbar = NavigationToolbar2Tk(canvas, self.right_panel)
        toolbar.update()

        # Coloca a toolbar embaixo e o canvas ocupando o resto
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def run_model_preview(self):
        """Função "despachante" que chama a lógica de ML correta."""
        opcao = self.ml_combo.get()
        if not opcao:
            self.controller.show_translated_message(
                 msg_type='warning',
                 title_key='warning_title',
                 message_key='select_ml_model_msg'
             )
            return
        if not self.current_param_frame:
            self.controller.show_translated_message(
                 msg_type='warning',
                 title_key='warning_title',
                 message_key='select_ml_model_again_msg'
             )
            return

        try:
            if opcao == 'Decision Trees': self.generate_preview_dt()
            elif opcao == 'Bagged Trees': self.generate_preview_bt()
            elif opcao == 'Neural network': self.generate_preview_nn()
            elif opcao == 'Nearest Neighbors': self.generate_preview_kn()
            elif opcao == 'Support Vector': self.generate_preview_svm()
            elif opcao == 'Gaussian Process': self.generate_preview_GP()
        except AttributeError as e:
             self.controller.show_translated_message(
                 msg_type='error',
                 title_key='parameter_error_title',
                 message_key='coud_not_read_parameter_msg',
                 option=opcao,
                 error=str(e)
             )
        except Exception as e:
            self.controller.show_translated_message(
                 msg_type='error',
                 title_key='execution_error_title',
                 message_key='model_error_msg',
                 option=opcao,
                 error=str(e)
             )

    def _get_common_params(self):
        city_file_name = self.data_combo.get() 
        base_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        print("Base dir", base_dir)
        if city_file_name == "Target":
            city_file_name = "target_clean.txt"
        elif city_file_name == "Neighbor A":
            city_file_name = "neighborA_clean.txt"
        elif city_file_name == "Neighbor B":
            city_file_name == "neighborB_clean.txt"
        else:
            city_file_name = "neighborC.txt"

        city_path = os.path.join(base_dir, city_file_name)

        try:
            print(city_path)
            if not os.path.exists(city_path):
                 self.controller.show_translated_message(
                    msg_type='error',
                    title_key='error_title',
                    message_key='file_not_found_msg',
                    city_path=city_path
                )
                 return None
        except Exception as e:
            self.controller.show_translated_message(
                msg_type='error',
                title_key='error_title',
                message_key='path_not_determinated_msg',
                error=str(e)
                )
            return None

        indicator = self.indicator_combo.get()
        indicator = self.indicator_combo.get()
        if not city_file_name or not indicator:
            self.controller.show_translated_message(
                msg_type='error',
                title_key='error_title',
                message_key='file_and_indicator_not_selected_msg'
                )
            return None
        try:
            split = int(self.split_var.get())
            tests = int(self.tests_var.get())
        except ValueError:
             self.controller.show_translated_message(
                msg_type='error',
                title_key='error_title',
                message_key='train_number_tests_msg'
                )
             return None

        try:
            if not os.path.exists(city_path):
                self.controller.show_translated_message(
                msg_type='error',
                title_key='error_title',
                message_key='file_not_found_msg',
                city_path=city_path
                )
                return None
        except Exception as e:
            self.controller.show_translated_message(
                msg_type='error',
                title_key='error_title',
                message_key='path_not_determinated_msg',
                error=str(e)
                )
            return None

        return (
            city_path,
            get_indicator_code(indicator),
            split,
            tests,
            self.save_model_var.get()
        )

    def int_float(self, value_str):
        """Tenta retornar int, senão float."""
        try:
            return int(value_str)
        except ValueError:
            try:
                return float(value_str)
            except ValueError:
                self.controller.show_translated_message(
                msg_type='error',
                title_key='value_error_title',
                message_key='value_error_msg',
                value_str=value_str
                )
                raise 

    def valid_maxf(self, value_str):
        """Retorna o tipo correto para max_features."""
        value_str = value_str.strip() 
        if value_str.isdigit():
            return int(value_str)
        elif value_str in ['sqrt', 'log2']:
             return value_str
        else:
             try:
                 val_float = float(value_str)
                 if val_float.is_integer():
                     return int(val_float)
                 return val_float
             except ValueError:
                 self.controller.show_translated_message(
                    msg_type='error',
                    title_key='value_error_title',
                    message_key='invalid_max_features_msg',
                    value_str=value_str
                    )
                 raise 

    def get_end(self, city_filename):
        """Obtém o caminho completo para um arquivo de cidade processado."""
        try:
            # Precisa encontrar a pasta 'processed_data'
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            processed_dir = os.path.join(base_dir, "processed_data")
            full_path = os.path.join(processed_dir, city_filename)
            if os.path.exists(full_path):
                return full_path
            else:
                 print(f"Aviso: Método get_end não encontrou o arquivo diretamente. {full_path}")
                 # treatment = DataProcessing() # Talvez precise instanciar aqui?
                 raise FileNotFoundError(f"Arquivo não encontrado via get_end: {city_filename}")
        except Exception as e:
            self.controller.show_translated_message(
                msg_type='error',
                title_key='get_end_error_title',
                message_key='cant_get_path_msg',
                city_file_name=city_filename,
                error=str(e)
                )
            raise

    def _read_param(self, param_name, type_func, default_value=None):
        """Helper function to read and convert a parameter, with error handling."""
        try:
            # Assumes param_name matches the attribute name in current_param_frame
            widget_var = getattr(self.current_param_frame, param_name)
            value_str = widget_var.get()

            # Handle boolean separately if using Checkbuttons/BooleanVar
            if type_func == bool:
                return widget_var.get() # BooleanVar returns bool directly

            # Handle specific string values like 'auto', 'scale', etc.
            if type_func == str and value_str in ['auto', 'scale', 'sqrt', 'log2', 'none', 'best', 'random', 'mse', 'mae', 'linear', 'poly', 'rbf', 'sigmoid', 'lbfgs', 'sgd', 'adam', 'constant', 'invscaling', 'adaptive', 'identity', 'logistic', 'tanh', 'relu', 'ball_tree', 'kd_tree', 'brute']:
                 return value_str # Return known string values directly

            # Attempt conversion for numeric types
            if type_func == int:
                return int(value_str)
            if type_func == float:
                 # Try int first in case user enters "5" for a float field
                 try: return int(value_str)
                 except ValueError: return float(value_str)

            # If type_func is str but not a known keyword, return as is
            if type_func == str:
                 return value_str

            # Fallback for unexpected types
            return type_func(value_str) # General conversion attempt

        except AttributeError:
            self.controller.show_translated_message(
                msg_type='error',
                title_key='internal_error_title',
                message_key='atribute_not_found_msg',
                param_name=param_name
                )
            raise # Stop execution
        except (ValueError, TypeError) as e:
            self.controller.show_translated_message(
                msg_type='error',
                title_key='value_error_title',
                message_key='value_invalid_for_parameter_msg',
                param_name=param_name,
                type_func=type_func.__name__,
                value_str=value_str,
                error=str(e)
                )
            raise
        except Exception as e:
            self.controller.show_translated_message(
                msg_type='error',
                title_key='unexpected_error_title',
                message_key='error_while_reading_parameter_msg',
                param_name=param_name,
                error=str(e)
                )
            raise


    def generate_preview_dt(self):
        params = self._get_common_params()
        if params is None: return
        city_path, indicator, split_percentage, n_tests, save_model_flag = params

        try:
            criterion = self._read_param('criterion_v', str)
            splitter = self._read_param('splitter_v', str)
            max_depth = self._read_param('maxd_v', int)
            min_samples_split = self._read_param('minsam_s_v', int)
            min_samples_leaf = self._read_param('minsam_l_v', int)
            min_weight_fraction_leaf = self._read_param('minweifra_l_v', float)
            max_features = self.valid_maxf(self.current_param_frame.maxfeat_v.get())

            max_leaf_nodes = self._read_param('maxleaf_n', int)
            min_impurity_decrease = self._read_param('minimp_dec', float)
            ccp_alpha = self._read_param('ccp_alp_v', float)
        except Exception:
            return

        prev = Training()
        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.decision_tree(
            city_path, indicator, split_percentage, criterion, splitter, max_depth,
            min_samples_leaf, max_features, max_leaf_nodes, n_tests, min_samples_split,
            min_weight_fraction_leaf, min_impurity_decrease, ccp_alpha, save_model_flag
        )
        self.data_preview(score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis)

    def generate_preview_bt(self):
        params = self._get_common_params()
        if params is None: return
        city_path, indicator, split_percentage, n_tests, save_model_flag = params

        try:
            # Parâmetros específicos do DT
            criterion = self._read_param('criterion_v', str)
            splitter = self._read_param('splitter_v', str)
            max_depth = self._read_param('maxd_v', int)
            min_samples_split = self._read_param('minsam_s_v', int)
            min_samples_leaf = self._read_param('minsam_l_v', int)
            min_weight_fraction_leaf = self._read_param('minweifra_l_v', float)
            max_features = self.valid_maxf(self.current_param_frame.maxfeat_v.get())
            max_leaf_nodes = self._read_param('maxleaf_n', int)
            min_impurity_decrease = self._read_param('minimp_dec', float)
            ccp_alpha = self._read_param('ccp_alp_v', float)
            # Parâmetro específico do Bagging
            n_estimators = self._read_param('n_estimators', int)
        except Exception:
            return

        prev = Training()
        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.bagging_trees(
             city_path, indicator, split_percentage, criterion, splitter, max_depth,
             min_samples_leaf, max_features, max_leaf_nodes, n_tests, min_samples_split,
             min_weight_fraction_leaf, min_impurity_decrease, ccp_alpha, save_model_flag,
             n_estimators
        )
        self.data_preview(score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis)

    def generate_preview_nn(self):
        params = self._get_common_params()
        if params is None: return
        city_path, indicator, split_percentage, n_tests, save_model_flag = params

        try:
            activation = self._read_param('activation_v', str)
            solver = self._read_param('solver_v', str)
            alpha = self._read_param('alpha_v', float)
            batch_size_str = self._read_param('batch_size_v', str) # Read as string first
            learning_rate = self._read_param('learning_rate_v', str)
            learning_rate_init = self._read_param('learning_rate_init_v', float)
            power_t = self._read_param('power_t_v', float)
            max_iter = self._read_param('max_iter_v', int)
            shuffle = self._read_param('shuffle_v', bool) # Read BooleanVar
            tol = self._read_param('tol_v', float)
            verbose = self._read_param('verbose_v', bool) # Read BooleanVar
            warm_start = self._read_param('warm_start_v', bool) # Read BooleanVar
            momentum = self._read_param('momentum_v', float)
            nesterovs_momentum = self._read_param('nesterovs_momentum_v', bool) # Read BooleanVar
            early_stopping = self._read_param('early_stopping_v', bool) # Read BooleanVar
            validation_fraction = self._read_param('validation_fraction_v', float)
            beta_1 = self._read_param('beta_1_v', float)
            beta_2 = self._read_param('beta_2_v', float)
            n_iter_no_change = self._read_param('n_iter_no_change_v', int)
            max_fun = self._read_param('max_fun_v', int)

            # Converte batch_size se não for 'auto'
            batch_size = int(batch_size_str) if batch_size_str != 'auto' else 'auto'

        except Exception:
            return

        prev = Training()
        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.neural_network(
             city_path, indicator, split_percentage, n_tests, activation, solver, alpha, batch_size,
             learning_rate, learning_rate_init, power_t, max_iter, shuffle, tol, verbose,
             warm_start, momentum, nesterovs_momentum, early_stopping, validation_fraction,
             beta_1, beta_2, n_iter_no_change, max_fun, save_model_flag
        )
        self.data_preview(score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis)

    def generate_preview_svm(self):
        params = self._get_common_params()
        if params is None: return
        city_path, indicator, split_percentage, n_tests, save_model_flag = params

        try:
            # ⚠️ Certifique-se que SVMParameterFrame foi refatorado e tem estes atributos
            kernel = self._read_param('kernel_v', str)
            degree = self._read_param('degree_v', int)
            gamma_str = self._read_param('gamma_v', str) # Read as string
            coef0 = self._read_param('coef0_v', float)
            tol = self._read_param('tol_v', float)
            c_param = self._read_param('c_v', float)
            epsilon = self._read_param('epsilon_v', float)
            shrinking = self._read_param('shrinking_v', bool) # BooleanVar?
            cache_size = self._read_param('cache_size_v', float)
            verbose = self._read_param('verbose_v', bool) # BooleanVar?
            max_iter = self._read_param('maxiter_v', int)

            # Converte gamma se necessário
            gamma = float(gamma_str) if gamma_str not in ['scale', 'auto'] else gamma_str

        except AttributeError:
             self.controller.show_translated_message(
                msg_type='error',
                title_key='internal_error_title',
                message_key='ui_problem_svm_msg',
                )
             return
        except Exception:
            return

        prev = Training()
        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.support_vector_regression(
             city_path, indicator, split_percentage, n_tests, kernel, degree, gamma, coef0,
             tol, c_param, epsilon, shrinking, cache_size, verbose, max_iter, save_model_flag
        )
        self.data_preview(score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis)

    def generate_preview_GP(self):
        params = self._get_common_params()
        if params is None: return
        city_path, indicator, split_percentage, n_tests, save_model_flag = params

        try:
            
            alpha_gp = self._read_param('alpha_gp', float)
            n_restarts_optimizer = self._read_param('n_restarts_op', int)
            normalize_y_gp = self._read_param('normalize_y_gp', bool)
            kernel_type = self._read_param('kernel_type', str)

            length_scale = self._read_param('length_scale', float)
            
            nu = self._read_param('nu', float) 
            
            sigma_0 = self._read_param('sigma_0', float)
            alpha_rq = self._read_param('alpha_rq', float)

        except Exception:
            return

        prev = Training()
        
        # print(f"GP Call: Type={kernel_type}, Len={length_scale}, Alpha={alpha_gp}, Nu={nu}")

        try:
            score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.gaussian_process_regression(
                city=city_path, 
                indicator_code=indicator, 
                division=split_percentage, 
                kernel_type=kernel_type, 
                len_scale=length_scale,  
                nu=nu, 
                sigma_0=sigma_0, 
                alpha_rq=alpha_rq, 
                alpha_noise=alpha_gp,    
                n_restart=n_restarts_optimizer, 
                normalize_y=normalize_y_gp, 
                save_model=save_model_flag
            )
            
            self.data_preview(score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis)
        
        except TypeError as e:
            self.controller.show_translated_message(
                 msg_type='error',
                 title_key='execution_error_title',
                 message_key='model_error_msg',
                 option='Gaussian Process',
                 error=f"Erro de assinatura na função: {str(e)}"
             )
        except Exception as e:
            self.controller.show_translated_message(
                 msg_type='error',
                 title_key='execution_error_title',
                 message_key='model_error_msg',
                 option='Gaussian Process',
                 error=str(e)
             )
            
    def generate_preview_kn(self):
        params = self._get_common_params()
        if params is None: return
        city_path, indicator, split_percentage, n_tests, save_model_flag = params

        try:
            n_neighbors = self._read_param('n_neighbors_v', int)
            algorithm = self._read_param('algorithm_v', str)
            leaf_size = self._read_param('leaf_size_v', int)
            p_value = self._read_param('p_v', int)
            n_jobs_str = self._read_param('n_jobs_v', str)

            # Converte n_jobs
            n_jobs = None if n_jobs_str.lower() == 'none' else int(n_jobs_str)

        except Exception:
            return

        prev = Training()
        score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis = prev.KNeighbors(
             city_path, indicator, split_percentage, n_tests, n_neighbors, algorithm, leaf_size, p_value, n_jobs, save_model_flag
        )
        self.data_preview(score, mean_abs_error, mean_rel_error, max_abs_error, exact_max, pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis)