import time
from typing import Tuple, List
import numpy as np
from sklearn.neural_network import MLPRegressor
from training.utils import calculate_errors

def neural_network(
    self, city: str, indicator_code: int, split_ratio: float, n_tests: int,
    activation: str, solver: str, alpha: float, batch_size, learning_rate: str,
    learning_rate_init: float, power_t: float, max_iter: int, shuffle: bool,
    tol: float, verbose: bool, warm_start: bool, momentum: float,
    nesterovs_momentum: bool, early_stopping: bool, validation_fraction: float,
    beta_1: float, beta_2: float, n_iter_no_change: int, max_fun: int
) -> Tuple[float, float, float, float, float, float, float, float, float, List[float], List[float], List[int]]:
    """
    Trains and evaluates an MLPRegressor multiple times and returns error statistics.

    Returns:
        Tuple containing:
            score, average absolute error, average relative error,
            max absolute error, exact value at max error, predicted value at max error,
            min absolute error, exact value at min error, predicted value at min error,
            list of exact values, list of predicted values, x axis indices
    """
    start_time = time.time()

    indicators = {3: 'Precipitação', 4: 'Temperatura máxima'}
    indicator = indicators.get(indicator_code, 'Temperatura mínima')

    train_X, train_y, val_X, val_y = self.prepara_matriz3(city, split_ratio, indicator_code)

    all_exact = []
    all_predicted = []
    total_absolute_error = 0
    total_relative_error = 0
    x_axis = []
    counter = 1

    for test in range(n_tests):
        model = MLPRegressor(
            activation=activation, solver=solver, alpha=alpha, batch_size=batch_size,
            learning_rate=learning_rate, learning_rate_init=learning_rate_init, power_t=power_t,
            max_iter=max_iter, shuffle=shuffle, tol=tol, verbose=verbose, warm_start=warm_start,
            momentum=momentum, nesterovs_momentum=nesterovs_momentum, early_stopping=early_stopping,
            validation_fraction=validation_fraction, beta_1=beta_1, beta_2=beta_2,
            n_iter_no_change=n_iter_no_change, max_fun=max_fun
        )

        model.fit(train_X, train_y)

        predictions = model.predict(val_X)
        absolute_errors = np.abs(np.array(val_y) - predictions)
        relative_errors = absolute_errors / np.array(val_y)

        total_absolute_error += np.mean(absolute_errors)
        total_relative_error += np.mean(relative_errors)

        if test != n_tests:  # sempre True — mesma situação da sua condição anterior
            all_exact.extend(val_y)
            all_predicted.extend(predictions)
            x_axis.extend(range(counter, counter + len(val_y)))
            counter += len(val_y)

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

    return (
        score, avg_absolute_error, avg_relative_error,
        max_error, exact_max, predicted_max,
        min_error, exact_min, predicted_min,
        all_exact, all_predicted, x_axis
    )
