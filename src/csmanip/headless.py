from tkinter import Frame
from tkinter import ttk
from tkinter import Canvas, Label, StringVar, Button, CENTER, DISABLED
import tkinter.filedialog as dlg
import tkinter.messagebox as msg
from matplotlib.figure import Figure
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import os
import numpy as np
import threading
import time
import sys
from .styles import colors
from .data_processing.data_processing import DataProcessing
from .triangulation.triangulation import Triangulation
from .machine_learning.machine_learning import MachineLearning
from .machine_learning.ml import Ml
from .training.hiperparam import Hiperparam
from .meta_learning.meta_learning import MetaLearning
from .meta_learning.test_generat import TestsGenerator
from .data_processing.era5_download import download_and_process_era_data
from .data_processing.noaa_download import download_noaa_data

class Headless():
    def __init__(self):
        self.all_city_names = []
        self.city_path_list = []

    def get_info(self, directory):  # Function that opens the folder with .csv files and returns important data
        print("Entrou Headless get_info")
        raw_data = []

        with open(directory, 'r') as file:
            for line in file:
                text = line.replace('\n', '')
                raw_data.append(text)
        # Remove the last element from the list
        if raw_data:
            del raw_data[-1]

        name = raw_data[0][6:]
        latitude = float(raw_data[2][10:])
        longitude = float(raw_data[3][10:])
        altitude = float(raw_data[4][10:])
        address = directory

        return name, latitude, longitude, altitude, address
    
    def set_cities(self, files):
        if(len(files) != 4): 
            raise TypeError("It must have 4 file paths")
        
        for city in files:
            name, lat, lon, alt, address = self.get_info(city)
            self.all_city_names.append(name)
            self.city_path_list.append([name, address])

        self.target_city = self.all_city_names[0]
        self.neighbor_a = self.all_city_names[1]
        self.neighbor_b = self.all_city_names[2]
        self.neighbor_c = self.all_city_names[3]

    def loading_animation(self, stop_event):
        dots = ['.', '..', '...', '.']
        step = 0
        while not stop_event.is_set():
            sys.stdout.write('\rLoading' + dots[step % len(dots)])
            sys.stdout.flush()
            step += 1
            time.sleep(0.5)
        sys.stdout.write('\rDone!            \n')

    def process_selection(self):
        if (
            self.target_city == ''
            or self.neighbor_a == ''
            or self.neighbor_b == ''
            or self.neighbor_c == ''
        ):
            raise  TypeError("Data is incomplete. One or more cities are not selected")
        
        self.city_history = [
            self.target_city,
            self.neighbor_a,
            self.neighbor_b,
            self.neighbor_c
        ]
        self.history_var = ""

        target_path = ''
        for city_name, path in self.city_path_list:
            if city_name == self.target_city:
                target_path = path
                break

        neighbor_a_path = ''
        for city_name, path in self.city_path_list:
            if city_name == self.neighbor_a:
                neighbor_a_path = path
                break

        neighbor_b_path = ''
        for city_name, path in self.city_path_list:
            if city_name == self.neighbor_b:
                neighbor_b_path = path
                break

        neighbor_c_path = ''
        for city_name, path in self.city_path_list:
            if city_name == self.neighbor_c:
                neighbor_c_path = path
                break

        try:
            data_processor = DataProcessing()
            data_processor.target = target_path
            data_processor.neighborA = neighbor_a_path
            data_processor.neighborB = neighbor_b_path
            data_processor.neighborC = neighbor_c_path
            data_processor.download_path = os.getcwd()

            self.save_location = os.getcwd()

            # thread para mostrar que está carregando
            stop_event = threading.Event()
            loading_thread = threading.Thread(target=self.loading_animation, args=(stop_event,))
            loading_thread.start()

            data_processor.get_processed_data()

            # thread é juntada novamente
            stop_event.set()
            loading_thread.join()

            print("Sucess! Files selected with sucess!")
        except:
            print("Error! Files could not be selected!")

    def get_col(self, parameter):
        print("Entrou Headless get_col")
        if parameter == "Precipitation":
            y_name = "Precipitation (mm)"
            col = 3
        elif parameter == "Maximum temperature":
            col = 4
            y_name = "Temperature (°C)"
        elif parameter == "Minimum temperature":
            y_name = "Temperature (°C)"
            col = 5
        return y_name, col
    
    def generate_range(self, city, parameter, begin, end):
        print("Entrou Headless generate_range")
        data_p = DataProcessing()
        self.years = data_p.get_year_range(city)

        if begin not in self.years or end not in self.years:
            raise ValueError("The selected year cannot be selected. Select one of these:", self.years)
        if begin > end:
            raise ValueError("The start year cannot be bigger than the end year")
        
        self.first_year = begin
        self.last_year = end
        self.range_graphs(city, parameter)
    
    def common_graphs(self, city: str, parameter: str, begin: int, end: int):
        print("Entrou Headless common_graphs")
        data_processor = DataProcessing()
        analyzed_data = data_processor.load_data_file(city)

        self.generate_range(city, parameter, begin, end)

        y_label, col_index = self.get_col(parameter)

        city_names = data_processor.get_city_names()

        x_axis = []
        data_table = []

        if city == 'Common data':
            y_axis_1, y_axis_2, y_axis_3, y_axis_4 = [], [], [], []
            common_count, target_count, va_count, vb_count, vc_count = data_processor.get_quantities()
            bar_y_values = [common_count, target_count, va_count, vb_count, vc_count]
            bar_x_labels = ['Common', city_names[0], city_names[1], city_names[2], city_names[3]]
        else:
            y_axis = []

        for row in analyzed_data:
            data_table.append(row)
            year, month, day = str(row[0]), str(row[1]), str(row[2])
            date_str = f"{month}/{day}/{year}"

            try:
                date_obj = dt.datetime.strptime(date_str, "%m/%d/%Y").date()
            except ValueError:
                continue

            try:
                if city == 'Common data':
                    y_axis_1.append(float(row[col_index].replace(',', '.')))
                    y_axis_2.append(float(row[col_index + 3].replace(',', '.')))
                    y_axis_3.append(float(row[col_index + 6].replace(',', '.')))
                    y_axis_4.append(float(row[col_index + 9].replace(',', '.')))
                else:
                    y_axis.append(float(row[col_index]))
                x_axis.append(date_obj)
            except ValueError:
                continue

        if city == 'Common data':
            fig, axs = plt.subplots(3, 2, figsize=(14.5, 9.5))
            axs = axs.flatten()

            axs[0].plot(x_axis, y_axis_1, label=city_names[0])
            axs[1].plot(x_axis, y_axis_2, label=city_names[1], color="red")
            axs[2].plot(x_axis, y_axis_3, label=city_names[2], color='green')
            axs[3].plot(x_axis, y_axis_4, label=city_names[3], color='orange')

            axs[4].scatter(x_axis, y_axis_1, s=2, alpha=1, color='blue')
            axs[4].scatter(x_axis, y_axis_2, s=2, alpha=1, color='red')
            axs[4].scatter(x_axis, y_axis_3, s=2, alpha=1, color='green')
            axs[4].scatter(x_axis, y_axis_4, s=2, alpha=1, color='orange')

            axs[5].bar(bar_x_labels, bar_y_values)

            for ax in axs[:5]:
                ax.set_xticks(x_axis[::max(1, len(x_axis) // 10)])
                ax.set_xticklabels([d.strftime("%m/%y") for d in x_axis[::max(1, len(x_axis) // 10)]], rotation=15, ha='right')
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))
                ax.grid(True)
                ax.set_ylabel(y_label)
                ax.legend()

            axs[5].set_ylabel('Data Count')

            plt.tight_layout()
            plt.show()

        else:
            fig, ax = plt.subplots(figsize=(14.5, 9.5))
            ax.plot(x_axis, y_axis)
            ax.set_xticks(x_axis[::max(1, len(x_axis) // 10)])
            ax.set_xticklabels([d.strftime("%m/%y") for d in x_axis[::max(1, len(x_axis) // 10)]], rotation=15, ha='right')
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))
            ax.grid(True)
            ax.set_ylabel(y_label)
            ax.set_title(city)

            plt.tight_layout()
            plt.show()

    def range_graphs(self, city, parameter):
        print("Entrou Headless range_graphs")
        my_data = DataProcessing()
        data_ana = my_data.load_data_file(city)

        nome_y, col = self.get_col(parameter)

        """
        if city == 'Common data':
            self.grafico_dc(city, self.first_year, self.last_year)
            return
        """
        eixo_x = []
        eixo_y = []
        dados_lb = []

        if city == 'Common data':
            eixo_y1 = []
            eixo_y2 = []
            eixo_y3 = []
            eixo_y4 = []
            util, tar, t_va, t_vb, t_vc = my_data.get_quantities()
            eixo_y_bar = [util, tar, t_va, t_vb, t_vc]
            eixo_x_bar = ['Comum', 'target', 'Total vA', 'Total vB', 'Total vC']
        else:
            eixo_y = []

        for i in data_ana:
            if self.first_year <= int(i[0]) <= self.last_year:
                dados_lb.append(i)
                text_data = f"{i[1]}/{i[2]}/{i[0]}"  # mes/dia/ano
                eixo_x.append(dt.datetime.strptime(text_data, "%m/%d/%Y").date())

                if city == 'Common data':
                    eixo_y1.append(float(i[col]))
                    eixo_y2.append(float(i[col + 3]))
                    eixo_y3.append(float(i[col + 6]))
                    eixo_y4.append(float(i[col + 9]))
                else:
                    eixo_y.append(float(i[col]))

        if city == 'Common data':
            fig, axs = plt.subplots(3, 2, figsize=(14.5, 9.5))
            axs = axs.flatten()

            axs[0].plot(eixo_x, eixo_y1, label="target")
            axs[1].plot(eixo_x, eixo_y2, label="Neighbor_a", color="red")
            axs[2].plot(eixo_x, eixo_y3, label="Neighbor_b", color='green')
            axs[3].plot(eixo_x, eixo_y4, label="Neighbor_c", color='orange')

            axs[4].scatter(eixo_x, eixo_y1, s=2, alpha=1, color='blue')
            axs[4].scatter(eixo_x, eixo_y2, s=2, alpha=0.6, color='red')
            axs[4].scatter(eixo_x, eixo_y3, s=2, alpha=0.6, color='green')
            axs[4].scatter(eixo_x, eixo_y4, s=2, alpha=0.6, color='orange')

            axs[5].bar(eixo_x_bar, eixo_y_bar)

            for ax in axs[:5]:
                ax.set_xticks(eixo_x[::max(1, len(eixo_x) // 10)])
                ax.set_xticklabels([d.strftime("%m/%y") for d in eixo_x[::max(1, len(eixo_x) // 10)]], rotation=15, ha='right')
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))
                ax.grid(True)
                ax.set_ylabel(nome_y)
                ax.legend()

            axs[5].set_ylabel('Qtd. de dados')

            plt.tight_layout()
            plt.show()

        else:
            fig, ax = plt.subplots(figsize=(14.5, 9.5))
            ax.plot(eixo_x, eixo_y)

            ax.set_xticks(eixo_x[::max(1, len(eixo_x) // 10)])
            ax.set_xticklabels([d.strftime("%m/%y") for d in eixo_x[::max(1, len(eixo_x) // 10)]], rotation=15, ha='right')
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))
            ax.grid(True)
            ax.set_ylabel(nome_y)
            ax.set_title(city)

            plt.tight_layout()
            plt.show()

    
    def show_map(self):
        triang = Triangulation()
        triang.show_map()

    def download_era5_data(self, city, start_date, end_date):
        download_and_process_era_data(city, start_date, end_date)

    def download_noaa_data(self, city, start_date, end_date):
        download_noaa_data(city, start_date, end_date)

    def triangulation(self, method, parameter):
        print("Entrou headless triangulation")
        trian = Triangulation()

        if parameter == "Precipitation":
            focus = 1
            y_label = "Precipitation (mm)"
        elif parameter == 'Maximum temperature':
            focus = 2
            y_label = "Temperature (°C)"
        elif parameter == "Minimum temperature":
            focus = 3
            y_label = "Temperature (°C)"
        else:
            print("Error! This parameter is not supported!")

        avg = ["Arithmetic Average", "AA", "MA", "Média Aritmética", "avg"]
        idw = ["idw", "IDW", "Inverse Distance Weighted"]
        oidw = ["oidw", "OIDW", "Optimized Inverse Distance Weighted"]
        rw = ["rw", "RW", "Regional Weight"]
        onr = ["onr", "ONR", "Optimized Normal Ratio"]

        if method in avg:
            trian.avg(focus)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, _ = trian.get_avg()
        elif method in idw:
            trian.idw(focus)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, _ = trian.get_idw()
        elif method in oidw:
            trian.oidw(focus)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, _ = trian.get_oidw()
        elif method in rw:
            trian.rw(focus)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, _ = trian.get_rw()
        elif method in onr:
            trian.onr(focus)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, _ = trian.get_onr()
        else:
            raise ValueError("Method of triangulation invalid")
        
        print(f"Method: {method}")
        print()
        print(f"media_ea: {media_ea}, media_er: {media_er}")

        media_ea = round(media_ea, 4)
        media_er = round(media_er, 4)
        title_text = f'Mean absolute error: {media_ea} | Mean relative error: {media_er}'

        plt.figure(figsize=(14.5, 9.5))
        plt.plot(eixo_x, eixo_y_exato, label='Exact', color='green')
        plt.plot(eixo_x, eixo_y_tri, label=method, color='red')
        plt.legend()
        plt.grid(True)
        plt.ylabel(y_label)
        plt.xlabel("Comparisons")
        plt.title(title_text)
        plt.tight_layout()
        plt.show()
        

    def preparar_eixos(self, mat, foco):
        x = list()
        y = list()

        for i in range(len(mat)):
            y.append(mat[i][foco])
            text = str(mat[i][1]) + '/' + str(mat[i][2]) + '/' + str(mat[i][0])
            x.append(dt.datetime.strptime(text,"%m/%d/%Y").date())
    
        return x, y

    def prepara_mat(self, dados, foco):
        mat = list()
        for i in range(len(dados)):
            mat.append([int(dados[i][0]), int(dados[i][1]), int(dados[i][2]), float(dados[i][foco])])
        return mat
    
    def separa_estacao(self, dados, est):
        if est == 1:
            mes1 = 12
            mes2 = 1
            mes3 = 2

        sazonal = list()
        aux = list()
        flag = 0
        for i in range(len(dados)):
            try:
                if mes1 == dados[i][1] or mes2 == dados[i][1] or mes3 == dados[i][1]:
                    aux.append(dados[i])
                    flag = 0
                elif dados[i+1][1] == mes3 + 1 and flag == 0:
                    sazonal.append(aux)
                    aux = list()
                    flag = 1
                
            except IndexError:
                sazonal.append(aux)
                aux = list()
        return sazonal

    def histograma(self, city, parameter):
        t = DataProcessing()
        data = t.load_data_file(city)
        
        if parameter == "Precipitation":
            col = 3
        elif parameter == "Maximum temperature":
            col = 4
        elif parameter == "Minimum temperature":
            col = 5

        mat = self.prepara_mat(data, col)
        saz = self.separa_estacao(mat, 1)
        del saz[0]

        ultimo = len(saz) - 2

        # Preparar os dados para os últimos 10 anos
        ys = []
        titulos = []
        for i in range(10):
            _, y = self.preparar_eixos(saz[ultimo - 9 + i], 3)
            ys.append(np.array(y))
            titulos.append(saz[ultimo - 9 + i][-1][0])

        # Definir limites do eixo X baseados nos dados
        max_lim = max(max(y) for y in ys) + 0.5
        min_lim = min(min(y) for y in ys) - 0.5

        # Criar figura e subplots
        fig, axs = plt.subplots(2, 5, figsize=(14.5, 9.5))
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)

        for i in range(10):
            ax = axs[i // 5][i % 5]
            ax.set_title(titulos[i])
            ax.hist(ys[i], bins=40, linewidth=0.5, edgecolor="white")
            ax.set_xlim(min_lim, max_lim)
            ax.axvline(ys[i].mean(), color='red')

        plt.show()

    def boxplot(self, city, parameter):
        t = DataProcessing()
        data = t.load_data_file(city)
        
        if parameter == "Precipitation":
            col = 3
        elif parameter == "Maximum temperature":
            col = 4
        elif parameter == "Minimum temperature":
            col = 5

        mat = self.prepara_mat(data, col)
        saz = self.separa_estacao(mat, 1)
        del saz[0]

        ultimo = len(saz) - 2

        ys = []
        for i in range(10):
            _, y = self.preparar_eixos(saz[ultimo - 9 + i], 3)
            ys.append(y)

        fig, ax = plt.subplots(figsize=(14.5, 9.5))
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)

        ax.set_title("Boxplot for Maximum temperature [10 Anos]")
        ax.boxplot(ys)
        ax.set_xlabel('Year')
        ax.set_ylabel(parameter)

        plt.show()
    
    def decision_tree(self, criterion_v="squared_error", splitter="best", maxd_v='10',
                      minsam_s_v=2, minsam_l_v=50, minweifra_l_v='0.0', maxfeat_v="sqrt",
                      maxleaf_n='10', minimp_dec='0.0', ccp_alp_v='0.0', 
                      por_trei=70, num_tests=5,save_model=False):
        ml = Ml()
        ml.decision_tree(criterion_v, splitter, maxd_v,
                      minsam_s_v, minsam_l_v, minweifra_l_v, maxfeat_v,
                      maxleaf_n, minimp_dec, ccp_alp_v, 
                      por_trei, num_tests,save_model)
        
    def bagged_trees(self, criterion_v="squared_error", splitter="best", maxd_v='10',
                      minsam_s_v=2, minsam_l_v=50, minweifra_l_v='0.0', maxfeat_v="sqrt",
                      maxleaf_n='10', minimp_dec='0.0', ccp_alp_v='0.0', 
                      por_trei=70, num_tests=5,save_model=False, n_estimators=10):
        ml = Ml()
        ml.bagged_trees(criterion_v, splitter, maxd_v,
                      minsam_s_v, minsam_l_v, minweifra_l_v, maxfeat_v,
                      maxleaf_n, minimp_dec, ccp_alp_v, 
                      por_trei, num_tests,save_model, n_estimators)
        
    def neural_network(self, activation_v='relu', solver_v='adam', alpha_v='0.0001',
                       batch_size_v='auto', learning_rate_v='constant', learning_rate_init_v='0.001',
                       power_t_v='0.5', max_iter_v='200', shuffle_v=True, tol_v='0.0001',
                       verbose_v=False, warm_start_v=False, momentum_v='0.9', nesterovs_momentum_v=True,
                       early_stopping_v=False, validation_fraction_v='0.1', beta_1_v='0.9',
                       beta_2_v='0.999', n_iter_no_change_v='10', max_fun_v='15000', por_trei=70,
                       num_tests=5, save_model=False, load_params='None'):
        ml = Ml()
        ml.neural_network(activation_v, solver_v, alpha_v,
                       batch_size_v, learning_rate_v, learning_rate_init_v,
                       power_t_v, max_iter_v, shuffle_v, tol_v,
                       verbose_v, warm_start_v, momentum_v, nesterovs_momentum_v,
                       early_stopping_v, validation_fraction_v, beta_1_v,
                       beta_2_v, n_iter_no_change_v, max_fun_v, por_trei,
                       num_tests, save_model, load_params)
        
    def nearest_neighbors(self, n_neighbors_v=5, algorithm_v='auto', leaf_size_v=30,
                          p_v=2, n_jobs_v='5', por_trei=70, num_teste=5, save_model=False,
                          load_params='None'):
        ml = Ml()
        ml.nearest_neighbors(n_neighbors_v, algorithm_v, leaf_size_v, p_v, n_jobs_v,
                             por_trei, num_teste, save_model, load_params)
        
    def support_vector_machine(self, kernel_v='rbf', degree_v=3, gamma_v='scale', coef0_v='0.0',
                       tol_v='0.001', c_v='1.0', epsilon_v='0.1', shrinking_v=True,
                       cache_size_v='200', verbose_v=False, maxiter_v=-1, por_trei=70,
                       num_tests=5, save_model=False, load_params='None'):
        ml = Ml()
        ml.support_vector(kernel_v, degree_v, gamma_v, coef0_v, tol_v, c_v, epsilon_v,
                          shrinking_v, cache_size_v, verbose_v, maxiter_v, por_trei,
                          num_tests, save_model, load_params)
        
    def gaussian_process(self, alpha_gp='0.0000000001', n_restarts_op=0,
                         normalize_y_gp=False, copy_X_train=False, rand_state_gp='None',
                         por_trei=70, num_teste=5, save_model=False, load_params='None'):
        ml = Ml()
        ml.gaussian_process(alpha_gp, n_restarts_op, normalize_y_gp, copy_X_train,
                            rand_state_gp, por_trei, num_teste, save_model, load_params)

    def generate_custom_test(self, base_model='Decision Trees', triangulation='Arithmetic Average',
                             meta_model='Decision Trees', indicator='Maximum temperature',
                             num_tests=1, input_window='Yes'):
        meta = TestsGenerator()
        meta.generate_custom_test(base_model, triangulation, meta_model,
                                  indicator, num_tests, input_window)
        
    def generate_global_test(self, indicator='Maximum temperature', 
                             num_tests=1, input_window='Yes', print_results=True):
        meta = TestsGenerator()
        meta.generate_global_test(indicator, num_tests, input_window, print_results)

    def grid_search_dt(self):
        hiper = Hiperparam()
        hiper.grid_search_dt()

    def randomized_search_dt(self):
        hiper = Hiperparam()
        hiper.randomized_search_dt()

    def optuna_optimization(self, n_trials, model_name, city, indicator, split, tests, 
                            save_model=True, gp_kernel_type='RBF'):
        Ml.optuna_optimization(n_trials, model_name, city, indicator, split, tests, save_model, gp_kernel_type)
