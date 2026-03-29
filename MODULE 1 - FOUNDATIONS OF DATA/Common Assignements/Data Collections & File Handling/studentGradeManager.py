def logging(studentname):
    with open("activity.log","a") as contxtMngr:
        contxtMngr.write(f"Added new studed: {studentname}")
        print("Entry logged successfully")


with open("StudentGradeManager.txt","w") as contxtMngr:
    print("---------------TASK-1---------------------")
    contxtMngr.write("Alice,85\nBob,92\nCharlie,78\nDiana,95")
    print("Data saved successfully")


try:
    with open("StudentGradeManager.txt","r") as contxtMngr:
         print("---------------TASK-2---------------------")
         for line in contxtMngr:
              Name,score = line.split(",")
              print(f"Student: {Name}, Score: {score}")    
except FileNotFoundError:
    print("File is not found")              

with open("StudentGradeManager.txt","a") as contxtMngr:
    print("---------------TASK-3&4---------------------")
    contxtMngr.write( "\nEve,88")
    print("New entry added into the file successfully")
    logging("Eve")



              