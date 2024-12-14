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

_Full Remaining Text (for plane ride)_
```txt
#TASK 1.5: Comparison of different runs

For this task, you just have to run LDA on your data two/three times, with the same data and parameters, and check the stability of the results, that is, check if LDA finds the same topics. Notice that two topics can be evaluated to be the same even if the word probabilities are not identical. You can perform the comparison of the different results manually, or (if you are more ambitious) you can write code to automatically and quantitatively compare the results. (Especially) if you perform a manual comparison, use a small K.

#TASK 1.6: Effect of parameters

Now you will try to replicate some of the observations by Wallach, H., Mimno, D., & McCallum, A. (2009) in their paper: Rethinking LDA: Why Priors Matter

Links to an external site.Öppna detta dokument med ReadSpeaker docReader . Advances in Neural Information Processing Systems, 22. This was an important paper, that raised awareness about the role of the hyper-parameters, explaining their effects and providing recommendations. At the same time, results found in research papers are sometimes stronger than what one would experience in real cases, for various reasons. Let's see what you can observe.

First, look at the default values parameters for Alpha and Beta used by the library. Using again a small K (to allow manual inspection), produce four results using symmetrical Dirichlet distributions both for Alpha and Beta: with low and high values of Beta, and with low and high values of Alpha. Being a symmetric distribution, both Alpha and Beta are scalars, you only need to provide a single number. Also, you may have removed stop words in your previous tasks - if yes, we suggest to keep them for this, because a good setting for the priors is supposed to take care of stop words.

Can you see any difference in the results, varying Alpha and Beta?

Then, pick one of the four executions and run it again making Alpha asymmetric. Can you see any difference in the results?

Here you find a summary of the expectations from the paper, left invisible so that you are not influenced while looking at your results - check them later! "[The best choice is to use] asymmetric prior over Θ and a symmetric prior over Φ. [...] The primary assumption underlying topic modeling is that a topic should capture semantically-related word co-occurrences. Topics must also be distinct in order to convey information: knowing only a few co-occurring words should be sufficient to resolve semantic ambiguities. A priori, we therefore do not expect that a particular topic’s distribution over words will be like that of any other topic. An asymmetric prior over Φ is therefore a bad idea: the base measure will reflect corpus-wide word usage statistics, and a priori, all topics will exhibit those statistics too. A symmetric prior over Φ only makes a prior statement (determined by the concentration parameter β) about whether topics will have more sparse or more uniform distributions over words, so the topics are free to be as distinct and specialized as is necessary. However, it is still necessary to account for power-law word usage. A natural way of doing this is to expect that certain groups of words will occur more frequently than others in every document in a given corpus. For example, the words “model,” “data,” and “algorithm” are likely to appear in every paper published in a machine learning conference."

#TASK 1.7:  Learning your similarity functions

For this last task with LDA, run the model with different values of K. Then randomly pick N pairs of units (without using any information about the results of the models) and rate them on a three-level scale (unrelated, somehow related, very related). Use this information to assess the different results.

As for Task 1.4, the objective is not to run a full validation, but: (1) To experience the complexity of this simple-sounding procedure. (2) To get a feeling about how differences in the parameters are captured in the quality of the results. (3) To adapt an evaluation protocol defined in a different context (in this case, to evaluate clusterings) to the more general mixed-membership case.

#TASK 1.8:  Empirical analysis: Topics & producers

To conclude this first part of the lab, choose at least one feature of the accounts (type and/or stance), choose your best model, and compute the association between account metadata and topics. Do you observe any differences, that is, topics that tend to be more frequent in some sub-populations?
```
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
