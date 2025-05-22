from training.neural_network_tr import neural_network
from training.k_neighbors_tr import KNeighbors
from training.support_vector_tr import support_vector_regression
from training.decision_tree_tr import decision_tree
from math import floor
from data_processing.data_processing import DataProcessing

class Training:
    def decision_tree(
        self, city: str, indicator_code: int, split_ratio: float, criterion: str, splitter: str,
        max_depth: int, min_samples_leaf: int, max_features, max_leaf_nodes: int,
        n_tests: int, min_samples_split: int, min_weight_fraction_leaf: float,
        min_impurity_decrease: float, ccp_alpha: float, save_model: bool
        ):
        return decision_tree(
            self, city, indicator_code, split_ratio, criterion, splitter,
            max_depth, min_samples_leaf, max_features, max_leaf_nodes,
            n_tests, min_samples_split, min_weight_fraction_leaf,
            min_impurity_decrease, ccp_alpha, save_model)
    
    def neural_network(
        self, city: str, indicator_code: int, split_ratio: float, n_tests: int,
        activation: str, solver: str, alpha: float, batch_size, learning_rate: str,
        learning_rate_init: float, power_t: float, max_iter: int, shuffle: bool,
        tol: float, verbose: bool, warm_start: bool, momentum: float,
        nesterovs_momentum: bool, early_stopping: bool, validation_fraction: float,
        beta_1: float, beta_2: float, n_iter_no_change: int, max_fun: int
        ):
        return neural_network(
            self, city, indicator_code, split_ratio, n_tests,
            activation, solver, alpha, batch_size, learning_rate,
            learning_rate_init, power_t, max_iter, shuffle,
            tol, verbose, warm_start, momentum,
            nesterovs_momentum, early_stopping, validation_fraction,
            beta_1, beta_2, n_iter_no_change, max_fun)
    
    def KNeighbors(self, city, indicator_index, split_ratio, n_tests, n_neighbors,
         algorithm, leaf_size, p_value, n_jobs, save_model):
        return KNeighbors(self, city, indicator_index, split_ratio, n_tests,
                               n_neighbors, algorithm, leaf_size, p_value, n_jobs, save_model)
    
    def support_vector_regression(self, city, indicator_code, division, num_tests, kernel,
         degree, gamma, coef0, tol, C, epsilon, shrinking, cache_size, verbose, max_iter, save_model):
        return support_vector_regression(self, city, indicator_code, division, num_tests, kernel,
                degree, gamma, coef0, tol, C, epsilon, shrinking, cache_size, verbose, max_iter, save_model)
    
    def prepare_matrix(self, file_path, division, indicator, n_test):
        """
        Prepares the training and validation matrices from a given file.

        Args:
            file_path (str): Path to the input file.
            division (int): Percentage of the data to be used for training.
            indicator (int): The selected indicator (e.g., precipitation, temperature).
            n_test (int): The number of test iterations.

        Returns:
            tuple: Training and validation matrices and results.
        """
        normalizer = DataProcessing()

        matrix = []
        aux_data = []
        results = []

        with open(file_path, 'r') as file:
            for line in file:
                row = []
                line = line.strip().replace("'", '').replace(" ", '').split(',')
                row.append(int(line[2]))  # Day
                row.append(int(line[1]))  # Month
                row.append(int(line[0]))  # Year
                row.append(float(line[indicator]))  # Selected indicator by user
                aux_data.append(row)

        normalized_data = normalizer.normalize_data(aux_data)

        for i in range(len(normalized_data)):
            row = []
            try:
                for j in range(5):
                    row.append(normalized_data[i + j][0])  # Year
                    row.append(normalized_data[i + j][1])  # Month
                    row.append(normalized_data[i + j][2])  # Day
                    row.append(normalized_data[i + j][3])  # Indicator value
                if len(row) == 20:
                    matrix.append(row[:19])
                    results.append(row[19])
            except IndexError:
                pass
        
        split_index = floor(len(matrix) * (division / 100))
        train_matrix = []
        train_results = []
        val_matrix = []
        val_results = []

        for i in range(len(matrix)):
            if i <= split_index:
                train_matrix.append(matrix[i])
                train_results.append(results[i])
            else:
                val_matrix.append(matrix[i])
                val_results.append(results[i])

        return train_matrix, train_results, val_matrix, val_results

    def prepare_matrix_by_city(self, city, division, indicator):
        """
        Prepares the training and validation matrices for a given city and indicator.

        Args:
            city (str): The target city ('Target City', 'Neighbor A', 'Neighbor B').
            division (int): Percentage of the data to be used for training.
            indicator (int): The selected indicator (e.g., precipitation, max temperature).

        Returns:
            tuple: Training and validation matrices and results.
        """
        matrix = []
        aux_data = []
        results = []

        focus_column = self._get_focus_column(city, indicator)

        t = DataProcessing()
        data = t.get_data('Common Data')

        for row in data:
            entry = [int(row[0]), int(row[1]), int(row[2]), float(row[focus_column])]
            aux_data.append(entry)

        normalized_data = t.normalize_data(aux_data)

        for i in range(len(normalized_data)):
            row = []
            try:
                for j in range(5):
                    row.append(normalized_data[i + j][0])  # Year
                    row.append(normalized_data[i + j][1])  # Month
                    row.append(normalized_data[i + j][2])  # Day
                    row.append(normalized_data[i + j][3])  # Indicator value
                if len(row) == 20:
                    matrix.append(row[:19])
                    results.append(row[19])
            except IndexError:
                pass

        split_index = floor(len(matrix) * (division / 100))
        train_matrix = []
        train_results = []
        val_matrix = []
        val_results = []

        for i in range(len(matrix)):
            if i <= split_index:
                train_matrix.append(matrix[i])
                train_results.append(results[i])
            else:
                val_matrix.append(matrix[i])
                val_results.append(results[i])

        return train_matrix, train_results, val_matrix, val_results

    def prepare_matrix_with_indicators(self, file_path, division, indicators, focus, normalize):
        """
        Prepares the training and validation matrices with specific indicators.

        Args:
            file_path (str): Path to the input file.
            division (int): Percentage of the data to be used for training.
            indicators (list): List of selected indicators.
            focus (int): The focus column for prediction.
            normalize (bool): Whether to normalize the data.

        Returns:
            tuple: Training and validation matrices and results.
        """
        matrix = []
        results = []

        with open(file_path, 'r') as file:
            for line in file:
                row = []
                line = line.strip().replace("'", '').replace(" ", '').split(',')
                row.append(int(line[2]))  # Day
                row.append(int(line[1]))  # Month
                row.append(int(line[0]))  # Year
                for indicator in indicators:
                    row.append(float(line[indicator]))
                results.append(float(line[focus]))
                matrix.append(row)

        split_index = floor(len(matrix) * (division / 100))
        train_matrix = []
        train_results = []
        val_matrix = []
        val_results = []

        if normalize:
            normalized_results = self.normalize(results)
            normalized_matrix = self.normalize(matrix)

            for i in range(len(matrix)):
                if i <= split_index:
                    train_matrix.append(normalized_matrix[i])
                    train_results.append(normalized_results[i])
                else:
                    val_matrix.append(normalized_matrix[i])
                    val_results.append(normalized_results[i])
        else:
            for i in range(len(matrix)):
                if i <= split_index:
                    train_matrix.append(matrix[i])
                    train_results.append(results[i])
                else:
                    val_matrix.append(matrix[i])
                    val_results.append(results[i])

        return train_matrix, train_results, val_matrix, val_results

    def normalize(self, data):
        """
        Normalizes the input data.

        Args:
            data (list): List of data values to normalize.

        Returns:
            list: Normalized data.
        """
        try:
            max_min = []
            num_columns = len(data[0])

            for i in range(num_columns):
                column_data = [float(data[j][i]) for j in range(len(data))]
                max_min.append(max(column_data))
                max_min.append(min(column_data))

            normalized_data = []
            for row in data:
                normalized_row = []
                for i in range(num_columns):
                    max_val = max_min[i * 2]
                    min_val = max_min[i * 2 + 1]
                    normalized_value = ((float(row[i]) - min_val) / (max_val - min_val)) * 0.6 + 0.2
                    normalized_row.append(normalized_value)
                normalized_data.append(normalized_row)

        except TypeError:
            max_val = max(data)
            min_val = min(data)
            normalized_data = [(float(value) - min_val) / (max_val - min_val) * 0.6 + 0.2 for value in data]

        return normalized_data

    def _get_focus_column(self, city, indicator):
        """
        Determines the focus column based on the city and indicator.

        Args:
            city (str): The target city.
            indicator (int): The selected indicator.

        Returns:
            int: The focus column index.
        """
        if city == 'Target city':
            return indicator
        elif city == 'Neighbor A':
            return 3 + indicator
        elif city == 'Neighbor B':
            return 6 + indicator
        else:
            return 9 + indicator