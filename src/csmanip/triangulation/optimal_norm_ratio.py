import math
from ..data_processing.data_processing import DataProcessing

def onr(self, focus):
    """
    Optimized normal ratio
    """
    treatment = DataProcessing()
    data = treatment.load_data_file('Common data')
    days, coef_a, coef_b, coef_c = self.generate_correlation_coefficients(focus)

    if focus == 1:
        target_index = 6
    elif focus == 2:
        target_index = 7
    elif focus == 3:
        target_index = 8
    else:
        raise ValueError("Invalid focus value. Must be 1, 2, or 3.")

    result = []
    correlation_counter = 0

    for i in range(len(data)):
        try:
            ca = coef_a[correlation_counter]
            cb = coef_b[correlation_counter]
            cc = coef_c[correlation_counter]
            d = days[correlation_counter]
            print("d", d)

            # Valor pequeno para evitar divisão por zero se r^2 for 1.0
            epsilon = 1e-9
            weight_a = math.pow((ca), round(2 * (d - 2) / (1 - ca**2 + epsilon)))
            weight_b = math.pow((cb), round(2 * (d - 2) / (1 - cb**2 + epsilon)))
            weight_c = math.pow((cc), round(2 * (d - 2) / (1 - cc**2+epsilon)))

            value_a = float(data[i][target_index])
            value_b = float(data[i][target_index + 3])
            value_c = float(data[i][target_index + 6])
            
            numerator = (weight_a * value_a) + (weight_b * value_b) + (weight_c * value_c)
            denominator = weight_a + weight_b + weight_c

            if denominator == 0:
                estimated_value = (value_a + value_b + value_c) / 3
            else:
                estimated_value = numerator / denominator
            
            result.append(estimated_value)
        except (IndexError, ValueError, ZeroDivisionError):
            print(f"Alerta: Falha no cálculo para o dia {i}. Usando média simples como fallback.")
            value_a = float(data[i][target_index])
            value_b = float(data[i][target_index + 3])
            value_c = float(data[i][target_index + 6])
            result.append((value_a + value_b + value_c) / 3)
        

        if i + 1 < len(data) and data[i][1] != data[i + 1][1]:
            correlation_counter += 1

    self.onr_y = []
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

    #self.onr_erro_abs, self.onr_erro_rel = self.calculate_errors(self.onr_y, self.onr_alv_y)
    self.onr_erro_abs, self.onr_erro_rel = self.calculate_errors_normalized(self.onr_y, self.onr_alv_y)