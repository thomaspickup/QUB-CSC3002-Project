setwd("c:/Users/thomaspickup/icloudDrive/Documents/University/CSC3002/Assignment/CSC3002-Project/Dataset")

# Dataset Prep
api.csv<-read.csv("api_results.csv")
sample.csv<-read.csv("sample_list.csv")
ds<-merge(x=api.csv, y=sample.csv, by.x="SampleName", by.y="MD5hash")
ds$SampleName<-NULL
ds$SampleID<-NULL
ds$Score<-NULL
ds$MalwareID = as.factor(ds$MalwareID)

library(caret)
library(e1071)

# Create index to split based on labels  
index <- createDataPartition(ds$MalwareID, p=0.75, list=FALSE)

# Subset training set with index
ds.training <- ds[index,]

# Subset test set with index
ds.test <- ds[-index,]

# Train a model
model_knn <- train(ds.training[, 1:271], ds.training[, 272], method='knn')

# Predict the labels of the test set
predictions<-predict(object=model_knn,ds.test[,1:271])

# Evaluate the predictions
table(predictions)
nr_correct<- predictions == ds.test[,272]
proportion_correct <- nrow(ds.test[nr_correct,])/nrow(ds.test)