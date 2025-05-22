import pickle
from sklearn.svm import SVR

def support_vector_regression(self, city, indicator_code, division, num_tests, kernel, degree, gamma, coef0, tol, C, epsilon, shrinking, cache_size, verbose, max_iter, save_model):
    """
    Applies Support Vector Regression (SVR) for predictive analysis.

    Parameters:
        city (str): Name of the city.
        indicator_code (int): Code representing the weather indicator.
        division (float): Data split ratio.
        num_tests (int): Number of test iterations.
        kernel (str): Kernel type for SVR.
        degree (int): Degree of the polynomial kernel function.
        gamma (str or float): Kernel coefficient.
        coef0 (float): Independent term in kernel function.
        tol (float): Tolerance for stopping criterion.
        C (float): Regularization parameter.
        epsilon (float): Epsilon-tube within which no penalty is associated.
        shrinking (bool): Whether to use shrinking heuristic.
        cache_size (float): Size of the kernel cache (in MB).
        verbose (bool): Enable verbose output.
        max_iter (int): Maximum number of iterations.
        save_model (bool): Whether to save the trained model.

    Returns:
        tuple: A tuple containing evaluation metrics and prediction data.
    """
    train_features, train_targets, val_features, val_targets = self.prepara_matriz3(city, division, indicator_code)
    total_relative_error = 0
    total_absolute_error = 0

    exact_values = []
    predicted_values = []
    x_axis = []
    count = 1

    if indicator_code == 3:
        indicator_name = 'Precipitation'
    elif indicator_code == 4:
        indicator_name = 'Maximum Temperature'
    else:
        indicator_name = 'Minimum Temperature'

    for test_round in range(num_tests):
        model = SVR(kernel=kernel, degree=degree, gamma=gamma, coef0=coef0,
                    tol=tol, C=C, epsilon=epsilon, shrinking=shrinking,
                    cache_size=cache_size, verbose=verbose, max_iter=max_iter)
        model.fit(train_features, train_targets)

        round_absolute_error = 0
        round_relative_error = 0

        for index in range(len(val_features)):
            exact_value = val_targets[index]
            predicted_value = model.predict([val_features[index]])[0]

            if test_round != num_tests:
                exact_values.append(exact_value)
                predicted_values.append(predicted_value)
                x_axis.append(count)
                count += 1

            absolute_error = abs(exact_value - predicted_value)
            relative_error = absolute_error / exact_value if exact_value != 0 else 0

            round_absolute_error += absolute_error
            round_relative_error += relative_error

        total_absolute_error += round_absolute_error / len(val_features)
        total_relative_error += round_relative_error / len(val_features)

    score = round((((total_relative_error / num_tests) * 100) - 100) * -1, 2)
    last_error = abs(exact_values[-1] - predicted_values[-1])

    max_absolute_error = last_error
    max_exact_value = exact_values[0]
    max_predicted_value = predicted_values[0]

    min_absolute_error = last_error
    min_exact_value = exact_values[0]
    min_predicted_value = predicted_values[0]

    for i in range(1, len(x_axis)):
        error = abs(exact_values[i] - predicted_values[i])

        if error > max_absolute_error:
            max_absolute_error = error
            max_exact_value = exact_values[i]
            max_predicted_value = predicted_values[i]

        if 0 < error < min_absolute_error:
            min_absolute_error = error
            min_exact_value = exact_values[i]
            min_predicted_value = predicted_values[i]

    mean_absolute_error = total_absolute_error / num_tests
    mean_relative_error = total_relative_error / num_tests

    if save_model:
        pickle.dump(model, open(r'E:\IC\Interface_Grafica\Dados_verificacao\modelo_svr.sav', 'wb'))

    return (
        score,
        mean_absolute_error,
        mean_relative_error,
        max_absolute_error,
        max_exact_value,
        max_predicted_value,
        min_absolute_error,
        min_exact_value,
        min_predicted_value,
        exact_values,
        predicted_values,
        x_axis
    )
