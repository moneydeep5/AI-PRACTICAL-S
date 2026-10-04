import heapq

goal = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)


def get_neighbors(state):
    neighbors = []

    zero = state.index(0)
    row = zero // 3
    col = zero % 3

    moves = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for dr, dc in moves:
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_zero = new_row * 3 + new_col

            new_state = list(state)
            new_state[zero], new_state[new_zero] = \
                new_state[new_zero], new_state[zero]

            neighbors.append(tuple(new_state))

    return neighbors


# Heuristic 1: Misplaced Tiles
def misplaced_tiles(state):
    count = 0

    for i in range(9):
        if state[i] != 0 and state[i] != goal[i]:
            count += 1

    return count


# Heuristic 2: Manhattan Distance
def manhattan_distance(state):
    distance = 0

    for i in range(9):
        tile = state[i]

        if tile != 0:
            current_row = i // 3
            current_col = i % 3

            goal_index = goal.index(tile)
            goal_row = goal_index // 3
            goal_col = goal_index % 3

            distance += abs(current_row - goal_row)
            distance += abs(current_col - goal_col)

    return distance


def a_star(start, heuristic):
    queue = []
    heapq.heappush(queue, (heuristic(start), 0, start, [start]))

    visited = set()
    nodes_checked = 0

    while queue:
        f, g, state, path = heapq.heappop(queue)

        if state in visited:
            continue

        visited.add(state)
        nodes_checked += 1

        if state == goal:
            return path, g, nodes_checked

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                new_g = g + 1
                new_f = new_g + heuristic(neighbor)

                heapq.heappush(
                    queue,
                    (new_f, new_g, neighbor, path + [neighbor])
                )

    return [], -1, nodes_checked


def print_puzzle(state):
    print(state[0], state[1], state[2])
    print(state[3], state[4], state[5])
    print(state[6], state[7], state[8])
    print()


start = (1, 2, 3,
         4, 0, 6,
         7, 5, 8)


print("Initial Puzzle:")
print_puzzle(start)


path1, cost1, nodes1 = a_star(start, misplaced_tiles)

print("Using Misplaced Tiles Heuristic")
print("Path Cost:", cost1)
print("Nodes Checked:", nodes1)
print("Solution Path:")

for state in path1:
    print_puzzle(state)


path2, cost2, nodes2 = a_star(start, manhattan_distance)

print("Using Manhattan Distance Heuristic")
print("Path Cost:", cost2)
print("Nodes Checked:", nodes2)
print("Solution Path:")

for state in path2:
    print_puzzle(state)


print("Comparison")
print("----------------------------")
print("Misplaced Tiles:")
print("Path Cost:", cost1)
print("Nodes Checked:", nodes1)

print()

print("Manhattan Distance:")
print("Path Cost:", cost2)
print("Nodes Checked:", nodes2)