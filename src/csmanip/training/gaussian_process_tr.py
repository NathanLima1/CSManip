from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, DotProduct, WhiteKernel, RationalQuadratic
import pickle
import os

def gaussian_process_regression(self, city, indicator_code, division, num_tests, kernel_type, 
                                len_scale, nu, sigma_0, alpha_rq, alpha, n_restart_optimizer, normalize_y, save_model):
    """
    Applies Gaussian Process Regression (GPR) for predictive analysis.

    Parameters:
        city (str): Name of the city.
        indicator_code (int): Code representing the weather indicator.
        division (float): Data split ratio.
        num_tests (int): Number of test iterations.
        kernel_type (str): Type of kernel ('RBF', 'Matern', 'DotProduct', 'RationalQuadratic').
        kernel_params (dict): Parameters specific to the kernel.
        alpha (float): Value added to the diagonal of the kernel matrix during fitting.
        n_restart_optimizer (int): Optimizer for hyperparameter tuning.
        normalize_y (bool): Whether to normalize the target values.
        save_model (bool): Whether to save the trained model.

    Returns:
        tuple: Evaluation metrics and prediction data.
    """
    train_features, train_targets, val_features, val_targets = self.prepare_matrix_by_city(city, division, indicator_code)
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

    # Escolher kernel baseado no parâmetro
    if kernel_type == 'RBF':
        kernel = RBF(length_scale=len_scale)
    elif kernel_type == 'Matern':
        kernel = Matern(length_scale=len_scale,
                        nu=nu)
    elif kernel_type == 'DotProduct':
        kernel = DotProduct(sigma_0=sigma_0)
    elif kernel_type == 'RationalQuadratic':
        kernel = RationalQuadratic(length_scale=len_scale,
                                   alpha=alpha_rq)
    else:
        kernel = RBF(1.0)  # default

    for test_round in range(num_tests):
        model = GaussianProcessRegressor(
            kernel=kernel,
            alpha=alpha,
            optimizer=None,
            n_restarts_optimizer=n_restart_optimizer,
            normalize_y=normalize_y
        )
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
        with open(os.path.join(os.getcwd(), 'modelo_gp.sav'), 'wb') as f:
            pickle.dump(model, f)

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