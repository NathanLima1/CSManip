from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from ..meta_learning.meta_learning import MetaLearning

class TestsGenerator:
    def __init__(self):
        self.ml_lv0_p = 'Decision Trees'
        lista_ml0 =  ['None','Decision Trees', 'Bagged Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        self.ml_tr0_p = 'Arithmetic Average'
        lista_tr0 =  ['None', 'Arithmetic Average', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']
        self.ml_lv1 = 'Decision Trees'
        lista_ml1 =  ['Decision Trees', 'Neural network', 'Bagged Trees', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        self.ind_meta_perso = 'Maximum temperature'
        lista_ind_meta_p = ["Precipitation", 'Maximum temperature', 'Minimum temperature']
        self.num_teste_mtp = 1
        self.pre_para_lv0 = False
        self.pre_para_lv1 = False
        # sliding window
        self.type_input = 'Yes'

        self.pre_nn_comb = False
        self.pre_dt_comb = False
        self.pre_nneig_comb = False
        self.pre_sv_comb = False
        self.pre_gp_comb = False
        self.pre_bt_comb = False

        self.ind_meta_comb = 'Maximum temperature'
        self.num_teste_mtc = 1
        

    def generate_custom_test(self, base_model='Decision Trees', triangulation='Arithmetic Average',
                             meta_model='Decision Trees', indicator='Maximum temperature',
                             num_tests=1, input_window='Yes'):

        if indicator == "Precipitation":
            focus = 1
        elif indicator == 'Maximum temperature':
            focus = 2
        elif indicator == 'Minimum temperature':
            focus = 3

        # Perform meta-learning
        meta = MetaLearning()
        meta_ea, meta_er, meta_percent_error, meta_r2, x_meta, y_meta, y_target, \
        base_ea, base_er, base_percent, base_r2, tria_ea, tria_er = \
            meta.customized_meta_learning(focus, base_model, triangulation, meta_model, 0, 0, num_tests, input_window)
        
        # Mostra resultados no terminal
        print("\n===== RESULTS PREVIEW =====")
        print(f"ABSOLUTE ERROR:  ML: {round(base_ea, 4)}  ||  Triangulation: {round(tria_ea, 4)}  ||  Meta: {round(meta_ea, 4)}")
        print(f"RELATIVE ERROR:  ML: {round(base_er, 4)}  ||  Triangulation: {round(tria_er, 4)}  ||  Meta: {round(meta_er, 4)}")
        print(f"ERROR (%):       ML: {round(base_percent, 4)}  ||  Triangulation: {round(tria_ea * 100, 4)}  ||  Meta: {round(meta_percent_error, 4)}")
        print(f"R²:              ML: {round(base_r2, 4)}  ||  Meta: {round(meta_r2, 4)}")

        # Plota os gráficos com matplotlib
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))

        axs[0, 0].bar(["ML", "Triang", "Meta"], [base_ea, tria_ea, meta_ea])
        axs[0, 0].set_title("Absolute Error")
        axs[0, 0].set_ylabel("Error")

        axs[0, 1].bar(["ML", "Triang", "Meta"], [base_er, tria_er, meta_er])
        axs[0, 1].set_title("Relative Error")
        axs[0, 1].set_ylabel("Error")

        axs[1, 0].bar(["ML", "Triang", "Meta"], [base_percent, tria_ea * 100, meta_percent_error])
        axs[1, 0].set_title("Percentage Error")
        axs[1, 0].set_ylabel("Error (%)")

        axs[1, 1].bar(["ML", "Meta"], [base_r2, meta_r2])
        axs[1, 1].set_title("R² Score")
        axs[1, 1].set_ylabel("Score")

        plt.tight_layout()
        plt.show()

    def generate_global_test(self, indicator='Maximum temperature', 
                             num_tests=1, window_type='Yes', print_results=True
    ):
        """
        Versão sem Tkinter da função generate_global_test
        """
        meta_learner = MetaLearning()
        # Executa o algoritmo de meta-aprendizado
        all_models, model_ranking = meta_learner.combine_meta_learning(
            indicator, 0, 0, num_tests, window_type
        )

        if print_results:
            print("=== GENERATED MODELS ===")
            headers = [
                'Model', 'Base Learning', 'Triangulation',
                'Meta Learning', 'Absolute Error',
                'Relative Error', 'Error (%)'
            ]
            print("\t".join(headers))
            for model in all_models:
                row = [
                    f"{model[0]}",  # Model name
                    model[1],  # Base learning
                    model[2],  # Triangulation
                    model[3],  # Meta learning
                    f"{model[5]:.4f}",  # Absolute Error
                    f"{model[6]:.4f}",  # Relative Error
                    f"{model[7]:.4f}"   # Percentage Error
                ]
                print("\t".join(row))

            print("\n=== MODEL RANKING ===")
            print("Model\tError (%)")
            for model in model_ranking:
                print(f"{model[0]}\t{model[1]}")

        # Preparar dados para gráfico
        x_labels = []
        y_values = []

        for i, model in enumerate(model_ranking[:15]):
            model_name = model[0]
            error_value = float(str(model[1]).replace(',', '.'))
            x_labels.append(model_name)
            y_values.append(error_value)

        # Criar gráfico com matplotlib puro
        plt.figure(figsize=(12, 3.3))
        plt.bar(x_labels, y_values)
        plt.ylabel("Error (%)")
        plt.xlabel("Models")
        plt.title("Model Ranking - Top 15")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        return all_models, model_ranking

