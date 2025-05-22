from data_processing.data_processing import DataProcessing

def choose_data(focus):
    data_process = DataProcessing()
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
    
    return index, a, data