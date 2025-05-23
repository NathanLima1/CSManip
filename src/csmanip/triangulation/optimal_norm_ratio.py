import math
from ..data_processing.data_processing import DataProcessing

def onr(self, focus):
        """
        Optimal normalizate ratio?
        """
        treatment = DataProcessing()
        data = treatment.load_data_file('Dados comum')
        days, coef_a, coef_b, coef_c = self.generate_correlation_coefficients(focus)

        if focus == 1:
            target_index = 6
        elif focus == 2:
            target_index = 7
        elif focus == 3:
            target_index = 8
        else:
            raise ValueError("Invalid focus value. Must be 1, 2, or 3.")

        self.onr_y = []
        result = []
        correlation_counter = 0

        for i in range(len(data)):
            try:
                if data[i][1] != data[i + 1][1]:
                    numerator = (
                        math.pow(coef_a[correlation_counter], 2 * ((days[correlation_counter] - 2) / (1 - coef_a[correlation_counter]))) * float(data[i][target_index]) +
                        math.pow(coef_b[correlation_counter], 2 * ((days[correlation_counter] - 2) / (1 - coef_b[correlation_counter]))) * float(data[i][target_index + 3]) +
                        math.pow(coef_c[correlation_counter], 2 * ((days[correlation_counter] - 2) / (1 - coef_c[correlation_counter]))) * float(data[i][target_index + 6])
                    )
                    denominator = (
                        math.pow(coef_a[correlation_counter], 2 * ((days[correlation_counter] - 2) / (1 - coef_a[correlation_counter]))) +
                        math.pow(coef_b[correlation_counter], 2 * ((days[correlation_counter] - 2) / (1 - coef_b[correlation_counter]))) +
                        math.pow(coef_c[correlation_counter], 2 * ((days[correlation_counter] - 2) / (1 - coef_c[correlation_counter])))
                    )

                    result.append(numerator / denominator)
                    correlation_counter += 1

                else:
                    numerator = (
                        math.pow(coef_a[correlation_counter], 2 * ((days[correlation_counter] - 2) / (1 - coef_a[correlation_counter]))) * float(data[i][target_index]) +
                        math.pow(coef_b[correlation_counter], 2 * ((days[correlation_counter] - 2) / (1 - coef_b[correlation_counter]))) * float(data[i][target_index + 3]) +
                        math.pow(coef_c[correlation_counter], 2 * ((days[correlation_counter] - 2) / (1 - coef_c[correlation_counter]))) * float(data[i][target_index + 6])
                    )
                    denominator = (
                        math.pow(coef_a[correlation_counter], 2 * ((days[correlation_counter] - 2) / (1 - coef_a[correlation_counter]))) +
                        math.pow(coef_b[correlation_counter], 2 * ((days[correlation_counter] - 2) / (1 - coef_b[correlation_counter]))) +
                        math.pow(coef_c[correlation_counter], 2 * ((days[correlation_counter] - 2) / (1 - coef_c[correlation_counter])))
                    )

                    result.append(numerator / denominator)

            except IndexError:
                last = correlation_counter - 1
                numerator = (
                    math.pow(coef_a[last], 2 * ((days[last] - 2) / (1 - coef_a[last]))) * float(data[i][target_index]) +
                    math.pow(coef_b[last], 2 * ((days[last] - 2) / (1 - coef_b[last]))) * float(data[i][target_index + 3]) +
                    math.pow(coef_c[last], 2 * ((days[last] - 2) / (1 - coef_c[last]))) * float(data[i][target_index + 6])
                )
                denominator = (
                    math.pow(coef_a[last], 2 * ((days[last] - 2) / (1 - coef_a[last]))) +
                    math.pow(coef_b[last], 2 * ((days[last] - 2) / (1 - coef_b[last]))) +
                    math.pow(coef_c[last], 2 * ((days[last] - 2) / (1 - coef_c[last])))
                )

                result.append(numerator / denominator)

            except ValueError:
                last = correlation_counter - 1
                numerator = (
                    math.pow(coef_a[last], 2 * ((days[last] - 2) / (1 - coef_a[last]))) * float(data[i][target_index]) +
                    math.pow(coef_b[last], 2 * ((days[last] - 2) / (1 - coef_b[last]))) * float(data[i][target_index + 3]) +
                    math.pow(coef_c[last], 2 * ((days[last] - 2) / (1 - coef_c[last]))) * float(data[i][target_index + 6])
                )
                denominator = (
                    math.pow(coef_a[last], 2 * ((days[last] - 2) / (1 - coef_a[last]))) +
                    math.pow(coef_b[last], 2 * ((days[last] - 2) / (1 - coef_b[last]))) +
                    math.pow(coef_c[last], 2 * ((days[last] - 2) / (1 - coef_c[last])))
                )

                result.append(numerator / denominator)

        self.onr_x = []
        self.onr_alv_y = []
        self.meta_matrix_onr = []

        for index, _ in enumerate(data):
            self.onr_x.append(index)
            self.onr_alv_y.append(float(data[index][target_index - 3]))
            self.onr_y.append(result[index])

            row = [
                float(data[index][0]),
                float(data[index][1]),
                float(data[index][2]),
                float(self.onr_y[index])
            ]
            self.meta_matrix_onr.append(row)

        self.onr_erro_abs, self.onr_erro_rel = self.calculate_errors(self.onr_y, self.onr_alv_y)
