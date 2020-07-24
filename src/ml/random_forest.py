import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split 
import pandas as pd

# Importing Data
file_data = pd.read_csv("/data/TNG300-2/catalogs/snap_099-10000_groups.csv", index_col=0)

# Splitting labels and data
data = file_data.drop(columns=['isBCG', 'GroupFirstSub', 'GroupNsubs',
                               'SubhaloGasMetallicity', 'Rel_R',
                               'SubhaloGrNr', ''])
labels = file_data['isBCG']

# Splitting into training sets and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels,
                                                    test_size=.25)
# Generate the classificator
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Test the accuracy of the classificator
print(clf.score(X_test, y_test))

