'''Write a simple Python program to evaluate a student's result using conditional statements.

Requirements:
Ask the user to enter:

Student name
Marks in Maths, Science, and English
Validate the marks:

If any mark is less than 0 or greater than 100, print Invalid marks entered and stop the program.
Calculate:

Total marks
Average percentage
Determine Pass / Fail:

If any subject mark is below 40, the student fails
Otherwise, the student passes
If the student passes, assign a grade:

A → Average ≥ 75
B → Average ≥ 60 and < 75
C → Average ≥ 40 and < 60
Display:

Student name
Total marks
Average percentage (2 decimal places)
Pass/Fail status
Grade (only if passed)
'''
import sys
name = input("Enter your name: ")
mathMark = int(input("Enter your marks in Math: "))
scienceMark = int(input("Enter your mark in Science: "))
engMark = int(input("Enter your mark in English: "))



if((mathMark<0 or mathMark>100)  or (scienceMark<0 or scienceMark>100) or (engMark<0 or engMark>100)):
    print(f"One of the marks entered is invalid")
    sys.exit()

totalMarks = mathMark+scienceMark+engMark
avgPercentage = (totalMarks/3)

if(mathMark < 40 or scienceMark < 40 or engMark < 40 ):
    status = "FAIL"
else:
    status = "PASS"
     
if(avgPercentage >= 75):
    grade = "A"
elif(avgPercentage >=60 and avgPercentage < 70):
    grade = "B"    
else:
    grade = "C"

print(f"Student Name: {name}")   
print(f"Total Marks: {totalMarks}")
print(f"Percentage: {avgPercentage}")
print(f"Status: {status}")
print(f"Grade: {grade}")        





