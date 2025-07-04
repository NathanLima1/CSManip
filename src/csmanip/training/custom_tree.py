from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.tree import DecisionTreeRegressor

class CustomDecisionTree(BaseEstimator, RegressorMixin):
    def __init__(self, criterion='squared_error', splitter='best', max_depth=None,
                 min_samples_leaf=1, max_features=None, max_leaf_nodes=None,
                 min_samples_split=2, min_weight_fraction_leaf=0.0,
                 min_impurity_decrease=0.0, ccp_alpha=0.0):
        self.criterion = criterion
        self.splitter = splitter
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes
        self.min_samples_split = min_samples_split
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.min_impurity_decrease = min_impurity_decrease
        self.ccp_alpha = ccp_alpha

    def fit(self, X, y):
        self.model_ = DecisionTreeRegressor(
            criterion=self.criterion,
            splitter=self.splitter,
            max_depth=self.max_depth,
            min_samples_leaf=self.min_samples_leaf,
            max_features=self.max_features,
            max_leaf_nodes=self.max_leaf_nodes,
            min_samples_split=self.min_samples_split,
            min_weight_fraction_leaf=self.min_weight_fraction_leaf,
            min_impurity_decrease=self.min_impurity_decrease,
            ccp_alpha=self.ccp_alpha
        )
        self.model_.fit(X, y)
        return self

    def predict(self, X):
        return self.model_.predict(X)
