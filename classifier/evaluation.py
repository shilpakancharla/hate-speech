import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score,roc_auc_score, f1_score, recall_score
from sklearn.metrics import  roc_curve, confusion_matrix, precision_score

def calculatePerformance(model, data, target, name):
    predictions = model.predict(data)
    modelProbability = model.predict_proba(data)[:,1]

    f1 = f1_score(target, predictions)
    accuracy = accuracy_score(target, predictions)
    rocScore = roc_auc_score(target, modelProbability)
    precision = precision_score(target, predictions)
    modelName = str(name)

    score = pd.DataFrame()

    score['Model'] = pd.Series(modelName)
    score['F1'] = pd.Series(f1)
    score['Accuracy'] = pd.Series(accuracy)
    score['ROC_Score'] = pd.Series(rocScore)
    score['Precision'] = pd.Series(precision)

    return score

def plotROCCurve(model, train, validation, y_train, y_val, title):
    basePredTrain = model.predict_proba(train)[:,1]
    baseFprTrain, baseTprTrain, baseThreshTrain = roc_curve(y_train, basePredTrain)

    basePredValidation = model.predict_proba(validation)[:,1]
    baseFprValidation, baseTprValidation, baseThreshValidation = roc_curve(y_val, basePredValidation)

    plt.style.use('seaborn')
    plt.figure(figsize=(12, 7))
    axis1 = sns.lineplot(baseFprTrain, baseTprTrain, label='Train')
    axis1.lines[0].set_color("red")

    axis2 = sns.lineplot(baseFprValidation, baseTprValidation, label='Validation')
    axis2.lines[1].set_color("blue")

    axis3 = sns.lineplot([0, 1], [0, 1], label='Baseline')
    axis3.lines[2].set_color("black")

    plt.title(str(title), ' ROC Curve')
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.show()

def maxSeqLength(sequence):
    length = []
    for i in range(0, len(sequence)):
        length.append(len(sequence[i]))
    
    return max(length)