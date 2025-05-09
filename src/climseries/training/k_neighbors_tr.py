import pickle
from sklearn.neighbors import KNeighborsRegressor


def KNeighbors(self, city, indicator_index, split_ratio, n_tests, n_neighbors, algorithm, leaf_size, p_value, n_jobs, save_model):
    """
    Performs K-Nearest Neighbors regression for weather indicator prediction.

    Parameters:
    ----------
    city : str
        Name of the city.
    indicator_index : int
        Index of the weather indicator (3: Precipitation, 4: Maximum temperature, others: Minimum temperature).
    split_ratio : float
        Ratio used to split the dataset into training and validation sets.
    n_tests : int
        Number of repeated tests.
    n_neighbors : int
        Number of neighbors used by the KNN model.
    algorithm : str
        Algorithm used to compute the nearest neighbors.
    leaf_size : int
        Maximum size of leaf in the tree.
    p_value : int
        Power parameter for the Minkowski distance metric.
    n_jobs : int
        Number of parallel jobs to run.
    save_model : int
        Flag to save the trained model (1 to save, 0 otherwise).

    Returns:
    -------
    tuple
        A tuple containing:
        - Score (float): Prediction accuracy score.
        - Mean absolute error (float).
        - Mean relative error (float).
        - Highest absolute error and its real and predicted values.
        - Lowest absolute error and its real and predicted values.
        - Lists for exact Y values, predicted Y values, and X axis points.
    """
    X_train, y_train, X_val, y_val = self.prepara_matriz3(city, split_ratio, indicator_index)
    total_relative_error = 0
    total_absolute_error = 0

    exact_y_values = []
    predicted_y_values = []
    x_axis_points = []
    counter = 1

    # Define the indicator name
    if indicator_index == 3:
        indicator_name = 'Precipitation'
    elif indicator_index == 4:
        indicator_name = 'Maximum Temperature'
    else:
        indicator_name = 'Minimum Temperature'

    for test in range(n_tests):
        model = KNeighborsRegressor(
            n_neighbors=n_neighbors,
            algorithm=algorithm,
            leaf_size=leaf_size,
            p=p_value,
            n_jobs=n_jobs
        )
        model.fit(X_train, y_train)

        absolute_error_sum = 0
        relative_error_sum = 0

        for i in range(len(X_val)):
            actual_value = y_val[i]
            predicted_value = model.predict([X_val[i]])[0]

            if test != n_tests:
                exact_y_values.append(actual_value)
                predicted_y_values.append(predicted_value)
                x_axis_points.append(counter)
                counter += 1

            absolute_error = abs(actual_value - predicted_value)
            relative_error = absolute_error / actual_value

            absolute_error_sum += absolute_error
            relative_error_sum += relative_error

        total_absolute_error += absolute_error_sum / len(X_val)
        total_relative_error += relative_error_sum / len(X_val)

    score = round((((total_relative_error / n_tests) * 100) - 100) * -1, 2)

    last_error = abs(exact_y_values[-1] - predicted_y_values[-1])

    max_error = last_error
    max_error_actual = exact_y_values[0]
    max_error_predicted = predicted_y_values[0]

    min_error = last_error
    min_error_actual = exact_y_values[0]
    min_error_predicted = predicted_y_values[0]

    for i in range(1, len(x_axis_points)):
        error = abs(exact_y_values[i] - predicted_y_values[i])
        if error > max_error:
            max_error = error
            max_error_actual = exact_y_values[i]
            max_error_predicted = predicted_y_values[i]

        if 0 < error < min_error:
            min_error = error
            min_error_actual = exact_y_values[i]
            min_error_predicted = predicted_y_values[i]

    mean_absolute_error = total_absolute_error / n_tests
    mean_relative_error = total_relative_error / n_tests

    if save_model == 1:
        pickle.dump(model, open(r'E:\IC\Interface_Grafica\Dados_verificacao\modelo_kn.sav', 'wb'))

    return (
        score,
        mean_absolute_error,
        mean_relative_error,
        max_error,
        max_error_actual,
        max_error_predicted,
        min_error,
        min_error_actual,
        min_error_predicted,
        exact_y_values,
        predicted_y_values,
        x_axis_points
    )
