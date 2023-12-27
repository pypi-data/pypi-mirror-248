import inspect
def func():

    '''
    from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
iris=load_iris()
print("Features:",iris.feature_names,"\n data:",iris.data,"\n target name:",iris.target_names, "\n target:",iris.target)
x_train,x_test,y_train,y_test=train_test_split(iris.data,iris.target,test_size=0.25)
clf=KNeighborsClassifier()
clf.fit(x_train,y_train)
print("Accuracy:",clf.score(x_test,y_test))
prediction=clf.predict(x_test)
print("Predicted data:",prediction)
print("y_test data :",y_test)
diff= prediction-y_test
print("result is:",diff)
count=0
for i in diff:
    if i!=0:
        count+=1
print("total points misclassified:",count)

   '''
   
def px():
    code=inspect.getsource(func)
    print(code)

