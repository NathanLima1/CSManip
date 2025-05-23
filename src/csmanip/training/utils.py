import numpy as np

def calculate_errors(all_exact, all_predicted, total_absolute_error, total_relative_error, n_tests):
    score = round((((total_relative_error / n_tests) * 100) - 100) * -1, 2)

    if all_exact:
        errors = np.abs(np.array(all_exact) - np.array(all_predicted))
        max_idx = np.argmax(errors)
        min_idx = np.argmin(errors[errors > 0]) if np.any(errors > 0) else 0

        max_error = errors[max_idx]
        min_error = errors[min_idx] if np.any(errors > 0) else 0

        exact_max = all_exact[max_idx]
        predicted_max = all_predicted[max_idx]

        exact_min = all_exact[min_idx]
        predicted_min = all_predicted[min_idx]
    else:
        max_error = min_error = exact_max = predicted_max = exact_min = predicted_min = 0

    avg_absolute_error = total_absolute_error / n_tests
    avg_relative_error = total_relative_error / n_tests

    return {
        "score": score,
        "max_error": max_error,
        "min_error": min_error,
        "exact_max": exact_max,
        "predicted_max": predicted_max,
        "exact_min": exact_min,
        "predicted_min": predicted_min,
        "avg_absolute_error": avg_absolute_error,
        "avg_relative_error": avg_relative_error
    }
