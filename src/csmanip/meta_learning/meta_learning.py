from data_processing.data_processing import DataProcessing
from training.training import Training
from triangulation.triangulation import Triangulation
from math import floor
import pyscreenshot
import os
from sklearn import tree
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from meta_learning.view import View
from meta_learning.gen_param import generate_param
from meta_learning.customized_meta_l import customized_meta_learning
from meta_learning.combine_meta_l import combine_meta_learning
from styles import colors


class MetaLearning:
    def prepare_input(self, indicator, sliding_window):
        if indicator == 1:
            focus_column = 3
        elif indicator == 2:
            focus_column = 4
        else: 
            focus_column = 5

        data_processor = DataProcessing()
        raw_data = data_processor.get_file('Dados comum')

        data_matrix = []
        for row in raw_data:  # Build a matrix with year, month, day and focus value
            processed_row = [
                float(row[0]),
                float(row[1]),
                float(row[2]),
                float(row[focus_column])
            ]
            data_matrix.append(processed_row)

        normalizer = Training()
        normalized_data = normalizer.normalize(data_matrix)  # Normalize each column and each row

        if sliding_window == 'Sim':
            input_matrix, target_matrix = self.sliding_window_matrix(normalized_data)  # Prepare data using sliding window format
        else:
            input_matrix, target_matrix = self.standard_input(normalized_data)

        model1_inputs, model1_targets = [], []
        model2_inputs, model2_targets = [], []  # For level-0 learning to make predictions, which will be used by the meta-learner
        model3_inputs, model3_targets = [], []

        total_samples = len(input_matrix)
        split_point1 = floor(total_samples * 0.4)
        split_point2 = split_point1 * 2

        for index in range(total_samples):  # Split the data into portions
            if index <= split_point1:
                model1_inputs.append(input_matrix[index])
                model1_targets.append(target_matrix[index])
            elif split_point1 < index <= split_point2:
                model2_inputs.append(input_matrix[index])
                model2_targets.append(target_matrix[index])
            else:
                model3_inputs.append(input_matrix[index])
                model3_targets.append(target_matrix[index])

        return (
            model1_inputs, model1_targets,
            model2_inputs, model2_targets,
            model3_inputs, model3_targets
        )
    
    def sliding_window(self, data):
        matrix = []
        result = []

        for i in range(len(data)):
            buff = []
            try:
                for j in range(5):
                    buff.append(data[i+j][0])
                    buff.append(data[i+j][1])
                    buff.append(data[i+j][2])
                    buff.append(data[i+j][3])
                if len(buff) == 20:
                    matrix.append(buff[:19])
                    result.append(buff[19])
            except IndexError:
                pass
        return matrix, result
    
    def common_input(self, data):
        matrix = list()
        result = list()
        
        for i in range(len(data)):
            buff = list()
            buff.append(data[i][0])
            buff.append(data[i][1])
            buff.append(data[i][2])
            matrix.append(buff)

            result.append(data[i][3])

        return matrix, result
    
    def base_learn(self, model_name, pretrained, num_tests,
               train_inputs, train_targets,
               validation_inputs, validation_targets,
               predict_inputs, predict_targets, sliding_window):

        if pretrained == 0:
            if model_name == 'Decision Trees':
                base_learner = tree.DecisionTreeRegressor()
            elif model_name == 'Neural network':
                base_learner = MLPRegressor()
            elif model_name == 'Nearest Neighbors':
                base_learner = KNeighborsRegressor()
            elif model_name == 'Support Vector':
                base_learner = SVR()

        total_relative_error = 0
        total_absolute_error = 0
        total_r2_score = 0

        for test_index in range(num_tests):
            base_learner = base_learner.fit(train_inputs, train_targets)
            
            fold_absolute_error = 0
            fold_relative_error = 0
            total_r2_score += base_learner.score(validation_inputs, validation_targets)

            for sample_index in range(len(validation_inputs)):
                expected_value = float(validation_targets[sample_index])
                predicted_value = float(base_learner.predict([validation_inputs[sample_index]])[0])
                
                absolute_error = abs(expected_value - predicted_value)
                relative_error = absolute_error / expected_value

                fold_absolute_error += absolute_error
                fold_relative_error += relative_error

            total_absolute_error += fold_absolute_error / len(validation_inputs)
            total_relative_error += fold_relative_error / len(validation_inputs)

        mean_absolute_error = total_absolute_error / num_tests
        mean_relative_error = total_relative_error / num_tests
        error_percentage = mean_absolute_error * 100
        mean_r2_score = total_r2_score / num_tests

        # Preparing level-0 learner predictions for level-1 learner
        prepared_predict_matrix = []
        
        if sliding_window == 'Sim':
            for i in range(len(predict_inputs)):
                predicted_value = float(base_learner.predict([predict_inputs[i]])[0])
                prepared_sample = [
                    predict_inputs[i][16],
                    predict_inputs[i][17],
                    predict_inputs[i][18],
                    predicted_value
                ]
                prepared_predict_matrix.append(prepared_sample)
        else:
            for i in range(len(predict_inputs)):
                predicted_value = float(base_learner.predict([predict_inputs[i]])[0])
                prepared_sample = [
                    predict_inputs[i][0],
                    predict_inputs[i][1],
                    predict_inputs[i][2],
                    predicted_value
                ]
                prepared_predict_matrix.append(prepared_sample)

        return prepared_predict_matrix, mean_absolute_error, mean_relative_error, error_percentage, mean_r2_score
    
    def triangula(self, metodo, focus):
        triang = Triangulation()
        nor = Training()
        if metodo == 'Inverse Distance Weighted':
            triang.idw(focus)
            matriz_triang = nor.normalize(triang.get_idw()[5])
            x,y,alv_y, erro_abs, erro_rel, mat_ext = triang.get_idw()
            erro_abs, erro_rel = self.calcula_erro_tri(alv_y, y)
        elif metodo == 'Arithmetic Average':
            triang.avg(focus)
            matriz_triang = nor.normalizar(triang.get_aa()[5])
            x,y,alv_y, erro_abs, erro_rel, mat_ext = triang.get_avg()
            erro_abs, erro_rel = self.calcula_erro_tri(alv_y, y)
        elif metodo == 'Regional Weight':
            triang.rw(focus)
            matriz_triang = nor.normalizar(triang.get_rw()[5])
            x,y,alv_y, erro_abs, erro_rel, mat_ext = triang.get_rw()
            erro_abs, erro_rel = self.calcula_erro_tri(alv_y, y)
        elif metodo == 'Optimized Normal Ratio':
            triang.onr(focus)
            matriz_triang = nor.normalizar(triang.get_onr()[5])
            x,y,alv_y, erro_abs, erro_rel, mat_ext = triang.get_onr()
            erro_abs, erro_rel = self.calcula_erro_tri(alv_y, y)

        tamanho = len(matriz_triang)
        t1 = floor(tamanho * 0.4)
        t2 = t1 * 2

        matriz_final_data = list()
        matriz_final_dado = list()
        
        for i in range(len(matriz_triang)):
            if i > t1 and i <= t2:
                aux = list()
                aux.append(matriz_triang[i][0])
                aux.append(matriz_triang[i][1])
                aux.append(matriz_triang[i][2])
                matriz_final_data.append(aux)
                matriz_final_dado.append(matriz_triang[i][3])
                

        return matriz_final_data, matriz_final_dado, erro_abs, erro_rel
       
    def calculate_error_tri(self, x, y):
        training = Training()
        mat1 = training.normalize(x)
        mat2 = training.normalize(y)
        
        sum_ea = 0
        sum_er = 0
        for i in range(len(mat1)):
            ea = abs(float(mat1[i]) - float(mat2[i]))
            er = ea / float(mat1[i])

            sum_ea += ea
            sum_er += er

        ea = sum_ea / len(mat1)
        er = sum_er / len(mat2)
        return ea, er
    
    def customized_meta_learning(self, indicator, base_l, triangulation_method, meta_l, pre1, pre2, n_test, sliding_window):
        return customized_meta_learning(self, indicator, base_l, triangulation_method, meta_l, pre1, pre2, n_test, sliding_window)

    def combine_meta_learning(self, target, pre1, pre2, n_test, window):
        return combine_meta_learning(self, target, pre1, pre2, n_test, window)

    def valid_maxf(self, val):
        if val.isdigit() == True:
            val = int(val)
        elif val.isalnum() == True and val.isdigit() == False:
            val = str(val)
        elif val.isalnum() == False and val.isdigit() == False and val.isalpha() == False:
            val = float(val)
        
        return val
    
    def salvar_paramt(self):
        img = pyscreenshot.grab(bbox=(0, 25, 1920, 1040))
        img.show()
        
        path = os.path.join(os.getcwd(), 'teste.png')
        img.save(path)

    def data_preview(self, pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x):
        v = View()
        v.data_preview(self, pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)

    def get_end(self, cidade):
        treatment = DataProcessing()
        return treatment.get_file_path(cidade)

    def generate_preview_dt(self):
        v = View()
        v.generate_preview_dt(self)
    
    def generate_preview_nn(self):
        """
        Generates a preview of the model Nearest Neighbors
        """
        v = View()
        v.generate_preview_nn(self)
    
    def generate_preview_svm(self):
        """
        Generates a preview of the model Support Vector Machine
        """
        v = View()
        v.generate_preview_svm(self)
    
    def generate_preview_Kn(self):
        """
        Generates a preview o K Neighbors
        """
        v = View()
        v.generate_preview_Kn

    def generate_param(self):
        generate_param(self)