# -*- coding: utf-8 -*-
"""capstone model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rZhUQ5ae7xqsSH1KiqHlainP2lenNllw
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/My Drive/Colab Notebooks/

import pandas as pd
##which are repeating in every dataset
redundant = ['Rk','Player','Nation','Squad','Pos','Comp','Age','Born','90s','Matches']
##reading the CSV and removing redundant feature
general = pd.read_excel('std_stats.xlsx',header=0)
general=general.drop(['Rk','Matches'],axis=1)
#print(general)

shooting = pd.read_excel('shooting_stats.xlsx',header=0)
shooting=shooting.drop(redundant,axis=1)
#shooting.head()

passing = pd.read_excel('passing_stats.xlsx',header=0)
passing=passing.drop(redundant,axis=1)
#passing.head()

passing_types = pd.read_excel('passing-type_stats.xlsx', header=0)
passing_types=passing_types.drop(redundant,axis=1)
#passing_types.head()

gca = pd.read_excel('goal_assist-creation_stats.xlsx',header=0)
gca=gca.drop(redundant,axis=1)
#gca.head()

defense = pd.read_excel('defensive_stats.xlsx', header=0)
defense=defense.drop(redundant,axis=1)
#defense.head()

possession = pd.read_excel('possesion_stats.xlsx', header=0)
possession=possession.drop(redundant,axis=1)
#possession.head()

misc = pd.read_excel('misc_stats.xlsx', header=0)
misc=misc.drop(redundant,axis=1)
#misc.head()

def renameColumns(table_no,df):
  num=str(table_no)+"_"
  return df.rename(columns= lambda x: num+x)

shooting=renameColumns(2,shooting)
passing=renameColumns(3,passing)
passing_types=renameColumns(4,passing_types)
gca=renameColumns(5,gca)
defense=renameColumns(6,defense)
possession=renameColumns(7,possession)
misc=renameColumns(8,misc)
final_stats2=pd.concat([general,shooting,passing,passing_types,gca,defense,possession,misc],axis=1)
#final_stats2.head()

df1= pd.DataFrame(final_stats2)

# Save the DataFrame to an Excel file
df1.to_excel("final_stats2.xlsx", index=False)

##null values
final_stats2.isnull().sum().sum()

##replacing null values with 0
final_stats2=final_stats2.fillna(0)

final_stats2.isnull().sum().sum()

##data transformation
# atleast 10 90s played
df3 =final_stats2.rename(columns={'90s': 'Ninetys'})
#df3.head()

df4 = df3[df3['Ninetys']>=3]
df4.head()

# create a dictionary mapping player+squad to their index
player_ID = {}
for i, player in enumerate(df4['Player']):
    for j, squad in enumerate(df4['Squad']):
        key = f"{player}+{squad}"
        player_ID[key] = (i, j)

# print the player dictionary
print(player_ID)

#players=[]
#for idx in range(len(df4)):
  #players.append(df4['Player'][idx] + ' {}'.format(df4['Squad'][idx]))
#player_ID=dict(zip(players,np.arrange(len(players))))
#player_ID

import seaborn as sns
import matplotlib 
from matplotlib import pyplot as plt
#sns.set_theme(style="white",font="Century Gothic")
ax=sns.countplot(x='Pos',hue='Comp',data=df4)
plt.xlabel('Position')
plt.title('Positional distribution in leagues')

import seaborn as sns
import matplotlib 
from matplotlib import pyplot as plt
sns.FacetGrid(df4,height=6,aspect=10/6).map(sns.distplot,'Age',bins=25)
plt.title("Age distribution among leagues",size=24)

from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
import numpy as np
import seaborn as sns
import matplotlib 
from matplotlib import pyplot as plt


# selecting only numerical metrics
stats=df4.iloc[:,5:]
#print(stats.dtypes)
# position types
labels = df4['Pos']

# standardizing the data
data = StandardScaler().fit_transform(stats)

# configuring tSNE params
model = TSNE(n_components=2, perplexity=30, random_state=0)
tsne_data = model.fit_transform(data)

# creating a new df to plot the result data
tsne_data = np.vstack((tsne_data.T, labels)).T
tsne_df = pd.DataFrame(data=tsne_data, columns=("Dimension 1", "Dimension 2", "Positions"))

# ploting the result of tSNE
ax = sns.FacetGrid(tsne_df, hue="Positions",).map(plt.scatter, 'Dimension 1', 'Dimension 2').add_legend()
plt.title('t-SNE - Outfield players', size=20)

df4.head()

stats=df4.iloc[:,5:90]
stats.head()

##null values
stats.isnull().sum().sum()

##replacing null values with 0
stats=stats.fillna(0)

from sklearn import decomposition
from sklearn.preprocessing import StandardScaler
import matplotlib 
from matplotlib import pyplot as plt
import numpy as np

# standardizing the data

data = StandardScaler().fit_transform(stats)

# setting up and running PCA
pca = decomposition.PCA()
pca.n_components = 156
pca_data = pca.fit_transform(data)

# % variance explained per components
percentage_var_explained = pca.explained_variance_ / np.sum(pca.explained_variance_);

# cumulative variance explained
cum_var_explained = np.cumsum(percentage_var_explained)

plt.figure(1, figsize=(6, 4))
plt.plot(cum_var_explained, linewidth=2)
plt.axis('tight')
plt.grid()
plt.xlabel('principal components')
plt.ylabel('Cumulative variance explained')
plt.title('PCA: components selection')

df_feature=df4.iloc[:,:90]
df_feature.head()

stats2=df4.iloc[:,5:40]
stats2.head()

print(stats)

from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np



# compute cosine similarity
cos_sim = cosine_similarity(stats)

# perform k-NN search
k = 5  # number of neighbors to return
nbrs = NearestNeighbors(n_neighbors=k, metric='cosine').fit(cos_sim)
player_names = df4["Player"].tolist()

# get nearest neighbors for each data point
distances, indices = nbrs.kneighbors(cos_sim)

# print results
print('Distances:', distances)
print('Indices:', indices)

for i in range(len(indices)):
  print(f"Player: {player_names[i]}")
  for j in range(1, len(indices[i])):
    print(f"  Neighbor {j}: {player_names[indices[i][j]]}")

##null values
df4.isnull().sum().sum()
df4=df4.fillna(0)

nan_sum = df4.isna().sum().sum()
nan_sum

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler, RobustScaler

# Standard Scaler
#scaler = StandardScaler()
#X_train_scaled = scaler.fit_transform(X_train)
#X_test_scaled = scaler.transform(X_test)

# Min-Max Scaler
#scaler = MinMaxScaler()
#X_train_scaled = scaler.fit_transform(X_train)
#X_test_scaled = scaler.transform(X_test)

# Robust Scaler
#scaler = RobustScaler()
#X_train_scaled = scaler.fit_transform(X_train)
#X_test_scaled = scaler.transform(X_test)
from sklearn.preprocessing import FunctionTransformer

# Define the logarithmic transformation function
#log_transform = FunctionTransformer(np.log1p, validate=True)

# Apply the logarithmic transformation to the data
#X_train_log = log_transform.transform(X_train)
#X_test_log = log_transform.transform(X_test)

from sklearn.preprocessing import QuantileTransformer

# Initialize the quantile transformer with the 'normal' method
quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)

# Fit and transform the data using the quantile transformer
#X_train_quantile = quantile_transformer.fit_transform(X_train)
#X_test_quantile = quantile_transformer.transform(X_test)

from sklearn.preprocessing import PowerTransformer

# Initialize the power transformer with the 'yeo-johnson' method
power_transformer = PowerTransformer(method='yeo-johnson', standardize=True)

# Fit and transform the data using the power transformer
#X_train_power = power_transformer.fit_transform(X_train)
#X_test_power = power_transformer.transform(X_test)





# Preprocess data
X = df4.drop(['Player', 'Pos','Nation','Squad','Comp'], axis=1)
scaler = MinMaxScaler()
X = scaler.fit_transform(X)
y = df4["Pos"].values

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Compute cosine similarity
cos_sim = cosine_similarity(X)

# Perform k-NN search
k =8 # number of neighbors to return
nbrs = KNeighborsClassifier(n_neighbors=k, metric='cosine')
nbrs.fit(X_train, y_train)

# Predict using the k-NN classifier
y_pred = nbrs.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='weighted'))
print("Recall:", recall_score(y_test, y_pred, average='weighted'))
print("F1 Score:", f1_score(y_test, y_pred, average='weighted'))

import pickle

# save the trained model to a file
with open('nearest_neighbors_model.pkl', 'wb') as f:
    pickle.dump(nbrs, f)
import pickle

# load the trained model from a file
with open('nearest_neighbors_model.pkl', 'rb') as f:
    nbrs = pickle.load(f)

# example usage
player_name = 'Nathan Aké'
player_index = player_names.index(player_name)
distances, indices = nbrs.kneighbors([cos_sim[player_index]])

# find nearest neighbors, excluding the input player
nearest_neighbors = []
for i in indices[0]:
    if player_names[i] != player_name:
        nearest_neighbors.append(player_names[i])

print(f"Nearest neighbors for {player_name}: {nearest_neighbors}")

import pickle

# save the trained model to a file
with open('nearest_neighbors_model.pkl', 'wb') as f:
    pickle.dump(nbrs, f)
import pickle

# load the trained model from a file
with open('nearest_neighbors_model.pkl', 'rb') as f:
    nbrs = pickle.load(f)

# example usage
player_name = 'Benoît Badiashile'
player_index = player_names.index(player_name)
distances, indices = nbrs.kneighbors([cos_sim[player_index]])

# find nearest neighbors, excluding the input player
nearest_neighbors = []
for i in indices[0]:
    if player_names[i] != player_name:
        nearest_neighbors.append(player_names[i])

print(f"Nearest neighbors for {player_name}: {nearest_neighbors}")

import pickle

# save the trained model to a file
with open('nearest_neighbors_model.pkl', 'wb') as f:
    pickle.dump(nbrs, f)
import pickle

# load the trained model from a file
with open('nearest_neighbors_model.pkl', 'rb') as f:
    nbrs = pickle.load(f)

# example usage
player_name = 'David López'
player_index = player_names.index(player_name)
distances, indices = nbrs.kneighbors([cos_sim[player_index]])

# find nearest neighbors, excluding the input player
nearest_neighbors = []
for i in indices[0]:
    if player_names[i] != player_name:
        nearest_neighbors.append(player_names[i])

print(f"Nearest neighbors for {player_name}: {nearest_neighbors}")

import pickle

# save the trained model to a file
with open('nearest_neighbors_model.pkl', 'wb') as f:
    pickle.dump(nbrs, f)
import pickle

# load the trained model from a file
with open('nearest_neighbors_model.pkl', 'rb') as f:
    nbrs = pickle.load(f)

# example usage
player_name = 'Mohamed Simakan'
player_index = player_names.index(player_name)
distances, indices = nbrs.kneighbors([cos_sim[player_index]])

# find nearest neighbors, excluding the input player
nearest_neighbors = []
for i in indices[0]:
    if player_names[i] != player_name:
        nearest_neighbors.append(player_names[i])

print(f"Nearest neighbors for {player_name}: {nearest_neighbors}")

import pickle

# save the trained model to a file
with open('nearest_neighbors_model.pkl', 'wb') as f:
    pickle.dump(nbrs, f)
import pickle

# load the trained model from a file
with open('nearest_neighbors_model.pkl', 'rb') as f:
    nbrs = pickle.load(f)

# example usage
player_name = input("Enter a player name: ")
player_index = player_names.index(player_name)
distances, indices = nbrs.kneighbors([cos_sim[player_index]])

# find nearest neighbors, excluding the input player
nearest_neighbors = []
for i in indices[0]:
    if player_names[i] != player_name:
        nearest_neighbors.append(player_names[i])

print(f"Nearest neighbors for {player_name}: {nearest_neighbors}")

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


# Preprocess data
X = df4.drop(['Player', 'Pos','Nation','Squad','Comp'], axis=1)
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = df4["Pos"].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train k-nearest neighbor model
# number of neighbors to consider
k = 6
model = KNeighborsClassifier(n_neighbors=k)
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Compute evaluation metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='macro')
recall = recall_score(y_test, y_pred, average='macro')
f1 = f1_score(y_test, y_pred, average='macro')
cm = confusion_matrix(y_test, y_pred)

# Print evaluation metrics
print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('F1 score:', f1)
print('Confusion matrix:\n', cm)

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler



# Preprocess data
X = df4.drop(['Player', 'Pos','Nation','Squad','Comp'], axis=1)
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = df4["Pos"].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train k-nearest neighbor model
k = 7 # number of neighbors to consider
model = KNeighborsClassifier(n_neighbors=k, metric='euclidean')
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Compute evaluation metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='macro')
recall = recall_score(y_test, y_pred, average='macro')
f1 = f1_score(y_test, y_pred, average='macro')
cm = confusion_matrix(y_test, y_pred)

# Print evaluation metrics
print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('F1 score:', f1)
print('Confusion matrix:\n', cm)

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler



# Preprocess data
X = df4.drop(['Player', 'Pos','Nation','Squad','Comp'], axis=1)
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = df4["Pos"].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train k-nearest neighbor model
k = 8 # number of neighbors to consider
model = KNeighborsClassifier(n_neighbors=k, metric='manhattan')
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Compute evaluation metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='macro')
recall = recall_score(y_test, y_pred, average='macro')
f1 = f1_score(y_test, y_pred, average='macro')
cm = confusion_matrix(y_test, y_pred)

# Print evaluation metrics
print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('F1 score:', f1)
print('Confusion matrix:\n', cm)

df4.head()

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


# Preprocess data
X = df4.drop(['Player', 'Pos','Nation','Squad','Comp'], axis=1)
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = df4["Pos"].values

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define multiple KNN models with different hyperparameters
model1 = KNeighborsClassifier(n_neighbors=3)
model2 = KNeighborsClassifier(n_neighbors=5)
model3 = KNeighborsClassifier(n_neighbors=7)

# Create a voting classifier that combines the predictions of the KNN models
ensemble = VotingClassifier(estimators=[('model1', model1), ('model2', model2), ('model3', model3)], voting='hard')

# Fit the ensemble model on the training data
ensemble.fit(X_train, y_train)

# Make predictions using the ensemble model on the testing data
y_pred = ensemble.predict(X_test)

# Evaluate the accuracy of the ensemble model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Compute evaluation metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='macro')
recall = recall_score(y_test, y_pred, average='macro')
f1 = f1_score(y_test, y_pred, average='macro')
cm = confusion_matrix(y_test, y_pred)

# Print evaluation metrics
print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('F1 score:', f1)
print('Confusion matrix:\n', cm)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
#
# Preprocess data
X = df4.drop(['Player', 'Pos','Nation','Squad','Comp'], axis=1)
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = df4["Pos"].values


# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize a KNN classifier
knn = KNeighborsClassifier()

# Initialize a bagging classifier
bagging = BaggingClassifier(base_estimator=knn, n_estimators=10, random_state=42)

# Fit the bagging classifier to the training data
bagging.fit(X_train, y_train)

# Predict the labels for the test data using the bagging classifier
y_pred_bagging = bagging.predict(X_test)

# Evaluate the performance of the bagging classifier using precision score
from sklearn.metrics import precision_score
precision_bagging = precision_score(y_test, y_pred_bagging, average='weighted')
print("Precision (Bagging):", precision_bagging)

df4

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
#
# Preprocess data
X = df4.drop(['Player', 'Pos','Nation','Squad','Comp'], axis=1)
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = df4["Pos"].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the base classifiers
knn = KNeighborsClassifier(n_neighbors=5)
rf = RandomForestClassifier(n_estimators=50, random_state=42)
et = ExtraTreesClassifier(n_estimators=50, random_state=42)
gb = GradientBoostingClassifier(n_estimators=50, random_state=42)

# Define the stacking classifier
estimators = [('knn', knn), ('rf', rf), ('et', et), ('gb', gb)]
stacking_clf = StackingClassifier(estimators=estimators, final_estimator=knn)

# Fit the stacking classifier on the training data
stacking_clf.fit(X_train, y_train)

# Predict on the testing data
y_pred = stacking_clf.predict(X_test)

# Evaluate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy (Stacking KNN):", accuracy)
# Calculate the precision of the model
precision = precision_score(y_test, y_pred, average='weighted')
print("Precision (Stacked KNN):", precision)

import joblib

# Save the trained stacking classifier model
joblib.dump(stacking_clf, 'stacking_clf_model.joblib')

# Load the saved stacking classifier model
stacking_clf_loaded = joblib.load('stacking_clf_model.joblib')

import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity





# Preprocess data for the inputted player
input_player_name = 'Tammy Abraham'
input_player_data = df4[df4['Player'] == input_player_name].drop(['Player', 'Pos', 'Nation', 'Squad', 'Comp'], axis=1)
scaler = StandardScaler()
input_player_data = scaler.fit_transform(input_player_data)

# Predict the probabilities of each position for the inputted player
position_probabilities = stacking_clf.predict_proba(input_player_data)[0]

# Sort the predicted probabilities in descending order and return the top few positions
recommended_positions = []
for pos, prob in sorted(zip(stacking_clf.classes_, position_probabilities), key=lambda x: x[1], reverse=True)[:3]:
    recommended_positions.append(pos)

# Compute the similarity between the inputted player and all other players in the dataset
similarity_scores = []
for index, row in df4.iterrows():
    if row['Player'] == input_player_name:
        continue
    player_data = row.drop(['Player', 'Pos', 'Nation', 'Squad', 'Comp'])
    player_data = scaler.transform([player_data])
    similarity_scores.append((row['Player'], cosine_similarity(input_player_data, player_data)))

# Return the top few players with the highest similarity scores
recommended_players = []
for player, score in sorted(similarity_scores, key=lambda x: x[1], reverse=True)[:3]:
    recommended_players.append(player)

print('Recommended positions:', recommended_positions)
print('Recommended players:')
print(recommended_players)



# Preprocess data for the inputted player
input_player_name = 'Lisandro Martínez'  # Replace with the desired player name
input_player_data = df4[df4['Player'] == input_player_name].drop(['Player', 'Pos', 'Nation', 'Squad', 'Comp'], axis=1)

print('Input player data:')
print(input_player_data)

input_player_data = scaler.transform(input_player_data)

# Predict the probabilities of each position for the inputted player
position_probabilities = stacking_clf.predict_proba(input_player_data)[0]

# Sort the predicted probabilities in descending order and return the top few positions
recommended_positions = []
for pos, prob in sorted(zip(stacking_clf.classes_, position_probabilities), key=lambda x: x[1], reverse=True)[:3]:
    recommended_positions.append(pos)

# Compute the similarity between the inputted player and all other players in the dataset
similarity_scores = []
for index, row in df4.iterrows():
    if row['Player'] == input_player_name:
        continue
    player_data = row.drop(['Player', 'Pos', 'Nation', 'Squad', 'Comp'])
    player_data = scaler.transform([player_data])
    similarity_scores.append((row['Player'], cosine_similarity(input_player_data, player_data)))

# Return the top few players with the highest similarity scores
recommended_players = []
for player, score in sorted(similarity_scores, key=lambda x: x[1], reverse=True)[:3]:
    recommended_players.append(player)

print('Recommended positions:', recommended_positions)
print('Recommended players:')
print(recommended_players)



import pandas as pd


# Define a mapping from values to integers
position_map = {'MF': 0, 'FW': 1, 'DF': 2, 'GK': 3, 'DF,FW': 4, 'DF,MF': 5, 
                'FW,DF': 6, 'FW,MF': 7, 'MF,DF': 8, 'MF,FW': 9}

# Replace the values in the 'Pos' column with integers
df4['Pos'] = df4['Pos'].replace(position_map)

# Print the updated dataframe
print(df4.head())