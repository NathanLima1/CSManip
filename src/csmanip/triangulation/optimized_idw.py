import math
from ..data_processing.data_processing import DataProcessing

def oidw(self, focus):
    """
    oidw = Optimized Inverse Distance Weightened
    """
    self.oidw_x = []
    self.oidw_y = []
    self.oidw_target_y = []
    self.meta_matrix_oidw = []

    monthly_target_avg = self.generate_monthly_avg(focus, 'target')
    monthly_neighborA_avg = self.generate_monthly_avg(focus, 'neighborA')
    monthly_neighborB_avg = self.generate_monthly_avg(focus, 'neighborB')
    monthly_neighborC_avg = self.generate_monthly_avg(focus, 'neighborC')

    monthly_data = []
    for i in range(len(monthly_target_avg)):
        row = [
            monthly_target_avg[i],
            monthly_neighborA_avg[i],
            monthly_neighborB_avg[i],
            monthly_neighborC_avg[i]
        ]
        monthly_data.append(row)


    if focus == 1:
        index_start = 6
        a = 3
    elif focus == 2:
        index_start = 7
        a = 4
    elif focus == 3:
        index_start = 8
        a = 5

    treatment = DataProcessing()
    raw_data = treatment.load_data_file('Common data')

    month_row_counter = 0
    row_counter = 1 # Contador eixo x

    # Calcula a soma dos inversos das distâncias
    denominator_sum = 1/self.distance[0]+1/self.distance[1]+1/self.distance[2]

    for i in range(len(raw_data)):
        weighted_sum = 0
        station_counter = 0
        neighbor_column_counter = 1

        for j in range(index_start, 15, 3):
            try:
                Y_i = float(raw_data[i][j])
                d_i = self.distance[station_counter]
                #print("i", i, "j", j, "row", month_row_counter)
                #print(f"data {monthly_data[month_row_counter][0]}")
                if month_row_counter >= len(monthly_data):
                    print(f"AVISO: Desalinhamento de dados na linha i={i}. O contador de mês ({month_row_counter}) é inválido para o tamanho de monthly_data ({len(monthly_data)}). Pulando linha.")
                    continue
                A = monthly_data[month_row_counter][0]
                A_i = monthly_data[month_row_counter][neighbor_column_counter]
                logH = math.log(self.h[0])
                logH_i = math.log(self.h[neighbor_column_counter])

                term_numerator = Y_i*A*logH
                term_denominator = d_i*A_i*logH_i

                if term_denominator != 0:
                    weighted_sum += term_numerator/term_denominator

                station_counter += 1
                neighbor_column_counter += 1

            except (ValueError, ZeroDivisionError) as e:
                print(f"Aviso: Erro no cálculo da linha {i}, dado ignorado. Detalhes: {e}")
                continue
        
        if denominator_sum == 0:
            calculate_oidw = 0
        else:
            calculate_oidw = weighted_sum/denominator_sum

        self.oidw_x.append(row_counter)
        self.oidw_y.append(calculate_oidw)
        self.oidw_target_y.append(float(raw_data[i][a]))

        meta_row = [
            float(raw_data[i][0]),
            float(raw_data[i][1]),
            float(raw_data[i][2]),
            calculate_oidw
        ]

        self.meta_matrix_oidw.append(meta_row)
        row_counter += 1

        try:
            if raw_data[i][1] != raw_data[i+1][1]:
                month_row_counter += 1
        except IndexError:
            # chegou ao final da lista de dados
            pass

    #self.oidw_abs_error, self.oidw_rel_error = self.calculate_errors(self.oidw_y, self.oidw_target_y)
    self.oidw_abs_error, self.oidw_rel_error = self.calculate_errors_normalized(self.oidw_y, self.oidw_target_y)