import time
import pickle
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor
from typing import Tuple, List
import os
import numpy as np
from .utils import calculate_errors

def bagging_trees_tr(
    self, city: str, indicator_code: int, split_ratio: float, criterion: str, splitter: str,
    max_depth: int, min_samples_leaf: int, max_features, max_leaf_nodes: int,
    n_tests: int, min_samples_split: int, min_weight_fraction_leaf: float,
    min_impurity_decrease: float, ccp_alpha: float, save_model: bool, n_estimators: int
) -> Tuple[float, float, float, float, float, float, float, float, float, List[float], List[float], List[int]]:
    """
    Trains and evaluates a Decision Tree Regressor multiple times and returns statistics.

    Returns:
        Tuple containing: 
            score, average absolute error, average relative error,
            max absolute error, exact value at max error, predicted value at max error,
            min absolute error, exact value at min error, predicted value at min error,
            list of exact values, list of predicted values, x axis indices
    """
    start_time = time.time()

    indicators = {3: 'Precipitation', 4: 'Maximum Temperature'}
    indicator = indicators.get(indicator_code, 'Minimum Temperature')

    train_X, train_y, val_X, val_y = self.prepare_matrix_by_city(city, split_ratio, indicator_code)

    all_exact = []
    all_predicted = []
    total_relative_error = 0
    total_absolute_error = 0

    for test in range(n_tests):
        base_estimator = DecisionTreeRegressor(
            criterion=criterion, splitter=splitter, max_depth=max_depth,
            min_samples_leaf=min_samples_leaf, max_features=max_features,
            max_leaf_nodes=max_leaf_nodes, min_samples_split=min_samples_split,
            min_weight_fraction_leaf=min_weight_fraction_leaf,
            min_impurity_decrease=min_impurity_decrease, ccp_alpha=ccp_alpha
        )

        model = BaggingRegressor(
             estimator=base_estimator,
             n_estimators=n_estimators,
             random_state=42
        )
        model.fit(train_X, train_y)

        predictions = model.predict(val_X)
        absolute_errors = np.abs(np.array(val_y) - predictions)
        relative_errors = absolute_errors / np.array(val_y)

        total_absolute_error += np.mean(absolute_errors)
        total_relative_error += np.mean(relative_errors)

        if test != n_tests:  # This check is always True, unless intended to avoid the last?
            all_exact.extend(val_y)
            all_predicted.extend(predictions)

    statistics = calculate_errors(all_exact, all_predicted, total_absolute_error, total_relative_error, n_tests)

    score = statistics["score"]
    max_error = statistics["max_error"]
    min_error = statistics["min_error"]
    exact_max = statistics["exact_max"]
    predicted_max = statistics["predicted_max"]
    exact_min = statistics["exact_min"]
    predicted_min = statistics["predicted_min"]
    avg_absolute_error = statistics["avg_absolute_error"]
    avg_relative_error = statistics["avg_relative_error"]
    
    if save_model:
        with open(os.path.join(os.getcwd(), 'modelo_bagging.sav'), 'wb') as f:
                pickle.dump(model, f)

    x_axis = list(range(1, len(all_exact) + 1))

    return (
        score, avg_absolute_error, avg_relative_error,
        max_error, exact_max, predicted_max,
        min_error, exact_min, predicted_min,
        all_exact, all_predicted, x_axis
    )
