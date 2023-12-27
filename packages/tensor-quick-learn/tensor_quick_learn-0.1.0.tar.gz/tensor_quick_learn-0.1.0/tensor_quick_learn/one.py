import inspect
def func():
   ''' 
   a=pd.read_csv("Weather.csv", header=None).to_numpy()
   num_attribute = len(a[0])-1
   print(a)
   hypothesis = ['0']*num_attribute
   print("\nThe initial hypothesis is : ",hypothesis,"\n")
   for i in range(0, len(a)):
      if a[i][num_attribute] == 'Yes':
         for j in range(0, num_attribute):
           if hypothesis[j] == '0' or hypothesis[j] == a[i][j]:
              hypothesis[j] = a[i][j]
           else:
               hypothesis[j] = '?'
         print("The hypothesis for the training instance", i+1, " is: " , hypothesis, "\n")
      else:
        print("The hypothesis for the training instance", i+1, " is: " , hypothesis, "\n")
      print("\nThe Maximally specific hypothesis for the training instance is ", hypothesis)
   '''
def px():
    code=inspect.getsource(func)
    print(code)

