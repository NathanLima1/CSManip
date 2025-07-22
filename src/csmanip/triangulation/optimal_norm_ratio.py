import math
from ..data_processing.data_processing import DataProcessing

def onr(self, focus):
    """
    Optimal normalizate ratio?
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

    self.onr_y = []
    result = []
    correlation_counter = 0

    for i in range(len(data)):
        try:
            # A lógica de cálculo é a mesma, independentemente da condição if/else abaixo.
            # Portanto, o cálculo foi movido para fora e simplificado.
            
            # Usamos abs() para garantir que a base da potência nunca será negativa.
            # <--- ALTERAÇÃO PRINCIPAL AQUI --->
            weight_a = math.pow(abs(coef_a[correlation_counter]), 2 * ((days[correlation_counter] - 2) / (1 - coef_a[correlation_counter])))
            weight_b = math.pow(abs(coef_b[correlation_counter]), 2 * ((days[correlation_counter] - 2) / (1 - coef_b[correlation_counter])))
            weight_c = math.pow(abs(coef_c[correlation_counter]), 2 * ((days[correlation_counter] - 2) / (1 - coef_c[correlation_counter])))

            numerator = (
                weight_a * float(data[i][target_index]) +
                weight_b * float(data[i][target_index + 3]) +
                weight_c * float(data[i][target_index + 6])
            )
            denominator = weight_a + weight_b + weight_c

            result.append(numerator / denominator)

            # Incrementa o contador apenas se o valor na próxima linha for diferente
            if i + 1 < len(data) and data[i][1] != data[i + 1][1]:
                correlation_counter += 1

        # Os blocos de exceção foram combinados, pois o código de recuperação era idêntico.
        except (IndexError, ValueError):
            # Ocorre no final do loop ou se houver um erro de matemática (como divisão por zero se o coef for 1).
            # Usamos o último contador válido.
            last = correlation_counter - 1 if correlation_counter > 0 else 0
            
            # <--- ALTERAÇÃO PRINCIPAL AQUI (no bloco de exceção) --->
            weight_a = math.pow(abs(coef_a[last]), 2 * ((days[last] - 2) / (1 - coef_a[last])))
            weight_b = math.pow(abs(coef_b[last]), 2 * ((days[last] - 2) / (1 - coef_b[last])))
            weight_c = math.pow(abs(coef_c[last]), 2 * ((days[last] - 2) / (1 - coef_c[last])))

            numerator = (
                weight_a * float(data[i][target_index]) +
                weight_b * float(data[i][target_index + 3]) +
                weight_c * float(data[i][target_index + 6])
            )
            denominator = weight_a + weight_b + weight_c
            
            # Evita divisão por zero caso os pesos sejam zero
            if denominator != 0:
                result.append(numerator / denominator)
            else:
                result.append(0) # Ou outro valor padrão

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