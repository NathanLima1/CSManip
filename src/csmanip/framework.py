from tkinter import Frame
from tkinter import ttk
from tkinter import Canvas, Label, StringVar, Button, CENTER, DISABLED
import tkinter.filedialog as dlg
import tkinter.messagebox as msg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.dates as mdates
import datetime as dt
import os
import numpy as np
from .styles import colors
from .data_processing.data_processing import DataProcessing
from .triangulation.triangulation import Triangulation
from .machine_learning.machine_learning import MachineLearning
from .meta_learning.meta_learning import MetaLearning
from .meta_learning.tests_generator import TestsGenerator

class Framework(Frame):
    def get_info(self, directory):  # Function that opens the folder with .csv files and returns important data
        print("Entrou Principal get_info")
        raw_data = []

        with open(directory, 'r') as file:
            for line in file:
                text = line.replace('\n', '')
                raw_data.append(text)
        # Remove the last element from the list
        if raw_data:
            del raw_data[-1]

        name = raw_data[0][6:]
        latitude = float(raw_data[2][10:])
        longitude = float(raw_data[3][10:])
        altitude = float(raw_data[4][10:])
        address = directory

        return name, latitude, longitude, altitude, address

    def list_cities(self):
        print("Entrou Principal list_cities")
        db_location = dlg.askdirectory()

        file_name_list = os.listdir(db_location)  # The user selects the location where the data is stored
        file_path_list = []

        for file_name in file_name_list:
            file_path_list.append(f"{db_location}/{file_name}")

        self.all_city_names = []
        self.city_path_list = []  # List containing city names and their file paths

        for file_path in file_path_list:
            name, lat, lon, alt, address = self.get_info(file_path)
            self.all_city_names.append(name)
            self.city_path_list.append([name, address])

        self.all_city_names.sort()

        self.target_city = StringVar()
        Label(self, text='Target city:', font='Arial 11 bold', bg=colors.fundo, fg='white').place(x=20, y=65)
        self.target_combo = ttk.Combobox(
            self,
            values=self.all_city_names,
            textvariable=self.target_city,
            width=20,
            font='Arial 11',
            justify=CENTER,
            state='normal'
        ).place(x=20, y=85)

        self.neighbor_a = StringVar()
        Label(self, text='Neighbor A:', font='Arial 11 bold', bg=colors.fundo, fg='white').place(x=220, y=65)
        self.combo_a = ttk.Combobox(
            self,
            values=self.all_city_names,
            textvariable=self.neighbor_a,
            width=20,
            font='Arial 11',
            justify=CENTER,
            state='readonly'
        ).place(x=224, y=85)

        self.neighbor_b = StringVar()
        Label(self, text='Neighbor B:', font='Arial 11 bold', bg=colors.fundo, fg='white').place(x=20, y=115)
        self.combo_b = ttk.Combobox(
            self,
            values=self.all_city_names,
            textvariable=self.neighbor_b,
            width=20,
            font='Arial 11',
            justify=CENTER,
            state='readonly'
        ).place(x=20, y=135)

        self.neighbor_c = StringVar()
        Label(self, text='Neighbor C:', font='Arial 11 bold', bg=colors.fundo, fg='white').place(x=220, y=115)
        self.combo_c = ttk.Combobox(
            self,
            values=self.all_city_names,
            textvariable=self.neighbor_c,
            width=20,
            font='Arial 11',
            justify=CENTER,
            state='readonly'
        ).place(x=224, y=135)

        Button(
            self,
            text='Confirmar Grupo',
            font='Arial 12 bold',
            fg='white',
            bg=colors.fun_b,
            width=38,
            command=self.process_selection
        ).place(x=20, y=170)

    def process_selection(self):
        # antiga tratar
        print("Entrou Principal process_section")
        if (
            self.target_city.get() == ''
            or self.neighbor_a.get() == ''
            or self.neighbor_b.get() == ''
            or self.neighbor_c.get() == ''
        ):
            msg.showerror(title='Dados Incompletos', message="Alguma(s) cidade(s) não foi(foram) selecionada(s)")
            return

        self.city_history = [
            self.target_city.get(),
            self.neighbor_a.get(),
            self.neighbor_b.get(),
            self.neighbor_c.get()
        ]
        self.history_var = StringVar()

        target_path = ''
        for city_name, path in self.city_path_list:
            if city_name == self.target_city.get():
                target_path = path
                break

        neighbor_a_path = ''
        for city_name, path in self.city_path_list:
            if city_name == self.neighbor_a.get():
                neighbor_a_path = path
                break

        neighbor_b_path = ''
        for city_name, path in self.city_path_list:
            if city_name == self.neighbor_b.get():
                neighbor_b_path = path
                break

        neighbor_c_path = ''
        for city_name, path in self.city_path_list:
            if city_name == self.neighbor_c.get():
                neighbor_c_path = path
                break

        data_processor = DataProcessing()
        data_processor.target = target_path
        data_processor.neighborA = neighbor_a_path
        data_processor.neighborB = neighbor_b_path
        data_processor.neighborC = neighbor_c_path
        data_processor.download_path = os.getcwd()

        self.save_location = os.getcwd()
        data_processor.get_processed_data()

        msg.showinfo(title="Sucesso!", message="Arquivos Selecionados com sucesso!")

    def get_col(self):
        print("Entrou Principal get_col")
        if self.parameter.get() == "Precipitação":
            y_name = "Precipitação (mm)"
            col = 3
        elif self.parameter.get() == "Temperatura máxima":
            col = 4
            y_name = "Temperatura (°C)"
        elif self.parameter.get() == "Temperatura mínima":
            y_name = "Temperatura (°C)"
            col = 5
        return y_name, col

    def common_graphs(self):
        print("Entrou Principal common_graphs")
        data_processor = DataProcessing()
        analyzed_data = data_processor.load_data_file(self.type_data.get())

        self.generate_range()

        y_label, col_index = self.get_col()

        x_axis = []
        if self.type_data.get() == 'Dados comum':
            y_axis_1, y_axis_2, y_axis_3, y_axis_4 = [], [], [], []
            common_count, target_count, va_count, vb_count, vc_count = data_processor.get_quantities()
            bar_y_values = [common_count, target_count, va_count, vb_count, vc_count]
            bar_x_labels = ['Common', 'Target', 'Total vA', 'Total vB', 'Total vC']
        else:
            y_axis = []

        data_table = []
        for row in analyzed_data:
            data_table.append(row)
            year, month, day = str(row[0]), str(row[1]), str(row[2])
            date_str = f"{month}/{day}/{year}"

            try:
                date_obj = dt.datetime.strptime(date_str, "%m/%d/%Y").date()
            except ValueError:
                continue

            if self.type_data.get() == 'Dados comum':
                try:
                    y_axis_1.append(float(row[col_index].replace(',', '.')))
                    y_axis_2.append(float(row[col_index + 3].replace(',', '.')))
                    y_axis_3.append(float(row[col_index + 6].replace(',', '.')))
                    y_axis_4.append(float(row[col_index + 9].replace(',', '.')))
                    x_axis.append(date_obj)
                except ValueError:
                    continue
            else:
                try:
                    y_axis.append(float(row[col_index]))
                    x_axis.append(date_obj)
                except ValueError:
                    continue

        fig = Figure(figsize=(14.5, 9.5), dpi=100)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)

        if self.type_data.get() == 'Dados comum':
            plot1 = fig.add_subplot(321)
            plot2 = fig.add_subplot(322)
            plot3 = fig.add_subplot(323)
            plot4 = fig.add_subplot(324)
            plot5 = fig.add_subplot(325)
            plot6 = fig.add_subplot(326)

            plot1.plot(x_axis, y_axis_1, label="Target")
            plot2.plot(x_axis, y_axis_2, label="Neighbor A", color="red")
            plot3.plot(x_axis, y_axis_3, label="Neighbor B", color='green')
            plot4.plot(x_axis, y_axis_4, label="Neighbor C", color='orange')

            plot5.scatter(x_axis, y_axis_1, s=2, alpha=1, color='blue')
            plot5.scatter(x_axis, y_axis_2, s=2, alpha=1, color='red')
            plot5.scatter(x_axis, y_axis_3, s=2, alpha=1, color='green')
            plot5.scatter(x_axis, y_axis_4, s=2, alpha=1, color='orange')

            plot6.bar(bar_x_labels, bar_y_values)

            for plot in [plot1, plot2, plot3, plot4, plot5]:
                plot.set_xticklabels(x_axis, rotation=15, ha='right')
                plot.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))
                plot.grid(True)
                plot.set_ylabel(y_label)
                plot.legend()

            plot6.set_ylabel('Data Count')
        else:
            plot1 = fig.add_subplot(111)
            plot1.plot(x_axis, y_axis)
            plot1.set_xticklabels(x_axis, rotation=15, ha='right')
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))
            plot1.grid(True)
            plot1.set_ylabel(y_label)
            plot1.set_title(self.parameter.get())

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=450, y=57)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def range_graphs(self):
        my_data = DataProcessing()
        data_ana = my_data.load_data_file(self.type_data.get())
        
        nome_y, col = self.get_col()

        ano_inicio = int(self.var_ini.get())
        ano_final = int(self.var_fim.get())
        if ano_final < ano_inicio:
            msg.showerror(title='Invalid', message='O range inserido é inválido')
            return
        if self.parameter.get() == 'Dados comum':
            self.grafico_dc(ano_inicio,ano_final)
            return
        
        eixo_x = list()
        if self.type_data.get() == 'Dados comum':
            eixo_y1 = list()
            eixo_y2 = list()
            eixo_y3 = list()
            eixo_y4 = list()
            util, tar,t_va, t_vb, t_vc = my_data.get_quantities()
            eixo_y_bar = [util, tar,t_va, t_vb, t_vc]
            eixo_x_bar = ['Comum', 'target','Total vA', 'Total vB', 'Total vC']
        else:
            eixo_y = list()

        dados_lb = list()

        for i in data_ana:
            if int(i[0]) >= ano_inicio and int(i[0]) <= ano_final:
                dados_lb.append(i)

                ano = str(i[0])
                
                mes = str(i[1])
                dia = str(i[2])
                text_data = mes + '/' + dia + '/' + ano
                eixo_x.append(dt.datetime.strptime(text_data,"%m/%d/%Y").date())

                if self.type_data.get() == 'Dados comum':
                    eixo_y1.append(float(i[col]))
                    eixo_y2.append(float(i[col+3]))
                    eixo_y3.append(float(i[col+6]))
                    eixo_y4.append(float(i[col+9]))
                else:
                    eixo_y.append(float(i[col]))
        
        
        fig = Figure(figsize=(14.5,9.5), dpi=100)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)

        if self.type_data.get() == 'Dados comum':
            plot1 = fig.add_subplot(321)
            plot2 = fig.add_subplot(322)
            plot3 = fig.add_subplot(323)
            plot4 = fig.add_subplot(324)
            plot5 = fig.add_subplot(325)
            plot6 = fig.add_subplot(326)
            plot1.plot(eixo_x, eixo_y1, label="target")
            plot2.plot(eixo_x, eixo_y2, label="Viz A", color="red")
            plot3.plot(eixo_x, eixo_y3, label="Viz B", color='green')
            plot4.plot(eixo_x, eixo_y4, label="Viz C", color='orange')
            plot5.scatter(eixo_x, eixo_y1, s=2, alpha=1, color='blue')
            plot5.scatter(eixo_x, eixo_y2, s=2, alpha=0.6, color='red')
            plot5.scatter(eixo_x, eixo_y3, s=2, alpha=0.6, color='green')
            plot5.scatter(eixo_x, eixo_y4, s=2, alpha=0.6, color='orange')
            plot6.bar(eixo_x_bar, eixo_y_bar)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot2.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot3.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot4.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot5.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot1.legend()
            plot2.legend()
            plot3.legend()
            plot4.legend()
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot3.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot4.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot5.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot1.grid(True)
            plot2.grid(True)
            plot3.grid(True)
            plot4.grid(True)
            plot5.grid(True)
            plot1.set_ylabel(nome_y)
            plot2.set_ylabel(nome_y)
            plot3.set_ylabel(nome_y)
            plot4.set_ylabel(nome_y)
            plot5.set_ylabel(nome_y)
            plot6.set_ylabel('Qtd. de dados')
            
        else:
            plot1 = fig.add_subplot(111)
            plot1.plot(eixo_x, eixo_y)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')   
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))   
                
            plot1.grid(True)
            plot1.set_ylabel(nome_y)
            plot1.set_title(self.parameter.get())
        canvas = FigureCanvasTkAgg(fig, master=self.master)
            
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=450, y=57)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
    
    def show_map(self):
        triang = Triangulation()
        triang.show_map()

    def generate_range(self):
        print("Entrou Principal generate_range")
        teste = DataProcessing()
        self.var_ini = StringVar()
        self.anos = teste.get_year_range(self.type_data.get())
        Label(self, text='Início:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=20, y=290)
        self.com_ini = ttk.Combobox(self, values=self.anos, textvariable=self.var_ini, font='Arial 12', justify=CENTER, state='readonly', width=12).place(x=20, y=310)

        self.var_fim = StringVar()
        Label(self, text='Final:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=165, y=290)
        self.com_fim = ttk.Combobox(self, values=self.anos, textvariable=self.var_fim, font='Arial 12', justify=CENTER, state='readonly', width=12).place(x=165, y=310)
        
        Button(self, text='Def. Range', font='Arial 11 bold', fg='white', bg=colors.fun_b, width=10, command=self.range_graphs).place(x=310, y=305)

    def triangulation(self):
        met = self.metodo.get()

        canvas = Canvas(self, height=200, width=200, bg=colors.fundo, border=0).place(x=450, y=200)
      
        trian = Triangulation()

        ind = self.paramt_tri.get()
        if ind == 'Precipitação':
            focus = 1
            y_label = "Precipitação (mm)"
        elif ind == 'Temperatura máxima':
            focus = 2
            y_label = "Temperatura(°C)"
        else:
            focus = 3
            y_label = "Temperatura(°C)"


        metodo_list = ['Arithmetic Averange', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']  

        if met == 'Arithmetic Averange':
            trian.avg(focus)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_avg()
        elif met == 'Inverse Distance Weighted':
            trian.idw(focus)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_idw()
        elif met == 'Regional Weight':
            trian.rw(focus)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_rw()
        else:
            trian.onr(focus)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_onr()

        

        
       
        media_ea = round(media_ea, 4)
        media_er = round(media_er, 4)
        texto = 'Média Erro absoluto: '+ str(media_ea) + ' | Média Erro relativo: '+ str(media_er)
        figura = Figure(figsize=(14.5,9.5), dpi=100)
        figura.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_tri, label='IDW', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel(y_label)
        plot_r.set_xlabel("Comparações")
        plot_r.set_title(texto)
        

        
        canvas = FigureCanvasTkAgg(figura, master=self.master)
        
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=450, y=57)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)

        toolbar.update()

    def preparar_eixos(self, mat, foco):
        x = list()
        y = list()

        for i in range(len(mat)):
            y.append(mat[i][foco])
            text = str(mat[i][1]) + '/' + str(mat[i][2]) + '/' + str(mat[i][0])
            x.append(dt.datetime.strptime(text,"%m/%d/%Y").date())
    
        return x, y

    def prepara_mat(self, dados, foco):
        mat = list()
        for i in range(len(dados)):
            mat.append([int(dados[i][0]), int(dados[i][1]), int(dados[i][2]), float(dados[i][foco])])
        return mat
    
    def separa_estacao(self, dados, est):
        if est == 1:
            mes1 = 12
            mes2 = 1
            mes3 = 2

        sazonal = list()
        aux = list()
        flag = 0
        for i in range(len(dados)):
            try:
                if mes1 == dados[i][1] or mes2 == dados[i][1] or mes3 == dados[i][1]:
                    aux.append(dados[i])
                    flag = 0
                elif dados[i+1][1] == mes3 + 1 and flag == 0:
                    sazonal.append(aux)
                    aux = list()
                    flag = 1
                
            except IndexError:
                sazonal.append(aux)
                aux = list()
        return sazonal

    def histograma(self):
        t = DataProcessing()
        data = t.load_data_file(self.data_hist.get())
        if self.paramt_hist.get() == "Precipitação":
            col = 3
        elif self.paramt_hist.get() == "Temperatura máxima":
            col = 4
        elif self.paramt_hist.get() == "Temperatura mínima":
            col = 5

        mat = self.prepara_mat(data, col)
        
        saz = self.separa_estacao(mat,1)
        del saz[0]
        
        ultimo = len(saz) - 2
        
        x1, y1 = self.preparar_eixos(saz[ultimo-9], 3)
        x2, y2 = self.preparar_eixos(saz[ultimo-8], 3)
        x3, y3 = self.preparar_eixos(saz[ultimo-7], 3)
        x4, y4 = self.preparar_eixos(saz[ultimo-6], 3)
        x5, y5 = self.preparar_eixos(saz[ultimo-5], 3)
        x6, y6 = self.preparar_eixos(saz[ultimo-4], 3)
        x7, y7 = self.preparar_eixos(saz[ultimo-3], 3)
        x8, y8 = self.preparar_eixos(saz[ultimo-2], 3)
        x9, y9 = self.preparar_eixos(saz[ultimo-1], 3)
        x10, y10 = self.preparar_eixos(saz[ultimo], 3)

        
        x = list()
        cont = 17
        
        for i in range(17, 50):
            x.append(cont)
            cont += 0.5
        max_lim = max(max(y1), max(y2), max(y3), max(y4), max(y5), max(y6), max(y7), max(y8), max(y9), max(y10)) +0.5
        min_lim = min(min(y1), min(y2), min(y3), min(y4), min(y5), min(y6), min(y7), min(y8), min(y9), min(y10)) -0.5

        
        y1 = np.array(y1)
        y2 = np.array(y2)
        y3 = np.array(y3)
        y4 = np.array(y4)
        y5 = np.array(y5)
        y6 = np.array(y6)
        y7 = np.array(y7)
        y8 = np.array(y8)
        y9 = np.array(y9)
        y10 = np.array(y10)


        fig = Figure(figsize=(14.5,9.5), dpi=100)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)
        plot1 = fig.add_subplot(2,5,1)
        plot1.set_title(saz[ultimo-9][len(saz[ultimo-9])-1][0])
        plot1.hist(y1, bins=40, linewidth=0.5, edgecolor="white")
        plot1.set_xlim((min_lim, max_lim))
        plot1.axvline(y1.mean(), color='red')
        

        plot2 = fig.add_subplot(2,5,2)
        plot2.set_title(saz[ultimo-8][len(saz[ultimo-8])-1][0])
        plot2.hist(y2, bins=40, linewidth=0.5, edgecolor="white")
        plot2.set_xlim((min_lim, max_lim))
        plot2.axvline(y2.mean(), color='red')

        plot3 = fig.add_subplot(2,5,3)
        plot3.set_title(saz[ultimo-7][len(saz[ultimo-7])-1][0])
        plot3.hist(y3, bins=40, linewidth=0.5, edgecolor="white")
        plot3.set_xlim((min_lim, max_lim))
        plot3.axvline(y3.mean(), color='red')


        plot4 = fig.add_subplot(2,5,4)
        plot4.set_title(saz[ultimo-6][len(saz[ultimo-6])-1][0])
        plot4.hist(y4, bins=40, linewidth=0.5, edgecolor="white")
        plot4.set_xlim((min_lim, max_lim))
        plot4.axvline(y4.mean(), color='red')


        plot5 = fig.add_subplot(2,5,5)
        plot5.set_title(saz[ultimo-5][len(saz[ultimo-5])-1][0])
        plot5.hist(y5, bins=40, linewidth=0.5, edgecolor="white")
        plot5.set_xlim((min_lim, max_lim))
        plot5.axvline(y5.mean(), color='red')


        plot6 = fig.add_subplot(2,5,6)
        plot6.set_title(saz[ultimo-4][len(saz[ultimo-4])-1][0])
        plot6.hist(y6, bins=40, linewidth=0.5, edgecolor="white")
        plot6.set_xlim((min_lim, max_lim))
        plot6.axvline(y6.mean(), color='red')


        plot7 = fig.add_subplot(2,5,7)
        plot7.set_title(saz[ultimo-3][len(saz[ultimo-3])-1][0])
        plot7.hist(y7, bins=40, linewidth=0.5, edgecolor="white")
        plot7.set_xlim((min_lim, max_lim))
        plot7.axvline(y7.mean(), color='red')


        plot8 = fig.add_subplot(2,5,8)
        plot8.set_title(saz[ultimo-2][len(saz[ultimo-2])-1][0])
        plot8.hist(y8, bins=40, linewidth=0.5, edgecolor="white")
        plot8.set_xlim((min_lim, max_lim))
        plot8.axvline(y8.mean(), color='red')


        plot9 = fig.add_subplot(2,5,9)
        plot9.set_title(saz[ultimo-1][len(saz[ultimo-1])-1][0])
        plot9.hist(y9, bins=40, linewidth=0.5, edgecolor="white")
        plot9.set_xlim((min_lim, max_lim))
        plot9.axvline(y9.mean(), color='red')


        plot10 = fig.add_subplot(2,5,10)
        plot10.set_title(saz[ultimo][len(saz[ultimo])-1][0])
        plot10.hist(y10, bins=40, linewidth=0.5, edgecolor="white")
        plot10.set_xlim((min_lim, max_lim))
        plot10.axvline(y10.mean(), color='red')


        canvas = FigureCanvasTkAgg(fig, master=self.master)
        
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=450, y=57)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def boxplot_grafico(self):
        t = DataProcessing()
        data = t.load_data_file(self.data_hist.get())
        if self.paramt_hist.get() == "Precipitação":
            col = 3
        elif self.paramt_hist.get() == "Temperatura máxima":
            col = 4
        elif self.paramt_hist.get() == "Temperatura mínima":
            col = 5

        mat = self.prepara_mat(data, col)
        
        saz = self.separa_estacao(mat,1)
        del saz[0]
        
        ultimo = len(saz) - 2
        
        x1, y1 = self.preparar_eixos(saz[ultimo-9], 3)
        x2, y2 = self.preparar_eixos(saz[ultimo-8], 3)
        x3, y3 = self.preparar_eixos(saz[ultimo-7], 3)
        x4, y4 = self.preparar_eixos(saz[ultimo-6], 3)
        x5, y5 = self.preparar_eixos(saz[ultimo-5], 3)
        x6, y6 = self.preparar_eixos(saz[ultimo-4], 3)
        x7, y7 = self.preparar_eixos(saz[ultimo-3], 3)
        x8, y8 = self.preparar_eixos(saz[ultimo-2], 3)
        x9, y9 = self.preparar_eixos(saz[ultimo-1], 3)
        x10, y10 = self.preparar_eixos(saz[ultimo], 3)

        
        x = list()
        cont = 17
        
        for i in range(17, 50):
            x.append(cont)
            cont += 0.5
        max_lim = max(max(y1), max(y2), max(y3), max(y4), max(y5), max(y6), max(y7), max(y8), max(y9), max(y10)) +0.5
        min_lim = min(min(y1), min(y2), min(y3), min(y4), min(y5), min(y6), min(y7), min(y8), min(y9), min(y10)) -0.5

        boxplot = list()
        boxplot.append(y1)
        boxplot.append(y2)
        boxplot.append(y3)
        boxplot.append(y4)
        boxplot.append(y5)
        boxplot.append(y6)
        boxplot.append(y7)
        boxplot.append(y8)
        boxplot.append(y9)
        boxplot.append(y10)


        fig = Figure(figsize=(14.5,9.5), dpi=100)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)
     
        plot1 = fig.add_subplot(1,1,1)
        plot1.set_title("Boxplot para Temperatura máxima [10 Anos]")
        plot1.boxplot(boxplot)
        plot1.set_xlabel('Ano')
        plot1.set_ylabel(self.data_hist.get())
        

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=450, y=57)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
    
    def open_machine(self):
        window = MachineLearning()
        window.mainloop()

    def open_meta(self):
        window = TestsGenerator()
        window.mainloop()

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, master=None, bg=colors.fundo) #Configurando a janela da ferramenta
        self.master.title("IC_FAPEMGIG - V1.0") #Colocando o titulo na aba da ferramenta
        self.master.geometry('800x800') #Definindo o tamanho inicial da tela (podendo expandir)

        Button(self, text='Selecionar Banco de Dados', font='Arial 12 bold', fg='white', bg=colors.fun_ap, width=38, command=self.list_cities).place(x=20, y=20) #Botão para os usuários selecionar a pasta que tem todos os arquivos.csv
        self.pack(fill='both', expand=True)

        Label(self, text='Target city:', font='Arial 11 bold', bg=colors.fundo, fg='white', state=DISABLED).place(x=20, y=65)
        self.comb_target = ttk.Combobox(self, width=20, font='Arial 11', justify=CENTER, state=DISABLED).place(x=20, y=85)
        Label(self, text='Neighbor A:', font='Arial 11 bold', bg=colors.fundo, fg='white', state=DISABLED).place(x=220, y=65)
        self.comb_va = ttk.Combobox(self, width=20, font='Arial 11', justify=CENTER, state=DISABLED).place(x=224, y=85)
        Label(self, text='Neighbor B:', font='Arial 11 bold', bg=colors.fundo, fg='white', state=DISABLED).place(x=20, y=115)
        self.comb_vb = ttk.Combobox(self, width=20, font='Arial 11', justify=CENTER, state=DISABLED).place(x=20, y=135)
        Label(self, text='Neighbor C:', font='Arial 11 bold', bg=colors.fundo, fg='white', state=DISABLED).place(x=220, y=115)
        self.comb_vc = ttk.Combobox(self, width=20, font='Arial 11', justify=CENTER, state=DISABLED).place(x=224, y=135)

        Button(self, text='Confirmar Grupo', font='Arial 12 bold', fg='white', bg=colors.fun_b, width=38, command=self.process_selection, state=DISABLED).place(x=20, y=170)


        Label(self, text='Visualizar Dados', font='Arial 14 bold', fg='white', bg=colors.fundo).place(x=140, y=210)
        Label(self, text='Dado:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=20, y=240)
        self.type_data = StringVar()
        data_list = ['Target city', 'Neighbor A', 'Neighbor B', 'Neighbor C', 'Dados comum']
        self.comb_type_data = ttk.Combobox(self, values=data_list, textvariable=self.type_data, width=12, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=260)
        
        Label(self, text='Parâmetro:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=165, y=240)
        self.parameter = StringVar()
        para_list = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        self.comb_parameter = ttk.Combobox(self, values=para_list, textvariable=self.parameter, width=12, font='Arial 12', justify=CENTER, state='readonly').place(x=165, y=260)
        Button(self, text='Selecionar', font='Arial 11 bold', fg='white', bg=colors.fun_b, width=10, command=self.common_graphs).place(x=310, y=255)

       
        Label(self, text='Início:', font='Arial 12 bold', fg='white', bg=colors.fundo, state=DISABLED).place(x=20, y=290)
        self.com_ini = ttk.Combobox(self, font='Arial 12', justify=CENTER, state=DISABLED, width=12).place(x=20, y=310)
        Label(self, text='Final:', font='Arial 12 bold', fg='white', bg=colors.fundo, state=DISABLED).place(x=165, y=290)
        self.com_fim = ttk.Combobox(self, font='Arial 12', justify=CENTER, state=DISABLED, width=12).place(x=165, y=310)
        
        Button(self, text='Def. Range', font='Arial 11 bold', fg='white', bg=colors.fun_b, width=10, command=self.range_graphs, state=DISABLED).place(x=310, y=305)


        Label(self, text='Dado', font='Arial 11 bold', fg='white', bg=colors.fundo).place(x=20, y=340)    
        self.data_hist = StringVar()
        datahist_list = ['Target city', 'Neighbor A', 'Neighbor B', 'Neighbor C']  
        ttk.Combobox(self, values=datahist_list, textvariable=self.data_hist, width=18, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=360)
        Label(self, text='Parâmetro', font='Arial 11 bold', fg='white', bg=colors.fundo).place(x=20, y=390)    
        self.paramt_hist = StringVar()
        ttk.Combobox(self, values=para_list, textvariable=self.paramt_hist, width=18, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=410)
        Button(self, text='Histograma, últimos 10y', font='Arial 11 bold', fg='white', bg=colors.fun_meta_le, width=20, command=self.histograma).place(x=220, y=355) 
        
        Button(self, text='Boxplot, últimos 10y', font='Arial 11 bold', fg='white', bg=colors.fun_meta_le, width=20, command=self.boxplot_grafico).place(x=220, y=405) 

        Label(self, text='Técnicas', font='Arial 14 bold', fg='white', bg=colors.fundo).place(x=170, y=460)
        Button(self, text='Machine Learning', font='Arial 11 bold', fg='white', bg=colors.fun_ap, width=42, command=self.open_machine).place(x=20, y=495)

        Label(self, text='Method', font='Arial 11 bold', fg='white', bg=colors.fundo).place(x=20, y=530)    
        self.metodo = StringVar()
        metodo_list = ['Arithmetic Averange', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']  
        self.comb_metodo = ttk.Combobox(self, values=metodo_list, textvariable=self.metodo, width=18, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=550)
        self.teste = Label(self, text='Parâmetro', font='Arial 11 bold', fg='white', bg=colors.fundo).place(x=20, y=580)    
        self.paramt_tri = StringVar()
        self.comb_para_tro = ttk.Combobox(self, values=para_list, textvariable=self.paramt_tri, width=18, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=600)
        Button(self, text='Triangulação', font='Arial 11 bold', fg='white', bg=colors.fun_alt, width=20, height=4, command=self.triangulation).place(x=220, y=540) 
        
        Button(self, text='Mostrar Localização', font='Arial 11 bold', fg='white', bg=colors.fun_alt, width=42, command=self.show_map).place(x=20, y=640) 

        Button(self, text='Meta Learning', font='Arial 11 bold', fg='white', bg=colors.fun_b, width=42, command=self.open_meta).place(x=20, y=680)
       