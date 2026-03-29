'''Problem Statement:

Create a grade calculation system that uses *args and **kwargs to handle different scoring scenarios.

Requirements:

Create a function calculate_grade() with:

Parameters:
*scores - Variable number of test scores
**adjustments - Optional keyword arguments for bonus points (e.g., attendance=5, project=10)
Returns: Final grade percentage (float)
Logic: Average of scores + sum of all bonus adjustments
Task: Calculate grades for:

Student with scores: 85, 90, 78 (no bonus)
Student with scores: 70, 65, 80 (with attendance=5, project=10 bonus)'''

def calculate_grade(*args,**kargs):
    avg = round(sum(args)/len(args),2)
    total = 0
    for key,val in kargs.items():
        total = total+val

    finalGrade = avg + total

    return finalGrade


print(f"Final Grade: {calculate_grade(85, 90, 78,attendance=0, project=0)}")
print(f"Final Grade: {calculate_grade(70, 65, 80,attendance=5, project=10)}")




