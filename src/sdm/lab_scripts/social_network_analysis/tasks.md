# Lab 2 Tasks
## PART 1: Network exploration

### Task 1.1: read the Retweet and Reply networks produced during the first lab into two iGraph objects. For now, consider the networks undirected. This task should familiarise you with network file formats (please look at the documentation) and make sure you can import your own data

TIPS
have a look at iGraph's read() function.
use the summary() method/function to check if the networks have been loaded correctly.
use the simplify() method if you want to remove loops and edge duplicates.
# Task 1.2: produce a descriptive summary of the two networks, choosing the whole-network measures that you find useful to report, but including at least: order, size, number of components, density, clustering coefficient / transitivity, and a plot of the degree distribution.

TIPS:
you will have to produce such a summary multiple times, to compare different graphs. So consider writing a function taking a network as input and producing the summary.
for the plot with the degree distribution, consider using log-log axes.
# Task 1.3: produce a node-link plot for each of the two networks, to get a visual understanding of their structure.

TIPS:
compute the layout of each network only once, save them in some variables, and use them as parameters of the plotting function, so that you always get the same node positions (for comparability) and you also save time by not recomputing a new layout every time.
consider creating a 'color' attribute for vertices and edges, maybe setting a low alpha, e.g. g.es['color']="rgba(1,1,1,0.01)"
in the plot, you should use parameters to generate a readable visualisation. For example: remove the vertex contours (vertex_frame_width=0), remove the labels, set a good vertex_size and edge_width.
you can save the plots to file using the "target" parameter of iGraph's plot() function.

### Task 1.4: compute the degree of all nodes, and produce new plots so that the values are represented by vertex size.

TIPS:
 for now - use the vertex_size parameter - do not use node degree and betweenness directly as vertex sizes, but produce a new array where vertex sizes are computed as a function of the centrality measure, for example proportional to it.
# Task 1.5: Repeat Task 1.4 using betweenness centrality. Betweenness may take a few minutes to compute on the reply network, and too much time on the retweet network. Therefore, to perform this task design a function to approximately but quickly compute betwenness. Validate your betweenness function and use it for the plots (where needed). 

 # Task 1.6: extract the IDs of the 10 actors with the highest degree and highest betweenness, for both networks. How many of them do you think are in the list of top-producers? Check if your intuition was correct. For those in such list, do you see any patterns regarding their language, stance, and type? Are the two centrality measures complementary, or are they highlighting slightly different sets of most-central actors?

# Task 1.7: pick one of the networks and extract its largest component into a new network. Produce its summary as in Task 1.2. You will use this network for the rest of the lab.

TIPS:
look at the method: connected_components().
 

## PART 2: Models

### Task 2.1: produce three ER networks with the same order and adjacency probability as the Retweet network. Produce the same descriptive statistics as for the Retweet network and compare them. Then keep one of the generated networks to be used in PART 3.

TIPS:
differently from the network you have read from file, this and the next synthetic networks will have no 'name' attribute for its edges. You can add it if you want it, e.g. in case some of your functions use this attribute.
### Task 2.2: produce three BA networks with the same order and adjacency probability as the Retweet network. Produce the same descriptive statistics as for the Retweet network and compare them. Then keep one of the generated networks to be used in PART 3.

### Task 2.3: produce three WS networks with the same order and adjacency probability as the Retweet network. Set the rewiring probability so that the model has a similar average path length and clustering coefficient as the Retweet network. Produce the same descriptive statistics as for the Retweet network and compare them. Then keep one of the generated networks to be used in PART 3.

### Task 2.4: produce a new network, starting from the Retweet network, by rewiring all edges so that the degree distribution is approximately preserved. That is, when you process edge A--B, choose a vertex C with the same degree as B that is not adjacent to A, choose one of the neighbours of C (D), and replace the edges A--B and C--D with A--C and B--D. Produce the same descriptive statistics as for the Retweet network and compare them. Then keep the generated network to be used in PART 3.

TIPS:
iGraph provides functions to rewire the edges (but feel free to implement this function from scratch if you have time.
 

## PART 3: Processes on networks

### Task 3.1: Simulate a process where a token is passed from actor to actor over the network. Every time an actor obtains the token, increase a counter on that actor. Then the actor passes the token to one of its neighbours, picked uniformly at random. This token can be interpreted as someone randomly walking across the graph - that is, this is an implementation of a random walk. The function you should write takes the graph, a starting actor, and the number of iterations as input, and returns the value of the counter for all actors in the network. Do you expect and can you find any relation between the values of the counters and the distance from the input actor, for the five networks? Can you use this function to highlight differences between the different networks (real, synthetic, and rewired)?

TIPS:

to write this function you need to extract the neighbors() of some actors, and perform random choices (for example using Python's random module).
### Task 3.2: Simulate an information diffusion process, where some information is spread over the network. Assume that every actor is in one of two possible states: + (i.e. the actor has already seen the entity that is being spread), or - (i.e. the actor has not yet seen it). The function you should write takes the graph, a starting actor, the number of iterations, and the probability beta of diffusion. At each iteration, all + actors will go through their neighbours one by one and with probability beta will pass the information (that is, set the neighbour's state to +) at the end of this iteration. The function should return the number of actors with state +. Using this function and the five networks, provide evidence regarding the factors increasing or decreasing the speed of diffusion.

### Task 3.3: Simulate an opinion diffusion process. As in Task 2, actors have two possible states + and -, representing opinions. At the beginning, all actors have opinion -. The function you should write takes the graph, the number of actors whose opinion should be set to +, the number of iterations, and the opinion change threshold th. At each iteration, all actors with state + will count the number of their neighbours with opinion + and -, and if the proportion of - is higher than or equal to the threshold th, the actor will change its opinion to - at the end of this iteration. The function should return the number of actors with state +. Using this function and the five networks, provide evidence regarding the factors increasing or decreasing the speed of adoption of a new opinion.

 

## PART 4: Adding edge directionality

This part is optional. If you have time for it, perform the same tasks as in PARTS 1-3 using directed networks.
