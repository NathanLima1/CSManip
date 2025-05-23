from ..data_processing.data_processing import DataProcessing

def rw(self, focus):
        """
        Residual weightening ou ratio weightened?
        """
        num_stations = 3
        monthly_avg_target = self.generate_monthly_avg(focus, 'target')
        monthly_avg_vizA = self.generate_monthly_avg(focus, 'VizA')
        monthly_avg_vizB = self.generate_monthly_avg(focus, 'VizB')
        monthly_avg_vizC = self.generate_monthly_avg(focus, 'VizC')

        if focus == 1:
            index = 6
        elif focus == 2:
            index = 7
        elif focus == 3:
            index = 8

        monthly_matrix = []
        self.idw_x = []
        self.idw_y = []
        self.idw_avg_y = []

        for i in range(len(monthly_avg_target)):
            temp = [
                monthly_avg_target[i],
                monthly_avg_vizA[i],
                monthly_avg_vizB[i],
                monthly_avg_vizC[i]
            ]
            monthly_matrix.append(temp)

        treatment = DataProcessing()
        data = treatment.load_data_file('Dados comum')

        current_index = 0
        sum_values = 0
        result = []
        ma_row = 0

        for i in range(len(data)):
            try:
                if i == self.index_end[current_index]:
                    sum_values = (
                        (monthly_matrix[ma_row][0] / monthly_matrix[ma_row][1]) * float(data[i][index]) +
                        (monthly_matrix[ma_row][0] / monthly_matrix[ma_row][2]) * float(data[i][index + 3]) +
                        (monthly_matrix[ma_row][0] / monthly_matrix[ma_row][3]) * float(data[i][index + 6])
                    ) * (1 / 3)
                    result.append(sum_values)
                    sum_values = 0
                    ma_row += 1
                    current_index += 1
                else:
                    sum_values = (
                        (monthly_matrix[ma_row][0] / monthly_matrix[ma_row][1]) * float(data[i][index]) +
                        (monthly_matrix[ma_row][0] / monthly_matrix[ma_row][2]) * float(data[i][index + 3]) +
                        (monthly_matrix[ma_row][0] / monthly_matrix[ma_row][3]) * float(data[i][index + 6])
                    ) * (1 / 3)
                    result.append(sum_values)
                    sum_values = 0
            except IndexError:
                sum_values = (
                    (monthly_matrix[ma_row - 1][0] / monthly_matrix[ma_row - 1][1]) * float(data[i][index]) +
                    (monthly_matrix[ma_row - 1][0] / monthly_matrix[ma_row - 1][2]) * float(data[i][index + 3]) +
                    (monthly_matrix[ma_row - 1][0] / monthly_matrix[ma_row - 1][3]) * float(data[i][index + 6])
                ) * (1 / 3)
                result.append(sum_values)
                sum_values = 0

        self.rw_x = []
        self.rw_y = []
        self.rw_avg_y = []
        self.meta_matrix_rw = []

        x = 0
        for i in range(len(data)):
            self.rw_x.append(x)
            self.rw_y.append(result[i])
            self.rw_avg_y.append(float(data[i][index - 3]))

            temp = [
                float(data[i][0]),
                float(data[i][1]),
                float(data[i][2]),
                float(result[i])
            ]
            self.meta_matrix_rw.append(temp)

            x += 1

        self.rw_abs_error, self.rw_rel_error = self.calculate_errors(self.rw_y, self.rw_avg_y)