from state import State
import argparse
from heapq import heappush, heappop, heapify
import itertools

moves = list()

initial_state = list()

goal_node = State
goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]

board_side = 0
board_len = 0


def a_star(start_state):

    global goal_node

    explored, heap, heap_entry = set(), list(), {}

    heuristic = h(start_state)

    # state, parent, move, cost, key(cost + h)
    root = State(start_state, None, None, 0, heuristic)

    # cost, move, state
    entry = (heuristic, 0, root)

    heappush(heap, entry)

    # to link the number to its node
    heap_entry[root.map] = entry

    while heap:

        node = heappop(heap)

        explored.add(node[2].map)

        if node[2].state == goal_state:
            # save the goal state to backtrack the solution
            goal_node = node[2]
            return

        neighbors = expand(node[2])

        for neighbor in neighbors:

            neighbor.key = neighbor.cost + h(neighbor.state)

            entry = (neighbor.key, neighbor.move, neighbor)

            if neighbor.map not in explored:

                heappush(heap, entry)

                explored.add(neighbor.map)

                heap_entry[neighbor.map] = entry

            elif neighbor.map in heap_entry and neighbor.key < heap_entry[neighbor.map][2].key:

                hindex = heap.index((heap_entry[neighbor.map][2].key,
                                     heap_entry[neighbor.map][2].move,
                                     heap_entry[neighbor.map][2]))

                # replace the old state with the new best
                heap[hindex] = entry
                heap_entry[neighbor.map] = entry

                # rearrange the heap
                heapify(heap)


def backtrack():
    """
    retrieve the moves from the initial node to the goal
    :return: list of moves
    """
    current_node = goal_node
    while current_node.state != initial_state:
        if current_node.move == 1:
            move = 'UP'
        elif current_node.move == 2:
            move = 'Down'
        elif current_node.move == 3:
            move = 'Left'
        else:
            move = 'Right'

        moves.insert(0, move)
        current_node = current_node.parent

    return moves


def move(state, direction):
    """
    state: list of numbers
    direction: number indicates the direction
    1: Up
    2: Down
    3: Left
    4: Right
    :return: new state or None
    """
    new_state = state[:]
    empty_position = state.index(0)

    if direction == 1:
        # if the empty position not in the first row conduct the new state
        if empty_position not in range(0, board_side):
            temp = new_state[empty_position - board_side]
            new_state[empty_position - board_side] = 0
            new_state[empty_position] = temp
            return new_state
        else:
            return None
    elif direction == 2:
        # if the empty position not in the last row
        if empty_position not in range(board_len - board_side, board_len):
            temp = new_state[empty_position + board_side]
            new_state[empty_position + board_side] = 0
            new_state[empty_position] = temp
            return new_state
        else:
            return None
    elif direction == 3:
        # if not in the first column
        if empty_position not in range(0, board_len, board_side):
            temp = new_state[empty_position - 1]
            new_state[empty_position - 1] = 0
            new_state[empty_position] = temp
            return new_state
        else:
            return None
    else:
        # if not in the last column
        if empty_position not in range(board_side - 1, board_len, board_side):
            temp = new_state[empty_position + 1]
            new_state[empty_position + 1] = 0
            new_state[empty_position] = temp
            return new_state
        else:
            return None


def expand(node):
    """
    expand the node in all directions if possible
    list of possible neighbors
    """

    neighbors = list()

    neighbors.append(State(move(node.state, 1), node, move=1, cost=node.cost+1, key=0))
    neighbors.append(State(move(node.state, 2), node, move=2, cost=node.cost+1, key=0))
    neighbors.append(State(move(node.state, 3), node, move=3, cost=node.cost+1, key=0))
    neighbors.append(State(move(node.state, 4), node, move=4, cost=node.cost+1, key=0))

    # return only the valid expansions
    return [neighbor for neighbor in neighbors if neighbor.state]


def h(state):
    """
    calculate the heuristic
    which is the sum of the distances of each cell away from it's correct position
    """
    sum = 0
    for i in range(1, board_len):
        # the manhatin distance
        sum += abs(state.index(i) % board_side - goal_state.index(i) % board_side) + abs(state.index(i) // board_side - goal_state.index(i) // board_side)
    return sum


def read(configrations):
    """
    configrations: string contains the board entered by the user "1,2,4,6,..."
    """
    global board_len, board_side
    board = configrations.split(',')
    for cell in board:
        initial_state.append(int(cell))

    # the side is the square root of the board because the board has to be a square
    board_len = len(initial_state)
    board_side = int(board_len ** 0.5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('board')
    args = parser.parse_args()
    read(args.board)

    a_star(initial_state)
    print(backtrack())


if __name__ == "__main__":
    main()
