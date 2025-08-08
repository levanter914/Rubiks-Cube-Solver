class OptimalCube:
    """3x3 Rubik's Cube with flat state, used by the BFS solver."""

    def __init__(self):
        self.state = (
            ['W'] * 9 + ['O'] * 9 + ['G'] * 9 +
            ['R'] * 9 + ['B'] * 9 + ['Y'] * 9
        )

    def clone(self):
        new_cube = OptimalCube()
        new_cube.state = list(self.state)
        return new_cube

    def state_to_tuple(self):
        return tuple(self.state)

    def __str__(self):
        colors = {
            'W': '\033[97m', 'Y': '\033[93m', 'G': '\033[92m',
            'B': '\033[94m', 'R': '\033[91m', 'O': '\033[33m',
            'END': '\033[0m'
        }
        def c(char): return f"{colors.get(char, '')}{char}{colors['END']}"
        s = self.state
        return "\n".join([
            f"         {c(s[0])} {c(s[1])} {c(s[2])}",
            f"         {c(s[3])} {c(s[4])} {c(s[5])}",
            f"         {c(s[6])} {c(s[7])} {c(s[8])}",
            f"{c(s[9])} {c(s[10])} {c(s[11])}   {c(s[18])} {c(s[19])} {c(s[20])}   {c(s[27])} {c(s[28])} {c(s[29])}   {c(s[36])} {c(s[37])} {c(s[38])}",
            f"{c(s[12])} {c(s[13])} {c(s[14])}   {c(s[21])} {c(s[22])} {c(s[23])}   {c(s[30])} {c(s[31])} {c(s[32])}   {c(s[39])} {c(s[40])} {c(s[41])}",
            f"{c(s[15])} {c(s[16])} {c(s[17])}   {c(s[24])} {c(s[25])} {c(s[26])}   {c(s[33])} {c(s[34])} {c(s[35])}   {c(s[42])} {c(s[43])} {c(s[44])}",
            f"         {c(s[45])} {c(s[46])} {c(s[47])}",
            f"         {c(s[48])} {c(s[49])} {c(s[50])}",
            f"         {c(s[51])} {c(s[52])} {c(s[53])}",
        ])
        
    def get_facelets_2d(self):
        """Return a list of 9 strings representing the cube layout in 2D without ANSI codes."""
        s = self.state
        return [
            f"         {s[0]} {s[1]} {s[2]}",
            f"         {s[3]} {s[4]} {s[5]}",
            f"         {s[6]} {s[7]} {s[8]}",
            f"{s[9]} {s[10]} {s[11]}   {s[18]} {s[19]} {s[20]}   {s[27]} {s[28]} {s[29]}   {s[36]} {s[37]} {s[38]}",
            f"{s[12]} {s[13]} {s[14]}   {s[21]} {s[22]} {s[23]}   {s[30]} {s[31]} {s[32]}   {s[39]} {s[40]} {s[41]}",
            f"{s[15]} {s[16]} {s[17]}   {s[24]} {s[25]} {s[26]}   {s[33]} {s[34]} {s[35]}   {s[42]} {s[43]} {s[44]}",
            f"         {s[45]} {s[46]} {s[47]}",
            f"         {s[48]} {s[49]} {s[50]}",
            f"         {s[51]} {s[52]} {s[53]}",
        ]

    def _apply_permutation(self, permutation):
        s = self.state
        for cycle in permutation:
            temp = s[cycle[-1]]
            for i in range(len(cycle) - 1, 0, -1):
                s[cycle[i]] = s[cycle[i-1]]
            s[cycle[0]] = temp
    
    def u(self):
        perm = [[0, 2, 8, 6], [1, 5, 7, 3],
                [9, 18, 27, 36], [10, 19, 28, 37], [11, 20, 29, 38]]
        self._apply_permutation(perm)

    def d(self):
        perm = [[45, 47, 53, 51], [46, 50, 52, 48],
                [15, 42, 33, 24], [16, 43, 34, 25], [17, 44, 35, 26]]
        self._apply_permutation(perm)

    def r(self):
        perm = [[27, 29, 35, 33], [28, 32, 34, 30],
                [2, 20, 47, 43], [5, 23, 50, 40], [8, 26, 53, 37]]
        self._apply_permutation(perm)

    def l(self):
        perm = [[9, 11, 17, 15], [10, 14, 16, 12],
                [0, 36, 45, 18], [3, 39, 48, 21], [6, 42, 51, 24]]
        self._apply_permutation(perm)

    def f(self):
        perm = [[18, 20, 26, 24], [19, 23, 25, 21],
                [6, 27, 47, 16], [7, 30, 46, 13], [8, 33, 45, 10]]
        self._apply_permutation(perm)

    def b(self):
        perm = [[36, 38, 44, 42], [37, 41, 43, 39],
                [0, 11, 53, 35], [1, 14, 52, 32], [2, 17, 51, 29]]
        self._apply_permutation(perm)

    def u_prime(self): self.u(); self.u(); self.u()
    def u2(self): self.u(); self.u()
    def d_prime(self): self.d(); self.d(); self.d()
    def d2(self): self.d(); self.d()
    def r_prime(self): self.r(); self.r(); self.r()
    def r2(self): self.r(); self.r()
    def l_prime(self): self.l(); self.l(); self.l()
    def l2(self): self.l(); self.l()
    def f_prime(self): self.f(); self.f(); self.f()
    def f2(self): self.f(); self.f()
    def b_prime(self): self.b(); self.b(); self.b()
    def b2(self): self.b(); self.b()

    def execute_sequence(self, sequence):
        moves_map = {
            "U": self.u, "U'": self.u_prime, "U2": self.u2,
            "D": self.d, "D'": self.d_prime, "D2": self.d2,
            "L": self.l, "L'": self.l_prime, "L2": self.l2,
            "R": self.r, "R'": self.r_prime, "R2": self.r2,
            "F": self.f, "F'": self.f_prime, "F2": self.f2,
            "B": self.b, "B'": self.b_prime, "B2": self.b2,
        }
        for move_str in sequence.split():
            if move_str in moves_map:
                moves_map[move_str]()
