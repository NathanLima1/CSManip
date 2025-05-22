from data_processing.data_processing import DataProcessing
from utils import choose_data

def idw(self, focus):
    """
    idw = Inverse Distance Weightened
    """
    data_process = DataProcessing()
    distance = self.distance
    # idw = inverse distance weightened
    self.idw_x = []
    self.idw_y = []
    self.idw_target_y = []

    index, a, data = choose_data(focus)
    
    cont2 = 1
    self.meta_matrix_idw = []
    for i, _ in enumerate(data):
        cont = 0
        add = 0
        for j in range(index, 15, 3):
            add += float(data[i][j])/distance[cont]
            cont += 1

        calculate_idw = round(add/(1/distance[0] + 1/distance[1] + 1/distance[2]), 4)
        aux = []
        aux.append(float(data[i][0]))
        aux.append(float(data[i][1]))
        aux.append(float(data[i][2]))
        aux.append(calculate_idw)

        self.meta_matrix_idw.append(aux) # Matrix for the meta learning
        self.idw_x.append(cont2)
        self.idw_y.append(float(calculate_idw))
        self.idw_target_y.append(float(data[i][a]))
        cont2 += 1

    self.idw_abs_error, self.idw_rel_error = self.calculate_errors(self.idw_y, self.idw_target_y)
