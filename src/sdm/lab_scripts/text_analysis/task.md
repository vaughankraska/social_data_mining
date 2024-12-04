## Text Analysis Lab (GPT Summary)

#### **Part I: Data Preparation**
1. **Task 1.1: Data Selection**
   - Extract tweets with metadata to define a research question.
   - Reflection: Filter unusable tweets.

2. **Task 1.2: Data Annotation**
   - Collaboratively annotate tweets (-1, 0, 1 for sentiment).
   - Reflection: Understand the importance of custom annotation vs. pre-trained datasets.

3. **Task 1.3: Dictionary Creation**
   - Build a shared sentiment dictionary from annotated tweets.

4. **Task 1.4: Reliability Test**
   - Use Krippendorff’s alpha to assess annotation reliability.
   - Resolve mismatches and consolidate annotations.

---

#### **Part II: Model Comparison & Validation**
1. **Task 2.1: Own Dictionary**
   - Use a custom dictionary for tweet annotation.

2. **Task 2.2: General Dictionary**
   - Employ VADER for sentiment analysis.

3. **Task 2.3: Machine Learning**
   - Train a classifier (e.g., Decision Trees, Naive Bayes) using bag-of-words features.

4. **Task 2.4: Transformer Model**
   - Apply a fine-tuned transformer model for sentiment analysis.

5. **Task 2.5: Comparison**
   - Compare all approaches using test and unlabelled data.
   - Optional: Fine-tune a transformer on training data.

---

#### **Part III: Hypothesis Testing**
- Formulate a hypothesis (e.g., activists use more negative sentiment) and test it using the selected data and best-performing model.

---

#### **Part IV: Scaling**
1. **Task 4.1: Data Selection**
   - Select tweets from two actor groups to define scale ends.

2. **Task 4.2: Word Scoring**
   - Identify and score distinctive words for each group.

3. **Task 4.3: Text Scoring**
   - Assign scores to account-level text and analyze patterns across groups.

