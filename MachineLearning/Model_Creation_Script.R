cat("~~ Model Production: Started ~~\n")

# Sets working directory to dataset location
setwd("c:/Users/thomaspickup/icloudDrive/Documents/University/CSC3002/Assignment/CSC3002-Project/Dataset")

cat("- Importing Libraries\n")
library(caret)
library(e1071)
library(Boruta)

# Sets the random seed to ensure repeatability
set.seed(3002)

cat("- Importing Dataset as CSV\n")
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

cat("- Performing Boruta Algorithm\n")
ds.boruta <- Boruta(ds[, malwareID_Col]~., data = ds, doTrace = 2)
ds.boruta.final <- TentativeRoughFix(ds.boruta)
ds.selected.attributes<-getSelectedAttributes(ds.boruta.final, withTentative = F)

# Gets the final dataset using only the selected features
ds.final <- ds[,ds.selected.attributes]

malwareID_Col <- ncol(ds.final)
lastFeature_Col <- malwareID_Col - 1

# Create index to split based on labels  
index <- createDataPartition(ds.final$MalwareID, p=0.9, list=FALSE)

# Subset training set with index
ds.training <- ds.final[index,]

# Subset test set with index
ds.test <- ds.final[-index,]

cat("- Training Model\n")
model <- train(ds.training[, 1:lastFeature_Col], ds.training[, malwareID_Col], method='knn')

cat("- Evaluating Model with test set\n")
predictions<-predict(object=model,ds.test[,1:lastFeature_Col])

# Evaluate the predictions
cat("- Saving Model and statistics\n")
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
write.table(t(colnames(ds.final[1:lastFeature_Col])), file = "api_headers.csv", sep = ",",  col.names = FALSE, row.names = FALSE)

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

cat("~~ Model Production: Complete ~~\n")
