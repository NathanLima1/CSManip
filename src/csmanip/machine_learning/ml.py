"""Module for the machine learning without interface.

This module creates a window with options for selecting different 
Machine Learning algorithms and integrates functionalities such as
parameter selection, data preview, and result visualization.
"""

from .ml_view import View
from .utils import *
from .ml_helpers import *
from ..data_processing.data_processing import DataProcessing
import optuna
import threading
import json
import functools
import os
import sys
from ..utils.indicator import get_indicator_code 
from ..training.training import Training

class Ml:
    def __init__(self):
        self.list_ml = ['Decision Trees',
                        'Bagged Trees',
                        'Neural network',
                        'Nearest Neighbors',
                        'Support Vector',
                        'Gaussian Process']
        
        self.list_ind = ["Precipitation", 'Maximum temperature', 'Minimum temperature']
        self.list_dt = ['Target city', 'Neighbor A', 'Neighbor B', 'Neighbor C']
        
        self.data_s = "Target_city"
        self.ind_s = "Maximum temperature"
        self.last_best_params = {}
        

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

    def _load_json_params(self, load_params):
        try:
            with open(load_params, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get("params", {})
        except Exception as e:
            print("Erro ao carregar JSON:", e)
            return None

    def decision_tree(self, criterion_v="squared_error", splitter="best", maxd_v='10',
                      minsam_s_v=2, minsam_l_v=50, minweifra_l_v='0.0', maxfeat_v="sqrt",
                      maxleaf_n='10', minimp_dec='0.0', ccp_alp_v='0.0', 
                      por_trei=70, num_teste=5,save_model=False, load_params='None'):
        
        if load_params is not 'None':
            try:
                with open(load_params, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    criterion = data["criterion"]
                    splitter = data["splitter"]
                    max_depth = data["max_depth"]
                    min_samples_s = data["min_samples_split"]
                    min_samples_l = data["min_samples_leaf"]
                    max_features = data["max_features"]
                    min_impurity_d = data["min_impurity_decrease"]
                    ccp_alpha = data["ccp_alpha"]

                    self.param_frame = DTParameter(criterion, splitter, max_depth, min_samples_s,
                                                   min_samples_l, max_features, maxleaf_n, min_impurity_d, ccp_alpha)
                    
                    self.por_trei = por_trei
                    self.num_teste = num_teste
                    self.save_model = save_model
                    self.generate_preview_dt()
            except Exception as e:
                print("Ocorreu um erro:", e)
        
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
                      por_trei=70, num_teste=5,save_model=False, n_estimators=10, load_params='None'):
        if load_params != 'None':
            params = self._load_json_params(load_params)
            if params:
                self.param_frame = BTParameter(
                    params["criterion"],
                    "best",
                    params["max_depth"],
                    params["min_samples_split"],
                    params["min_samples_leaf"],
                    '0.0',
                    params["max_features"],
                    maxleaf_n,
                    params["min_impurity_decrease"],
                    params["ccp_alpha"],
                    params["n_estimators_bag"]
                )
                
                self.por_trei = por_trei
                self.num_teste = num_teste
                self.save_model = save_model
                self.n_estimators = params["n_estimators_bag"]
                self.generate_preview_bt()
                return
        
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
                       num_teste=5, save_model=False, load_params='None'):
        
        if load_params != 'None':
            params = self._load_json_params(load_params)
            if params:
                self.param_frame = NNParameter(
                    params["activation"],
                    params["solver"],
                    params["alpha"],
                    params["batch_size"],
                    params["learning_rate"],
                    params["learning_rate_init"],
                    '0.5',
                    params["max_iter"],
                    True, '0.0001', False, False,
                    params.get("momentum", 0.9),
                    True, False, '0.1',
                    0.9, 0.999, 10, 15000
                )
                self.save_model = save_model
                self.num_teste = num_teste
                self.por_trei = por_trei
                self.generate_preview_nn()
                return
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
                          p_v=2, n_jobs_v='5', por_trei=70, num_teste=5, save_model=False, load_params='None'):
        
        if load_params != 'None':
            params = self._load_json_params(load_params)
            if params:
                self.param_frame = NNeighParameter(
                    params["n_neighbors"],
                    'auto',
                    30,
                    params["p_value"],
                    '-1'
                )
                self.save_model = save_model
                self.num_teste = num_teste
                self.por_trei = por_trei
                self.generate_preview_kn()
                return
        
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
                       num_teste=5, save_model=False, load_params='None'):
        
        if load_params != 'None':
            params = self._load_json_params(load_params)
            if params:
                self.kernel_v = 'rbf'
                self.gamma_v = params["gamma"]
                self.c_v = params["c_param"]
                self.epsilon_v = params["epsilon"]
                self.por_trei = por_trei
                self.num_teste = num_teste
                self.save_model = save_model
                self.generate_preview_svm()
                return
        
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
                         por_trei=70, num_teste=5, save_model=False, load_params='None'):
        if load_params != 'None':
            params = self._load_json_params(load_params)
            if params:
                self.param_frame = GPParameter(
                    params.get("alpha_gp", alpha_gp),
                    n_restarts_op,
                    normalize_y_gp,
                    copy_X_train,
                    rand_state_gp
                )
                self.por_trei = por_trei
                self.num_teste = num_teste
                self.save_model = save_model
                self.generate_preview_svm()
                return
            
        self.param_frame = GPParameter(alpha_gp, n_restarts_op, normalize_y_gp, copy_X_train, rand_state_gp)
        self.por_trei = por_trei
        self.num_teste = num_teste
        self.save_model = save_model
        self.generate_preview_svm()

    def _get_common_params(self, city, indicator, split, tests, save_model):
        """Prepara os caminhos e parâmetros comuns"""
        base_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

        file_map = {
            "Target city": "target_clean.txt",
            "Neighbor A": "neighborA_clean.txt",
            "Neighbor B": "neighborB_clean.txt",
            "Neighbor C": "neighborC.txt"
        }

        city_file_name = file_map.get(city, "target_clean.txt")
        city_path = os.path.join(base_dir, city_file_name)

        if not os.path.exists(city_path):
            print(f"Erro: Arquivo não encontrado em {city_path}")
            return None
        
        return (
            city_path,
            get_indicator_code(indicator),
            split,
            tests,
            save_model
        )

    def optuna_optimization(self, n_trials, model_name, city, indicator, split, tests, 
                            save_model=True, gp_kernel_type='RBF'):
        common_params = self._get_common_params(city, indicator, split, tests, save_model)

        if common_params is None: return
        
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
            print(f"Modelo {model_name} não suportado.")
            return
        
        print(f"--- Iniciando Otimização para {model_name} ({n_trials} trials) ---")
        
        optuna.logging.set_verbosity(optuna.logging.INFO)
        study = optuna.create_study(direction='maximize')

        if model_name == 'Gaussian Process':
            objective_func = functools.partial(base_objective, common_params=common_params, kernel_type=gp_kernel_type)
        else:
            objective_func = functools(base_objective, common_params=common_params)

        try:
            study.optimize(objective_func, n_trials=n_trials)
        except Exception as e:
            print(f"Erro durante a otimização: {e}")
            return
        
        self.last_best_params = study.best_params
        best_value = study.best_value
        best_params = study.best_params

        print("\n" + "="*40)
        print(f"Otimização Finalizada!")
        print(f"Melhor Score (R2/Metrics): {best_value}")
        print(f"Melhores Hiperparâmetros: {best_params}")
        print("="*40 + "\n")

        print(f"Salvando JSON de hiperparâmetros...")
        self.save_hyperparameters(model_name)

        print(f"Gerando modelo final para {model_name} com os melhores parâmetros...")
        self._train_final_model(model_name, best_params, common_params, gp_kernel_type)

    def _train_final_model(self, model_name, best_params, common_params, gp_kernel_type):
        """
        Treina o modelo com os melhores parâmetros encontrados
        """
        city_path, indicator, split_percentage, n_tests, save_model = common_params
        trainer = Training()

        try:
            if model_name == 'Decision Trees':
                trainer.decision_tree(
                    city_path, indicator, split_percentage,
                    criterion=best_params['criterion'],
                    splitter=best_params['splitter'],
                    max_depth=best_params['max_depth'],
                    min_samples_split=best_params['min_samples_split'],
                    min_samples_leaf=best_params['min_samples_leaf'],
                    max_features=best_params['max_features'],
                    min_impurity_decrease=best_params['min_impurity_decrease'],
                    ccp_alpha=best_params['ccp_alpha'],
                    n_tests=n_tests,
                    save_model=save_model
                )

            elif model_name == 'Bagged Trees':
                trainer.bagging_trees(
                    city_path, indicator, split_percentage,
                    criterion=best_params['criterion'],
                    splitter='best',
                    max_depth=best_params['max_depth'],
                    min_samples_leaf=best_params['min_samples_leaf'],
                    max_features=best_params['max_features'],
                    min_samples_split=best_params['min_samples_split'],
                    min_impurity_decrease=best_params['min_impurity_decrease'],
                    ccp_alpha=best_params['ccp_alpha'],
                    n_estimators=best_params['n_estimators_bag'],
                    n_tests=n_tests,
                    save_model=save_model
                )

            elif model_name == 'Neural network':
                momentum = best_params.get('momentum', 0.9)
                batch_size = int(best_params['batch_size']) if best_params['batch_size'] != 'auto' else 'auto'
                
                trainer.neural_network(
                    city_path, indicator, split_percentage, n_tests,
                    activation=best_params['activation'],
                    solver=best_params['solver'],
                    alpha=best_params['alpha'],
                    batch_size=batch_size,
                    learning_rate=best_params['learning_rate'],
                    learning_rate_init=best_params['learning_rate_init'],
                    max_iter=best_params['max_iter'],
                    momentum=momentum,
                    save_model=save_model
                )

            elif model_name == 'Support Vector':
                trainer.support_vector_regression(
                    city_path, indicator, split_percentage, n_tests,
                    kernel='rbf',
                    degree=3,
                    gamma=best_params['gamma'],
                    C=best_params['c_param'],
                    epsilon=best_params['epsilon'],
                    save_model=save_model
                )
            
            elif model_name == 'Nearest Neighbors':
                trainer.KNeighbors(
                    city_path, indicator, split_percentage, n_tests,
                    n_neighbors=best_params['n_neighbors'],
                    p=best_params['p_value'],
                    algorithm='auto',
                    leaf_size=30,
                    n_jobs=-1,
                    save_model=save_model
                )

            elif model_name == 'Gaussian Process':
                trainer.gaussian_process_regression(
                    city_path, indicator, split_percentage, n_tests,
                    kernel=gp_kernel_type,
                    len_scale=best_params.get('length_scale', 1.0),
                    nu=best_params.get('nu', 1.5),
                    sigma_0=best_params.get('sigma_0', 1.0),
                    alpha_rq=best_params.get('alpha_rq', 1.0),
                    alpha_gp=best_params.get('alpha_gp', 1e-10),
                    n_restarts_optimizer=0,
                    save_model=save_model
                )
            
            print(f"Sucesso: Modelo {model_name} salvo corretamente.")
            
        except Exception as e:
            print(f"Erro ao salvar o modelo final: {e}")

    def save_hyperparameters(self, model_name):
        """
        Salva os parâmetros otimizados automaticamente em um arquivo JSON
        no diretório de execução, sem abrir janelas.
        """
        if not self.last_best_params:
            print("Aviso: Nenhum parâmetro encontrado para salvar.")
            return

        safe_name = model_name.replace(" ", "_")
        file_name = f"params_{safe_name}.json"
        
        file_path = os.path.join(os.getcwd(), file_name)

        try:
            data_to_save = {
                "model": model_name,
                "params": self.last_best_params
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4)
            
            print(f"Sucesso: Hiperparâmetros salvos em: {file_path}")
        except Exception as e:
            print(f"Erro ao salvar arquivo JSON: {str(e)}")

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

    def objective_gp(self, trial, common_params, kernel_type='RBF'):
        """
        Função objetivo do gaussian process.
        """
        city_path, indicator, split_percentage, n_tests, _ = common_params
        
        length_scale = 1.0
        nu = 1.5
        alpha_rq = 1.0
        sigma_0 = 1.0

        if kernel_type in ['RBF', 'Matern', 'RationalQuadratic']:
            length_scale = trial.suggest_float('length_scale', 1e-2, 1e2, log=True)
        
        if kernel_type == 'Matern':
            nu = trial.suggest_categorical('nu', [0.5, 1.5, 2.5])
            
        if kernel_type == 'RationalQuadratic':
            alpha_rq = trial.suggest_float('alpha_rq', 1e-2, 1e2, log=True)
            
        if kernel_type == 'DotProduct':
            sigma_0 = trial.suggest_float('sigma_0', 1e-2, 10.0, log=True)
        
        alpha_gp = trial.suggest_float('alpha_gp', 1e-10, 1e-1, log=True)

        prev = Training()
        score, *_ = prev.gaussian_process_regression(
             city_path, indicator, split_percentage, n_tests, kernel_type, 
             len_scale=length_scale, nu=nu, sigma_0=sigma_0, alpha_rq=alpha_rq,
             alpha_gp=alpha_gp, n_restarts_optimizer=0, normalize_y_gp=False, save_model=False
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
