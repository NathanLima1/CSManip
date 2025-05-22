import math
from data_processing.data_processing import DataProcessing

def oidw(self, focus):
    """
    oidw = Optimized Inverse Distance Weightened
    """
    num_stations = 4  # Number of stations used

    monthly_target_avg = self.generate_monthly_avg(focus, 'target')
    monthly_neighborA_avg = self.generate_monthly_avg(focus, 'VizA')
    monthly_neighborB_avg = self.generate_monthly_avg(focus, 'VizB')
    monthly_neighborC_avg = self.generate_monthly_avg(focus, 'VizC')

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
    elif focus == 2:
        index_start = 7
    elif focus == 3:
        index_start = 8

    treatment = DataProcessing()
    raw_data = treatment.load_data_file('Dados comum')

    oidw_results = []
    weighted_sum = 0
    denominator_sum = 0
    month_row_counter = 0
    neighbor_column_counter = 1
    station_counter = 0

    for i in range(len(raw_data)):
        try:
            if raw_data[i][1] != raw_data[i + 1][1]:
                station_counter = 0
                neighbor_column_counter = 1

                for j in range(index_start, 15, 3):
                    weighted_sum += (
                        float(raw_data[i][j]) *
                        monthly_data[month_row_counter][0] *
                        math.log(self.h[0])
                    ) / (
                        self.d[station_counter] +
                        monthly_data[month_row_counter][neighbor_column_counter] *
                        math.log(self.h[neighbor_column_counter])
                    )

                    denominator_sum = 1 / self.d[0] + 1 / self.d[1] + 1 / self.d[2]
                    station_counter += 1
                    neighbor_column_counter += 1

                oidw_results.append(weighted_sum / denominator_sum)
                weighted_sum = 0
                denominator_sum = 0
                month_row_counter += 1

            else:
                station_counter = 0
                neighbor_column_counter = 1

                for j in range(index_start, 15, 3):
                    weighted_sum += (
                        float(raw_data[i][j]) *
                        monthly_data[month_row_counter][0] *
                        math.log(self.h[0])
                    ) / (
                        self.d[station_counter] +
                        monthly_data[month_row_counter][neighbor_column_counter] *
                        math.log(self.h[neighbor_column_counter])
                    )

                    denominator_sum = 1 / self.d[0] + 1 / self.d[1] + 1 / self.d[2]
                    station_counter += 1
                    neighbor_column_counter += 1

        except IndexError:
            pass