import inspect
def func():

    '''
	import pandas as pd
import numpy as np

data = pd.read_csv('data.csv')
arr = np.array(data)
dict_counts = {}
for i in range(0, arr.shape[0]):
  for j in range(0, arr.shape[1] - 1):
    if arr[i][j] not in dict_counts:
      dict_counts[arr[i][j]] = [0, 0]
    if arr[i][-1] == 'Yes':
      dict_counts[arr[i][j]][0] += 1
    else:
      dict_counts[arr[i][j]][1] += 1
print(dict_counts)
count_yes = np.sum(arr[:, -1] == 'Yes')
count_no = np.sum(arr[:, -1] == 'No')
print("\n\npositive :", count_yes, "\nNegative : ", count_no)
prior_yes = count_yes / arr.shape[0]
prior_no = count_no / arr.shape[0]
print("\n\npositive :", prior_yes, "\nNegative : ", prior_no)
inp = input("Enter test file name: ")
test = pd.read_csv(inp)

# Convert test data to numpy array
test_arr = np.array(test)

# Initialize lists to store actual and predicted labels
actual_labels = []
predicted_labels = []

# Iterate through test data
for i in range(test_arr.shape[0]):
  prob_yes = prior_yes
  prob_no = prior_no

  # Calculate conditional probabilities for each attribute
  for j in range(test_arr.shape[1] - 1):
    if test_arr[i][j] in dict_counts:
      prob_yes *= dict_counts[test_arr[i][j]][0] / count_yes
      prob_no *= dict_counts[test_arr[i][j]][1] / count_no

  # Predict the class based on the probabilities
  if prob_yes > prob_no:
    predicted_labels.append('Yes')
  else:
    predicted_labels.append('No')

  # Record the actual label
  actual_labels.append(test_arr[i][-1])

# Calculate accuracy
correct_predictions = np.sum(
    np.array(actual_labels) == np.array(predicted_labels))
accuracy = (correct_predictions / len(actual_labels)) * 100

print("Accuracy: {:.2f}%".format(accuracy))
   '''
   
def px():
    code=inspect.getsource(func)
    print(code)

