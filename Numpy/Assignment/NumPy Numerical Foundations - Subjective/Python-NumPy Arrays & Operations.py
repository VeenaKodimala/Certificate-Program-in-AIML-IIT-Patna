import numpy as np
np.random.seed(42)

print("----------------TASK-1--------------------------")
scores = np.random.randint(50,101,(5,4))
print(f"scores:: {scores}")

print(f"Scores of 3rd student in 2nd subject: {scores[2][1]}")
print(f"Scores of last 2nd student: {scores[len(scores)-2]}")
print(f"Scores of last student: {scores[len(scores)-1]}")
for i in range(0,3):
    print(f"Scores of student {i+1} in 2nd subject: {scores[i][1]}")
    print(f"Scores of student {i+1} in 3rd subject: {scores[i][2]}")

print("--------------TASK-2--------------------------")

print(f"mean column-wise:{np.mean(scores)}")

##Clip is used to limit te values be it lower limit or the upper.
##None means no lower limit.
curved_scores=np.clip(scores+np.array([5, 3, 7, 2]),None,100)
print(f"curved_scores: {curved_scores}")
#This will give the mmax element in each row, axis=1
print(f"best subject score: {curved_scores.max(axis=1)}")
print(f"worst score in all subjects: {curved_scores.min(axis=0)}")

print("------------------TASK-3--------------------")

row_min = curved_scores.min(axis=1,keepdims=True)
print(f"row_min: {row_min}")
row_max = curved_scores.max(axis=1,keepdims=True)
print(f"row_max: {row_max}")

minMaxArr = (curved_scores - row_max)/(row_max-row_min)
print(f"Min-Max normalised array: {minMaxArr}")

#argmax will give the index of the large element
#  in a 1-D array, meaning a flattened array.
#  our (4,3) 2d array will become (!2,) 1-d array
#In our array 0 is the max elemnt, 
# and the first occurance of it is 3 index
flatIndex = np.argmax(minMaxArr)
print("flatIndex: ",flatIndex)

'''Here the curved_scores>90 will give a boolean 2d 
array where true will be set for the values satisfying 
the condition,and false for otherwise.
then cureved_scores[booleanarry] will automatiacally
get flattened into a 1d array with scores
' where the boolean values was true in boolean array'''
above90Scores = curved_scores[curved_scores > 90]
print("above90Scores:: ", above90Scores)



