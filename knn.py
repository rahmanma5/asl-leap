import pandas as pd
import os
import numpy as np
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

files = os.listdir()

# creating one datatable from all csvs....
allTables = []
for file in files:
    if file.endswith('Data'):
        data = pd.read_csv(file, header=None).select_dtypes(include=['float64'])
        data['symbol'] = file[0]
        allTables.append(data)

data = pd.concat(allTables)

data.symbol = data.symbol.astype('category')

# separating into input and output variables then testing and training sets...
X = data.select_dtypes(exclude=['category'])
y = data.copy().select_dtypes(include=['category'])
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

# generating model and training. tentatively using 5 as n_neighbors
knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn.fit(X_train, np.ravel(y_train,order='C'))

# predicted value
y_pred = knn.predict(X_test)

# output report
# print('\nClasification report:\n', classification_report(y_test, y_pred))