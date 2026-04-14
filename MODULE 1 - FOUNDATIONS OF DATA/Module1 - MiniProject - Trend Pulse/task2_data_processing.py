import pandas as pd

trendsDF = pd.read_json(r"D:\Veena\Certificate Program in Artificial Intelligence and Machine Learning\Certificate-Program-in-AIML-IIT-Patna\MODULE 1 - FOUNDATIONS OF DATA\Module1 - MiniProject - Trend Pulse\data\trendingStories_15042026.json")

print(f"shape of trendsDF: {trendsDF.shape}")

duplicates = trendsDF.duplicated().sum()
print(f"Total no.of duplicated present in the dataset: {duplicates}")
if duplicates > 0:
    #Dropping the duplicate rows where the duplicate is the post_id.
    trendsDF = trendsDF.drop_duplicates(subset=['post_id'])
    print(f"Total no.of duplicated present in the dataset after dropping post_id column duplicates: {trendsDF.duplicated.sum()}")

print(f"length of dataset: {len(trendsDF)}")
trendsDF.info()

if(trendsDF[['post_id','title','score']].isna().values.any()):
    trendsDF=trendsDF.dropna(subset=['post_id','title','score'])
    print(f"shape of trendsCDF after deleting rows with missing post_id,title and score: {trendsDF.shape}")

print(f"Datatype of score column :{trendsDF['score'].dtypes}")

print(f"Datatype of num_comments column :{trendsDF['num_comments'].dtypes}")

print(f"Data where score is less than 5: {(trendsDF['score']<5).sum()}")

#Dropping the rows where the score is less than 5.
print(f"shape of trendsDF before deleting rows with score < 5: {trendsDF.shape}")
trendsDF = trendsDF[trendsDF['score']>5]
print(f"shape of trendsDF after deleting rows with score < 5: {trendsDF.shape}")

#Stripping empty spaces from title column.
trendsDF['title'] = trendsDF['title'].str.strip()

print(f"shape of trendsDF after cleaning data: {trendsDF.shape}")

trendsDF.to_csv(r"D:\Veena\Certificate Program in Artificial Intelligence and Machine Learning\Certificate-Program-in-AIML-IIT-Patna\MODULE 1 - FOUNDATIONS OF DATA\Module1 - MiniProject - Trend Pulse\data\trends_clean.csv",index=False)

print(f"no.of rows saved to csv: {len(pd.read_csv(r"D:\Veena\Certificate Program in Artificial Intelligence and Machine Learning\Certificate-Program-in-AIML-IIT-Patna\MODULE 1 - FOUNDATIONS OF DATA\Module1 - MiniProject - Trend Pulse\data\trends_clean.csv"))}")

#Get the count of stories in each category.
print(f"Category wise split of stories: \n{trendsDF.groupby(trendsDF['category']).size()}")

