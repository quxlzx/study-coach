Naive Bayes:: Core idea and the "naive" assumption :: Probabilistic classifier from Bayes theorem assuming all features are conditionally independent given the class label
Naive Bayes:: Final decision rule (MAP) :: Predict the class y that maximizes P(y) * product of P(x_i | y); the denominator P(X) is dropped because it is constant for all classes
Naive Bayes:: Four assumptions of Naive Bayes :: 1) feature independence given class, 2) all features contribute equally, 3) continuous attributes are Gaussian within each class, 4) no missing data
Naive Bayes:: Why is Naive Bayes popular for text / NLP? :: Text has high dimensionality with each word as a feature; used for spam filtering and sentiment analysis
Naive Bayes:: Sports text example priors :: With 5 documents (3 Sports, 2 Non-Sports): P(Sports) = 3/5, P(Non-Sports) = 2/5
Naive Bayes:: What breaks when a word never appears in a class? :: Its likelihood is 0, and one zero factor makes the entire product 0, killing that class regardless of other evidence
Naive Bayes:: Laplace (additive) smoothing formula :: P(word | class) = (count + alpha) / (total + V) with alpha usually 1 and V = number of unique words; every word gets a non-zero probability
Naive Bayes:: Laplace example value :: If 'close' appears 0 times in 9 Non-Sports words and V = 14: P(close | Non) = (0+1)/(9+14) = 1/23
SVM:: What does an SVM search for? :: The optimal hyperplane in N-dimensional feature space that separates classes with the maximum margin; used for classification and regression
SVM:: Support vectors :: The data points closest to the hyperplane; they define and influence its position and orientation, and removing them could change the boundary
SVM:: Margin definition and why maximize it :: Margin = distance between the hyperplane and the nearest support vectors; a larger margin is a wider buffer zone, giving better generalization and robustness to noise
SVM:: Decision boundary equation :: w*x + b = 0; SVM chooses w and b to maximize the margin
SVM:: What is a hyperplane? :: A flat surface one dimension lower than the feature space: a line (y = mx + b) in 2D, a plane (x + 3y - 2z = 5) in 3D
SVM:: SVM loss function :: Hinge loss, which measures how far a data point is from being correctly classified and drives margin maximization (labels y = +1 or -1)
SVM:: Kernel trick :: Maps data to a higher-dimensional space where it becomes linearly separable; kernel functions compute inner products in that space directly, without computing the mapping, so it stays fast and scalable
SVM:: Kernel trick 1D example :: Points on a line that no single cut can separate become separable by lifting with y = x^2 (a horizontal line then splits them)
Multiclass:: One-vs-all strategy :: Train one classifier per class (class vs everything else): n models for n classes; the highest-scoring classifier wins
Multiclass:: One-vs-one strategy :: Train a classifier for every pair of classes: n(n-1)/2 models for n classes; majority of pairwise votes decides
Overfitting:: KNN overfit vs underfit in terms of k :: k = 1 memorizes training data and is hypersensitive to noise (overfitting, high variance); k = N uses everyone, misses local patterns (underfitting, high bias)
Overfitting:: Why are decision trees prone to overfitting? :: They use every scrap of information and can memorize the entire training set with over-complex trees that generalize poorly
Overfitting:: Fixes for decision tree overfitting :: Depth limit / early stopping, pruning (chop branches below a level), tuning hyperparameters on the test set, or ensembles of trees (random forests)
Ensembles:: Bagging (bootstrap aggregating) steps :: Create bootstrap samples with replacement, train a model on each, then aggregate by majority vote / averaging; reduces variance and overfitting
Ensembles:: Random Forest key steps :: Bootstrap sampling (left-out samples = OOB), build a tree per sample using random feature subsets for splits for diversity, then majority vote (classification) or average (regression); N trees is a hyperparameter
Ensembles:: Boosting vs bagging :: Boosting trains weak models sequentially, each focusing on previous mistakes (weight adjustment) with weighted voting; it reduces bias, while bagging reduces variance
Ensembles:: Examples of boosting algorithms :: AdaBoost, Gradient Boosting Machines (GBM), XGBoost, LightGBM
Model Eval:: Fair model comparison practice :: Put all candidate classifiers in a dict, fit/predict each on identical train/test splits, and report the same metrics (accuracy, macro F1); always use a held-out set or cross-validation
