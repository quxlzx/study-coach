Unsupervised Learning:: What distinguishes unsupervised from supervised learning? :: Data comes with no predefined labels; algorithms discover hidden patterns or groupings without human intervention
Unsupervised Learning:: What is the main goal of unsupervised algorithms? :: Study the intrinsic hidden structure of data, segment it into similar groups, or simplify it
Applications:: Name the three main applications of clustering from the slides :: Cluster analysis (natural groupings), dimensionality reduction (aggregate similar variables), anomaly detection (find outliers)
Applications:: Give real-world examples of what can be clustered :: News articles by topic, protein sequences/genes by expression, social network users by interest, customers by purchase history
Clustering Objective:: What two distances does clustering optimize? :: Minimize intra-cluster distance (similar inside a group) and maximize inter-cluster distance (different across groups)
Clustering Algorithms:: List the four most common clustering algorithms :: K-Means, Hierarchical Clustering, DBSCAN, Gaussian Clustering Model (GMM)
K-Means:: K-Means algorithm steps? :: 1 choose K, 2 initialize K centroids randomly, 3 assign each point to nearest centroid, 4 re-compute each centroid as the average of its points, 5 repeat 3-4 until convergence
K-Means:: How are points assigned to clusters in K-Means? :: Compute the distance from each point to every centroid; each point joins the cluster with minimum distance to its centroid
K-Means:: How is a centroid re-initialized? :: New centroid = average of all data points in that cluster; for cluster Ci with Ni points, mi = mean of its points
K-Means:: K-Means convergence / stopping criteria? :: Centroids stop changing, points remain in the same cluster, or the maximum number of iterations is reached
Choosing K:: What goes wrong when K is too large or K = 1? :: K too large gives a cluster for every data point (defeats the purpose); K = 1 gives one big cluster for the whole dataset
Choosing K:: What indicates an ideal K? :: Clusters are distinct: distance from each point to its own cluster center is much smaller than the distance between different cluster centers
K-Means Objective:: What does K-Means minimize and what is it called? :: Total intra-cluster variance = Within-Cluster Sum of Squares (WCSS) = inertia: sum of squared distances of each point to its centroid
K-Means Objective:: K-Means assumptions? :: Every observation belongs to one of the K clusters, clusters do not overlap, variation within each cluster is minimized
Elbow Method:: How does the elbow method choose K? :: Plot WCSS vs K; it drops fast for small K then slows down - the bend (elbow) is the right K; alternative: silhouette score
K-Means Weakness:: Why can K-Means give a bad clustering? :: It starts randomly and can converge to a poor local minimum depending on the initial centroid placement
K-Means Fixes:: Three fixes for bad random initialization? :: Run K-Means 10-50 times with different seeds and keep lowest inertia; use K-Means++ which spreads initial centroids out to cover the space and reduce poor local minima; use Hierarchical or DBSCAN (no random centroids)
Hierarchical:: What is hierarchical clustering? :: Builds a hierarchy of clusters as a tree (dendrogram); does not require pre-specifying K
Hierarchical:: Agglomerative vs divisive? :: Agglomerative = bottom-up, each point starts as its own cluster and closest clusters merge step-by-step; divisive = top-down, start with one cluster and split recursively
Hierarchical:: Linkage methods? :: How distance between clusters is measured: single linkage (min), complete linkage (max), average linkage (mean)
DBSCAN:: What is DBSCAN and its key parameters? :: Density-based clustering that groups closely packed points, finds arbitrary-shaped clusters and noise; parameters: epsilon (neighborhood radius) and minPts (min points in an eps-neighborhood)
DBSCAN:: Core, border, and noise points? :: Core: has >= minPts neighbors within eps and expands clusters; Border: within eps of a core but too sparse to expand; Noise: neither - an isolated outlier
DBSCAN:: Why does DBSCAN need both core and border points? :: Core points grow dense clusters; border points smooth cluster edges and avoid abrupt cuts - together they find naturally shaped clusters
Hard vs Soft:: Hard vs soft clustering, and which algorithms are which? :: Hard: each point belongs to exactly one cluster (K-Means, Hierarchical, DBSCAN - flexible shape but still deterministic assignment); soft: points belong to multiple clusters with probabilities (Gaussian Mixture Models)
