import math

class RouteProblem:
    def __init__(self, filename):
        self.nodes = {}
        self.edges = {}
        self.origin = None
        self.destinations = []
        
        self.parse_input_file(filename)

    def parse_input_file(self, filename):
        with open(filename, 'r') as file:
            section = None
            for line in file:
                line = line.strip()
                
                if line == 'Nodes:':
                    section = 'nodes'
                    continue
                elif line == 'Edges:':
                    section = 'edges'
                    continue
                elif line == 'Origin:':
                    section = 'origin'
                    continue
                elif line == 'Destinations:':
                    section = 'destinations'
                    continue
                
                if section == 'nodes':
                    node_id, coords = line.split(': ')
                    node_id = int(node_id)
                    x, y = map(int, coords.strip('()').split(','))
                    self.nodes[node_id] = (x, y)
                
                elif section == 'edges':
                    if not line.strip():
                        continue

                    if ': ' in line:
                        try:
                            edge, cost = line.split(': ')
                            start, end = map(int, edge.strip('()').split(','))
                            cost = int(cost)
            
                            if start not in self.edges:
                                self.edges[start] = {}
                            self.edges[start][end] = cost
                        except ValueError:
                            print(f"Warning: Skipping invalid edge line -> {line}")
                    else:
                        print(f"Warning: Skipping malformed line -> {line}")

                
                elif section == 'origin':
                    self.origin = int(line)
                
                elif section == 'destinations':
                    self.destinations = [int(dest) for dest in line.split(';')]

    def actions(self, state):
        return list(self.edges.get(state, {}).keys())

    def result(self, state, action):
        return action

    def path_cost(self, cost_so_far, state, action, next_state):
        return cost_so_far + self.edges[state][next_state]

    def goal_test(self, state):
        return state in self.destinations

    def dfs(self):
        stack = [(self.origin, [self.origin], 0)] 
        visited = set()
        nodes_expanded = 0

        while stack:
            node, path, cost = stack.pop()
            nodes_expanded += 1

            if node in self.destinations:
                return node, nodes_expanded, path, cost

            if node not in visited:
                visited.add(node)
                for neighbor in sorted(self.actions(node), reverse=True):
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor], cost + self.edges[node][neighbor]))

        return None, nodes_expanded, [], float('inf')

if __name__ == "__main__":
    filename = "PathFinder-test.txt"
    route_problem = RouteProblem(filename)
    
    goal, nodes_expanded, path, cost = route_problem.dfs()
    
    print(f"DFS Search Result:")
    if goal:
        print(f"Goal Node: {goal}")
        print(f"Nodes Expanded: {nodes_expanded}")
        print(f"Path: {' -> '.join(map(str, path))}")
        print(f"Total Cost: {cost}")
    else:
        print("No path found.")
