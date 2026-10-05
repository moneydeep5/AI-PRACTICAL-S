# Ethics and Explainability Report — MoodLens AI

## 1. Project Overview

MoodLens AI is a mini natural language processing application created for educational demonstration. A user enters a short text statement and the system predicts one of three classes: **Positive, Negative, or Neutral**.

The application uses Python and Flask for the backend and standard HTML, CSS, and JavaScript for the interface. The classifier is a small Naive Bayes model implemented directly in Python. This design avoids external model downloads and makes the algorithm easy to inspect.

## 2. Why Explainability Matters

An AI prediction can influence how a user interprets a piece of text. Showing only a label such as "negative" gives little insight into how the system reached the result. MoodLens therefore exposes the words that contribute strongly to the class probabilities.

This supports three goals:

1. **Transparency:** the user can inspect which words influenced the result.
2. **Debugging:** a developer can identify obvious classification errors.
3. **Human oversight:** the user is reminded that the model is an aid, not an authority.

## 3. Model Explainability Approach

The classifier calculates a score for each class using the Naive Bayes idea:

`score(class) = log P(class) + sum(log P(word | class))`

Laplace smoothing is used so that unseen words do not cause zero probabilities.

For the explanation, each known input word is compared across the class-specific word probabilities. Words with a larger difference between classes are displayed as stronger evidence.

This is a useful **local explanation** because it refers to the current input. It should not be interpreted as a complete causal explanation of the model's reasoning.

## 4. Ethical Considerations

### 4.1 Bias

The dataset is small, handcrafted, and not representative of all users or writing styles. This can introduce systematic errors. For example, slang, dialects, culturally specific expressions, sarcasm, and mixed-language text may not be handled well.

**Mitigation:** expand the training data, test on diverse examples, report class-wise performance, and avoid claiming that the model is universally accurate.

### 4.2 Privacy

The demo processes input locally and does not intentionally store user text. Nevertheless, any real deployment should define data retention, logging, access control, and deletion practices.

**Mitigation:** minimize stored data, avoid sensitive text collection, and document how user input is handled.

### 4.3 Human Oversight

A confidence percentage can look more certain than it really is. Confidence is based on the model and dataset, not on truth.

**Mitigation:** keep a human reviewer in the loop for meaningful decisions and display clear limitations.

### 4.4 Appropriate Use

This prototype should not be used to make high-impact decisions such as hiring, admissions, medical diagnosis, insurance, credit, policing, or disciplinary decisions.

The system is intended for learning, prototyping, and low-risk text analysis.

### 4.5 Accuracy and Evaluation

The demo dataset is intentionally small to keep the source code understandable. Therefore, the application should not be presented as a production-grade sentiment model.

**Mitigation:** use a larger held-out test set, measure accuracy, precision, recall, and F1-score, and inspect false positives and false negatives.

## 5. Limitations of Explainability

The visible evidence words are correlated signals learned from the training examples. They do not prove that a word is the true cause of the sentiment. Language depends on context, negation, sarcasm, grammar, and world knowledge.

Example: a sentence containing the word "great" can still be negative in a sarcastic context. The present model does not fully understand such context.

## 6. Responsible AI Conclusion

MoodLens AI demonstrates a basic responsible-AI principle: an NLP system should communicate both its prediction and its limitations. Explainability improves transparency, while ethical safeguards prevent users from treating a small educational model as an objective decision maker.

For a college mini project, the recommended scope is **educational demonstration only**, with manual review of important outputs.
