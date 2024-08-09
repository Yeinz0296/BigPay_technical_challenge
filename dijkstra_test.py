import heapq
from typing import List, Tuple, Dict, Optional

def dijkstra(graph: Dict[str, List[Tuple[str, int]]], start_node: str) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
    queue: List[Tuple[int, str]] = [(0, start_node)]
    distances: Dict[str, int] = {node: float('inf') for node in graph}  # Initialize all nodes with inf distance
    predecessors: Dict[str, Optional[str]] = {node: None for node in graph}  # Initialize predecessors
    distances[start_node] = 0

    print(f"Starting Dijkstra's algorithm from node {start_node}")

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        # Debug print to understand the current state
        print(f"Processing node {current_node} with current distance {current_distance}")

        if current_distance > distances.get(current_node, float('inf')):
            continue

        for neighbor, weight in graph.get(current_node, []):
            distance = current_distance + weight
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
                print(f"Updated distance for node {neighbor} to {distance}")

    return distances, predecessors

# Example usage of dijkstra function to debug
def example_usage():
    # Example graph setup for debugging
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 5)],
        'C': [('A', 4), ('B', 2), ('D', 1)],
        'D': [('B', 5), ('C', 1)]
    }
    start_node = 'A'
    distances, predecessors = dijkstra(graph, start_node)
    print("Distances:", distances)
    print("Predecessors:", predecessors)

# Run example usage
example_usage()
