from sklearn import tree
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from math import floor

def combine_meta_learning(self, target, pre1, pre2, n_test, window):
        machine_learning_models = ['None', 'Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector']
        interpolation_methods = ['None', 'Arithmetic Average', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']
        meta_models = ['Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector']

        all_models = []
        ranked_models = []

        if target == 'Precipitação':
            indicator = 1
        elif target == 'Temperatura máxima':
            indicator = 2
        else:
            indicator = 3

        m1_40_t, m1_40_r, m2_40_t, m2_40_r, m3_20_t, m3_20_r = self.prepara_input(indicator, window)

        log_file = open('meta_comb.txt', 'w')
        csv_results = open('meta_res.csv', 'w')
        csv_best = open('meta_best_results.csv', 'w')

        csv_results.write("Model;Machine Learning;Interpolation;Meta Learning;Absolute Error;Relative Error;Error(%);R2;\n")
        csv_best.write("Model;Error(%);\n")

        models_scores = {}
        model_counter = 1

        for i in range(len(machine_learning_models)):
            for j in range(len(interpolation_methods)):
                for k in range(len(meta_models)):
                    if machine_learning_models[i] == 'None' and interpolation_methods[j] == 'None':
                        k += 1  # Skip invalid combination
                    else:
                        if machine_learning_models[i] != 'None':
                            input_matrix, abs_err_base, rel_err_base, perc_err_base, r2_base = self.base_learn(
                                machine_learning_models[i], 0, n_test, m1_40_t, m1_40_r, m3_20_t, m3_20_r, m2_40_t, m2_40_r, window
                            )
                            del input_matrix[:2]

                        if interpolation_methods[j] != 'None':
                            _, interp_matrix, interp_abs_err, interp_rel_err = self.triangula(interpolation_methods[j], indicator)
                            del interp_matrix[:4]

                        base_dates, _, _, _ = self.triangula('Arithmetic Average', indicator)
                        del base_dates[:4]
                        del m2_40_r[:2]

                        final_matrix = []
                        for l in range(len(base_dates)):
                            entry = []
                            if machine_learning_models[i] == 'None' and interpolation_methods[j] != 'None':
                                entry.extend([base_dates[l][0], base_dates[l][1], base_dates[l][2], interp_matrix[l]])
                            elif interpolation_methods[j] == 'None' and machine_learning_models[i] != 'None':
                                entry.extend([base_dates[l][0], base_dates[l][1], base_dates[l][2], input_matrix[l][3]])
                            else:  # Both methods are used
                                entry.extend([base_dates[l][0], base_dates[l][1], base_dates[l][2], interp_matrix[l], input_matrix[l][3]])
                            final_matrix.append(entry)

                        os.system('cls')  # Clear terminal
                        print(f"{final_matrix[0]} ---")

                        if pre2 == 0:
                            if meta_models[k] == 'Decision Trees':
                                meta_learner = tree.DecisionTreeRegressor()
                            elif meta_models[k] == 'Neural network':
                                meta_learner = MLPRegressor()
                            elif meta_models[k] == 'Nearest Neighbors':
                                meta_learner = KNeighborsRegressor()
                            elif meta_models[k] == 'Support Vector':
                                meta_learner = SVR()

                        train_split = len(m2_40_r) - floor(len(m2_40_r) * 0.2)
                        X_train, Y_train, X_test, Y_test = [], [], [], []

                        for n in range(len(m2_40_r)):
                            try:
                                if n <= train_split:
                                    X_train.append(final_matrix[n])
                                    Y_train.append(m2_40_r[n])
                                else:
                                    X_test.append(final_matrix[n])
                                    Y_test.append(m2_40_r[n])
                            except IndexError:
                                pass

                        total_r2 = 0
                        total_abs_error = 0
                        total_rel_error = 0

                        for _ in range(n_test):
                            meta_learner.fit(X_train, Y_train)
                            total_r2 += meta_learner.score(X_test, Y_test)

                            fold_abs_error = 0
                            fold_rel_error = 0
                            for m in range(len(X_test)):
                                predicted = meta_learner.predict([X_test[m]])[0]
                                actual = Y_test[m]

                                error_abs = abs(actual - predicted)
                                error_rel = error_abs / actual

                                fold_abs_error += error_abs
                                fold_rel_error += error_rel

                            total_abs_error += fold_abs_error / len(X_test)
                            total_rel_error += fold_rel_error / len(X_test)

                        avg_abs_error = total_abs_error / n_test
                        avg_rel_error = total_rel_error / n_test
                        avg_percent_error = avg_abs_error * 100
                        avg_r2 = total_r2 / n_test

                        log_line = f"{model_counter} -> Machine Learning: {machine_learning_models[i]} || Interpolation: {interpolation_methods[j]} || Meta Learning: {meta_models[k]} |Tests: {n_test}| --> Abs Error: {avg_abs_error} | Rel Error: {avg_rel_error} | Error(%): {avg_percent_error} | R2: {avg_r2}"
                        log_file.write(log_line + "\n")

                        csv_line = f"{model_counter};{machine_learning_models[i]};{interpolation_methods[j]};{meta_models[k]};{str(avg_abs_error).replace('.', ',')};{str(avg_rel_error).replace('.', ',')};{str(avg_percent_error).replace('.', ',')};{str(avg_r2).replace('.', ',')};\n"
                        csv_results.write(csv_line)

                        models_scores[str(model_counter)] = avg_percent_error

                        all_models.append([
                            model_counter,
                            machine_learning_models[i],
                            interpolation_methods[j],
                            meta_models[k],
                            n_test,
                            round(avg_abs_error, 4),
                            round(avg_rel_error, 4),
                            round(avg_percent_error, 4),
                            round(avg_r2, 4)
                        ])

                        model_counter += 1

        for model_id in sorted(models_scores, key=models_scores.get):
            csv_best.write(f"{model_id};{str(models_scores[model_id]).replace('.', ',')};\n")
            ranked_models.append([model_id, str(models_scores[model_id]).replace('.', ',')])

        log_file.close()
        csv_results.close()
        csv_best.close()

        return all_models, ranked_models