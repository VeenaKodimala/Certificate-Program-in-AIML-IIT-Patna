## CLUSTURING
- Until now we have used many alogo's like Linear reg, logistic reg,Decision tree, random forest etc. All of them depend on a target column, i.e, the main job of those algo's is to find the target column value. hat if the target column doesn;t exists???  These also's are useless. That is when **Clusturing** comes into pic.
- Grouping the data into categories is known as ***Clusturing***.
- ![alt text](image.png)
- Generally clusturing means, the dataset will not be labelled, that is the reason "Clusturing" is under ***Unsupervised Learning***.
- Now, some of the common problems taht clustering solves are:
   - New articles, unlabelled, will be clustured together like: sports, crime, health etc.
   - Movie lovers: action, crime, mystery etc.
   - Participant iof ecommerce websites and their behaviour.
# Clustering Model Evaluation

Unlike classification, clustering is an **unsupervised learning** technique, meaning there are **no true labels** to compare against. Therefore, we evaluate clustering by checking how well the data has been grouped rather than measuring prediction accuracy.

---

# Questions Asked During Clustering Evaluation

## 1. Are the clusters well separated?

### Question
> Are different clusters far away from each other?

A good clustering algorithm should create clusters that are **distinct** and **do not overlap much**. This is known as **Inter-cluster distance**.

### Good Example

```
● ● ● ● ●


          ▲ ▲ ▲ ▲ ▲
```

### Poor Example

```
● ▲ ● ▲ ▲ ● ▲ ●
```

Here, the clusters overlap significantly, making them difficult to distinguish.

---

## 2. Are the points within the same cluster similar?

### Question
> Are members of the same cluster close to each other?

A good cluster should contain data points that are highly similar.

### Good Example

```
Cluster A (Age)

23
24
22
25
24
```

All members are very similar.

### Poor Example

```
Cluster A (Age)

20
65
38
80
12
```

The members vary widely, indicating poor clustering.

This property is known as **high intra-cluster similarity (or cohesion).**

---

## 3. Does every point belong to the appropriate cluster?

### Question
> Does this point really belong with the other points in the cluster?

Although we usually don't have labels, we can often inspect whether a point logically fits into its assigned cluster.

Example:

```
Dog
Dog
Dog
Cat
Dog
```

The "Cat" appears to be incorrectly grouped with dogs.

---

## 4. Is the chosen number of clusters appropriate?

### Question
> How many clusters should the algorithm create?

For example, when clustering customers:

Should there be:

```
2 clusters?
```

or

```
5 clusters?
```

or

```
20 clusters?
```

There is usually no single correct answer.

Common techniques for choosing the number of clusters include:

- Elbow Method
- Silhouette Score

---

## 5. Are the clusters meaningful?

### Question
> Can humans interpret these clusters?

Example of meaningful clusters:

```
Cluster 1
---------
Students
Young
Low income

Cluster 2
---------
Working professionals

Cluster 3
---------
Retired customers
```

These clusters are easy to understand and useful for business decisions.

If each cluster contains a random mixture of different customer types, the clustering may not be useful.

---

## 6. Are there any outliers?

### Question
> Are there points that don't belong to any cluster?

Example:

```
● ● ● ● ●

▲ ▲ ▲ ▲ ▲


                 ★
```

The star is far away from every cluster.

This could indicate:

- Fraud
- An anomaly
- Incorrect data
- A rare event

---

## 7. Are the clusters stable?

### Question
> Will the algorithm produce similar clusters if we rerun it?

Run 1

```
Cluster A
A B C D

Cluster B
E F G H
```

Run 2

```
Cluster A
A B D

Cluster B
C E F G H
```

If the clustering changes drastically with small changes in the data, it may not be reliable.

---

# Common Clustering Evaluation Metrics

| Metric | Measures | Better Value |
|----------|----------|--------------|
| **Silhouette Score** | Balance between cluster cohesion and separation | Higher (Range: -1 to 1) |
| **Inertia (WCSS)** | Sum of squared distances of points from their cluster centroid | Lower |
| **Elbow Method** | Helps determine the optimal number of clusters | Look for the "elbow" point |
| **Davies-Bouldin Index** | Ratio of within-cluster similarity to between-cluster separation | Lower |
| **Calinski-Harabasz Index** | Ratio of between-cluster dispersion to within-cluster dispersion | Higher |

---

# If True Labels Are Available

Sometimes clustering is performed on a labeled dataset to compare the discovered clusters with the actual classes.

In such cases, the following metrics can be used:

- Adjusted Rand Index (ARI)
- Normalized Mutual Information (NMI)
- Homogeneity
- Completeness
- V-Measure

These compare the generated clusters against the true labels.

---

# Interview Summary

When asked **"How do you evaluate a clustering model?"**, the expected points are:

1. **Are points within the same cluster close together?** (High Cohesion)
2. **Are different clusters well separated?** (High Separation)
3. **Is the chosen number of clusters appropriate?**
4. **Are the clusters stable across multiple runs?**
5. **Are the clusters meaningful and useful from a business perspective?**

---

# Key Takeaway

A good clustering model should have:

- ✅ High intra-cluster similarity (high cohesion)
- ✅ High inter-cluster separation
- ✅ Appropriate number of clusters
- ✅ Stable results
- ✅ Meaningful and interpretable clusters
--------------------------------------------------------

![alt text](image-1.png)
- The clustured marked, is our target, to find them. The also we are going to use is ***K-MEANS CLUSTURING ALGO***
- **STEP-1: Pick random points from the dataset as initial centroids.** 
![alt text](image-2.png)
- **STEP-2: Calculate distance from the above picked cenroids to every data points**
![alt text](image-3.png)
![alt text](image-5.png)
- **STEP-3: Calculate the new centroids, from the obtained initial level clusters.**
![alt text](image-6.png)
- **STEP-4: Now with the new centroids, calculate the distance to every data point**
![alt text](image-7.png)
- **Repeat the steps from 3 to 4, until we get the same clustures in different iterations, i.e , the same data points going into same clustures, as their prev. iterations. When this happens, then it means that the algo has "Converged".**
- **So, basically, this process repeats until the centroids and clustures are same, i.e, until "Convergence" is attained.**
![alt text](image-8.png)

## Biggest question - How to decide the k(No.of clustures to consider)
- Here, "K" is a hyper-parameter.
- By tuning this hyper parameter and calculating inter(distance b/w centroids of clusters) and intra(distance between centroid and points in a cluster) cluster, the 
"Silhouette Score" is calculated. This will tell us how efficent is the clusturing done by our model. Higher the score, best is the clusturing.
- Scaling has to be done, inorder to give equal imp to all features.
----------------------------------------------------------
![alt text](image-9.png)
------------------CALCULATION OF SILHOUETTE SCORE(WITH EXAMPLE)------------------------