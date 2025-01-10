# Feedback (Matteo)

Data and descriptive analysis: ok. What I will be interested in hearing at the presentation is the "why". Different platform affordances lead to different ways in which they are used - that, I believe. So what? This is a difficult question, and one that is often not even answered in the "technical social data science literature". But from the three of you, I have high expectations, so I encourage you to put some time into discussing this and using some time during your presentation to convince me that this analysis, if fully performed and validated, would be well-spent time. Some guiding questions (to choose from): Is there anything useful that your results would enable you to do? Is there anything that clashes with the expectations that you have, based on your knowledge of the platforms? Does your analysis tell you anything about human behaviour that is not about these two platforms?
TODO:
So what? Platforms are different and they are used differently but the interesting thing is how they are inter-related (bridge between platforms). 
What could we do/so what? We can model the differences between the platforms and how they are affectively used.
- Take out twitter specifict lingo hashtags etc and rerun the emebddings
- Use mixing proportions as measurement of similartiy within clusters.
- Expore the results more and what drives the clustering in order to answer these questions more in-depth
- LIMITATIONS


Regarding the method: (1) the way in which you operationalise the concept of "discussion" can significantly influence your results. To the point where you can probably control how fragmented your conversations are by changing way of measuring them. This is a crucial point, closely connected to the discussion we had about modelling and validity - I expect this to be a core discussion point for a higher grade.
TODO:
On twitter there is literally "reply" and on reddit that same functionality exists in comments reply to comment.
- We will defend this and compare reply networks
- Revisit slide on modelling and validity
- LIMITATIONS

Item 2 (Thematic Divergence) sounds very ambitious, please consider that you are not judged on how good your results are (there is too little time to do a complete analysis), but on your research design: make sure to show that you have the limitations of the study under control, and feel free to suggest things that you could do but you did not have time to do - this is the second requirement for higher grades.
TODO:
- Do limitations on all points.

Same thing about item 3. In summary: (-) present a good a design for the study, then (-) do what you can of it, or do something slightly simplified pointing out what the consequences of your simplifications are. This is what I'm going to look for.
TODO:
- Interop of account types that have twweets recurring on reddit as well.
- LIMITATIONS

- **Data and Descriptive Analysis**: 
  - **Key Interest**: Emphasis on the "why" behind the analysis.
  
- **Platform Affordances and Usage**:
  - **Belief**: Different platforms afford different usages.
  - **Critical Question**: So what? 
  - **Challenge**: Addressing this question is difficult and often unaddressed in technical social data science literature.
  - **Expectation**: High expectations for a thorough discussion on this topic.
  - **Presentation Focus**: 
    - Use time to convince the audience that the analysis is valuable if fully performed and validated.
  - Key Differences in the platform:
    - Reddit: Long form responses on topics, more ananymous, less PR/Companies ie more individual opinions.
    - Twitter: Short blurbs, memes and very public facing.
  
- **Guiding Questions** (to explore):
  - **Utility**: Is there anything useful that your results would enable you to do?
    - 
  - **Expectations vs. Reality**: Is there anything that clashes with your expectations based on platform knowledge?
  - **Broader Insights**: Does your analysis reveal anything about human behavior beyond these two platforms?
  
- **Method**:
  - **Operationalization of "Discussion"**:
    - **Impact**: The method of operationalizing "discussion" can significantly influence results.
    - **Control**: It is possible to control conversation fragmentation through measurement methods.
    - **Core Discussion**: Important for modelling and validity, essential for achieving a higher grade.
  
- **Ambition and Results**:
  - **Ambition Level**: Acknowledge that item 2 sounds ambitious.
  - **Evaluation Criteria**: 
    - **Focus**: Research design is more critical than the quality of results due to time constraints.
    - **Study Limitations**: Show control over study limitations and suggest unperformed actions due to time constraints.
  - **Higher Grade Requirement**: 
    - Demonstrate awareness of study limitations and potential actions.
  
- **Summary**:
  - **Study Design**: Present a well-structured design.
  - **Execution**: 
    - Execute what is feasible or a simplified version.
    - Highlight consequences of simplifications.
  - **Evaluation Focus**: The evaluation will focus on the study design and understanding of limitations.


My scratch queries:
avg distance of groups
```sql
WITH v1 AS (
    SELECT id, embedding
    FROM embeddings
    WHERE doc_type = 'tweet'
),
v2 AS (
    SELECT id, embedding
    FROM embeddings
    WHERE doc_type = 'submission'
)
SELECT avg(v1.embedding <-> v2.embedding) AS avg_distance
FROM v1, v2
WHERE v1.id != v2.id;
```
select embeddings with account type

