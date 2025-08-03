import cube

def optimize_moves(moves):
    def invert_move(move):
        if move.endswith('i'):
            return move[:-1]
        elif move.endswith('2'):
            return move  
        else:
            return move + 'i'

    def cancel_rotations(rotations):
        axes = {'X': 0, 'Y': 0, 'Z': 0}
        for move in rotations:
            axis = move[0]
            if move.endswith('2'):
                axes[axis] += 2
            elif move.endswith('i'):
                axes[axis] -= 1
            else:
                axes[axis] += 1
        out = []
        for axis in 'XYZ':
            count = axes[axis] % 4
            if count == 1:
                out.append(axis)
            elif count == 2:
                out.append(axis + '2')
            elif count == 3:
                out.append(axis + 'i')
        return out

    i = 0
    moves = moves[:]
    out = []

    while i < len(moves):
        # Compress full cube rotations
        if moves[i][0] in 'XYZ':
            j = i
            while j < len(moves) and moves[j][0] in 'XYZ':
                j += 1
            out.extend(cancel_rotations(moves[i:j]))
            i = j
            continue

        # R R R => R'
        if i + 2 < len(moves) and moves[i] == moves[i+1] == moves[i+2]:
            out.append(invert_move(moves[i]))
            i += 3
            continue

        # R R' => remove both
        if i + 1 < len(moves) and invert_move(moves[i]) == moves[i+1]:
            i += 2
            continue

        # R R => R2
        if i + 1 < len(moves) and moves[i] == moves[i+1]:
            out.append(moves[i] + '2')
            i += 2
            continue

        # R R2 => R'
        if i + 1 < len(moves) and moves[i] + '2' == moves[i+1]:
            out.append(invert_move(moves[i]))
            i += 2
            continue

        # R2 R => R'
        if i + 1 < len(moves) and moves[i] == moves[i+1] + '2':
            out.append(invert_move(moves[i+1]))
            i += 2
            continue

        out.append(moves[i])
        i += 1

    return out
