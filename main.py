import heapq
from collections import defaultdict
from typing import List, Tuple, Dict, Any

class Train:
    def __init__(self, name: str, capacity: int, starting_node: str) -> None:
        self.name = name
        self.capacity = capacity
        self.current_node = starting_node
        self.packages: List[str] = []
        self.time: int = 0

class Package:
    def __init__(self, name: str, weight: int, starting_node: str, destination_node: str) -> None:
        self.name = name
        self.weight = weight
        self.current_node = starting_node
        self.destination_node = destination_node

class Edge:
    def __init__(self, node1: str, node2: str, journey_time: int) -> None:
        self.node1 = node1
        self.node2 = node2
        self.journey_time = journey_time

def dijkstra(graph: Dict[str, List[Tuple[str, int]]], start_node: str) -> Tuple[Dict[str, int], Dict[str, str]]:
    queue: List[Tuple[int, str]] = [(0, start_node)]
    distances: Dict[str, int] = {start_node: 0}
    predecessors: Dict[str, str] = {start_node: None}

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return distances, predecessors

def get_path(predecessors: Dict[str, str], start_node: str, end_node: str) -> List[str]:
    path: List[str] = []
    current_node: str = end_node
    while current_node != start_node:
        path.append(current_node)
        current_node = predecessors[current_node]
    path.append(start_node)
    path.reverse()
    return path

def main(nodes: List[str], edges: List[Tuple[str, str, str, int]], trains: List[Tuple[str, int, str]], packages: List[Tuple[str, int, str, str]]) -> None:
    graph: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
    for edge in edges:
        name, node1, node2, journey_time = edge
        journey_time *= 60  # Convert minutes to seconds
        graph[node1].append((node2, journey_time))
        graph[node2].append((node1, journey_time))

    train_objects: Dict[str, Train] = {t[0]: Train(t[0], t[1], t[2]) for t in trains}
    package_objects: Dict[str, Package] = {p[0]: Package(p[0], p[1], p[2], p[3]) for p in packages}
    package_destinations: Dict[str, str] = {p[0]: p[3] for p in packages}
    
    moves: List[Tuple[int, str, str, List[str], str, List[str]]] = []
    pq: List[Tuple[int, str, str]] = [(0, train.name, train.current_node) for train in train_objects.values()]
    heapq.heapify(pq)
    
    while pq:
        current_time, train_name, current_node = heapq.heappop(pq)
        train: Train = train_objects[train_name]
        train.time = current_time
        train.current_node = current_node

        if train.packages:
            destination: str = package_destinations[train.packages[0]]
        else:
            destination = None
            for package in package_objects.values():
                if package.current_node == train.current_node and train.capacity >= package.weight:
                    train.packages.append(package.name)
                    package.current_node = None
                    destination = package.destination_node
                    break

        if destination:
            distances, predecessors = dijkstra(graph, current_node)
            path = get_path(predecessors, current_node, destination)
            next_node = path[1]
            journey_time = distances[next_node] - distances[current_node]
            move_time = current_time + journey_time
            moves.append((current_time, train.name, current_node, train.packages.copy(), next_node, []))
            train.current_node = next_node
            train.time = move_time
            for package in train.packages:
                package_objects[package].current_node = next_node
            heapq.heappush(pq, (move_time, train.name, next_node))
        else:
            moves.append((current_time, train.name, current_node, [], current_node, train.packages.copy()))
            train.packages.clear()

    for move in moves:
        print(f"W={move[0]}, T={move[1]}, N1={move[2]}, P1={move[3]}, N2={move[4]}, P2={move[5]}")

# Example input
nodes: List[str] = ['A', 'B', 'C']
edges: List[Tuple[str, str, str, int]] = [('E1', 'A', 'B', 30), ('E2', 'B', 'C', 10)]
trains: List[Tuple[str, int, str]] = [('Q1', 6, 'B')]
packages: List[Tuple[str, int, str, str]] = [('K1', 5, 'A', 'C')]

main(nodes, edges, trains, packages)
