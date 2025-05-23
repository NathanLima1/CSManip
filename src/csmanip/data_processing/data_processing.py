import csv
import os

class DataProcessing:
    global target
    global neighborA
    global neighborB
    global neighborC
    global download_path
    target = neighborA = neighborB = neighborC = download_path = ''

    def __init__(self):
        self.target = target
        self.neighborA = neighborA
        self.neighborB = neighborB
        self.neighborC = neighborC
        self.download_path = download_path

    def find_columns(self, header_line:str, sample_line:str) -> int:
        # procura_colunas
        """
        Find the columns of preciptation, tmax and tmin
        """
        print("Entrou dataP find_columns")
        station = (str(sample_line).split(' '))[2]
        station = station.strip("]").strip("'")

        if station[0] != 'A':
            col_prec = 3
            col_tmax = 4
            col_tmin = 6
        else:
            col_prec = 1
            col_tmax = 4
            col_tmin = 6

        return col_prec, col_tmax, col_tmin

    def get_processed_data(self) -> None:
        # get_data_trada
        """
        Generates the files with the processed data for use
        """
        print("Entrou dataP get_processed_data")
        files = [self.target, self.neighborA, self.neighborB, self.neighborC]
        output_files = [
            f"{self.download_path}/target_clean.txt",
            f"{self.download_path}/neighborA_clean.txt",
            f"{self.download_path}/neighborB_clean.txt",
            f"{self.download_path}/neighborC_clean.txt"
        ]

        with open("end.txt", "w") as f:
            f.write(
                "\n".join(output_files + [
                    f"{self.download_path}/common_data.csv",
                    f"{self.download_path}/buff.txt",
                    f"{self.download_path}/Coordinates.txt"
                ])
            )

        counter = 0
        common_target = common_neighborA = common_neighborB = common_neighborC = []
    
        for path in files:
            temp_data = []

            with open(path) as f:
                reader = csv.reader(f, delimiter=';')
                for line in reader:
                    temp_data.append(line)
            
            del temp_data[10][-1]

            col_prec, col_tmax, col_tmin = self.find_columns(temp_data[10], temp_data[1])

            del temp_data[-1]      # remove last empty row
            del temp_data[:11]     # remove header rows

            selected_columns = [1, 2, 3]
            buffer = []

            for i in range(len(temp_data)):  # percorre cada linha da tabela
                buffer2 = []
                buffer2.append(temp_data[i][0])
                for j in selected_columns:
                    buffer2.append(temp_data[i][j])

                buffer.append(buffer2)

            cleaned = []
            for row in buffer:
                if all(cell not in ['null', ''] for cell in row[1:4]):
                    cleaned.append(row)

            for row in cleaned:
                date_parts = row[0].split('-')
                row.insert(0, int(date_parts[0]))
                row.insert(1, int(date_parts[1]))
                row.insert(2, int(date_parts[2]))
                del row[3]

            with open(output_files[counter], 'w') as out_f:
                formatted_data = []
                for row in cleaned:
                    formatted_row = [str(cell).replace(',', '.') for cell in row]
                    formatted_data.append(formatted_row)

                    line = str(formatted_row).replace(' ', '').strip('[]')
                    if counter == 0:
                        common_target.append(line)
                    elif counter == 1:
                        common_neighborA.append(line)
                    elif counter == 2:
                        common_neighborB.append(line)
                    else:
                        common_neighborC.append(line)

                    out_f.write(f"{line}\n")

            counter += 1

        self.get_coordinates()
        self.common_data_2()

    def common_data(self) -> None:
        # dadosc
        city1, t1 = self.prepare_common_data(f"{self.download_path}/target_clean.txt")
        city2, t2 = self.prepare_common_data(f"{self.download_path}/neighborA_clean.txt")
        city3, t3 = self.prepare_common_data(f"{self.download_path}/neighborB_clean.txt")
        city4, t4 = self.prepare_common_data(f"{self.download_path}/neighborC_clean.txt")

        start_year = max(city1[0][0], city2[0][0], city3[0][0], city4[0][0])
        min_length = min(len(city1), len(city2), len(city3), len(city4))

        # Find indexes for start_year
        for i in range(len(city1)):
            if start_year == city1[i][0]:
                idx1 = i
                break
        for i in range(len(city2)):
            if start_year == city2[i][0]:
                idx2 = i
                break
        for i in range(len(city3)):
            if start_year == city3[i][0]:
                idx3 = i
                break
        for i in range(len(city4)):
            if start_year == city4[i][0]:
                idx4 = i
                break

        final_data = []
        with open(f"{self.download_path}/common_data.txt", 'w') as f_out, open(f"{self.download_path}/buff.txt", 'w') as buff_out:
            total = 0
            for i in range(min_length):
                y1, m1, d1 = map(int, city1[idx1 + i][:3])
                for j in range(min_length):
                    y2, m2, d2 = map(int, city2[idx2 + j][:3])
                    if (y1, m1, d1) == (y2, m2, d2):
                        for k in range(min_length):
                            y3, m3, d3 = map(int, city3[idx3 + k][:3])
                            if (y2, m2, d2) == (y3, m3, d3):
                                for z in range(min_length):
                                    y4, m4, d4 = map(int, city4[idx4 + z][:3])
                                    if (y3, m3, d3) == (y4, m4, d4):
                                        row = [
                                            y1, m1, d1,
                                            *city1[idx1 + i][3:6],
                                            *city2[idx2 + j][3:6],
                                            *city3[idx3 + k][3:6],
                                            *city4[idx4 + z][3:6]
                                        ]
                                        final_data.append(row)

                                        csv_line = ";".join(map(str, row)) + ";\n"
                                        f_out.write(csv_line)
                                        total += 1
                                        break
                                break
                        break

            buff_out.write(f"{total} {t1} {t2} {t3} {t4}")

    def common_data_2(self):
        # dadosc2
        target, t1 = self.prepare_common_data(str(self.download_path) + "/target_clean.txt")
        neighA, t2 = self.prepare_common_data(str(self.download_path) + "/neighborA_clean.txt")
        neighB, t3 = self.prepare_common_data(str(self.download_path) + "/neighborB_clean.txt")
        neighC, t4 = self.prepare_common_data(str(self.download_path) + "/neighborC_clean.txt")
        start = max(target[0][0], neighA[0][0], neighB[0][0], neighC[0][0])

        idx1 = idx2 = idx3 = idx4 = 0
        for i in range(len(target)):
            if int(start) == int(target[i][0]):
                idx1 = i
                break
        for i in range(len(neighA)):
            if int(start) == int(neighA[i][0]):
                idx2 = i
                break
        for i in range(len(neighB)):
            if int(start) == int(neighB[i][0]):
                idx3 = i
                break
        for i in range(len(neighC)):
            if int(start) == int(neighC[i][0]):
                idx4 = i
                break

        file_out = open(str(self.download_path) + '/common_data.csv', 'w')
        file_buff = open(str(self.download_path) + '/buff.txt', 'w')
        common_count = 0

        for i in range(idx1, len(target)):
            try:
                year1, month1, day1 = target[i][0], target[i][1], target[i][2]
                for j in range(idx2, len(neighA)):
                    year2, month2, day2 = neighA[j][0], neighA[j][1], neighA[j][2]
                    if (year1 == year2) and (month1 == month2) and (day1 == day2):
                        for k in range(idx3, len(neighB)):
                            year3, month3, day3 = neighB[k][0], neighB[k][1], neighB[k][2]
                            if (year2 == year3) and (month2 == month3) and (day2 == day3):
                                for l in range(idx4, len(neighC)):
                                    year4, month4, day4 = neighC[l][0], neighC[l][1], neighC[l][2]
                                    if (year3 == year4) and (month3 == month4) and (day3 == day4):
                                        t_target = str(target[i]).strip('[]').replace(' ', '')

                                        del neighA[j][:3]
                                        t_neighA = str(neighA[j]).strip('[]').replace(' ', '')

                                        del neighB[k][:3]
                                        t_neighB = str(neighB[k]).strip('[]').replace(' ', '')

                                        del neighC[l][:3]
                                        t_neighC = str(neighC[l]).strip('[]').replace(' ', '')

                                        text = t_target + ',' + t_neighA + ',' + t_neighB + ',' + t_neighC
                                        text = text.replace(',', ';')

                                        file_out.write(text + ';\n')
                                        common_count += 1
            except IndexError:
                pass

        file_buff.write(f"{common_count} {t1} {t2} {t3} {t4}")
        file_out.close()
        file_buff.close()

    def prepare_common_data(self, dir):
        #prepara_dadosc
        """
        Prepares the data in common for later use
        """
        file = open(dir)
        prepared_data = []

        for i in file:
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            i = i.split(',')  
            prepared_data.append(i)

        file.close()
        return prepared_data, len(prepared_data)
    
    def load_data_file(self, option: str) -> list:
        """
        Receives a string with the city selected, 
        open the file of the selected city and returns a list with the data
        """
        # nova retorna_arq
        print("Entrou dataP load_data_file")
        arq = open('end.txt') 
        a = arq.readlines()
        arq.close()
        if option == 'Target city':
            di = a[0].replace("\n", '')
        elif option == 'Neighbor A':
            di = a[1].replace("\n", '')
        elif option == 'Neighbor B':
            di = a[2].replace("\n", '')
        elif option == 'Neighbor C':
            di = a[3].replace("\n", '')
        elif option == 'Dados comum':
            di = a[4].replace("\n", '')
            
        
        lista = list()
        
        arq = open(di)
        
        for i in arq:
            
            i = i.replace('\n', '')
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            
            if option == 'Dados comum':
                i = i.split(';')
                del i[len(i)-1]
                
            else:
                i = i.split(',')  
            lista.append(i)
        arq.close()
        
        return lista

    def get_year_range(self, option: str):
        # get_range
        print("Entrou dataP get_year_range")
        is_common_data = False

        with open('end.txt') as file:
            paths = [line.strip() for line in file]

        options = {
            'Target city': 0,
            'Neighbor A': 1,
            'Neighbor B': 2,
            'Neighbor C': 3,
            'Dados comum': 4
        }

        index = options.get(option)
        if index is None or index >= len(paths):
            raise ValueError(f"Invalid option or index out of range: '{option}'")

        selected_path = paths[index]

        if option == 'Dados comum':
            is_common_data = True

        years = []

        with open(selected_path) as data_file:
            for line in data_file:
                line = line.strip().replace("'", "").replace(" ", "")
                if is_common_data:
                    items = line.split(';')
                    if items and items[-1] == '':
                        items.pop()
                else:
                    items = line.split(',')
                years.append(int(items[0]))

        unique_years = []
        last_value = None

        for year in years:
            if year != last_value:
                unique_years.append(year)
                last_value = year

        return unique_years

    def get_quantities(self) -> int:
        # get_qtd
        with open('end.txt') as file:
            paths = [line.strip() for line in file]

        quantity_file_path = paths[5]

        with open(quantity_file_path) as quantity_file:
            first_line = quantity_file.readline().strip()
            values = first_line.split()

            if len(values) < 5:
                raise ValueError("Expected at least 5 values in the quantity file.")

            total_units = int(values[0])
            target_city = int(values[1])
            neighbor_a = int(values[2])
            neighbor_b = int(values[3])
            neighbor_c = int(values[4])

        return total_units, target_city, neighbor_a, neighbor_b, neighbor_c

    def normalize_data(self, matrix: list) -> list:
        """
        Function that receives a matrix of data and normalize this data
        """
        # normalizar dados
        max_min = []
        temp_values = []
        num_columns = len(matrix[0])

        for col in range(num_columns):
            temp_values.clear()
            for row in matrix:
                temp_values.append(row[col])
            max_min.append(max(temp_values))
            max_min.append(min(temp_values))

        normalized_data = []

        for row in matrix:
            normalized_row = []
            index = 0
            for col in range(num_columns):
                if index <= 36:
                    max_value = max_min[index]
                    min_value = max_min[index + 1]
                    normalized = ((float(row[col]) - float(min_value)) / (float(max_value) - float(min_value))) * 0.6 + 0.2
                    normalized_row.append(normalized)
                    index += 2
            normalized_data.append(normalized_row)

        return normalized_data

    def get_coordinates(self) -> None:
        """
        This function retires the coordinates of the cities and write in a file
        """
        # get_coordinates
        coordinates = []
        temp_data = []

        # Read file paths from end.txt
        with open('end.txt') as file:
            paths = [line.strip() for line in file]

        city_files = [self.target, self.neighborA, self.neighborB, self.neighborC]

        for city_file in city_files:
            temp_data.clear()

            with open(city_file, newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    temp_data.append(row)

            # Keep only the first 10 lines, assuming coordinates are within that range
            temp_data = temp_data[:10]

            station = temp_data[0][0].split(':')[1].strip(" []'")
            latitude = temp_data[2][0].split(':')[1].strip(" []'")
            longitude = temp_data[3][0].split(':')[1].strip(" []'")
            altitude = temp_data[4][0].split(':')[1].strip(" []'")

            coordinates.extend([station, latitude, longitude, altitude])

        # Write coordinates to output file
        output_file_path = paths[6]
        with open(output_file_path, 'w') as output_file:
            for item in coordinates:
                output_file.write(f"{item}\n")

    def get_location_coordinates(self) -> str:
        """
        Get the path of the file with the coordinates
        """
        # get_local_cord
        with open('end.txt') as file:
            lines = file.readlines()
        path = lines[6].strip()
        return path

    def get_file_path(self, option: str) -> str:
        """
        Receives a string with the option of choice and returns the path 
        for the file of the selected city
        """
        # retorna_end
        with open('end.txt') as file:
            lines = file.readlines()

        if option == 'Cidade alvo':
            return lines[0].replace("\n", '')
        elif option == 'Neighbor A':
            return lines[1].replace("\n", '')
        elif option == 'Neighbor B':
            return lines[2].replace("\n", '')
        elif option == 'Neighbor C':
            return lines[3].replace("\n", '')