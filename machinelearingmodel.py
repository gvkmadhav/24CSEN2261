#chatgpt
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MachineLearningModel:
    def __init__(self):
        self.data = load_iris()
        self.X = self.data.data
        self.y = self.data.target
        self.model = RandomForestClassifier(n_estimators=100)
    
    def train_and_evaluate(self):
        """Train the model and evaluate using cross-validation."""
        logging.info("Training the model...")
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=42)
        
        self.model.fit(X_train, y_train)
        logging.info("Model trained successfully.")
        
        # Evaluate model using cross-validation
        scores = cross_val_score(self.model, self.X, self.y, cv=5)
        logging.info(f"Cross-validation scores: {scores}")
        logging.info(f"Mean cross-validation score: {scores.mean()}")

        # Predictions and evaluation
        y_pred = self.model.predict(X_test)
        logging.info(f"Classification report:\n{classification_report(y_test, y_pred)}")
        logging.info(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
        
        # Plotting feature importance
        self.plot_feature_importance()

    def plot_feature_importance(self):
        """Plot feature importance using a bar chart."""
        feature_importance = self.model.feature_importances_
        feature_names = self.data.feature_names
        
        plt.barh(feature_names, feature_importance)
        plt.xlabel("Feature Importance")
        plt.title("Feature Importance in RandomForest Classifier")
        plt.show()

# Example usage
def main():
    ml_model = MachineLearningModel()
    ml_model.train_and_evaluate()

if __name__ == "__main__":
    main()
