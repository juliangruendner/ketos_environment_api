
install.packages(c('randomForest', 'caret', 'doMC', 'plyr', 'reshape'))

genPrep <- function(seed){
  #Clean environment 
  rm(list=ls())
  gc()
  
  #include libraries
  library(caret)
  library(randomForest)
  library(doMC)
  library(plyr)
  library(reshape)
  
  #register DoMC cores
  registerDoMC(cores = 8)
}

splitData <- function(seed, data){
  # randomly splits data into training (0.8) and test (0.2) data
  
  set.seed(seed)
  training_index <- createDataPartition(data[[ncol(data)]], p = 0.8, list = F)
  training <- data[training_index,]
  test <- data[-training_index,]
  
  return(list(training=training,test=test))
}

trainModels <- function(dataset = NULL, outcomeVar = NULL, metric = "Accuracy", control = NULL){
  # trains all the caret models according to control and metric
  
  retList <- list()
  
  form <- as.formula(paste(c(outcomeVar, "~."), collapse=" "))
  
  #set.seed(seed)
  
  print("start train GLMNET")
  set.seed(seed)
  retList$glmnet <- caret::train(form, data=dataset, method="glmnet", metric=metric, preProc=c("center", "scale"), trControl=control)

  # KNN (KNN - k-nearest-neighbour)
  print("start train KNN")
  set.seed(seed)
  retList$knn <- caret::train(form, data=dataset, method="knn", metric=metric, preProc=c("center", "scale"), trControl=control)

  # nnet (ANN - artificial neural network)
  print("start train ANN")
  set.seed(seed)
  retList$ann <- caret::train(form, data=dataset, method="nnet", metric=metric, trControl=control)

  #C5.0 (DT - decision tree)
  print("start train DT")
  set.seed(seed)
  retList$dt <- caret::train(form, data=dataset, method="C5.0", metric=metric, trControl=control)

  # RF (RF - random forest)
  print("start train RF")
  set.seed(seed)
  retList$rf <- caret::train(form, data=dataset, method="rf", metric=metric, trControl=control)
  
  return(retList)
  
}

dataFile <- "iris_data_ml_omop_final.csv"
data <- read.csv(dataFile, header = TRUE, sep = ";", quote = "\"",dec = ".", fill = TRUE, comment.char = "")
genPrep()

seed <- 7
splitData <- splitData(seed, data)
trainingData<-splitData$training
testData <- splitData$test
fileTrain <- "training.csv"
fileTest <- "test.csv"

write.table(trainingData, fileTrain, sep = ";", quote = TRUE, dec = ".", row.names = FALSE, append = FALSE)
write.table(testData, fileTest, sep = ";", quote = TRUE, dec = ".", row.names = FALSE, append = FALSE)

metric <- "Accuracy"
control <- trainControl(method="repeatedcv", number=10, repeats=10, sampling="down", savePredictions="all")
outcomeVar <- "human.body.structure"
trainedModels <- trainModels(trainingData, outcomeVar,metric,control)
modeltoSave <- 'myCreatedModels'
save(trainedModels,file = modeltoSave)

createPredictModels <- function(dataset, modellist, packType = "caret"){
  ret <- list()
  
  for(model in modellist){
      modelName <- model$method
      ret[[modelName]] <- predict(model, dataset) 
    }
    
  return(ret)
}

evalModelListsAccsDf <- function(modellist, data, outcomeVar, packType = "caret", evalMetric = "Accuracy"){
  
  Model <- c();
  Accuracy <- c();
  cnt <- 1
  modelNames <- names(modellist)
  
  for (model in modellist){
      
      confMat <- confusionMatrix(model, data[,outcomeVar])
      Model[cnt] <- modelNames[cnt] 
      Accuracy[cnt] <- confMat[[c("overall",evalMetric)]]
      cnt <- cnt + 1
  }

    return(data.frame(Model, Accuracy))
  
  
}

predictFunc = function(){
     library(caret)
     modeltoLoad <- "myCreatedModels"
     load(modeltoLoad)
     training <- read.csv('training.csv', header = TRUE, sep = ";", quote = "\"",dec = ".", fill = TRUE, comment.char = "")
     testData <- read.csv('test.csv', header = TRUE, sep = ";", quote = "\"",dec = ".", fill = TRUE, comment.char = "")
     
     predictTrainCaretModels <- createPredictModels(training, trainedModels)
     predictTestCaretModels <- createPredictModels(testData, trainedModels)
     outcomeVar = 'human.body.structure'
     evalMetric <- "Accuracy"
     evalCaretModelsTraining <- evalModelListsAccsDf(predictTrainCaretModels, training, outcomeVar, evalMetric = evalMetric)
     evalCaretModelsTest <- evalModelListsAccsDf(predictTestCaretModels, testData, outcomeVar, evalMetric = evalMetric)
   
    #evalCaretModelsTraining
    evalCaretModelsTest

}

predictFunc()

#ketos_predict
ketos_predict = function(){
    load("myCreatedModels")
    predict_data <- read.csv('test_input.csv', header = TRUE, sep = ";", quote = "\"",dec = ".", fill = TRUE, comment.char = "")
    model = trainedModels$glmnet
    prediction = predict(model, predict_data)
    return(prediction)
}

myPrediction = ketos_predict()
print(as.character(myPrediction))
print('test')