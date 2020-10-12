import numpy as np

filename = "skolemdata_nine.txt"
skolemdata = open(filename,"r")
training_data_pre = []
training_labels_pre = []

for i in range(150000):
    linedata = skolemdata.readline()
    linedata = linedata.strip()
    linedata = linedata.split(", ")

    linedata[0] = linedata[0][1]
    linedata[8] = linedata[8][0]

    for j in range(10):
        linedata[j] = int(linedata[j])
    training_data_temp = []
    for k in range(9):
        training_data_temp.append(linedata[k])
    training_data_pre.append(training_data_temp)
    training_labels_pre.append(linedata[9])
test_data_pre = []
test_labels_pre = []
count = 0
for i in range(150000):
    linedata = skolemdata.readline()
    linedata = linedata.strip()
    linedata = linedata.split(", ")

    linedata[0] = linedata[0][1]
    linedata[8] = linedata[8][0]

    for j in range(10):
        linedata[j] = int(linedata[j])
    test_data_temp = []
    for k in range(9):
        test_data_temp.append(linedata[k])

    test_data_pre.append(test_data_temp)
    test_labels_pre.append(linedata[9]) 

    if linedata[9] == 1:
        count+=1
training_data = np.asarray(training_data_pre)
training_labels = np.asarray(training_labels_pre)
test_data = np.asarray(test_data_pre)
test_labels = np.asarray(test_labels_pre)



from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import accuracy_score

names = ["Nearest Neighbors", "Linear SVM",
         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
         "Naive Bayes", "QDA"]

classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=1),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis()]

print(len(names))
print(len(classifiers))
for name,clf in zip(names,classifiers):
    clf.fit(training_data,training_labels)
    pred = clf.predict(test_data)

    acc = accuracy_score(pred,test_labels)
    print("The name of the algorithm used is %s, and the accuracy it achieved is" % name)
    print(acc)

print(count)
print(count/150000)
