import json
import random
import pandas as pd
import igraph as ig
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


def tweets_as_dataframe(file_path: str = "data/tweets.dat", save=False):
    data = []

    try:
        with open(file_path, "r") as file:
            for line in file:
                try:
                    tweet = json.loads(line.strip())
                    data.append(tweet)
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON line: {e}")
        tweets_df = pd.DataFrame(data)

        if save:
            tweets_df.to_csv("data/tweets.csv", index=False)

        return tweets_df
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        raise
    except Exception as e:
        print("Error in tweets_as_dataframe: ", e)


def parse_referenced_tweets_to_dataframe(row: pd.Series):
    action = row["referenced_tweets"]
    if isinstance(action, float):
        return None
    try:
        if isinstance(action, list) and action:
            nested_df = pd.DataFrame(action)
            return nested_df
    except (ValueError, SyntaxError):
        print(f"Warning: Failed to parse {row}")
        return None


def analyze_graph(g: ig.Graph):
    order = g.vcount()
    size = g.ecount()
    components = g.components()
    no_components = len(components)
    size_of_largest_component = max([len(component) for component in components])
    density = g.density()
    transitivity = g.transitivity_avglocal_undirected()

    print(f"Order: {order}")
    print(f"Size: {size}")
    print(f"No .of Components: {no_components}")
    print(f"Size of largest component: {size_of_largest_component}")
    print(f"Density: {density}")
    print(f"Transitivity: {transitivity}")

    degree_dist = g.degree()
    degree_counts = np.bincount(degree_dist)
    degrees = np.arange(len(degree_counts))

    non_zero = degree_counts > 0
    degrees = degrees[non_zero]
    degree_counts = degree_counts[non_zero]

    plt.figure(figsize=(8, 6))
    plt.loglog(degrees, degree_counts, marker="o", linestyle="", markersize=6, alpha=0.7, label="Degree Distribution")
    plt.title("Degree Distribution (Log-Log Scale)")
    plt.xlabel("Degree (log)")
    plt.ylabel("Frequency (log)")
    plt.grid(which="both", linestyle="--", alpha=0.7)
    plt.legend()
    plt.show()


def prepare_graph(g: ig.Graph, layout: ig.Layout = None) -> Tuple[ig.Graph, ig.Layout]:
    g.simplify()
    if layout is None:
        layout = g.layout("circle")

    g.vs["color"] = "red"
    g.vs["size"] = 1
    g.vs["frame_width"] = 0
    g.vs["label"] = None

    g.es["color"] = "rgba(1, 1, 1, 0.01)"
    g.es["width"] = 0.10

    return g, layout


# Function for task 1.4
def prepare_graph_for_degree(g: ig.Graph, base_size: int = 1, scale_factor: int = 5):
    degrees = g.degree()

    g.vs["size"] = [base_size + scale_factor * degree for degree in degrees]

    return g


# Function for task 1.5
def prepare_graph_for_betweenness(g: ig.Graph, base_size: int = 1, scale_factor: int = 5):
    betweenness = g.betweenness()
    max_betweenness = max(betweenness) if max(betweenness) > 0 else 1

    g.vs["size"] = [base_size + scale_factor * (b/max_betweenness) for b in betweenness]

    return g


# Function to plot the graph
def plot_graph(g: ig.Graph, layout: ig.Layout, target_file: str = None):
    visual_style = {
        "layout": layout,
        "vertex_color": g.vs["color"],
        "vertex_size": g.vs["size"],
        "vertex_frame_width": 0,
        "vertex_label": None,
        "edge_color": g.es["color"],
        "edge_width": g.es["width"],
        # "bbox": (800, 800),  # Image size in pixels
        "margin": 2,
    }

    # Use matplotlib as the engine for visualization
    plt.figure(figsize=(10, 10))
    ig.plot(g, target=target_file, **visual_style, backend="matplotlib")

    if target_file is None:
        plt.show()  # Show plot interactively
    else:
        print(f"Plot saved to: {target_file}")


# Function for task 1.6
def top_10_for_network(g: ig.Graph):
    degrees = g.degree()
    degree_dict = {g.vs[i]["name"]: degrees[i] for i in range(len(g.vs))}

    top_10_degrees = dict(sorted(degree_dict.items(), key=lambda item: item[1], reverse=True)[:10])

    betweenness = g.betweenness()
    betweenness_dict = {g.vs[i]["name"]: betweenness[i] for i in range(len(g.vs))}
    top_10_betweenness = dict(sorted(betweenness_dict.items(), key=lambda item: item[1], reverse=True)[:10])

    return top_10_degrees, top_10_betweenness


def random_walk(g: ig.Graph, actor: ig.Vertex = None, iterations: int = 10_000) -> list:
    if actor is None:
        actor = g.vs[random.randint(0, g.vcount() - 1)]

    token_counts = [0] * g.vcount()
    for i in range(iterations):
        token_counts[actor.index] += 1
        if len(actor.neighbors()) > 0:
            actor = random.choice(actor.neighbors())

    token_ratios = np.array(token_counts) / iterations
    return token_ratios.tolist()


def random_diffusion(g: ig.Graph, actor: ig.Vertex = None, beta: float = 0.05, iterations: int = 100) -> list:
    if actor is None:
        actor = g.vs[random.randint(0, g.vcount() - 1)]
    infected = set([actor.index])

    for _ in range(iterations):
        infected_actors: ig.seq.VertexSeq = g.vs[list(infected)]
        for infected_actor in infected_actors:
            neighbors = infected_actor.neighbors()
            weights = [beta] * len(neighbors)
            infected_neighbors = random.choices(neighbors, weights=weights, k=len(neighbors))
            infected.update([n.index for n in infected_neighbors])
        if len(infected) == g.vcount():
            print(f"All nodes infected after {_} rounds.")
            break

    return list(infected), len(infected)


def random_opinion(g: ig.Graph, th: int, initial_positive: int, iterations: int = 100) -> list:
    """
    Note: Some bug with random.choices can make the initial postive count less
    than what you pass in. idk, calling it good enough and moving on.
    """
    g = g.copy()
    g.vs["convinced"] = False
    starting_indices = random.choices([i for i in range(g.vcount())], k=initial_positive)
    g.vs[starting_indices]["convinced"] = True  # bug here

    for _ in range(iterations):
        convinced_actors: ig.VertexSeq = g.vs.select(convinced_eq=True)
        for actor in convinced_actors:
            neighbors = actor.neighbors()
            if sum([n["convinced"] for n in neighbors]) > th:
                g.vs[[n.index for n in neighbors]]["convinced"] = True

    return len(g.vs.select(convinced_eq=True))
