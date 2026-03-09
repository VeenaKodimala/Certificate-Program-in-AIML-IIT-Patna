'''Real-World Context:
You're maintaining a simple grade book for 5 students with their marks in 3 subjects. Use Python data structures to store and analyze this data.

Your Task:
Write a Python program using Lists, Dictionaries, Tuples, and Sets to:

Store student names and marks
Calculate averages
Find top scorer
Display results
Requirements:
Use these data structures:

List - Store student names
Dictionary - Store marks for each student
Tuple - Store subject names
Set - Store unique grades
Program should:

Display all student names
Show first 3 students (using slicing)
Calculate and print each student's average
Find student with highest average
Show all unique grades
Sample Data to Use:
Students: Raj, Priya, Amit, Sneha, Karan

Marks:
Raj: Math=85, Science=78, English=90
Priya: Math=92, Science=88, English=85
Amit: Math=70, Science=75, English=68
Sneha: Math=95, Science=90, English=92
Karan: Math=80, Science=82, English=78
Grading Logic:

Average ≥ 85: Grade A
Average ≥ 70: Grade B
Average < 70: Grade C
'''

students = ['Raj', 'Priya', 'Amit', 'Sneha', 'Karan']
marks = {'Raj': {'Math':85, 'Science':78, 'English':90},
'Priya': {'Math':92, 'Science':88, 'English':85},
'Amit': {'Math':70, 'Science':75, 'English':68},
'Sneha': {'Math':95, 'Science':90, 'English':92},
'Karan': {'Math':80, 'Science':82, 'English':78}}

resultDict = {}

print(f"All student: {students}")

for key,value in marks.items():
    sum = 0
    innerLgth = len(value)
    for key1,value1 in value.items():
        sum = sum + value1

    avg = round((sum/innerLgth),2)
    resultDict[key] = avg

studentsSorted = sorted(resultDict,reverse=True)

del studentsSorted[len(studentsSorted)-1]
del studentsSorted[len(studentsSorted)-1]
print(f"First 3 Students:: {studentsSorted}")

uniqueGrades = set()
for key,val in resultDict.items():
    if val >= 85:
        grade='A'
    elif val >= 70:
        grade = 'B'
    else:
        grade = 'C'

    uniqueGrades.add( grade)
    print(f"{key} - Average: {val} - Grade: {grade}")     

print(f"Top Student: {studentsSorted[0]}")
topMarks = marks.get(studentsSorted[0])
print(f"Unique Grades: {uniqueGrades}")
    




