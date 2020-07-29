import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split 
import pandas as pd

snapshots = [99,91,84,78,72,67,59,50,40,33,25,21]
results = []

for i, snapshot in enumerate(snapshots):
# Importing Data
     file_data = pd.read_csv("/data/TNG300-2/catalogs/snap_0{}-10000_groups.csv".format(snapshot), index_col=0)
     
     # Splitting labels and data
     # data = file_data.drop(['isBCG'], axis=1)
     # data = file_data.drop(['isBCG', 'SubhaloGrNr', 'SubhaloGasMetallicity', 'GroupFirstSub', 'GroupNsubs', 'Rel_R'], axis=1)
     # data = file_data.drop(['isBCG', 'SubhaloGrNr', 'SubhaloGasMetallicity', 'GroupFirstSub', 'GroupNsubs'], axis=1)
     data = file_data.drop(['isBCG', 'SubhaloGrNr', 'GroupFirstSub', 'GroupNsubs'], axis=1)

     labels = file_data['isBCG']
     
     # Splitting into training sets and testing sets
     X_train, X_test, y_train, y_test = train_test_split(data, labels,
                                                         test_size=.25)
     # Generate the classificator
     clf = RandomForestClassifier()
     clf.fit(X_train, y_train)
     
     # Test the accuracy of the classificator
     results.append(clf.score(X_test, y_test))
     print("Accuracy result for snapshot {}: {}".format(snapshot, results[i]))
