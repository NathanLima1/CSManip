from data_processing.data_processing import DataProcessing

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

    if focus == 1: # Precipitação
        index = 6
        a = 3
        data = data_process.normalize_data(data_process.load_data_file("Dados comum"))
    elif focus == 2: # Temperatura Máxima
        index = 7
        a = 4
        data = data_process.load_data_file("Dados comum")
    elif focus == 3: #Temperatura Minima
        index = 8
        a = 5
        data = data_process.load_data_file("Dados comum")
    
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
