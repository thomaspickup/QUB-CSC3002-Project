setwd("/Users/thomaspickup/Documents/University/CSC3002/Assignment/CSC3002-Project/Dataset")

# Dataset Prep
api.csv<-read.csv("api_results.csv")
sample.csv<-read.csv("sample_list.csv")
ds<-merge(x=api.csv, y=sample.csv, by.x="SampleName", by.y="MD5hash")
ds$SampleName<-NULL
ds$SampleID<-NULL
ds$MalwareID = as.factor(ds$MalwareID)

library(caret)
library(e1071)

# Create index to split based on labels  
index <- createDataPartition(ds$MalwareID, p=0.75, list=FALSE)

# Subset training set with index
ds.training <- ds[index,]

# Subset test set with index
ds.test <- ds[-index,]

# Overview of algos supported by caret
names(getModelInfo())

# Train a model
model_knn <- train(ds.training[, 1:222], ds.training[, 223], method='knn')

# Predict the labels of the test set
predictions<-predict(object=model_knn,ds.test[,1:222])

# Evaluate the predictions
table(predictions)

# Confusion matrix 
confusionMatrix(predictions,ds.test[,223])
