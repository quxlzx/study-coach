Decision Trees:: What is a decision tree in ML? :: A supervised learning algorithm that makes predictions by asking a sequence of questions (feature tests), like a flowchart; used for both classification and regression
Decision Trees:: Root node vs internal node vs leaf node :: Root = top starting decision node with no incoming branches; internal node tests a feature and splits into branches; leaf = terminal node with the final prediction and no further splits
Decision Trees:: What are layer and depth in a tree? :: Layer = nodes at the same depth from the root; depth = maximum number of layers from root to the farthest leaf
Decision Trees:: What is a binary decision tree? :: A decision tree in which every node has exactly two branches
Decision Trees:: Classification tree vs regression tree output :: Classification tree outputs a discrete category (Yes/No, Cat/Dog); regression tree predicts a continuous numerical value (house price, temperature)
Decision Trees:: What does each root-to-leaf path represent? :: An IF-THEN decision rule; the whole tree is a set of such rules (a logical predicate)
Decision Trees:: Tennis dataset setup (Mitchell example) :: 14 examples, 4 categorical features (Outlook, Temp, Humidity, Wind), binary target Play vs No-Play
Decision Trees:: How does ID3 grow the tree (divide and conquer)? :: Pick the best feature at the root, then recursively split each child to get purer subsets; iterate choosing the highest-IG feature at each node
Decision Trees:: Pure node vs impure node :: Pure = all (or majority) samples one class, no further splitting needed; impure = mixed classes, requires further splitting (e.g. Sunny and Rain in tennis, Overcast is pure)
Decision Trees:: Entropy formula :: H(S) = - sum p_i * log2(p_i), where p_i is the proportion of class i; 0*log2(0) is treated as 0
Decision Trees:: Entropy values: pure vs maximally mixed :: H = 0 for a pure node (zero uncertainty); H = 1 for a 50/50 binary split (maximum impurity); higher entropy = greater uncertainty
Decision Trees:: Information gain formula :: IG = Entropy(before) - weighted Entropy(after) over the branches; higher IG = greater impurity reduction = better split
Decision Trees:: Tennis root split numbers :: S = [9+,5-] has H = 0.940; IG(S,outlook) = 0.246, IG(S,humidity) = 0.151, IG(S,temp) = 0.029, IG(S,wind) = 0.048 -> outlook chosen as root
Decision Trees:: Tennis level-2 splits :: Sunny subset picks Humidity (gain 0.970 > temp 0.570 > wind 0.019); Overcast is pure (4+/0-) so it stops at Yes; Rain subset picks Wind
Decision Trees:: Rule about reusing features when growing a tree :: If a feature has already been tested along a path, do not consider it again deeper on that path
Decision Trees:: Final tennis tree :: Outlook -> Sunny: Humidity (High=No, Normal=Yes); Overcast: Yes; Rain: Wind (Weak=Yes, Strong=No)
Decision Trees:: Boolean representation of a decision tree :: Each path is an AND (conjunction) of tests; the whole tree is an OR of AND rules; trees can represent ANY boolean function (AND, OR, XOR), though some need exponentially large trees
Decision Trees:: Why prefer simpler trees? :: Occam's razor: fewer splits give better generalization and human-interpretable rules
Decision Trees:: Continuous features in a decision tree :: Internal nodes test a continuous feature against a threshold (e.g. age > 30), creating two branches
Decision Trees:: What causes decision tree overfitting? :: The tree grows very deep with extra splits to fit noisy or coincidental training examples (e.g. noisy D15), memorizing the training set and generalizing poorly
Decision Trees:: When to stop splitting? :: Node sufficiently pure, too few samples, max depth reached, little improvement from extra splits, or validation performance says so
Decision Trees:: Prediction at an impure leaf :: Predict the probability of each class (e.g. p(green) = 80%) or simply the majority label
Decision Trees:: Pre-pruning vs post-pruning :: Pre-pruning stops the tree from growing too much (depth limit, min samples); post-pruning grows the full tree first, then removes unnecessary branches
Decision Trees:: How to decide what to prune? :: Use a separate validation set; prefer the simpler tree when added complexity does not improve validation performance
Decision Trees:: sklearn decision tree with overfitting control :: DecisionTreeClassifier(max_depth=4); controlling depth prevents overfitting and yields a simpler tree
