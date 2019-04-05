# Sets working directory to dataset location
setwd("c:/Users/thomaspickup/icloudDrive/Documents/University/CSC3002/Assignment/CSC3002-Project/Experimental/Production")

cat("- Importing Libraries\n")
library(caret)
library(e1071)

# Sets the random seed to ensure repeatability
set.seed(3002)

cat("- Importing Dataset as CSV\n")
predict_this<-read.csv("product_api.csv")

# Nullifies any identifying data
predict_this$SampleName<-NULL

setwd("c:/Users/thomaspickup/icloudDrive/Documents/University/CSC3002/Assignment/CSC3002-Project/Experimental/Model")
load("knn_model.rda")

cat("- Evaluating Model with sample passed\n")
predictions<-predict(object=model,predict_this)

setwd("c:/Users/thomaspickup/icloudDrive/Documents/University/CSC3002/Assignment/CSC3002-Project/Experimental/DataSet")
malware_types<-read.csv("malware_types.csv")

prediction_text = levels(malware_types[, 2])[predictions]
cat(paste("Predicted Class: ", prediction_text, "\n"))
