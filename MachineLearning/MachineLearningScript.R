print("~~ Model Production: Started ~~")

setwd("c:/Users/thomaspickup/icloudDrive/Documents/University/CSC3002/Assignment/CSC3002-Project/Dataset")
library(caret)
library(e1071)
set.seed(3002)

# Dataset Prep
api.csv<-read.csv("api_results.csv")
sample.csv<-read.csv("sample_list.csv")
ds<-merge(x=api.csv, y=sample.csv, by.x="SampleName", by.y="MD5hash")
ds$SampleName<-NULL
ds$SampleID<-NULL
ds$Score<-NULL
ds$MalwareID = as.factor(ds$MalwareID)

malwareID_Col <- ncol(ds)
lastFeature_Col <- malwareID_Col - 1

# Create index to split based on labels  
index <- createDataPartition(ds$MalwareID, p=0.75, list=FALSE)

# Subset training set with index
ds.training <- ds[index,]

# Subset test set with index
ds.test <- ds[-index,]

# Train a model
model <- train(ds.training[, 1:lastFeature_Col], ds.training[, malwareID_Col], method='knn')

# Predict the labels of the test set
predictions<-predict(object=model,ds.test[,1:lastFeature_Col])

# Evaluate the predictions
correct_predictions<- predictions == ds.test[,malwareID_Col]
cMatrix = confusionMatrix(predictions, ds.test[,malwareID_Col])
nr_correct<-nrow(ds.test[correct_predictions,])
nr_test_items<-nrow(ds.test)
nr_incorrect<-nr_test_items - nr_correct

setwd("c:/Users/thomaspickup/icloudDrive/Documents/University/CSC3002/Assignment/CSC3002-Project/Model")
save(model, file = 'knn_model.rda')

fileConn<-file("accuracies.txt")
accuracy <- round((nr_correct/nr_test_items) * 100, digits=2)
output <- c(paste("Accuracy: ", accuracy, "%", sep = ""),
            "",
            paste("Correct: ", nr_correct, " Predictions", sep = ""),
            paste("Incorrect: ", nr_incorrect, " Predictions", sep = ""),
            paste("Total: ", nr_test_items, " Test Items", sep = ""))
writeLines(output, fileConn)
close(fileConn)

write.csv(cMatrix$byClass, file = "confusionMatrix.csv")

print("~~ Model Production: Complete ~~")
