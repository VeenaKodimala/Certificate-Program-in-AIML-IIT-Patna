import pandas as pd
import numpy as np


trendsData = pd.read_csv(r"D:\Veena\Certificate Program in Artificial Intelligence and Machine Learning\Certificate-Program-in-AIML-IIT-Patna\MODULE 1 - FOUNDATIONS OF DATA\Module1 - MiniProject - Trend Pulse\data\trends_clean.csv")

#First 5 rows of DF
print(trendsData.head(5))

#shape of DF
print(trendsData.shape)

#Average score
print(f"Average score of DF: {trendsData['score'].mean():.2f}")
#Average num_comments
print(f"Average num_comments of DF: {trendsData['num_comments'].mean():.2f}")

print(f"Mean of score column:{trendsData['score'].mean():.2f}")
print(f"Median of score column:{trendsData['score'].median():.2f}")
print(f"Standard deviation score column:{trendsData['score'].std():.2f}")

print(f"Highest score of DF:{trendsData['score'].max():.2f}")
print(f"Lowest score of DF:{trendsData['score'].min():.2f}")

print(f"Category with max no.of stories: \n{trendsData.groupby(trendsData['category']).size().sort_values(ascending=False).head(1)}")

print(f"Story with max no.of comments: \n{trendsData.sort_values(by='num_comments',ascending=False)[['title','num_comments']].head(1)}")

#Adding new column to the DF
trendsData['engagement']=trendsData['num_comments'] / (trendsData['score'] + 1)
print(f"Columns of trendsData after adding engagement column: \n{trendsData.columns}")
print(trendsData.head(5))

averageScore = trendsData['score'].mean()
print(f"averageScore of trendsData: {averageScore}")

trendsData['is_popular'] =  trendsData['score'] > averageScore
print(f"Columns of trendsData after adding engagement column: \n{trendsData.columns}")
print(trendsData.head(5))


trendsData.to_csv(r"D:\Veena\Certificate Program in Artificial Intelligence and Machine Learning\Certificate-Program-in-AIML-IIT-Patna\MODULE 1 - FOUNDATIONS OF DATA\Module1 - MiniProject - Trend Pulse\data\trends_analysed.csv")

print(f"No.of rows saved in ccsv: {len(pd.read_csv(r"D:\Veena\Certificate Program in Artificial Intelligence and Machine Learning\Certificate-Program-in-AIML-IIT-Patna\MODULE 1 - FOUNDATIONS OF DATA\Module1 - MiniProject - Trend Pulse\data\trends_analysed.csv"))}")