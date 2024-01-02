import numpy as np

def load_value(s):
    try:
        return float(s.strip())
    except:
        return 0

converters = {}
for i in range(1, 20):
    converters[i] = load_value

x = np.loadtxt("/Users/abigailt/Desktop/My Documents/PrivacySecurity/AI Privacy/PR/websites/360 site/demo/datasets/hepatitis.data",
                usecols=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19), delimiter=",",
                converters=converters)

y = np.loadtxt("/Users/abigailt/Desktop/My Documents/PrivacySecurity/AI Privacy/PR/websites/360 site/demo/datasets/hepatitis.data",
                usecols=0, delimiter=",")

# transform labels to 0 and 1
y = y - 1

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=97)

from sklearn.naive_bayes import GaussianNB
from art.estimators.classification.scikitlearn import ScikitlearnGaussianNB

base_model = GaussianNB()
base_model.fit(X_train, y_train)

art_classifier = ScikitlearnGaussianNB(base_model)

print('Base model accuracy: ', base_model.score(X_test, y_test))

x_train_predictions = np.array([np.argmax(arr) for arr in art_classifier.predict(X_train)]).reshape(-1,1)
print('Train accuracy: ', base_model.score(X_train, y_train))

from apt.minimization import GeneralizeToRepresentative
from sklearn.model_selection import train_test_split


# default target_accuracy is 0.998
# target_accuracies = [0.84, 0.85, 0.9, 0.925, 0.95]
target_accuracies = [0.84]
X_generalizer_train, x_generalizer_test, y_generalizer_train, y_generalizer_test = train_test_split(X_test,
                                                                                                    y_test,
                                                                                                    stratify=y_test,
                                                                                                    test_size=0.5,
                                                                                                    random_state=1)
for acc in target_accuracies:
    minimizer = GeneralizeToRepresentative(base_model, target_accuracy=acc)

    # Fitting the minimizar can be done either on training or test data. Doing it with test data is better as the
    # resulting accuracy on test data will be closer to the desired target accuracy (when working with training
    # data it could result in a larger gap)
    # Don't forget to leave a hold-out set for final validation!

    x_generalizer_train_predictions = base_model.predict(X_generalizer_train)
    minimizer.fit(X_generalizer_train, x_generalizer_train_predictions)
    transformed = minimizer.transform(x_generalizer_test)
    print(acc)
    print('Accuracy on minimized data: ', base_model.score(transformed, y_generalizer_test))

    generalizations = minimizer.generalizations
    print(generalizations)

from apt.anonymization import Anonymize
# from art.attacks.inference.membership_inference import MembershipInferenceBlackBox

# attack_model_type can be nn (neural network), rf (random forest) or gb (gradient boosting)
# bb_attack = MembershipInferenceBlackBox(art_classifier, attack_model_type='rf')
#
# # use half of each dataset for training the attack
# attack_train_ratio = 0.5
# attack_train_size = int(len(X_train) * attack_train_ratio)
# attack_test_size = int(len(X_test) * attack_train_ratio)

k_values = [5, 10]
model_accuracy = []
attack_accuracy = []
unique_values = []

# QI = all
QI = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
print('unique rows in original data: ', len(np.unique(X_train, axis=0)))

for k in k_values:
    anonymizer = Anonymize(k, QI)
    anon = anonymizer.anonymize(X_train, x_train_predictions)
    unique_values.append(len(np.unique(anon, axis=0)))

    anon_model = GaussianNB()
    anon_model.fit(anon, y_train)

    anon_art_classifier = ScikitlearnGaussianNB(anon_model)

    model_accuracy.append(anon_model.score(X_test, y_test))

    minimizer = GeneralizeToRepresentative(anon_model, target_accuracy=0.57)
    minimizer.fit(X_generalizer_train, x_generalizer_train_predictions)
    transformed = minimizer.transform(x_generalizer_test)

    print('Accuracy on minimized data: ', base_model.score(transformed, y_generalizer_test))

    generalizations = minimizer.generalizations
    print(k)
    print(generalizations)

    # anon_bb_attack = MembershipInferenceBlackBox(anon_art_classifier, attack_model_type='rf')
    #
    # # train attack model
    # anon_bb_attack.fit(X_train[:attack_train_size], y_train[:attack_train_size],
    #                    X_test[:attack_test_size], y_test[:attack_test_size])
    #
    # # get inferred values
    # anon_inferred_train_bb = anon_bb_attack.infer(X_train[attack_train_size:], y_train[attack_train_size:])
    # anon_inferred_test_bb = anon_bb_attack.infer(X_test[attack_test_size:], y_test[attack_test_size:])
    # # check accuracy
    # anon_train_acc = np.sum(anon_inferred_train_bb) / len(anon_inferred_train_bb)
    # anon_test_acc = 1 - (np.sum(anon_inferred_test_bb) / len(anon_inferred_test_bb))
    # anon_acc = (anon_train_acc * len(anon_inferred_train_bb) + anon_test_acc * len(anon_inferred_test_bb)) / (
    #             len(anon_inferred_train_bb) + len(anon_inferred_test_bb))
    # attack_accuracy.append(anon_acc)

# print('k values: ', k_values)
# print('unique rows:', unique_values)
print('model accuracy:', model_accuracy)
# print('attack accuracy:', attack_accuracy)