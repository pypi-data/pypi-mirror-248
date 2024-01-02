from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from apt.utils.models import SklearnRegressor
from apt.utils.datasets import ArrayDataset
from apt.minimization import GeneralizeToRepresentative
from apt.utils.dataset_utils import get_iris_dataset_np

(x_train, y_train), (x_test, y_test) = get_iris_dataset_np()
features = ['sepal length', 'sepal width', 'petal length', 'petal width']

base_est = LogisticRegression(solver='liblinear', penalty='l2')
apt_model = SklearnRegressor(base_est)
apt_model.fit(ArrayDataset(x_train, y_train))

print('Base model accuracy: ', apt_model.score(ArrayDataset(x_test, y_test)))

x_generalizer_train, x_test, y_generalizer_train, y_test = train_test_split(x_test, y_test, stratify=y_test, test_size=0.2, random_state=38)
x_train_preds = apt_model.predict(ArrayDataset(x_generalizer_train))

minimizer = GeneralizeToRepresentative(estimator=apt_model, target_accuracy=0.99, features_to_minimize=features, is_regression=True)
minimizer.fit(dataset=ArrayDataset(x_generalizer_train, x_train_preds, features))

gener = minimizer.generalizations
print(gener)

transformed = minimizer.transform(dataset=ArrayDataset(x_train, features_names=features))
print('Accuracy on minimized data: ', apt_model.score(test_data=ArrayDataset(transformed, y_train)))