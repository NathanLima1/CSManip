from sklearn import tree
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

def customized_meta_learning(self, indicator, base_l, triangulation_method, meta_l, pre1, pre2, n_test, sliding_window):
        m1_40_t, m1_40_r, m2_40_t, m2_40_r, m3_20_t, m3_20_r = self.prepare_input(indicator, sliding_window)

        if base_l != 'Nenhum':
            input_matrix, base_ea, base_er, base_percentage, base_r2 = self.base_learn(
                base_l, 0, n_test, m1_40_t, m1_40_r, m3_20_t, m3_20_r, m2_40_t, m2_40_r, sliding_window
            )
            del input_matrix[:2]

        if triangulation_method != 'Nenhum':
            _, triangulation_matrix, tria_ea, tria_er = self.triangula(triangulation_method, indicator)
            del triangulation_matrix[:4]

        data_matrix, _, _, _ = self.triangula('Arithmetic Average', indicator)
        del data_matrix[:4]
        del m2_40_r[:2]

        final_matrix = []
        final_results = []

        for i in range(len(data_matrix)):
            aux = []
            if base_l == 'Nenhum':
                aux.extend([data_matrix[i][0], data_matrix[i][1], data_matrix[i][2], triangulation_matrix[i]])
            elif triangulation_method == 'Nenhum':
                aux.extend([data_matrix[i][0], data_matrix[i][1], data_matrix[i][2], input_matrix[i][3]])
            else:
                aux.extend([data_matrix[i][0], data_matrix[i][1], data_matrix[i][2], triangulation_matrix[i], input_matrix[i][3]])
            final_matrix.append(aux)

        if pre2 == 0:
            if meta_l == 'Decision Trees':
                level1_learner = tree.DecisionTreeRegressor()
            elif meta_l == 'Neural network':
                level1_learner = MLPRegressor()
            elif meta_l == 'Nearest Neighbors':
                level1_learner = KNeighborsRegressor()
            elif meta_l == 'Support Vector':
                level1_learner = SVR()

        total_size = len(final_matrix)
        train_limit = total_size - floor(total_size * 0.2)

        x_train = []
        y_train = []
        x_test = []
        y_test = []

        for i in range(total_size):
            if i <= train_limit:
                x_train.append(final_matrix[i])
                y_train.append(m2_40_r[i])
            else:
                x_test.append(final_matrix[i])
                y_test.append(m2_40_r[i])

        r2_sum = 0
        total_absolute_error = 0
        total_relative_error = 0

        x_meta = []
        y_meta = []
        y_target = []
        x_counter = 0

        for _ in range(n_test):
            level1_learner = level1_learner.fit(x_train, y_train)
            r2_sum += level1_learner.score(x_test, y_test)

            fold_absolute_error = 0
            fold_relative_error = 0

            for j in range(len(x_test)):
                expected_value = float(y_test[j])
                predicted_value = float(level1_learner.predict([x_test[j]])[0])

                y_meta.append(predicted_value)
                y_target.append(expected_value)
                x_meta.append(x_counter)
                x_counter += 1

                absolute_error = abs(expected_value - predicted_value)
                relative_error = absolute_error / expected_value

                fold_absolute_error += absolute_error
                fold_relative_error += relative_error

            total_absolute_error += fold_absolute_error / len(x_test)
            total_relative_error += fold_relative_error / len(x_test)

        meta_ea = total_absolute_error / n_test
        meta_er = total_relative_error / n_test
        meta_percentage_error = meta_ea * 100
        meta_r2 = r2_sum / n_test

        if base_l == 'Nenhum':
            return meta_ea, meta_er, meta_percentage_error, meta_r2, x_meta, y_meta, y_target, 0, 0, 0, 0, tria_ea, tria_er
        elif triangulation_method == 'Nenhum':
            return meta_ea, meta_er, meta_percentage_error, meta_r2, x_meta, y_meta, y_target, base_ea, base_er, base_percentage, base_r2, 0, 0
        else:
            return meta_ea, meta_er, meta_percentage_error, meta_r2, x_meta, y_meta, y_target, base_ea, base_er, base_percentage, base_r2, tria_ea, tria_er
