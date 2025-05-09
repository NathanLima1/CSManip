from data_processing.data_processing import DataProcessing
from training.training import Training
from haversine import haversine, Unit
import folium
from folium.map import Popup
import webbrowser
import math
from scipy import stats
from triangulation.ratio_weightened import rw
from triangulation.optimal_norm_ratio import onr
from triangulation.inverse_dist_weightened import idw
from triangulation.optimized_idw import  oidw

class Triangulation:
    def __init__(self):
        self.coordinates  = []
        processed_data = DataProcessing()
        local = processed_data.get_location_coordinates()
        file = open(local)
        aux = []

        for i in file:
            aux.append(i)

        for i in range(len(aux)):
            aux[i] = str(aux[i]).strip('\n')
            self.coordinates.append(aux[i])

        file.close()

        dt_target = []
        dt_cityA = []
        dt_cityB = []
        dt_cityC = []

        for i in range(0, 4):
            dt_target.append(self.coordinates[i])
        for i in range(4,8):
            dt_cityA.append(self.coordinates[i])
        for i in range(8,12):
            dt_cityB.append(self.coordinates[i])
        for i in range(12, 16):
            dt_cityC.append(self.coordinates[i])

        self.tuple_target = (float(dt_target[1]), float(dt_target[2]))
        self.tuple_cityA = (float(dt_cityA[1]), float(dt_cityA[2]))
        self.tuple_cityB = (float(dt_cityB[1]), float(dt_cityB[2]))
        self.tuple_cityC = (float(dt_cityC[1]), float(dt_cityC[2]))
        self.h = [float(self.coordinates[3]), float(self.coordinates[7]), 
                  float(self.coordinates[11]), float(self.coordinates[15])]
        d1 = round(haversine(self.tuple_target, self.tuple_cityA, Unit.KILOMETERS), 4)
        d2 = round(haversine(self.tuple_target, self.tuple_cityB, Unit.KILOMETERS), 4)
        d3 = round(haversine(self.tuple_target, self.tuple_cityC, Unit.KILOMETERS), 4)

        mean = (d1+d2+d3)/3
        self.distance = [d1, d2, d3]

    def idw(self, focus):
        """
        Calculate Inverse Distance Weightened
        """
        idw(self, focus)

    def get_idw(self):
        """
        Returns the variables of the inverse distance weightened
        """
        return self.idw_x, self.idw_y, self.idw_target_y, self.idw_abs_error, self.idw_rel_error, self.meta_matrix_idw

    def avg(self, focus):
        """
        aa = Averaging Arithmetic que virou avg
        """
        data_process = DataProcessing()

        self.avg_x = []
        self.avg_y = []
        self.avg_target_y = []

        if focus == 1:
            index = 6
            a = 3
            data = data_process.normalize_data(data_process.load_data_file("Dados comum"))
        elif focus == 2:
            index = 7
            a = 4
            data = data_process.load_data_file("Dados comum")
        elif focus == 3:
            index = 8
            a = 5
            data = data_process.load_data_file("Dados comum")

        cont = 1
        self.meta_matrix_avg = []

        for i in range(len(data)): # Resolver depois para mais 3 estações Neighbors
            sum = 0
            for j in range(index, 15, 3):
                sum += float(data[i][j])

            avg = (1/3)*sum
            aux = []

            aux.append(float(data[i][0]))
            aux.append(float(data[i][1]))
            aux.append(float(data[i][2]))
            aux.append(avg)
            self.meta_matrix_avg.append(aux)

            self.avg_x.append(cont)
            self.avg_y.append(avg)
            self.avg_target_y.append(float(data[i][a]))

            cont += 1

        self.avg_abs_error, self.avg_rel_error = self.calculate_errors(self.avg_y, self.avg_target_y)

    def get_avg(self):
        """
        Returns the data relative to Averaging Arithmetic
        """
        return self.avg_x, self.avg_y, self.avg_target_y, self.avg_abs_error, self.avg_rel_error, self.meta_matrix_avg

    def show_map(self):
        m = folium.Map(location=self.tuple_target)
        folium.Marker(location=self.tuple_target, popup=Popup('Target', show=True)).add_to(m)
        folium.Marker(location=self.tuple_cityA, popup=Popup('Neighbor A', show=True)).add_to(m)
        folium.Marker(location=self.tuple_cityB, popup=Popup('Neighbor B', show=True)).add_to(m)
        folium.Marker(location=self.tuple_cityC, popup=Popup('Neighbor C', show=True)).add_to(m)
        m.save('map.html')
    
        webbrowser.open_new_tab('map.html')

    def oidw(self, focus):
        oidw(self, focus)

    def rw(self, focus):
        """
        Calculate ratio weightened
        """
        rw(self, focus)

    def get_rw(self):
        return self.rw_x, self.rw_y, self.rw_avg_y, self.rw_abs_error, self.rw_rel_error, self.meta_matrix_rw

    def generate_monthly_avg(self, foco, cidade):
        treatment = DataProcessing()
        

        monthly_avg = list()
        self.index_end = list()
        sum = 0
        cont = 2


        if cidade == 'target':
            if foco == 1:
                index = 3 #precipitação na target
                data = treatment.normalize_data(treatment.load_data_file('Dados comum'))
            elif foco == 2:
                index = 4 #Temperatura maxima na target
                data = treatment.load_data_file('Dados comum')
            elif foco == 3:
                index = 5 #Temperatura minima na target
                data = treatment.load_data_file('Dados comum')
        elif cidade == 'VizA':
            if foco == 1:
                index = 6 
                data = treatment.normalize_data(treatment.load_data_file('Dados comum'))
            elif foco == 2:
                index = 7
                data = treatment.load_data_file('Dados comum')
            elif foco == 3:
                index = 8
                data = treatment.load_data_file('Dados comum')
        elif cidade == 'vizB':
            if foco == 1:
                index = 9
                data = treatment.normalize_data(treatment.load_data_file('Dados comum'))
            elif foco == 2:
                index = 10
                data = treatment.load_data_file('Dados comum')
            elif foco == 3:
                index = 11
                data = treatment.load_data_file('Dados comum')
        else:
            if foco == 1:
                index = 12
                data = treatment.normalize_data(treatment.load_data_file('Dados comum'))
            elif foco == 2:
                index = 13
                data = treatment.load_data_file('Dados comum')
            elif foco == 3:
                index = 14
                data = treatment.load_data_file('Dados comum')

        #encontar o index da ultima data de cada mes
        for i in range(len(data)):
            try:
                if data[i][1] != data[i+1][1]:
                    self.index_end.append(i)
            except IndexError:
                pass
       
        for i in range(len(data)):
            try:
                if data[i][1] != data[i+1][1]:
                    sum = sum + float(data[i][index])
                    cont = cont + 1
                    monthly_avg.append(sum/cont)
                    sum = 0
                    cont = 1
                else:
                    sum = sum + float(data[i][index])
                    cont = cont + 1

                
            except IndexError:
                pass
        return monthly_avg
    
    def generate_correlation_coefficients(self, focus):
        treatment = DataProcessing()
        normalization = Training()

        if focus == 1:
            index = 3  # Precipitation at target station
            data = normalization.normalize(treatment.load_data_file('Dados comum'))
        elif focus == 2:
            index = 4  # Maximum temperature at target station
            data = treatment.load_data_file('Dados comum')
        elif focus == 3:
            index = 5  # Minimum temperature at target station
            data = treatment.load_data_file('Dados comum')

        coef_target_A = []
        coef_target_B = []
        coef_target_C = []
        days_per_month = []
        day_counter = 0

        values_target = []
        values_station_A = []
        values_station_B = []
        values_station_C = []

        insufficient_days_indices = []

        for i in range(len(data)):
            try:
                if data[i][1] != data[i + 1][1]:
                    values_target.append(float(data[i][index]))
                    values_station_A.append(float(data[i][index + 3]))
                    values_station_B.append(float(data[i][index + 6]))
                    values_station_C.append(float(data[i][index + 9]))
                    day_counter += 1

                    if day_counter >= 2:
                        days_per_month.append(day_counter)
                        day_counter = 0

                        correlation_A = stats.pearsonr(values_target, values_station_A)
                        correlation_B = stats.pearsonr(values_target, values_station_B)
                        correlation_C = stats.pearsonr(values_target, values_station_C)

                        coef_target_A.append(correlation_A[0])
                        coef_target_B.append(correlation_B[0])
                        coef_target_C.append(correlation_C[0])

                        values_target = []
                        values_station_A = []
                        values_station_B = []
                        values_station_C = []
                    else:
                        insufficient_days_indices.append(i)
                else:
                    values_target.append(float(data[i][index]))
                    values_station_A.append(float(data[i][index + 3]))
                    values_station_B.append(float(data[i][index + 6]))
                    values_station_C.append(float(data[i][index + 9]))
                    day_counter += 1

            except IndexError:
                values_target.append(float(data[i - 1][index]))
                values_station_A.append(float(data[i - 1][index + 3]))
                values_station_B.append(float(data[i - 1][index + 6]))
                values_station_C.append(float(data[i - 1][index + 9]))
                day_counter += 1

        return days_per_month, coef_target_A, coef_target_B, coef_target_C

    def onr(self, focus):
        """
        Calculate Optimized Normal Ratio
        """
        onr(self, focus)

    def get_onr(self):
        return self.onr_x, self.onr_y, self.onr_alv_y, self.onr_erro_abs, self.onr_erro_rel, self.meta_matrix_onr


    def calculate_errors(self, real, approx):
        t = Training()
        '''
        exact = t.normalize(real)
        approximate = t.normalize(approx)
        ''' 
        exact = real
        approximate = approx
        sum_ea = 0
        sum_er = 0
        
        for i in range(len(exact)):
            ea = abs(exact[i] - approximate[i])
            er = ea / exact[i]

            sum_ea += ea
            sum_er += er
        
        absolute_error = sum_ea / len(exact)
        relative_error = sum_er / len(exact)

        return absolute_error, relative_error