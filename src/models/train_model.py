import pandas as pd
import numpy as np
import xgboost as xgb


def train_xgboost(train_path, target_col, num_rounds = 371):
    params = {
        'max_depth': 8, 
        'objective': 'reg:squarederror',
        'eta': 0.3,
        'subsample': 0.7,
        'lambda': 4,  
        'colsample_bytree': 0.9,
        'colsample_bylevel': 1,
        'min_child_weight': 10,
        'nthread': 8,
        'eval_metric': "rmse",
        'seed': 42
    }
    
    # Load training dataset
    df_train = pd.read_csv(train_path)

    # Separate features and target
    Y_train = np.log1p(df_train[target_col].values)
    X_train = df_train.drop(target_col, axis=1).values

    # Create DMatrix for training data
    dmatrix_train = xgb.DMatrix(X_train, label=Y_train)

    # Train the model
    model = xgb.train(params, dmatrix_train, num_boost_round=num_rounds)

    return model