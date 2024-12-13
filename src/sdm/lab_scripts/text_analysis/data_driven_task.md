**(gpt summary for easy copy into jupyter)**
# Part 1: Long Texts

## Task 1.1: Actor-level Data
- Create a dataset with concatenated tweets for each top producer account.
- Use a sample if texts are long.
- Ensure texts are long enough for LDA analysis.

## Task 1.2: Pre-processing
- Apply pre-processing to the data, creating a list of tokens for topic modeling.
- Write a reusable function for tokenization.
- Refer to relevant papers for guidance.

## Task 1.3: LDA (Default)
- Run LDA with learned priors (alpha, eta).
- Choose an appropriate number of topics (K).
- Inspect topics and check if they make sense.

## Task 1.4: Evaluation
- Evaluate inferred topics via blind evaluations:
  - Identify intruders.
  - Relate sampled texts to topics.
- Reflect on the evaluation process.
1. **First Task (Repeated N times):**
   - Randomly select a topic (z).
   - Randomly sample S units related to topic z (try S = 2).
   - Randomly sample 1 unit not related to topic z.
   - Shuffle the S+1 units and identify the intruder (the one not related to topic z).
   - You can adjust S if needed.

2. **Second Task (Repeated N times):**
   - Randomly select a topic (z).
   - Randomly sample S units related to topic z (try S = 1).
   - Based on the sampled units and descriptions of topics, try to identify the topic (z). 


## Task 1.5: Comparison of Different Runs
- Run LDA multiple times and check topic consistency.
- Optionally, automate result comparison.

## Task 1.6: Effect of Parameters
- Vary alpha and beta priors and observe changes in results.
- Compare with asymmetric alpha to see impact.

## Task 1.7: Learning Similarity Functions
- Run LDA with different K values.
- Rate pairs of units for similarity.
- Assess how parameter changes affect the results.

## Task 1.8: Empirical Analysis: Topics & Producers
- Analyze the relationship between account features (e.g., type, stance) and topics using your best model.


# Part 2: Short Texts

## Task 2.1: Tweet-level Data
- Sample tweets from top producers for analysis.
- Choose a sampling strategy to investigate different research questions.

## Task 2.2: Pre-processing
- Reapply or adjust pre-processing steps for tweet-level data.
- Consider shorter text lengths when pre-processing.

## Task 2.3: LDA (Baseline)
- Run LDA on tweet-level data for a baseline comparison.

## Task 2.4: BTM
- Use BTM to compute topics.
- Compare the results with LDA (e.g., speed, topic quality).

## Task 2.5: Embeddings
- Use BERT embeddings to cluster tweets.
- Evaluate the clusters' quality.
- Compare the results to generative models.

## Task 2.6: Explanation
- Quantify clusters using TF-IDF.
- Identify top terms for each cluster.
- Reflect on how the clusters match or alter your understanding of topics.
