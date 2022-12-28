import re
import math

class NaiveBayesClassifier:
    def __init__(self, alpha):
        self.alpha = alpha

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        self.all, self.good, self.maybe, self.never = {}, {}, {}, {}
        for i in range(len(X)):
            for w in re.sub(r'[^\w\s]', '', X[i]).lower().split():
                w = w.strip()
                self.all[w] = self.all.get(w, 0) + 1
                if y[i] == "good":
                    self.good[w] = self.good.get(w, 0) + 1
                elif y[i] == "maybe":
                    self.maybe[w] = self.maybe.get(w, 0) + 1
                elif y[i] == "never":
                    self.never[w] = self.never.get(w, 0) + 1

    def predict(self, X):
        m = []
        for s in X:
            good = maybe = never = math.log(1/3)
            for i in s.split():
                denominator = self.all.get(i, 0) + self.alpha * len(self.all)
                good += math.log((self.good.get(i, 0) + self.alpha) / denominator)
                maybe += math.log((self.maybe.get(i, 0) + self.alpha) / denominator)
                never += math.log((self.never.get(i, 0) + self.alpha) / denominator)
            v = {'good': good, 'maybe': maybe, 'never': never}
            m.append(max(v, key=v.get))
        return m

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        x = 0
        m = self.predict(X_test)
        for i in range(len(X_test)):
            x += m[i] == y_test[i]
        return x / len(X_test)
