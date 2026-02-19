import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, DotProduct, RationalQuadratic, WhiteKernel
from sklearn.metrics import mean_absolute_error
import pickle
import os

def gaussian_process_regression(self, city, indicator_code, division, kernel_type, 
                                len_scale, nu, sigma_0, alpha_rq, alpha_noise, n_restart, normalize_y, save_model):
    
    X_train, y_train, X_val, y_val = self.prepare_matrix_by_city(city, division, indicator_code)

    noise_kernel = WhiteKernel(noise_level=1e-5, noise_level_bounds=(1e-10, 1e+1))
    
    if kernel_type == 'RBF':
        base_kernel = RBF(length_scale=len_scale)
    elif kernel_type == 'Matern':
        base_kernel = Matern(length_scale=len_scale, nu=nu)
    elif kernel_type == 'RationalQuadratic':
        base_kernel = RationalQuadratic(length_scale=len_scale, alpha=alpha_rq)
    elif kernel_type == 'DotProduct':
        base_kernel = DotProduct(sigma_0=sigma_0)
    else:
        base_kernel = RBF(1.0)

    kernel = base_kernel + noise_kernel

  
    model = GaussianProcessRegressor(
        kernel=kernel,
        alpha=alpha_noise,
        n_restarts_optimizer=n_restart,
        normalize_y=normalize_y,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred, y_std = model.predict(X_val, return_std=True)

    errors = np.abs(y_val - y_pred)
    
    with np.errstate(divide='ignore', invalid='ignore'):
        relative_errors = np.where(y_val != 0, errors / np.abs(y_val), 0)

    mean_abs_error = np.mean(errors)
    mean_rel_error = np.mean(relative_errors)
    
    max_error_idx = np.argmax(errors)
    min_error_idx = np.argmin(errors) 

    metrics = {
        "score": model.score(X_val, y_val),
        "mae": mean_abs_error,
        "mre": mean_rel_error,
        "max_error": errors[max_error_idx],
        "max_val_real": y_val[max_error_idx],
        "max_val_pred": y_pred[max_error_idx],
        "kernel_params": model.kernel_.get_params()
    }

    if save_model:
        path = os.path.join(os.getcwd(), f'modelo_gp_{city}_{indicator_code}.sav')
        with open(path, 'wb') as f:
            pickle.dump(model, f)

    return metrics, y_val, y_pred, y_std