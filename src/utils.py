import json
import pandas as pd
import igraph as ig
import numpy as np
import matplotlib.pyplot as plt


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
    transitivity = g.transitivity_undirected()  # Thea suggested there's a better one
    
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

# Function for task 1.4
def prepare_graph_for_degree(g: ig.Graph, base_size = 1, scale_factor = 5):
    degrees = g.degree()
    
    g.vs["size"] = [base_size + scale_factor * degree for degree in degrees]
    
    return g

# Function for task 1.5
def prepare_graph_for_betweenness(g: ig.Graph, base_size = 1, scale_factor = 5):
    betweenness = g.betweenness()
    max_betweenness = max(betweenness) if max(betweenness) > 0 else 1
    
    g.vs["size"] = [base_size + scale_factor * (b/max_betweenness) for b in betweenness]
    
    return g

# Function to plot the graph
def plot_graph(g: ig.Graph, layout: ig.Layout, target_file = None):
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
    ig_plot = ig.plot(g, target=target_file, **visual_style, backend="matplotlib")

    if target_file is None:
        plt.show()  # Show plot interactively
    else:
        print(f"Plot saved to: {target_file}")

# Function for task 1.6
def top_10_for_network(g: ig.Graph):
    degrees = g.degree()
    top_10_degrees = sorted(degrees, reverse=True)[:10]
    top_10_degree_authors = [g.vs[i]["name"] for i in top_10_degrees]
    
    betweenness = g.betweenness()
    top_10_betweenness = sorted(betweenness, reverse=True)[:10]
    top_10_betweenness_authors = [g.vs[i]["name"] for i in top_10_betweenness]
    
    return top_10_degree_authors, top_10_betweenness_authors