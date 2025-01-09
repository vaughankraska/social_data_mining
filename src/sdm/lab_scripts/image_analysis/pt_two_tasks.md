## PART II Summary

### Task Overview
In this task, you are required to assign identifiers to images, grouping analytically equivalent images under the same identifier. Analytically equivalent images share the same base content but may differ slightly in presentation, such as cropping, resizing, or minor modifications (e.g., text changes in an image).

### Key Questions
1. **Definition of Analytically Equivalent**: 
   - What criteria define images as analytically equivalent for your analysis?
2. **Computational Capturing of Definition**: 
   - How can you implement this definition in a computational model? Consider the balance between definition accuracy and the amount of manual post-processing needed.

### TASK 2.1: ID Assignment
- Assign IDs to images using an appropriate method so that all analytically equivalent images receive the same ID.

### Tips for ID Assignment Methods
- **Perceptual Hashing**: A technique that generates a hash value based on the image's visual content, which can be used to identify visually similar images.
- **Feature Vectors**: Compute feature vectors (e.g., color histograms) for each image and use these vectors to define similarity.
- **Image Embeddings**: Re-use embeddings to cluster images, but only consider images with highly similar embeddings as nearly equivalent.
- **Additional Methods**: Feel free to explore and apply other methods to determine image equivalence.

### Threshold Justification
- A crucial part of the task is identifying and justifying a threshold for considering two images as analytically equivalent.

## PART III: Analysis

### Objective
Analyze the diffusion of grouped images online by selecting one cluster (from Part I) and one group of nearly-identical images (from Part II).

### Analytical Angles
You can explore various aspects such as:
- **Temporal Patterns**: Examine the timing of image posts, looking for trends or peaks.
- **Spreading**: Analyze both the initial postings and subsequent sharing (e.g., retweets).
- **Account Types**: Investigate if different types of accounts posted the images or if they were confined to specific profiles.
- **Reactions and Metadata**: Study how reactions (e.g., likes) correlate with image metadata and the account types that posted the images.


### OG text
```txt
PART II

For this second task, you should assign an identifier to the images, where images that are analytically equivalent receive the same identifier. Analytically equivalent means that they do not need to be equal pixel-by-pixel, but can be considered equivalent wrt the objective of your analysis. For example, two versions of the same image cropped in different ways, or two different images depicting exactly the same scene, could be considered equivalent if you want to study how that specific image has spread online. Here we focus on nearly-equivalent images: the same base image, including small modifications of it (e.g. resizing, or changing a small part of it, such as the text written in a sign held by a protester).

In summary, this part of the lab has two underlying questions you should think about:

What is your definition of analytically equivalent?
How can that definition be captured computationally?
The two questions are not independent: you may need to adjust your definition if you want it to be able to capture it computationally. The definition also affects the amount of manual work (e.g. post-processing to filter out wrong results) that is needed in the computational analysis.

TASK 2.1: ID assignment

Assign IDs to all images choosing an appropriate method, so that all analytically equivalent images get the same ID.

Tips:

Choose at least one method to pass this lab. You are however encouraged to use and compare multiple approaches. Some possibilities:
One option is to use perceptual hashing.
A second option is to compute a feature vector from each image (e.g. its colour histogram) and use the vectors to define image similarity.
A third option is to re-use the embeddings, but differently from Task 1.3 only include images in the same cluster when their embeddings are so close that the images are (nearly) equivalent.
You can think of additional methods if you want.  
If you haven't worked with this type of task before, you can start hereLinks to an external site..
A core part of this task is to identify and justify a threshold to consider two images to be analytically equivalent.

PART III: Analysis

In the previous two parts of the lab, you have grouped images, first broadly (in clusters/topics) then in a more fine-grained way. For this last task, pick one of the groupings from each of the two parts (that is, a cluster of your interest, and a group of nearly-identical images) and look at how these two groups diffused online. 

Tips: Feel free to choose the analytical angle you prefer. For example,

you can look at temporal patterns of production (was this posted equally during the event, or had any picks?),
you can look at spreading (that is, not just production, but also including retweets),
you can look at if it has been posted by different types of accounts or only by specific profiles,
you can look at how reactions to these images (e.g. likes) associate to the metadata, for example if they get more or less reactions when they are posted by different account types.
```
