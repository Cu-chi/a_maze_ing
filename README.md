*This project has been created as part of the 42 curriculum by equentin, mchauvin.*

## Description
**A-Maze-ing** is an interactive command-line application for generating, visualizing, and solving mazes. The project focuses on data structure manipulation (matrices), graph theory algorithms, and dynamic UI management within a terminal using ANSI escape sequences. The maze has to be reusable for futur project involving a maze. A seed is also needed to be able to reproduce the same maze again.

**Main Goals:**
- Generate both "perfect" (unicursal) and "imperfect" (braid) mazes.
- Integrate a static visual element (the "42" logo) within the procedural generation.
- Implement an automated solver to find the shortest path from entry to exit.

## Instructions

### Prerequisites
- **Python 3.10** or higher.
- A terminal supporting ANSI colors.
- Poetry (https://python-poetry.org/docs/)

### Installation & Execution
1. Clone the repository:
   git clone https://github.com/Cu-chi/a_maze_ing.git  
   If poetry isn't in the machine :
```sh
curl -sSL https://install.python-poetry.org | python3 -
```  

2. Run the program:  
```sh
make install
make run  
```  

3. Check norme:   
```sh
make lint
make lint-strict
``` 

4. Build package:  
```sh
make build-mazegen
```

5. Debug:  
```sh
make debug
```

**Controls**:
Arrow Keys: Navigate the menu.

Enter: Confirm selection.

Number Keys (0-9): Direct shortcut to menu options.

### Configuration & Structure
The project rely on an external configuration file: "config.txt", this file will contains the size of the desired maze, the entry and exit point of the main, the name of the output file, the perfect flag and the optional seed parameter:

width / height: Minimum dimensions 10x10.

entry / exit: Customizable coordinates (tuples).

perfect: If false, the generated maze will create a braid maze. If true the maze generated will be perfect.

seed: Optional parameter to replay a specific generation.

| Key         | Description                                        | Example              | Optional |
|-------------|----------------------------------------------------|----------------------|----------|
| WIDTH       | Maze width (number of cells)                       | WIDTH=20             | NO       |
| HEIGHT      | Maze height                                        | HEIGHT=20            | NO       |
| ENTRY       | "Entry coordinates (x,y)"                          | ENTRY=1,1            | NO       |
| EXIT        | "Exit coordinates (x,y)"                           | EXIT=2,2             | NO       |
| OUTPUT_FILE | Output filename                                    | OUTPUT_FILE=maze.txt | NO       |
| PERFECT     | Is the maze perfect? (True or False)               | PERFECT=True         | NO       |
| SEED        | Optional parameter to replay a specific generation | SEED=1245            | YES      |
| PATH_ANIM   | Optional parameter to animate or not the path      | PATH_ANIM=True       | YES (True by default)|
### Generation Algorithms
Implemented Algorithms:
DFS (Recursive Backtracking): Creates "perfect" mazes with long, winding paths by exploring depth-first.

HAK (Hunt-and-Kill): An iterative alternative that avoids Python’s recursion limit on large grids while maintaining perfect maze properties.

DFS_NOT_PERFECT: A variant that creates "Braid mazes" (cycles) by intentionally removing random walls after the initial generation.

Why these choices?  
The aim was to compare two different approaches to perfect maze generation (recursive vs. iterative) and to provide a "non-perfect" option to test the solver's robustness when faced with multiple possible paths.

### Reusable Code
Menu Class: Completely independent of the maze logic. It can be reused for any CLI project requiring an interactive interface, non-canonical terminal mode handling, and cursor manipulation.

BaseAlgorithm Class: A standardized interface allowing any new generation algorithm to be added simply by implementing a .generate() method.

### Project Management
Roles:  
mchauvin: - HAK Algorithm, parsing & error handling, makefile, first algorithm for path_finding.  
equentin: - DFS / Not-Perfect Algorithm, menu, vizualiser, package configuration.

At the beginning of the project, we made a plan and divide every task between us. The deeper in the project the more we started adding new things to optimize everything.  

Overall everything works relatively well, we could've had some more animation when we display the maze. The DFS Not-Perfect algorithm can also be improve, because it is pretty random and hardcoded.  


### Tools Used
Git: Version control.
Termios/Sys: Low-level handling of standard input (stdin) for interactive mode.
Poetry: https://python-poetry.org/docs
### Resources & AI
Maze Theory: Jamis Buck’s work on graph algorithms. (https://weblog.jamisbuck.org/projects)  
Terminal Documentation: termios man pages for non-canonical mode. (https://docs.python.org/fr/3/library/termios.html)  
Path_finding: https://levelup.gitconnected.com/solve-a-maze-with-python-e9f0580979a1

### AI Usage:
Gemini Pro was used to create a plan for each person to work on specific code. It was also used to get some information about new concept that we didn't use before like creating a menu, poetry, some git-hub command etc...  
Finally it was also used to check the grammar and vocabulary of this readme.

### Advanced Features
Color Rotation: Dynamic customization of walls, path, and "42" logo colors.  
Path Animation: The solver animates the path progression at a speed proportional to the path length.  
Multiple algorithm: Multiple algorithm to solve the maze.  
Switch command: The possibility to switch algorithm in the menu.  
Menu navigation: User friendly navigation system.  
