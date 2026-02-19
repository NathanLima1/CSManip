from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint
from .custom_tree import CustomDecisionTree
from .training import Training

import numpy as np

class Hiperparam:
    def grid_search_dt(self):
        pipeline = Training()
        city = "Target city"
        indicator_code = 3
        split_ratio = 0.7

        train_X, train_y, _, _ = pipeline.prepare_matrix_by_city(city, split_ratio, indicator_code)

        param_grid = {
            'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
            'splitter': ['best', 'random'],
            'max_depth': [i for i in range(5, 25)],
            'min_samples_split': [i for i in range(2, 15)],
            'min_samples_leaf': [i for i in range(1, 15)],
            'max_leaf_nodes': [i for i in range(5, 20)],
            'max_features': ['sqrt', 'log2'],
            'ccp_alpha': [0.0, 0.001]
        }

        grid = GridSearchCV(CustomDecisionTree(), param_grid=param_grid,
                            scoring='neg_mean_absolute_error', cv=5)
        grid.fit(train_X, train_y)

        print("Melhores hiperparâmetros encontrados:", grid.best_params_)

        # Usar os melhores parâmetros no pipeline original
        best = grid.best_params_

        results = pipeline.decision_tree(
            city=city,
            indicator_code=indicator_code,
            split_ratio=split_ratio,
            criterion=best['criterion'],
            splitter=best['splitter'],
            max_depth=best['max_depth'],
            min_samples_leaf=1,
            max_features=None,
            max_leaf_nodes=None,
            min_samples_split=best['min_samples_split'],
            min_weight_fraction_leaf=0.0,
            min_impurity_decrease=0.0,
            ccp_alpha=best['ccp_alpha'],
            n_tests=5,
            save_model=True
        )

        print("Score final:", results[0])
        print("Erro absoluto médio:", results[1])

    def randomized_search_dt(self):
        pipeline = Training()
        city = "Target city"
        indicator_code = 3
        split_ratio = 0.7

        train_X, train_y, _, _ = pipeline.prepare_matrix_by_city(city, split_ratio, indicator_code)

        param_grid = {
            'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
            'splitter': ['best', 'random'],
            'max_depth': [i for i in range(5, 30)],
            'min_samples_split': [i for i in range(2, 15)],
            'min_samples_leaf': [i for i in range(1, 15)],
            'max_leaf_nodes': [i for i in range(5, 20)],
            'max_features': ['sqrt', 'log2'],
            'ccp_alpha': [0.0, 0.001]
        }

        random = RandomizedSearchCV(
            CustomDecisionTree(),
            param_distributions=param_grid,
            scoring='neg_mean_absolute_error',
            cv=5,
            n_iter=50,  # Define quantas combinações serão testadas
            random_state=42
        )
        random.fit(train_X, train_y)

        print("Melhores hiperparâmetros encontrados:", random.best_params_)

        # Usar os melhores parâmetros no pipeline original
        best = random.best_params_

        results = pipeline.decision_tree(
            city=city,
            indicator_code=indicator_code,
            split_ratio=split_ratio,
            criterion=best['criterion'],
            splitter=best['splitter'],
            max_depth=best['max_depth'],
            min_samples_leaf=1,
            max_features=None,
            max_leaf_nodes=None,
            min_samples_split=best['min_samples_split'],
            min_weight_fraction_leaf=0.0,
            min_impurity_decrease=0.0,
            ccp_alpha=best['ccp_alpha'],
            n_tests=5,
            save_model=True
        )

        print("Score final:", results[0])
        print("Erro absoluto médio:", results[1])