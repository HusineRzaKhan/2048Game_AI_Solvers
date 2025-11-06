# 2048 Game with AI Solvers

This is an implementation of the popular 2048 game with two different AI solving strategies: Alpha-Beta Pruning and Min-Max algorithms. The game features both manual play mode and AI-assisted solving.

## Creator
- Hussain Raza Khan
- HussainRazaKhanBaloch@gmail.com
- https://github.com/HusineRzaKhan

## Features

- Classic 2048 game implementation with GUI using Tkinter
- Two AI solving strategies:
  - Alpha-Beta Pruning
  - Min-Max Algorithm
- Manual play mode with keyboard controls
- Real-time visualization of AI moves
- Configurable AI search depth

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)

## Project Structure

The project contains two main implementations:

### 2048AlphaBeta/
- `Model.py` - Core game logic and state management
- `GameController.py` - Game control and AI integration
- `GameManager.py` - Abstract base classes for game nodes and players
- `GameUI.py` - GUI implementation using Tkinter
- `Search.py` - Alpha-Beta pruning algorithm implementation
- `display.py` - Game board visualization

### 2048MinMax/
Similar structure with Min-Max algorithm implementation

## How to Run

1. Clone the repository
2. Navigate to the project directory
3. Run the game:
   ```bash
   python 2048AlphaBeta/GameUI.py   # For Alpha-Beta version
   # OR
   python 2048MinMax/GameUI.py      # For Min-Max version
   ```

## Controls

- **Arrow Keys**: Move tiles (Manual mode)
- **Ctrl+A**: Start AI solver
- **Ctrl+S**: Stop AI solver
- **Ctrl+R**: Restart game

## AI Strategy

The AI uses the following heuristics to evaluate board states:
- Empty tile availability
- Largest value in corner
- Board monotonicity (increasing/decreasing patterns)
- Merge possibilities

## Configuration

You can adjust the AI's search depth by modifying the `plies` variable in the `GameController` class.

## Contributing

Feel free to fork the project and submit pull requests. Areas for improvement include:
- Additional AI strategies
- Performance optimizations
- Enhanced UI features
- Better heuristics for AI decision making

## License

This project is open source and available under the MIT License.