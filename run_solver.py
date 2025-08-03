import time
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import box
import cube
import solver
import optimize
import optimal_solver
from optimal_cube import OptimalCube
from colorama import Fore, Style

console = Console()

def translate_scramble(scramble):
    # Translate scramble notation for solver compatibility
    translated_moves = []
    for move in scramble.split():
        if '2' in move:
            base_move = move[0]
            translated_moves.extend([base_move, base_move])
        elif "'" in move:
            translated_moves.append(f"{move[0]}i")
        else:
            translated_moves.append(move)
    return " ".join(translated_moves)

def print_cube(cube_obj):
    # Print cube using rich markup colors
    colors = {
        'W': "[white]W[/]",
        'Y': "[yellow]Y[/]",
        'G': "[green]G[/]",
        'B': "[blue]B[/]",
        'R': "[red]R[/]",
        'O': "[orange]O[/]"
    }
    stringified = str(cube_obj)
    visual = "".join(colors.get(c, c) for c in stringified)
    console.print(visual)

def colorize(c):
    # Terminal background color for facelets
    color_map = {
        'W': '\033[107m',
        'Y': '\033[103m',
        'R': '\033[101m',
        'O': '\033[43m',
        'G': '\033[102m',
        'B': '\033[104m',
        None: '\033[0m',
    }
    return f"{color_map.get(c, '')}  \033[0m"

def print_flat_cube(cube):
    # Print cube colors in flat net layout
    colors = cube._color_list()
    def block(i): return colorize(colors[i])
    net = (
        f"        {block(0)}{block(1)}{block(2)}\n"
        f"        {block(3)}{block(4)}{block(5)}\n"
        f"        {block(6)}{block(7)}{block(8)}\n"
        f"{block(9)}{block(10)}{block(11)} {block(12)}{block(13)}{block(14)} {block(15)}{block(16)}{block(17)} {block(18)}{block(19)}{block(20)}\n"
        f"{block(21)}{block(22)}{block(23)} {block(24)}{block(25)}{block(26)} {block(27)}{block(28)}{block(29)} {block(30)}{block(31)}{block(32)}\n"
        f"{block(33)}{block(34)}{block(35)} {block(36)}{block(37)}{block(38)} {block(39)}{block(40)}{block(41)} {block(42)}{block(43)}{block(44)}\n"
        f"        {block(45)}{block(46)}{block(47)}\n"
        f"        {block(48)}{block(49)}{block(50)}\n"
        f"        {block(51)}{block(52)}{block(53)}\n"
    )
    print(net)

def solve_with_lbl(scramble_algo):
    # Solve cube with Layer-by-Layer beginner method
    translated_moves = []
    for move in scramble_algo.split():
        if '2' in move:
            base_move = move[0]
            translated_moves.extend([base_move, base_move])
        elif "'" in move:
            translated_moves.append(f"{move[0]}i")
        else:
            translated_moves.append(move)
    lbl_scramble = " ".join(translated_moves)

    print("\n--- Scrambling Cube for LBL Solver ---")
    print(f"(Note: Translating scramble '{scramble_algo}' to '{lbl_scramble}' for this solver)")

    solved_str = 'W'*9 + ('O'*3+'G'*3+'R'*3+'B'*3)*3 + 'Y'*9
    walkthrough_cube = cube.Cube(solved_str)
    walkthrough_cube.sequence(lbl_scramble)
    cube_to_solve = cube.Cube(walkthrough_cube)

    print_flat_cube(walkthrough_cube)
    print("\n⏳ Solving with Beginner's Method...")
    start_time = time.time()

    solver_instance = solver.Solver(cube_to_solve)
    solver_instance.solve()
    duration = time.time() - start_time

    if not cube_to_solve.is_solved():
        print(f"{Fore.RED}Could not solve the cube.{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}Solved! Time taken: {duration:.2f} seconds.{Style.RESET_ALL}")

    opt_moves = optimize.optimize_moves(solver_instance.moves)
    print(f"Solution ({len(opt_moves)} moves): {' '.join(opt_moves)}")
    print("-" * 30)

    print("\nFinal Cube State:")
    colors = {'W': Fore.WHITE, 'Y': Fore.YELLOW, 'G': Fore.GREEN, 'B': Fore.BLUE, 'R': Fore.RED, 'O': Fore.MAGENTA}
    for char in str(cube_to_solve):
        print(colors.get(char, '') + char + Style.RESET_ALL, end='')
    print()

def solve_with_optimal(scramble_algo):
    # Solve cube optimally and show walkthrough if requested
    console.rule("[bold cyan]Optimal Solver[/]")
    walkthrough_cube = OptimalCube()
    walkthrough_cube.execute_sequence(scramble_algo)
    cube_to_solve = walkthrough_cube.clone()

    print_cube(walkthrough_cube)
    console.print(f"\n[cyan]Searching for optimal solution...[/]")

    start_time = time.time()
    solution = optimal_solver.solve(cube_to_solve)
    duration = time.time() - start_time

    console.print(f"\n[green]Solved in {duration:.2f} seconds[/]")
    console.print(f"Solution: [white]{solution}[/]")
    console.print(f"Moves: [bold]{len(solution.split())}[/]")

    choice = Prompt.ask("\nView optimal walkthrough? [y/n]").lower()
    if choice == 'y':
        for i, move in enumerate(solution.split()):
            console.print(f"\n[cyan]Step {i+1}:[/] Applying '[bold]{move}[/]'")
            walkthrough_cube.execute_sequence(move)
            print_cube(walkthrough_cube)
            time.sleep(1)

def run():
    # Main entrypoint: get scramble and solver choice
    console.rule("[bold green]Rubik's Cube Solver[/]")
    scramble = Prompt.ask("Enter scramble (e.g., R U R' U')")
    if not scramble:
        console.print("[red]No scramble entered. Exiting.[/]")
        return

    table = Table(title="Choose a Solver", box=box.ROUNDED)
    table.add_column("Option", style="cyan", justify="center")
    table.add_column("Method", style="magenta", justify="center")
    table.add_row("1", "Beginner's Method (Visual)")
    table.add_row("2", "Optimal Solver (Shortest Path)")

    console.print(table)
    choice = Prompt.ask("Enter your choice", choices=["1", "2"])

    if choice == "1":
        solve_with_lbl(scramble)
    else:
        solve_with_optimal(scramble)

