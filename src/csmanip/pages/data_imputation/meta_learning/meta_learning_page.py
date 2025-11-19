import tkinter as tk
from tkinter import ttk, messagebox as msg, StringVar, IntVar, BooleanVar
import typing
import os
import threading

from ...tooltip import CreateToolTip
from ....meta_learning.meta_learning import MetaLearning

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tksheet import Sheet

if typing.TYPE_CHECKING:
    from ...start_page import StartPage

class MetaLearningPage(ttk.Frame):
    """Tela para configuração e execução de Meta Learning."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.ml_lv0_var = StringVar(value='Decision Trees')
        self.ml_tr0_var = StringVar(value='Arithmetic Average')
        self.ml_lv1_var = StringVar(value='Decision Trees')
        self.ind_meta_perso_var = StringVar(value='Maximum temperature')
        self.num_teste_mtp_var = IntVar(value=1)
        self.pre_para_lv0_var = IntVar(value=0)
        self.pre_para_lv1_var = IntVar(value=0)
        self.type_input_var = StringVar(value='Yes')

        self.pre_nn_comb_var = IntVar(value=0)
        self.pre_dt_comb_var = IntVar(value=0)
        self.pre_bt_comb_var = IntVar(value=0)
        self.pre_nneig_comb_var = IntVar(value=0)
        self.pre_sv_comb_var = IntVar(value=0)
        self.pre_gp_comb_var = IntVar(value=0)
        self.ind_meta_comb_var = StringVar(value='Maximum temperature')
        self.num_teste_mtc_var = IntVar(value=1)

        # --- Flags de Animação ---
        self.loading_ct = False
        self.loading_gt = False

        # --- Frame Superior ---
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        self.back_button = ttk.Button(top_frame, text="", command=self.go_to_previous_page)
        self.back_button.pack(side=tk.LEFT)
        self.page_title = ttk.Label(top_frame, text="", font=("Verdana", 16, "bold"))
        self.page_title.pack(side=tk.LEFT, expand=True)

        # --- Layout Principal ---
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_container.grid_columnconfigure(0, weight=1, minsize=400) # Painel esquerdo maior
        main_container.grid_columnconfigure(1, weight=3) # Painel direito
        main_container.grid_rowconfigure(0, weight=1)

        # --- PAINEL ESQUERDO (Com Scrollbar) ---
        left_panel_base = ttk.Frame(main_container)
        left_panel_base.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_panel_base.grid_rowconfigure(0, weight=1)
        left_panel_base.grid_columnconfigure(0, weight=1)

        canvas_left = tk.Canvas(left_panel_base)
        canvas_left.grid(row=0, column=0, sticky="nsew")
        scrollbar_left = ttk.Scrollbar(left_panel_base, orient="vertical", command=canvas_left.yview)
        scrollbar_left.grid(row=0, column=1, sticky="ns")
        canvas_left.configure(yscrollcommand=scrollbar_left.set)
        self.scrollable_frame_left = ttk.Frame(canvas_left)
        canvas_left.create_window((0, 0), window=self.scrollable_frame_left, anchor="nw")
        self.scrollable_frame_left.bind("<Configure>", lambda e: canvas_left.configure(scrollregion=canvas_left.bbox("all")))
        canvas_left.bind_all("<MouseWheel>", lambda e: canvas_left.yview_scroll(int(-1*(e.delta/120)), "units")) # Windows
        canvas_left.bind_all("<Button-4>", lambda e: canvas_left.yview_scroll(-1, "units")) # Linux up
        canvas_left.bind_all("<Button-5>", lambda e: canvas_left.yview_scroll(1, "units")) # Linux down

        custom_test_frame = ttk.LabelFrame(self.scrollable_frame_left, text="")
        custom_test_frame.pack(fill=tk.X, padx=5, pady=5)
        self.custom_test_frame_label = custom_test_frame

        self.lbl_base_learning = ttk.Label(custom_test_frame, text="")
        self.lbl_base_learning.pack(anchor="w", padx=5)
        lista_ml0 = ['None','Decision Trees', 'Bagged Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        self.ml0 = ttk.Combobox(custom_test_frame, values=lista_ml0, textvariable=self.ml_lv0_var, state='readonly')
        self.ml0.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.ml0_hint = CreateToolTip(self.ml0, text='')

        self.lbl_triangulation = ttk.Label(custom_test_frame, text="")
        self.lbl_triangulation.pack(anchor="w", padx=5)
        lista_tr0 = ['None', 'Arithmetic Average', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']
        self.tr0 = ttk.Combobox(custom_test_frame, values=lista_tr0, textvariable=self.ml_tr0_var, state='readonly')
        self.tr0.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.tr0_hint = CreateToolTip(self.tr0, text='')

        self.lbl_meta_learning = ttk.Label(custom_test_frame, text="")
        self.lbl_meta_learning.pack(anchor="w", padx=5)
        lista_ml1 = ['Decision Trees', 'Bagged Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        self.ml1 = ttk.Combobox(custom_test_frame, values=lista_ml1, textvariable=self.ml_lv1_var, state='readonly')
        self.ml1.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.ml1_hint = CreateToolTip(self.ml1, text='')

        self.lbl_indicator_ct = ttk.Label(custom_test_frame, text="")
        self.lbl_indicator_ct.pack(anchor="w", padx=5)
        lista_ind_meta_p = ["Precipitation", 'Maximum temperature', 'Minimum temperature']
        self.indicator_ct = ttk.Combobox(custom_test_frame, values=lista_ind_meta_p, textvariable=self.ind_meta_perso_var, state='readonly')
        self.indicator_ct.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.indicator_ct_hint = CreateToolTip(self.indicator_ct, text='')

        self.lbl_num_tests_ct = ttk.Label(custom_test_frame, text="")
        self.lbl_num_tests_ct.pack(anchor="w", padx=5)
        self.num_tests = ttk.Entry(custom_test_frame, textvariable=self.num_teste_mtp_var, justify=tk.CENTER)
        self.num_tests.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.num_tests_hint = CreateToolTip(self.num_tests, text='')

        self.lbl_pretrained = ttk.Label(custom_test_frame, text="")
        self.lbl_pretrained.pack(anchor="w", padx=5)
        self.pretrained_hint = CreateToolTip(self.lbl_pretrained, text='')
        pretrained_frame = ttk.Frame(custom_test_frame)
        pretrained_frame.pack(fill=tk.X, padx=5)
        self.cb_pre_lv0 = ttk.Checkbutton(pretrained_frame, text="", variable=self.pre_para_lv0_var, onvalue=1, offvalue=0)
        self.cb_pre_lv0.pack(side=tk.LEFT, padx=(0, 10))
        self.cb_pre_lv1 = ttk.Checkbutton(pretrained_frame, text="", variable=self.pre_para_lv1_var, onvalue=1, offvalue=0)
        self.cb_pre_lv1.pack(side=tk.LEFT)

        self.lbl_sliding_window = ttk.Label(custom_test_frame, text="")
        self.lbl_sliding_window.pack(anchor="w", padx=5, pady=(10, 0))
        lista_type_input = ['Yes', 'No']
        self.sliding_window = ttk.Combobox(custom_test_frame, values=lista_type_input, textvariable=self.type_input_var, state='readonly')
        self.sliding_window.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.sliding_window_hint = CreateToolTip(self.sliding_window, text='')

        self.button_ct = ttk.Button(custom_test_frame, text="", command=self.on_click_custom)
        self.button_ct.pack(fill=tk.X, padx=5, pady=10)
        self.prev_ct_hint = CreateToolTip(self.button_ct, text='')

        global_test_frame = ttk.LabelFrame(self.scrollable_frame_left, text="")
        global_test_frame.pack(fill=tk.X, padx=5, pady=5)
        self.global_test_frame_label = global_test_frame

        self.lbl_which_mls = ttk.Label(global_test_frame, text="")
        self.lbl_which_mls.pack(anchor="w", padx=5)
        self.wich_mls_hint = CreateToolTip(self.lbl_which_mls, text='')
        mls_check_frame = ttk.Frame(global_test_frame)
        mls_check_frame.pack(fill=tk.X, padx=5)
        self.ml_check_vars = {
            'NN': self.pre_nn_comb_var, 'DT': self.pre_dt_comb_var,
            'NNeig.': self.pre_nneig_comb_var, 'SV': self.pre_sv_comb_var,
            'GP': self.pre_gp_comb_var, 'BT': self.pre_bt_comb_var
        }
        self.ml_checkbuttons = {}
        for name, var in self.ml_check_vars.items():
            cb = ttk.Checkbutton(mls_check_frame, text=name, variable=var, onvalue=1, offvalue=0)
            cb.pack(side=tk.LEFT, padx=5)
            self.ml_checkbuttons[name] = cb

        self.lbl_indicator_gt = ttk.Label(global_test_frame, text="")
        self.lbl_indicator_gt.pack(anchor="w", padx=5, pady=(10, 0))
        self.indicator_global = ttk.Combobox(global_test_frame, values=lista_ind_meta_p, textvariable=self.ind_meta_comb_var, state='readonly')
        self.indicator_global.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.indicator_gt_hint = CreateToolTip(self.indicator_global, text='')

        self.lbl_num_tests_gt = ttk.Label(global_test_frame, text="")
        self.lbl_num_tests_gt.pack(anchor="w", padx=5)
        self.num_tests_global = ttk.Entry(global_test_frame, textvariable=self.num_teste_mtc_var, justify=tk.CENTER)
        self.num_tests_global.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.num_tests_gt_hint = CreateToolTip(self.num_tests_global, text='')

        self.button_gt = ttk.Button(global_test_frame, text="", command=self.on_click_global)
        self.button_gt.pack(fill=tk.X, padx=5, pady=10)
        self.button_gt_hint = CreateToolTip(self.button_gt, text='')

        warning_frame = ttk.LabelFrame(self.scrollable_frame_left, text="")
        warning_frame.pack(fill=tk.X, padx=5, pady=5)
        self.warning_frame_label = warning_frame
        self.lbl_warning1 = ttk.Label(warning_frame, text="", wraplength=380, justify=tk.LEFT)
        self.lbl_warning1.pack(anchor="w", padx=5)
        self.lbl_warning2 = ttk.Label(warning_frame, text="", wraplength=380, justify=tk.LEFT)
        self.lbl_warning2.pack(anchor="w", padx=5)
        self.lbl_warning3 = ttk.Label(warning_frame, text="", wraplength=380, justify=tk.LEFT)
        self.lbl_warning3.pack(anchor="w", padx=5, pady=(0,5))

        # --- PAINEL DIREITO ---
        self.right_panel = ttk.Frame(main_container)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self.update_texts()

    def go_to_previous_page(self):
        """Importa e navega para a página anterior."""
        from ..imputation_techniques_page import ImputationTechniquesPage
        self.controller.show_frame(ImputationTechniquesPage)

    def _clear_panel(self, panel):
        """Remove todos os widgets de um painel."""
        for widget in panel.winfo_children():
            widget.destroy()

    # --- Button Animation Logic (Adapted) ---
    def on_click_custom(self):
        self.button_ct.config(state=tk.DISABLED)
        self.loading_ct = True
        self.loading_step = 0
        self.animate_loading_ct()
        threading.Thread(target=self.run_process_custom, daemon=True).start()

    def animate_loading_ct(self):
        if self.loading_ct:
            dots = '.' * (self.loading_step % 4)
            i18n = self.controller.i18n
            loading_text = i18n.get('loading_text')
            self.button_ct.config(text=f"{loading_text}{dots}")
            self.loading_step += 1
            self.after(500, self.animate_loading_ct)

    def run_process_custom(self):
        try:
            results = self._generate_custom_test_logic()
            self.after(0, self._display_custom_results, results)
        except Exception as e:
            self.after(0, self.controller.show_translated_message(
                msg_type='error',
                title_key='customized_test_error_title',
                message_key='error_msg',
                error=str(e)
                ))
        finally:
            self.after(0, self.reset_button_custom)

    def reset_button_custom(self):
        self.loading_ct = False
        i18n = self.controller.i18n
        self.button_ct.config(text=i18n.get('generate_preview_btn'), state=tk.NORMAL)

    def on_click_global(self):
        self.button_gt.config(state=tk.DISABLED)
        self.loading_gt = True
        self.loading_step = 0
        self.animate_loading_gt()
        threading.Thread(target=self.run_process_global, daemon=True).start()

    def animate_loading_gt(self):
        if self.loading_gt:
            dots = '.' * (self.loading_step % 4)
            i18n = self.controller.i18n
            loading_text = i18n.get('loading_text')
            self.button_gt.config(text=f"{loading_text}{dots}")
            self.loading_step += 1
            self.after(500, self.animate_loading_gt)

    def run_process_global(self):
        try:
            results = self._generate_global_test_logic()
            self.after(0, self._display_global_results, results)
        except Exception as e:
             self.after(0, self.controller.show_translated_message(
                msg_type='error',
                title_key='global_test_error_title',
                message_key='error_msg',
                ))
        finally:
            self.after(0, self.reset_button_global)

    def reset_button_global(self):
        self.loading_gt = False
        i18n = self.controller.i18n
        self.button_gt.config(text=i18n.get('generate_preview_gt_btn'), state=tk.NORMAL)


    def _generate_custom_test_logic(self):
        """Coleta inputs e chama a lógica de meta-learning customizado."""
        base_model = self.ml_lv0_var.get()
        triangulation = self.ml_tr0_var.get()
        meta_model = self.ml_lv1_var.get()
        indicator = self.ind_meta_perso_var.get()
        num_tests = self.num_teste_mtp_var.get()
        pre_level_0 = self.pre_para_lv0_var.get()
        pre_level_1 = self.pre_para_lv1_var.get()
        input_window = self.type_input_var.get()

        if indicator == "Precipitation": focus = 1
        elif indicator == 'Maximum temperature': focus = 2
        else: focus = 3

        meta = MetaLearning()
        results_tuple = meta.customized_meta_learning(
            focus, base_model, triangulation, meta_model,
            pre_level_0, pre_level_1, num_tests, input_window
        )
        return results_tuple

    def _generate_global_test_logic(self):
        """Coleta inputs e chama a lógica de meta-learning global."""
        target_variable = self.ind_meta_comb_var.get()
        num_tests = self.num_teste_mtc_var.get()
        window_type = 'Yes'

        selected_models = [name for name, var in self.ml_check_vars.items() if var.get() == 1]
        if not selected_models:
            raise ValueError("Nenhum modelo de ML selecionado para o teste global.")

        meta = MetaLearning()
        all_models, model_ranking = meta.combine_meta_learning(
            target_variable, 0, 0, num_tests, window_type, selected_models
        )
        return all_models, model_ranking


    def _display_custom_results(self, results):
        """Exibe os resultados do teste customizado no painel direito."""
        self._clear_panel(self.right_panel)
        if results is None: return

        (meta_ea, meta_er, meta_percent_error, meta_r2, x_meta, y_meta, y_target,
         base_ea, base_er, base_percent, base_r2, tria_ea, tria_er) = results

        i18n = self.controller.i18n

        results_frame = ttk.LabelFrame(self.right_panel, text=i18n.get('results_preview_label'))
        results_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))
        stats_frame = ttk.Frame(results_frame)
        stats_frame.pack(padx=5, pady=5, fill=tk.X)

        # Labels com as métricas
        errors = [
            (i18n.get('abs_error_label'), base_ea, tria_ea, meta_ea),
            (i18n.get('rel_error_label'), base_er, tria_er, meta_er),
            (i18n.get('perc_error_label'), base_percent, tria_ea * 100 if tria_ea is not None else None, meta_percent_error),
            (i18n.get('r2_label'), base_r2, None, meta_r2)
        ]

        for idx, (label, val_ml, val_tri, val_meta) in enumerate(errors):
            row_frame = ttk.Frame(stats_frame)
            row_frame.pack(fill=tk.X)
            ttk.Label(row_frame, text=f"{label}:", width=15, anchor="w").pack(side=tk.LEFT, padx=(0,5))
            if val_ml is not None:
                 ttk.Label(row_frame, text=f"{i18n.get('ml_label')}: {round(val_ml, 4)}", width=20).pack(side=tk.LEFT, padx=5)
            if val_tri is not None:
                 ttk.Label(row_frame, text=f"{i18n.get('triang_label')}: {round(val_tri, 4)}", width=20).pack(side=tk.LEFT, padx=5)
            if val_meta is not None:
                 ttk.Label(row_frame, text=f"{i18n.get('meta_label')}: {round(val_meta, 4)}", width=20).pack(side=tk.LEFT, padx=5)


        figure = Figure(figsize=(10, 6), dpi=100) 

        # Absolute Error
        ax1 = figure.add_subplot(2, 2, 1)
        bars1_x = [i18n.get('ml_label'), i18n.get('triang_label'), i18n.get('meta_label')]
        bars1_y = [base_ea, tria_ea, meta_ea]
        ax1.bar(bars1_x, bars1_y)
        ax1.set_ylabel(i18n.get('abs_error_header'))

        # Relative Error
        ax2 = figure.add_subplot(2, 2, 2)
        bars2_y = [base_er, tria_er, meta_er]
        ax2.bar(bars1_x, bars2_y) # Reusa x labels
        ax2.set_ylabel(i18n.get('rel_error_header'))

        # Percentage Error
        ax3 = figure.add_subplot(2, 2, 3)
        bars3_y = [base_percent, tria_ea * 100 if tria_ea is not None else 0, meta_percent_error]
        ax3.bar(bars1_x, bars3_y)
        ax3.set_ylabel(i18n.get('perc_error_header'))

        # R² Score
        ax4 = figure.add_subplot(2, 2, 4)
        bars4_x = [i18n.get('ml_label'), i18n.get('meta_label')]
        bars4_y = [base_r2, meta_r2]
        ax4.bar(bars4_x, bars4_y)
        ax4.set_ylabel(i18n.get('r2_label'))

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=self.right_panel)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.right_panel)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        toolbar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))

    def _display_global_results(self, results):
        """Exibe os resultados do teste global (tabelas e gráfico) no painel direito."""
        self._clear_panel(self.right_panel)
        if results is None: return

        all_models, model_ranking = results
        i18n = self.controller.i18n

        all_models_frame = ttk.LabelFrame(self.right_panel, text=i18n.get('generated_models_label'))
        all_models_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        all_data = [[m[0], m[1], m[2], m[3], m[5], m[6], m[7]] for m in all_models]
        headers = [
            i18n.get('model_header'), i18n.get('base_learning_header'),
            i18n.get('triangulation_header'), i18n.get('meta_learning_header'),
            i18n.get('abs_error_header'), i18n.get('rel_error_header'),
            i18n.get('perc_error_header')
        ]

        all_models_table = Sheet(all_models_frame, data=all_data, headers=headers)
        all_models_table.enable_bindings()
        all_models_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Ranking e Gráfico ---
        bottom_frame = ttk.Frame(self.right_panel)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        bottom_frame.grid_columnconfigure(0, weight=1) # Tabela Ranking
        bottom_frame.grid_columnconfigure(1, weight=3) # Gráfico Ranking
        bottom_frame.grid_rowconfigure(0, weight=1)

        # Frame para a Tabela de Ranking
        ranking_frame = ttk.LabelFrame(bottom_frame, text=i18n.get('model_ranking_label'))
        ranking_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        ranking_data = [[m[0], round(float(str(m[1]).replace(',', '.')), 4)] for m in model_ranking]
        ranking_headers = [i18n.get('model_header'), i18n.get('error_header')]
        ranking_table = Sheet(ranking_frame, data=ranking_data, headers=ranking_headers, width=250)
        ranking_table.enable_bindings()
        ranking_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        graph_frame = ttk.LabelFrame(bottom_frame, text=i18n.get('model_ranking_label'))
        graph_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        top_n = 15
        x_labels = [str(m[0]) for i, m in enumerate(model_ranking) if i < top_n]
        y_values = [round(float(str(m[1]).replace(',', '.')), 4) for i, m in enumerate(model_ranking) if i < top_n]

        figure = Figure(figsize=(8, 3), dpi=100)
        plot = figure.add_subplot(111)
        plot.bar(x_labels, y_values)
        plot.set_ylabel(i18n.get('perc_error_header'))
        plot.tick_params(axis='x', rotation=45, labelsize=8)
        plot.grid(True, axis='y')
        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=graph_frame)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, graph_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        toolbar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=(0, 5))

    def update_texts(self):
        """Atualiza os textos estáticos da tela."""
        i18n = self.controller.i18n
        self.back_button.config(text=i18n.get('back_btn'))
        self.page_title.config(text=i18n.get('meta_learning_page_title'))
        self.custom_test_frame_label.config(text=i18n.get('custom_test_label'))
        self.lbl_base_learning.config(text=i18n.get('base_learning_l0_label'))
        self.lbl_triangulation.config(text=i18n.get('triangulation_l0_label'))
        self.lbl_meta_learning.config(text=i18n.get('meta_learning_l1_label'))
        self.lbl_indicator_ct.config(text=i18n.get('climatic_indicator_label'))
        self.lbl_num_tests_ct.config(text=i18n.get('num_tests_label'))
        self.lbl_pretrained.config(text=i18n.get('use_pretrained_label'))
        self.cb_pre_lv0.config(text=i18n.get('level0_label'))
        self.cb_pre_lv1.config(text=i18n.get('level1_label'))
        self.lbl_sliding_window.config(text=i18n.get('use_sliding_window_label'))
        self.button_ct.config(text=i18n.get('generate_preview_btn'))
        self.global_test_frame_label.config(text=i18n.get('global_test_label'))
        self.lbl_which_mls.config(text=i18n.get('which_mls_label'))
        self.lbl_indicator_gt.config(text=i18n.get('climatic_indicator_label'))
        self.lbl_num_tests_gt.config(text=i18n.get('num_tests_label'))
        self.button_gt.config(text=i18n.get('generate_preview_gt_btn'))
        self.warning_frame_label.config(text=i18n.get('warning_label'))
        self.lbl_warning1.config(text=i18n.get('warning_text_1'))
        self.lbl_warning2.config(text=i18n.get('warning_text_2'))
        self.lbl_warning3.config(text=i18n.get('warning_text_3'))
        if not self.loading_ct:
             self.button_ct.config(text=i18n.get('generate_preview_btn'))
        if not self.loading_gt:
             self.button_gt.config(text=i18n.get('generate_preview_gt_btn'))

        self.ml0_hint.text = i18n.get('ml0_MeL_hint')
        self.tr0_hint.text = i18n.get('tr0_MeL_hint')
        self.ml1_hint.text = i18n.get('ml1_MeL_hint')
        self.indicator_ct_hint.text = i18n.get('ct_ind_MeL_hint')
        self.num_tests_hint.text = i18n.get('num_tests_MeL_hint')
        self.pretrained_hint.text = i18n.get('pretrained_MeL_hint')
        self.sliding_window_hint.text = i18n.get('sliding_window_MeL_hint')
        self.prev_ct_hint.text = i18n.get('prev_ct_MeL_hint')
        self.wich_mls_hint.text = i18n.get('wich_ml_MeL_hint')
        self.indicator_gt_hint.text = i18n.get('indicator_gt_MeL_hint')
        self.num_tests_gt_hint.text = i18n.get('num_tests_gt_MeL_hint')
        self.button_gt_hint.text = i18n.get('btn_gt_MeL_hint')
