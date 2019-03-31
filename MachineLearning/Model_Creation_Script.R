print("~~ Model Production: Started ~~")

# Sets working directory to dataset location
setwd("c:/Users/thomaspickup/icloudDrive/Documents/University/CSC3002/Assignment/CSC3002-Project/Dataset")

# Installs the libraries if needed and imports them
library(caret)
library(e1071)

# Sets the random seed to ensure repeatability
set.seed(3002)

# Imports the Api Results and sample list
api.csv<-read.csv("api_results.csv")
sample.csv<-read.csv("sample_list.csv")
malware.csv<-read.csv("malware_types.csv")

# Merges together to create one data frame
ds<-merge(x=api.csv, y=sample.csv, by.x="SampleName", by.y="MD5hash")
mu<-merge(x=ds, y=malware.csv, by="MalwareID")

# Nullifies any identifying data
ds$SampleName<-NULL
ds$SampleID<-NULL
ds$Score<-NULL

# Changes malware ID to be a factor rather than an integer
ds$MalwareID = as.factor(ds$MalwareID)

# Gets the ID of the malwareID column 
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
cMatrix<- confusionMatrix(predictions, ds.test[,malwareID_Col])
nr_correct<-nrow(ds.test[correct_predictions,])
nr_test_items<-nrow(ds.test)
nr_incorrect<-nr_test_items - nr_correct

# Saves the model to file
setwd("c:/Users/thomaspickup/icloudDrive/Documents/University/CSC3002/Assignment/CSC3002-Project/Model")
save(model, file = 'knn_model.rda')

# Outputs the stats file
fileConn<-file("accuracies.txt")
accuracy <- round((nr_correct/nr_test_items) * 100, digits=2)
output <- c(paste("Accuracy: ", accuracy, "%", sep = ""),
            "",
            paste("Correct: ", nr_correct, " Predictions", sep = ""),
            paste("Incorrect: ", nr_incorrect, " Predictions", sep = ""),
            paste("Total: ", nr_test_items, " Test Items", sep = ""))
writeLines(output, fileConn)
close(fileConn)

# Writes confusion matrix to csv file
write.csv(cMatrix$byClass, file = "confusionMatrix.csv")

# Writes the api_headers to a csv for use with model
write.table(t(colnames(ds[1:lastFeature_Col])), file = "api_headers.csv", sep = ",",  col.names = FALSE, row.names = FALSE)

# Exports the list of malware used to text file
malware.used<- data.frame(mu$SampleName, mu$MalwareID, mu$MalwareName)

fileConn<-file("malware_used.txt")
currentMalwareID<- 0
malwareSplit <- summary(malware.used$mu.MalwareName)

outputMal <- ""
i = 1
for (type in malwareSplit) {
  outputMal <- c(outputMal, 
                 paste(names(malwareSplit)[i], ": ", type, sep = ""))
  i = i + 1
}

outputMal <- c(outputMal, "")

for (i in 1:nrow(malware.used)) {
  if (currentMalwareID != malware.used[i, "mu.MalwareID"]) {
    outputMal = c(outputMal, 
                  "", 
                  paste("", malware.used[i, "mu.MalwareName"], sep = ""), 
                  paste("", malware.used[i, "mu.SampleName"], sep = ""))
    currentMalwareID = malware.used[i, "mu.MalwareID"]
  } else {
    outputMal = c(outputMal, 
                  paste("", malware.used[i, "mu.SampleName"], sep = ""))
  }
}
writeLines(outputMal, fileConn)
close(fileConn)

print("~~ Model Production: Complete ~~")
