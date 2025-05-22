def get_parameters_ml(self):
    return {
        "cidade": self.get_end(self.data_s.get()),
        "save_model": self.save_model.get(),
        "num_testes": int(self.num_teste.get()),
        "porcentagem_treinamento": int(self.por_trei.get()),
        "n_neighbors": self.n_neighbors_v.get(),
        "algorithm": self.algorithm_v.get(),
        "leaf_size": self.leaf_size_v.get(),
        "p_v": self.p_v.get(),
        "n_jobs": int(self.n_jobs_v.get()) if self.n_jobs_v.get().isdigit() else self.n_jobs_v.get()
    }