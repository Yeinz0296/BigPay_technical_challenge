import heapq
from collections import defaultdict
from typing import List, Tuple, Dict, Optional

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

def dijkstra(graph: Dict[str, List[Tuple[str, int]]], start_node: str) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
    queue: List[Tuple[int, str]] = [(0, start_node)]
    distances: Dict[str, int] = {start_node: 0}
    predecessors: Dict[str, Optional[str]] = {start_node: None}

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return distances, predecessors

def get_path(predecessors: Dict[str, Optional[str]], start_node: str, end_node: str) -> List[str]:
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
        journey_time *= 60 
        graph[node1].append((node2, journey_time))
        graph[node2].append((node1, journey_time))

    train_objects: Dict[str, Train] = {t[0]: Train(t[0], t[1], t[2]) for t in trains}
    package_objects: Dict[str, Package] = {p[0]: Package(p[0], p[1], p[2], p[3]) for p in packages}
    
    moves: List[Tuple[int, str, str, List[str], str, List[str]]] = []
    
    for train in train_objects.values():
        current_node = train.current_node
        
        if not any(package.current_node == current_node for package in package_objects.values()):
            distances, predecessors = dijkstra(graph, current_node)
            nearest_package_node = None
            for package in package_objects.values():
                if package.current_node is not None:
                    nearest_package_node = package.current_node
                    break

            if nearest_package_node:
                path = get_path(predecessors, current_node, nearest_package_node)
                for i in range(1, len(path)):
                    next_node = path[i]
                    journey_time = distances[next_node] - distances[current_node]
                    train.time += journey_time
                    moves.append((train.time, train.name, current_node, [], next_node, []))
                    current_node = next_node
                    train.current_node = next_node

        while True:
            loaded_package: bool = False
            for package_name, package in package_objects.items():
                if package.current_node == current_node and package.weight <= train.capacity:
                    train.packages.append(package_name)
                    package.current_node = None
                    loaded_package = True
                    break
            
            if not train.packages:
                break

            destination = package_objects[train.packages[0]].destination_node
            distances, predecessors = dijkstra(graph, current_node)
            path = get_path(predecessors, current_node, destination)
            
            for i in range(1, len(path)):
                next_node = path[i]
                journey_time = distances[next_node] - distances[current_node]
                move_time = train.time + journey_time
                
                moves.append((move_time, train.name, current_node, train.packages.copy(), next_node, []))
                
                train.time = move_time
                train.current_node = next_node
                current_node = next_node
            
            drop_off_packages = []
            for package_name in train.packages:
                if package_objects[package_name].destination_node == current_node:
                    drop_off_packages.append(package_name)
            train.packages = [p for p in train.packages if p not in drop_off_packages]
            moves.append((train.time, train.name, current_node, [], current_node, drop_off_packages))
        
        if not train.packages:
            break

    # Output moves
    for move in moves:
        print(f"W={move[0]}, T={move[1]}, N1={move[2]}, P1={move[3]}, N2={move[4]}, P2={move[5]}")

# Example input
nodes: List[str] = ['A', 'B', 'C', 'D']
edges: List[Tuple[str, str, str, int]] = [('E1', 'A', 'B', 30), ('E2', 'B', 'C', 10), ('E3', 'C', 'D', 5)]
trains: List[Tuple[str, int, str]] = [('Q1', 10, 'B'), ('Q2', 6, 'D')]
packages: List[Tuple[str, int, str, str]] = [('K1', 5, 'A', 'D'), ('K2', 5, 'A', 'D')]

main(nodes, edges, trains, packages)
