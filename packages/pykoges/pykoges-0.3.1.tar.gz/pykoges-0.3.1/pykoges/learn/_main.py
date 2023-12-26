__all__ = ["model"]

from IPython.display import display
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    roc_curve,
    auc,
    accuracy_score,
    confusion_matrix,
)
from sklearn import svm
from sklearn.preprocessing import (
    MinMaxScaler,
    RobustScaler,
    StandardScaler,
    MaxAbsScaler,
)
from sklearn.tree import DecisionTreeClassifier

import torch
from torch import nn, optim
import torch.nn.functional as F

from ..koges import split_data
from ..utils import arr_to_df, isdiscrete, isbinary
from ..utils.map import name_map

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd, numpy as np, random


def __scale(koges, scaler):
    df = koges.data
    X = df[koges.x].astype(float)
    Y = df[koges.y[0]]
    Y = Y.reset_index(drop=True)
    scaler = scaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=koges.x)
    df = pd.concat([X_scaled, Y], axis=1)
    return df


def __split(koges):
    X = koges.data[koges.x].astype(float)
    y = koges.data[koges.y[0]]
    val_rate = 0.2
    random_state = random.randint(1, 100)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=val_rate, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


class model:
    def __init__(
        self,
        koges,
    ) -> None:
        self.koges = koges
        self.scalers = [
            MinMaxScaler,
            StandardScaler,
            RobustScaler,
            MaxAbsScaler,
        ]

    def regressor(self, isdisplay=True):
        X_train, X_test, y_train, y_test = __split(self.koges)

        model = self.model()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        n = len(y_test + y_train)

        # adjusted R2
        r2 = 1 - (1 - r2) * (n - 1) / (n - X_test.shape[1] - 1)

        name = model.__class__.__name__
        result = arr_to_df(
            [
                ["모델", name],
                ["MAE", f"{mae:.4f}"],
                ["MSE", f"{mse:.4f}"],
                ["R2 score", f"{r2:.4f}"],
            ]
        )
        if isdisplay:
            display(result)

        plt.ioff()
        # 입력이 하나인 경우 plot을 그립니다.
        if len(self.koges.x) == 1 and isinstance(model, LinearRegression) and isdisplay:
            plt.figure(figsize=(6, 4))
            plt.scatter(X_test, y_test, alpha=0.1)
            plt.plot(X_test, y_pred)
            plt.xlabel(self.koges.x[0])
            plt.ylabel(self.koges.y[0])
            plt.title("Regression Curve")
            plt.show()

        # 요소별 중요도를 그릴 수 있는 경우 상위 8개 요소에 대한 중요도를 그립니다.
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            indices = np.argsort(importances)[-8:]
            features = X_test.columns
            features = [features[i] for i in indices]

            fig = plt.figure(figsize=(5, len(indices) * 0.5))
            plt.title("Feature Importances")
            plt.barh(
                range(len(indices)), importances[indices], color="b", align="center"
            )
            plt.yticks(range(len(indices)), [name_map.get(x, x) for x in features])
            plt.xlabel("Relative Importance")
            if isdisplay:
                plt.show()
            self.koges.SAVE["importance"] = fig
        plt.close()

        self.koges.SAVE[name] = result
        self.koges.r2 = r2

    def logistic(self):
        y = self.koges.y[0]
        data = __scale(self.koges, scaler=scaler)
        data[y] = data[y].astype(int)
        X_train, X_test, y_train, y_test = __split(self.koges)

        model = LogisticRegression()
        model.fit(X_train, y_train)

        y_pred_prob = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
        roc_auc = auc(fpr, tpr)

        y_name = name_map.get(y, y)
        plt.plot(fpr, tpr, color="grey", lw=2, label=f"ROC curve (auc = {roc_auc:.2f})")
        plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
        plt.xlabel("FPR")
        plt.ylabel("TPR")
        plt.title(f"{y_name} ({scaler.__name__})")
        plt.legend(loc="lower right")

        self.koges.model = model
        self.koges.roc_auc = roc_auc

    def muticlassRoc(self):
        for i, _class in enumerate(self.koges.classes):
            if (self.y_test == i).sum():
                fpr, tpr, _ = roc_curve(self.y_test == i, self.predictions[:, i])
                roc_auc = auc(fpr, tpr)
                plt.plot(
                    fpr,
                    tpr,
                    lw=2,
                    label=f"{_class} (auc = {roc_auc:.2f})",
                    color="b",
                    alpha=(1 - i * 0.2),
                )
        plt.plot([0, 1], [0, 1], "k--", lw=2)
        plt.xlabel("FPR")
        plt.ylabel("TPR")
        plt.legend(loc="lower right")

    def classifier(koges):
        X_train, X_test, y_train, y_test = __split(koges)
        model = koges.model()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        name = model.__class__.__name__
        print("----------------------------")
        print(f"{model.__class__.__name__}")
        print(f"예측 정확도 : {accuracy*100:.2f}%")

        fig = plt.figure(figsize=(3, 3))
        conf_matrix = pd.DataFrame(
            confusion_matrix(y_test, y_pred, labels=range(koges.n_class)),
            index=koges.classes,
            columns=koges.classes,
        )
        sns.heatmap(
            conf_matrix.rename(index=name_map, columns=name_map),
            annot=True,
            fmt="d",
            cmap="Blues",
        )
        plt.title(name)
        plt.show()

        koges.SAVE[name] = fig
        koges.model = model

    def svmClassifier(koges):
        X_train, X_test, y_train, y_test = __split(koges)
        model = svm.SVC(kernel="linear", C=1.0)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print("----------------------------")
        print(f"{model.__class__.__name__}")
        print(f"예측 정확도 : {accuracy*100:.2f}%")

        plt.figure(figsize=(3, 3))
        conf_matrix = pd.DataFrame(
            confusion_matrix(y_test, y_pred, labels=range(koges.n_class)),
            index=koges.classes,
            columns=koges.classes,
        )
        sns.heatmap(
            conf_matrix.rename(index=name_map, columns=name_map),
            annot=True,
            fmt="d",
            cmap="Blues",
        )
        plt.show()
        koges.model = model

    def softmax(self):
        __scale(self.koges, scaler=self.koges.scaler)

        X_train, X_test, y_train, y_test = __split(self.koges)
        model = nn.Linear(X_train.shape[1], self.koges.n_class)
        optimizer = optim.SGD(model.parameters(), lr=0.01)

        X_tensor = torch.FloatTensor(X_train.values)
        y_tensor = torch.tensor(y_train.values, dtype=torch.long)

        # model.fit의 과정, n번 학습
        n = 1000
        for i in range(n):
            cost = F.cross_entropy(model(X_tensor), y_tensor)
            optimizer.zero_grad()
            cost.backward()
            optimizer.step()

        X_test_tensor = torch.FloatTensor(X_test.values)
        predictions = F.softmax(model(X_test_tensor), dim=1)

        y_pred = torch.argmax(predictions, dim=1)
        # accuracy = accuracy_score(y_test, y_pred)
        # print('----------------------------')
        # print('SoftMax Classifier')
        # print(f"예측 정확도 : {accuracy*100:.2f}%")

        # plt.show()
        conf_matrix = pd.DataFrame(
            confusion_matrix(y_test, y_pred, labels=range(self.koges.n_class)),
            index=self.koges.classes,
            columns=self.koges.classes,
        )
        self.conf_matrix = conf_matrix
        self.predictions = predictions.detach().numpy()
        self.y_test = y_test
        self.model = model

    def learn(self):
        y = self.koges.y[0]
        # Logistic의 경우 AUC로 정확도를
        # Linear, Randomforest의 경우 MSE,MAE,R2로 정확도를 보겠습니다.
        if self.koges.data.empty:
            print("조건을 만족하는 데이터가 존재하지 않습니다.")
            return
        if isdiscrete(self.koges.q, y):
            # classes : 통계분석에서 filtered된 class
            # svmClassifier(df, classes)
            # classifier(df, DecisionTreeClassifier, classes)
            # classifier(df, RandomForestClassifier, classes)

            confs = []
            fig, ax = plt.subplots(
                nrows=1,
                ncols=3,
                figsize=(11, 4),
                constrained_layout=True,
                sharey=False,
            )
            for i, scaler in enumerate(self.scalers):
                self.softmax()
                plt.subplot(1, 3, i + 1)
                self.muticlassRoc()
                y_pred = torch.argmax(self.predictions, dim=1)
                accuracy = accuracy_score(y, y_pred)
                plt.title(f"{scaler.__name__} (accuracy={accuracy:.2f})")
                confs.append(self.conf_matrix)
            plt.suptitle("Multiclass ROC curve")
            plt.show()

            fig2, ax = plt.subplots(
                nrows=1, ncols=3, figsize=(10, 4), constrained_layout=True, sharey=True
            )
            for i, scaler in enumerate(self.scalers):
                plt.subplot(1, 3, i + 1)
                sns.heatmap(confs[i], annot=True, fmt="d", cmap="Blues")
                plt.title(f"Softmax ({scaler.__name__})")
            plt.suptitle("Confusion matrix")
            plt.show()
            self.koges.SAVE["multiclassRoc"] = fig
            self.koges.SAVE["softmaxClassifier"] = fig2
        elif isbinary(y):
            fig, ax = plt.subplots(
                nrows=1, ncols=3, figsize=(9, 3), constrained_layout=True, sharey=False
            )
            plt.subplot(1, 3, 1)
            model1, auc1 = logisticRegression(df, scaler=StandardScaler)
            plt.subplot(1, 3, 2)
            model2, auc2 = logisticRegression(df, scaler=MinMaxScaler)
            plt.subplot(1, 3, 3)
            model3, auc3 = logisticRegression(df, scaler=RobustScaler)
            plt.suptitle("ROC curve")
            plt.show()
            self.koges.SAVE["LogisticRegression"] = fig
            model = [model1, model2, model3][
                [auc1, auc2, auc3].index(max(auc1, auc2, auc3))
            ]
        else:
            df = __scale(df, RobustScaler)
            model, r2 = regressor(df, LinearRegression)
            regressor(df, RandomForestRegressor)
            # regression의 결과가 안좋은 경우 classification도 진행합니다.
            if r2 < 0.8:
                dfs, _, _ = split_data(df, n_class=self.koges.n_class)
                for i in range(self.koges.n_class):
                    dfs[i].loc[:, y] = i
                df = pd.concat(dfs.values())
                classifier(df, DecisionTreeClassifier, self.koges.classes)
                classifier(df, RandomForestClassifier, self.koges.classes)
                softmaxClassifier(df, self.koges.classes)

        return model
