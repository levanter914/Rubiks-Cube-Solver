from collections import deque
from optimized_solver.optimal_cube import OptimalCube

def invert_moves(sequence):
    """Invert a move sequence, e.g. 'R U'' -> 'U R''."""
    if not sequence:
        return ""
    inverted_sequence = []
    for move in reversed(sequence.split()):
        if "'" in move:
            inverted_sequence.append(move[0])
        elif "2" in move:
            inverted_sequence.append(move)
        else:
            inverted_sequence.append(move + "'")
    return " ".join(inverted_sequence)

def solve(scrambled_cube):
    """Bidirectional BFS solver for the Rubik's Cube."""
    solved_cube = OptimalCube()
    if scrambled_cube.state_to_tuple() == solved_cube.state_to_tuple():
        return "Cube is already solved."

    forward_q = deque([(scrambled_cube, "")])
    backward_q = deque([(solved_cube, "")])

    visited_forward = {scrambled_cube.state_to_tuple(): ""}
    visited_backward = {solved_cube.state_to_tuple(): ""}

    moves = ["U", "U'", "U2", "D", "D'", "D2",
             "L", "L'", "L2", "R", "R'", "R2",
             "F", "F'", "F2", "B", "B'", "B2"]

    while forward_q and backward_q:
        if len(forward_q) <= len(backward_q):
            current_cube, current_path = forward_q.popleft()
            for move in moves:
                next_cube = current_cube.clone()
                next_cube.execute_sequence(move)
                next_state_tuple = next_cube.state_to_tuple()

                if next_state_tuple in visited_backward:
                    path_from_backward = visited_backward[next_state_tuple]
                    full_path = (current_path + " " + move).strip() + " " + invert_moves(path_from_backward)
                    return full_path.strip()

                if next_state_tuple not in visited_forward:
                    new_path = (current_path + " " + move).strip()
                    visited_forward[next_state_tuple] = new_path
                    forward_q.append((next_cube, new_path))
        else:
            current_cube_b, current_path_b = backward_q.popleft()
            for move in moves:
                next_cube_b = current_cube_b.clone()
                next_cube_b.execute_sequence(move)
                next_state_tuple_b = next_cube_b.state_to_tuple()

                if next_state_tuple_b in visited_forward:
                    path_from_forward = visited_forward[next_state_tuple_b]
                    full_path = path_from_forward + " " + invert_moves((current_path_b + " " + move).strip())
                    return full_path.strip()

                if next_state_tuple_b not in visited_backward:
                    new_path_b = (current_path_b + " " + move).strip()
                    visited_backward[next_state_tuple_b] = new_path_b
                    backward_q.append((next_cube_b, new_path_b))

    return "No solution found."
