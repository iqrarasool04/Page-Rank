from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

# Task 1
def create_web_graph(links):
    web_graph = defaultdict(list)
    for source, target in links:
        web_graph[source].append(target)
        if target not in web_graph:
            web_graph[target] = []
    return web_graph

# Task 2
def calculate_pagerank(graph, iterations, d=0.85):
    num_pages = len(graph)
    initial_value = 1.0 / num_pages
    page_rank = {page: initial_value for page in graph}
    for _ in range(iterations):
        new_page_rank = {}
        for page in graph:
            new_pr = (1 - d) / num_pages
            new_pr += d * sum(page_rank[link] / len(graph[link]) for link in graph if page in graph[link])
            new_page_rank[page] = new_pr
        page_rank = new_page_rank
    return page_rank

# Task 3
def calculate_pagerank_with_dangling(graph, iterations, d=0.85):
    num_pages = len(graph)
    initial_value = 1.0 / num_pages
    page_rank = {page: initial_value for page in graph}
    for _ in range(iterations):
        new_page_rank = {}
        total_pr_dangling = sum(page_rank[page] for page in graph if not graph[page])
        for page in graph:
            new_pr = (1 - d) / num_pages
            new_pr += d * sum(page_rank[link] / len(graph[link]) for link in graph if page in graph[link])
            new_pr += d * total_pr_dangling / num_pages if not graph[page] else 0
            new_page_rank[page] = new_pr
        page_rank = new_page_rank
    return page_rank

# Task 4
def calculate_pagerank_with_convergence(graph, iterations, d=0.85, tolerance=1.0e-8):
    num_pages = len(graph)
    initial_value = 1.0 / num_pages
    page_rank = {page: initial_value for page in graph}
    for _ in range(iterations):
        new_page_rank = {}
        for page in graph:
            new_pr = (1 - d) / num_pages
            new_pr += d * sum(page_rank[link] / len(graph[link]) for link in graph if page in graph[link])
            new_page_rank[page] = new_pr
        if sum(abs(new_page_rank[page] - page_rank[page]) for page in graph) < tolerance:
            break
        page_rank = new_page_rank
    return page_rank

# Task 5
def visualize_web_graph(graph, page_rank):
    G = nx.DiGraph()
    G.add_edges_from([(source, target) for source in graph for target in graph[source]])
    node_sizes = [10000 * page_rank[page] for page in graph]
    nx.draw(G, with_labels=True, node_size=node_sizes, font_size=10, node_color='skyblue')
    plt.show()

# Web graph
web_graph = {'A': [], 'B':['C','G'], 'C':['A'], 'D':['C'], 'E':['C'], 'F':['C','G'], 'G':['B']}

# Task 1
print("Web graph representation")
print(create_web_graph([('A', 'B'), ('B', 'C'), ('B', 'G'), ('C', 'A'), ('D', 'C'), ('E', 'C'), ('F', 'C'), ('F', 'G'), ('G', 'B')]))

# Task 2
print("\nPageRank without dangling pages")
print(calculate_pagerank(web_graph, iterations=100))

# Task 3
print("\nPageRank with dangling pages")
print(calculate_pagerank_with_dangling(web_graph, iterations=100))

# Task 4
print("\nPageRank with convergence check")
print(calculate_pagerank_with_convergence(web_graph, iterations=100))

# Task 5
print("\nVisualization of the web graph with PageRank scores")
page_rank = calculate_pagerank_with_convergence(web_graph, iterations=100)
visualize_web_graph(web_graph, page_rank)
