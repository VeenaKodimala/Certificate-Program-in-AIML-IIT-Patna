import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sb
trendsData = pd.read_csv(r"D:\Veena\Certificate Program in Artificial Intelligence and Machine Learning\Certificate-Program-in-AIML-IIT-Patna\MODULE 1 - FOUNDATIONS OF DATA\Module1 - MiniProject - Trend Pulse\data\trends_analysed.csv")

#First 5 rows of DF
print(trendsData.head(5))


#Function to plot top 10 stories
def plot_top_stories(df, ax=None):
    top = df.sort_values(by='score', ascending=False).head(10)
    top['short_title'] = top['title'].str.slice(0, 50)

    if ax is None:
        fig, ax = plt.subplots(figsize=(10,6))

    ax.barh(top['short_title'], top['score'])
    ax.set_title("Top 10 Stories by Score")
    ax.set_xlabel("Score")
    ax.set_ylabel("Story Title")
    ax.invert_yaxis()

    return ax

#Function to plot categories and it's count
def plot_categories(df, ax=None):
    counts = df['category'].value_counts()
    colors = plt.cm.tab10(range(len(counts)))

    if ax is None:
        fig, ax = plt.subplots(figsize=(10,6))

    ax.bar(counts.index, counts.values, color=colors)
    ax.set_title("Stories per Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Count")

    return ax

#Function to plot scatter between score and comments.
def plot_scatter(df, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(10,6))

    sb.scatterplot(
        data=df,
        x='score',
        y='num_comments',
        hue='is_popular',
        ax=ax
    )

    ax.set_title("Score vs Comments")
    ax.set_xlabel("Score")
    ax.set_ylabel("Comments")

    return ax


plot_top_stories(trendsData)
plt.savefig(r"D:\Veena\Certificate Program in Artificial Intelligence and Machine Learning\Certificate-Program-in-AIML-IIT-Patna\MODULE 1 - FOUNDATIONS OF DATA\Module1 - MiniProject - Trend Pulse\data\outputs\chart1_top_stories.png", bbox_inches='tight')
plt.show()

plot_categories(trendsData)
plt.savefig(r"D:\Veena\Certificate Program in Artificial Intelligence and Machine Learning\Certificate-Program-in-AIML-IIT-Patna\MODULE 1 - FOUNDATIONS OF DATA\Module1 - MiniProject - Trend Pulse\data\outputs\chart2_categories.png", bbox_inches='tight')
plt.show()

plot_scatter(trendsData)
plt.savefig(r"D:\Veena\Certificate Program in Artificial Intelligence and Machine Learning\Certificate-Program-in-AIML-IIT-Patna\MODULE 1 - FOUNDATIONS OF DATA\Module1 - MiniProject - Trend Pulse\data\outputs\chart3_scatter.png", bbox_inches='tight')
plt.show()

#Saving the entire dashboard.
fig, axes = plt.subplots(1, 3, figsize=(20,6))

plot_top_stories(trendsData, ax=axes[0])
plot_categories(trendsData, ax=axes[1])
plot_scatter(trendsData, ax=axes[2])

fig.suptitle("TrendPulse Dashboard", fontsize=16)

plt.tight_layout(rect=[0,0,1,0.95])

plt.savefig(r"D:\Veena\Certificate Program in Artificial Intelligence and Machine Learning\Certificate-Program-in-AIML-IIT-Patna\MODULE 1 - FOUNDATIONS OF DATA\Module1 - MiniProject - Trend Pulse\data\outputs\dashboard.png", bbox_inches='tight')
plt.show()