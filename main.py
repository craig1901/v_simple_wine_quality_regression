import pandas
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.feature_selection import SelectKBest,f_classif
from sklearn.feature_selection import f_regression
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt

from math import sqrt
import csv
class Dataset:
	numberOfInstance = 0
	"""docstring for Dataset"""
	# columns,target,datsetValues,
	def __init__(self, columns,target,datsetValues):
		self.columns = columns
		self.target = target
		self.datsetValues = datsetValues
	def getColums(self):
		return self.columns
	def getTarget(self):
		return self.target
	def setNumOfInstace(self,numberOfInstance):
		self.numberOfInstance = numberOfInstance
	def setDatasetName(self,DatasetName):
		self.datasetName = DatasetName
	def getDatasetName(self):
		return self.datasetName
	def getDataset(self):
		return self.datsetValues

ListOFDatasetObetcs = []
ListOFDatasets = ["Datasets/winequality-red.csv","Datasets/winequality-white.csv"]
ListOfAlgorithms = []
ListOfAlgorithms.append(linear_model.Lasso(alpha=0.1))
OutputList = []
folds=list(range(1,11))
for datasetName in ListOFDatasets:
	#calculate columns and target and and read dataset values
	#create an object of dataset using above calculated values.
	#store these calculated objects in a list for further calculations
	if(datasetName == "Datasets/winequality-red.csv"):
		dataset = pandas.read_csv(datasetName,sep=';')
		toalNumOfInstance = len(dataset.index)
		columns = dataset.columns
		#columns = [c for c in columns if c not in ["alcohol","pH","suplphates","density","residual sugar"]]
		target = "quality"
		datasetObject = Dataset(columns,target,dataset)
		datasetObject.setNumOfInstace(toalNumOfInstance)
		datasetObject.setDatasetName(datasetName)
		ListOFDatasetObetcs.append(datasetObject)
	if(datasetName == "Datasets/winequality-white.csv"):
		dataset = pandas.read_csv(datasetName,sep=';')
		toalNumOfInstance = len(dataset.index)
		columns = dataset.columns
		#columns = [c for c in columns if c not in ["alcohol","pH","suplphates","density","residual sugar"]]
		target = "quality"
		datasetObject = Dataset(columns,target,dataset)
		datasetObject.setNumOfInstace(toalNumOfInstance)
		datasetObject.setDatasetName(datasetName)
		ListOFDatasetObetcs.append(datasetObject)

kf = KFold(n_splits=10, shuffle = True)
# print(ListOFDatasetObetcs[0].numberOfInstance)
for datasetObject in ListOFDatasetObetcs:#got throgh dataset objects
	print(datasetObject.getDatasetName())
	for model in ListOfAlgorithms:
		TmpList = []
		varList=[]
		#TmpList.append(datasetObject.getDatasetName())
		dataset = datasetObject.getDataset()
		columns = datasetObject.getColums()
		target = datasetObject.getTarget()
		print(datasetObject.numberOfInstance)
		
		for train_indices, test_indices in kf.split(dataset) :
			# print(numOFInstanceUsed)
			train = dataset.iloc[train_indices[:len(train_indices)]]
			test =  dataset.iloc[test_indices[:len(test_indices)]]
			columns = datasetObject.getColums()
			#print(columns)
			#print(type(columns))

			#target=datasetObject.getTarget()
			selector=SelectKBest(score_func=f_classif, k=5)
			selector.fit(train[columns],train[target])
			new_features=[]
			msk=selector.get_support()
			for i in range(len(columns)):
				if(msk[i]==True):
				   new_features.append(columns[i])
			#print(new_features)
			#x_new = SelectKBest(score_func=f_classif, k=5).fit_transform(train[columns], train[target])
			#mask =  x_new.get_support() #list of booleans
			#new_features = [] # The list of your K best features
			model.fit(train[columns],train[target])
			x_new_test = SelectKBest(f_regression, k=5).fit_transform(test[columns], test[target])
			prediction = model.predict(test[columns])
			#prediction=prediction[0]
			#actualValue=test.iloc[0][target]
			#print(sqrt(((prediction-actualValue)**2).mean()))
			actualValue = test[target]
			rmse = sqrt(mean_squared_error(actualValue,prediction))
			var = explained_variance_score(actualValue, prediction)
			varList.append(var)
			#print(prediction[0])
			#print(test.iloc[0][target])
			TmpList.append(rmse)
		OutputList.append(TmpList)
		OutputList.append(varList)

for i in range(int(len(OutputList)/int(2))):
	print("maen of rmse is "+str(sum(OutputList[2*i])/len(OutputList[2*i])))
	print("mean of var is "+str(sum(OutputList[2*i+1])/len(OutputList[2*i+1])))
	plt.plot(folds,OutputList[2*i])
	plt.show()
