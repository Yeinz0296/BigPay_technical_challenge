import heapq
from collections import defaultdict
from typing import List, Tuple, Dict, Optional

class Train:
    def __init__(self, name: str, capacity: int, starting_node: str) -> None:
        self.name: str = name
        self.capacity: int = capacity
        self.current_node: str = starting_node
        self.packages: List[str] = []
        self.time: int = 0

class Package:
    def __init__(self, name: str, weight: int, starting_node: str, destination_node: str) -> None:
        self.name: str = name
        self.weight: int = weight
        self.current_node: str = starting_node
        self.destination_node: str = destination_node

def dijkstra(graph: Dict[str, List[Tuple[str, int]]], start_node: str) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
    queue: List[Tuple[int, str]] = [(0, start_node)]
    distances: Dict[str, int] = {node: float('inf') for node in graph}  # Initialize all nodes with inf distance
    predecessors: Dict[str, Optional[str]] = {node: None for node in graph}  # Initialize predecessors
    distances[start_node] = 0

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances.get(current_node, float('inf')):
            continue
        for neighbor, weight in graph.get(current_node, []):
            distance = current_distance + weight
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return distances, predecessors

def get_path(predecessors: Dict[str, Optional[str]], start_node: str, end_node: str) -> List[str]:
    path: List[str] = []
    current_node: str = end_node
    while current_node != start_node:
        path.append(current_node)
        current_node = predecessors.get(current_node, start_node)
    path.append(start_node)
    path.reverse()
    return path

def get_nearest_package_location(train: Train, graph: Dict[str, List[Tuple[str, int]]], package_objects: Dict[str, Package]) -> Optional[str]:
    distances, _ = dijkstra(graph, train.current_node)
    nearest_package_node = None
    min_distance = float('inf')

    for package in package_objects.values():
        if package.current_node is not None:
            distance = distances.get(package.current_node, float('inf'))
            if distance < min_distance:
                min_distance = distance
                nearest_package_node = package.current_node

    return nearest_package_node

def main(nodes: List[str], edges: List[Tuple[str, str, str, int]], trains: List[Tuple[str, int, str]], packages: List[Tuple[str, int, str, str]]) -> None:
    graph: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
    for edge in edges:
        name, node1, node2, journey_time = edge
        journey_time *= 60  # Convert minutes to seconds
        graph[node1].append((node2, journey_time))
        graph[node2].append((node1, journey_time))
    
    print(f"Graph: {graph}")  # Debug print for graph
    
    train_objects: Dict[str, Train] = {t[0]: Train(t[0], t[1], t[2]) for t in trains}
    package_objects: Dict[str, Package] = {p[0]: Package(p[0], p[1], p[2], p[3]) for p in packages}
    
    moves: List[Tuple[int, str, str, List[str], str, List[str]]] = []

    for train in train_objects.values():
        current_node = train.current_node
        print(f"\nProcessing train {train.name} at node {current_node}")
        
        # Log the initial position
        moves.append((train.time, train.name, current_node, train.packages.copy(), current_node, []))
        
        # Find nearest package
        nearest_package_node = get_nearest_package_location(train, graph, package_objects)
        print(f"Nearest package node for train {train.name}: {nearest_package_node}")

        if nearest_package_node:
            distances, predecessors = dijkstra(graph, current_node)
            path = get_path(predecessors, current_node, nearest_package_node)
            print(f"Path from {current_node} to {nearest_package_node}: {path}")
            
            for i in range(1, len(path)):
                next_node = path[i]
                journey_time = next((time for node, time in graph[current_node] if node == next_node), 0)
                train.time += journey_time
                moves.append((train.time, train.name, current_node, train.packages.copy(), next_node, []))
                current_node = next_node
                train.current_node = next_node

            # Load packages
            loaded_package = False
            for package_name, package in package_objects.items():
                if package.current_node == current_node and package.weight <= train.capacity:
                    if package_name not in train.packages:
                        train.packages.append(package_name)
                        package.current_node = None
                        loaded_package = True
                        print(f"Loaded package {package_name} onto train {train.name} at node {current_node}")
                    break  # Break the loop after loading a package

            if loaded_package:
                moves.append((train.time, train.name, current_node, train.packages.copy(), current_node, []))

            # Deliver packages
            if train.packages:
                destination = package_objects[train.packages[0]].destination_node
                distances, predecessors = dijkstra(graph, current_node)
                path = get_path(predecessors, current_node, destination)
                print(f"Path from {current_node} to {destination}: {path}")
                
                for i in range(1, len(path)):
                    next_node = path[i]
                    journey_time = next((time for node, time in graph[current_node] if node == next_node), 0)
                    train.time += journey_time
                    moves.append((train.time, train.name, current_node, train.packages.copy(), next_node, []))
                    current_node = next_node
                    train.current_node = next_node

            # Drop off packages
            drop_off_packages = []
            for package_name in train.packages:
                if package_objects[package_name].destination_node == current_node:
                    drop_off_packages.append(package_name)
            train.packages = [p for p in train.packages if p not in drop_off_packages]
            if drop_off_packages:
                moves.append((train.time, train.name, current_node, [], current_node, drop_off_packages))
        
        # Continue to next train or exit
        if not train.packages:
            continue

    # Output moves
    for move in moves:
        print(f"W={move[0]}, T={move[1]}, N1={move[2]}, P1={move[3]}, N2={move[4]}, P2={move[5]}")

# Example input
nodes: List[str] = ['A', 'B', 'C']
edges: List[Tuple[str, str, str, int]] = [('E1', 'A', 'B', 30), ('E2', 'B', 'C', 10)]
trains: List[Tuple[str, int, str]] = [('Q1', 6, 'B')]
packages: List[Tuple[str, int, str, str]] = [('K1', 5, 'A', 'C')]

# nodes: List[str] = ['A', 'B', 'C', 'D']
# edges: List[Tuple[str, str, str, int]] = [('E1', 'A', 'B', 10), ('E2', 'B', 'C', 10), ('E3', 'C', 'D', 10), ('E4', 'A', 'D', 30)]
# trains: List[Tuple[str, int, str]] = [('T1', 10, 'A'), ('T2', 5, 'B')]
# packages: List[Tuple[str, int, str, str]] = [('P1', 5, 'C', 'D'), ('P2', 3, 'A', 'C')]

main(nodes, edges, trains, packages)
