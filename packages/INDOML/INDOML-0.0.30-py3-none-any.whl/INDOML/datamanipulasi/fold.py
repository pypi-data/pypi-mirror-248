import numpy as np

def train_val_split(x:np.ndarray, y:np.ndarray, val_size=0.2, random_state=None):
    if random_state is not None:
        np.random.seed(random_state)

    data_size = len(x)
    val_size = int(val_size * data_size)

    indices = np.random.permutation(data_size)
    train_indices, val_indices = indices[val_size:], indices[:val_size]

    X_train, X_val = x[train_indices], x[val_indices]
    y_train, y_val = y[train_indices], y[val_indices]

    return X_train, X_val, y_train, y_val