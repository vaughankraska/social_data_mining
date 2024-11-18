import json
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


def prepare_graph(g: ig.Graph, layout: ig.Layout = None) -> Tuple[ig.Graph, ig.Layout]:
    if layout is None:
        layout = g.layout("circle")

    g.vs["color"] = "red"
    g.vs["size"] = 1
    g.vs["frame_width"] = 0
    g.vs["label"] = None

    g.es["color"] = "rgba(0, 0, 0, 0.1)"
    g.es["width"] = 0.5

    return g, layout


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
