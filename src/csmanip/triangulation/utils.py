from ..data_processing.data_processing import DataProcessing

def choose_data(focus):
    print("Entrou utils choose_data")
    data_process = DataProcessing()
    if focus == 1: # Precipitation
        index = 6
        a = 3
        data = data_process.normalize_data(data_process.load_data_file('Common data'))
    elif focus == 2: # Maximum temperature
        index = 7
        a = 4
        data = data_process.load_data_file('Common data')
    elif focus == 3: #Maximum temperature
        index = 8
        a = 5
        data = data_process.load_data_file('Common data')
    
    return index, a, data