from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score ,classification_report


data =load_iris()
x=data.data
y=data.target

x_train,x_test,y_train,y_test=train_test_split(x,y,train_size=0.3,random_state=42)
model=RandomForestClassifier(n_estimators=100, max_depth=5,random_state=42)
model.fit(x_train,y_train)
 
y_pred=model.predict(x_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

