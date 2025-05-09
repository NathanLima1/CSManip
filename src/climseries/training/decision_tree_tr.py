import time
import pickle
from sklearn.tree import DecisionTreeRegressor
from typing import Tuple, List
import numpy as np

def decision_tree(
    self, city: str, indicator_code: int, split_ratio: float, criterion: str, splitter: str,
    max_depth: int, min_samples_leaf: int, max_features, max_leaf_nodes: int,
    n_tests: int, min_samples_split: int, min_weight_fraction_leaf: float,
    min_impurity_decrease: float, ccp_alpha: float, save_model: bool
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

    train_X, train_y, val_X, val_y = self.prepare_matrix3(city, split_ratio, indicator_code)

    all_exact = []
    all_predicted = []
    total_relative_error = 0
    total_absolute_error = 0

    for test in range(n_tests):
        model = DecisionTreeRegressor(
            criterion=criterion, splitter=splitter, max_depth=max_depth,
            min_samples_leaf=min_samples_leaf, max_features=max_features,
            max_leaf_nodes=max_leaf_nodes, min_samples_split=min_samples_split,
            min_weight_fraction_leaf=min_weight_fraction_leaf,
            min_impurity_decrease=min_impurity_decrease, ccp_alpha=ccp_alpha
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

    score = round((((total_relative_error / n_tests) * 100) - 100) * -1, 2)

    if all_exact:
        errors = np.abs(np.array(all_exact) - np.array(all_predicted))
        max_idx = np.argmax(errors)
        min_idx = np.argmin(errors[errors > 0]) if np.any(errors > 0) else 0

        max_error = errors[max_idx]
        min_error = errors[min_idx] if np.any(errors > 0) else 0

        exact_max = all_exact[max_idx]
        predicted_max = all_predicted[max_idx]

        exact_min = all_exact[min_idx]
        predicted_min = all_predicted[min_idx]
    else:
        max_error = min_error = exact_max = predicted_max = exact_min = predicted_min = 0

    avg_absolute_error = total_absolute_error / n_tests
    avg_relative_error = total_relative_error / n_tests

    if save_model:
        pickle.dump(model, open(r'E:\IC\Interface_Grafica\Dados_verificacao\modelo_ad.sav', 'wb'))

    x_axis = list(range(1, len(all_exact) + 1))

    return (
        score, avg_absolute_error, avg_relative_error,
        max_error, exact_max, predicted_max,
        min_error, exact_min, predicted_min,
        all_exact, all_predicted, x_axis
    )
