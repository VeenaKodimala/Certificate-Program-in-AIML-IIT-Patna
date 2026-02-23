#Triple time double quotes are for multi line comments.
"""
Numeric Input Processing: Accept the number of games played and convert it to an integer data type
Score Data Entry: Collect the total score achieved and store it as an integer
Computation: Calculate the average score per game using division
Output Display: Present the results in the specified format shown below
Expected Output Format
Player: <name>

Games Played: <number>

Total Score: <score>

Average Score: <average>

Execution Instructions
Save your script with the exact filename: game_score.py
Execute the program from the terminal/command line
Test the script with at least one set of sample inputs
Verify that all output matches the required format
Upload it to your GitHub Repository and share the GitHub link and the Output of the Program.
"""


try:
    playerName=input("Player:")
    gamesPlayed = int(input("Games Played:"))
    totalScore = int(input("Total Score:"))
    averageScore = totalScore/gamesPlayed
    print(f"Average Score: {averageScore}")

except:
    print("Invalid values entered")

