import numpy as np

from art.utils import load_nursery

(X_train, y_train), (X_test, y_test), _, _ = load_nursery(test_set=0.5)

from sklearn.ensemble import RandomForestClassifier
from art.estimators.classification.scikitlearn import ScikitlearnRandomForestClassifier

base_model = RandomForestClassifier()
base_model.fit(X_train, y_train)

art_classifier = ScikitlearnRandomForestClassifier(base_model)

print('Base model accuracy: ', base_model.score(X_test, y_test))

x_train_predictions = np.array([np.argmax(arr) for arr in art_classifier.predict(X_train)]).reshape(-1,1)
print('Train accuracy: ', base_model.score(X_train, y_train))

from diffprivlib.models import RandomForestClassifier as DPRandomForestClassifier
import matplotlib.pyplot as plt

feature_domains={'0': ['0.44703412960814864', '1.3415165649791168', '-0.4474483057628194', '-1.3419307411337875'], '1': ['-0.7069430801121958', '1.4145410403356578'], '2': ['-0.7071886364604442', '1.4140498707743785'], '3': ['-0.7071886364604442', '1.4140498707743785'], '4': ['-0.49980706154018284', '2.0007720517562224'], '5': ['-0.5000482322868048', '1.999807089461813'], '6': ['-0.5000482322868048', '1.999807089461813'], '7': ['-0.5000482322868048', '1.999807089461813'], '8': ['-0.5000482322868048', '1.999807089461813'], '9': ['-0.5771720471544519', '1.7325856387712393'], '10': ['-0.5774096765334255', '1.731872603874021'], '11': ['-0.5774096765334255', '1.731872603874021'], '12': ['-0.5774096765334255', '1.731872603874021'], '13': ['-0.7069430801121959', '1.4145410403356582'], '14': ['-0.7071886364604442', '1.4140498707743787'], '15': ['-0.7071886364604442', '1.4140498707743787'], '16': ['-0.999845667103024', '1.0001543567192954'], '17': ['0.999845667103024', '-1.0001543567192954'], '18': ['-0.7070658547341222', '1.4142954200157634'], '19': ['-0.7070658547341222', '1.4142954200157634'], '20': ['-0.7071886364604442', '1.4140498707743787'], '21': ['-0.7071886364604442', '1.4140498707743787'], '22': ['-0.7071886364604442', '1.4140498707743787'], '23': ['-0.7069430801121959', '1.4145410403356582']}

# model = DPRandomForestClassifier(feature_domains=feature_domains)
model = DPRandomForestClassifier()
X_all = np.concatenate((X_train, X_test), axis=0)
y_all = np.concatenate((y_train, y_test), axis=0)
model.fit(X_all, y_all)
print(model.feature_domains_)
model.score(X_test, y_test)
