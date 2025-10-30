# Flappy Bird Demo Mode

## Overview

The Flappy Bird game now includes a **demo mode** where an AI plays the game automatically. The AI navigates through obstacles, saves scores to a leaderboard, and continuously replays the game.

## Features

### Demo Mode
- **Automatic gameplay**: AI makes intelligent decisions to navigate through obstacles
- **Auto-start**: Game starts automatically after 1.5 seconds on the intro screen
- **Auto-restart**: Game restarts automatically 2 seconds after game over
- **Continuous play**: Keeps playing indefinitely until manually stopped
- **Visual indicators**: "DEMO MODE" shown on intro screen, "DEMO" shown during gameplay

### AI Player
- **Physics-based navigation**: Analyzes obstacle positions and Mona's velocity
- **Smart jumping**: Calculates optimal jump timing to pass through gaps
- **Altitude management**: Maintains safe flying height when no obstacles are nearby
- **Performance optimized**: Decision-making completes within single frame
- **Crash-resistant**: Comprehensive error handling prevents game crashes

### Leaderboard System
- **Persistent storage**: Scores saved to `/system/apps/flappy/scores.txt`
- **Top 10 tracking**: Maintains the highest 10 scores
- **Player differentiation**: Tracks whether score is from DEMO or HUMAN player
- **High score display**: Shows current high score on game over screen
- **Fail-safe design**: Handles file system errors gracefully

## Usage

### Playing in Demo Mode
1. Launch the Flappy Bird app
2. The game starts in demo mode by default
3. Watch the AI play automatically
4. Scores are saved to the leaderboard after each game
5. Game restarts automatically after game over

### Switching to Manual Mode
- Press **Button C** on the intro screen to toggle between demo and manual modes
- In manual mode, press **Button A** to start and jump

### Switching Back to Demo Mode
- Press **Button C** again to return to demo mode

## Technical Details

### AI Decision Logic

The AI uses a physics-based approach to make jump decisions:

1. **Obstacle Detection**: Scans for obstacles within 80 pixels ahead
2. **Gap Analysis**: Calculates the center of gaps between top and bottom pipes
3. **Position Prediction**: Estimates future position based on current velocity
4. **Jump Timing**: 
   - Jumps when falling below gap center
   - Maintains altitude when no obstacles nearby
   - Respects 200ms minimum interval between jumps

### Performance Characteristics

- **Frame rate**: Runs at game's native frame rate (varies by hardware)
- **Processing time**: AI decision completes within single frame
- **Memory usage**: Minimal - only stores last jump time and constants
- **Jump frequency**: Maximum 5 jumps per second (200ms interval)

### Safety Features

- **Exception handling**: All AI operations wrapped in try-catch blocks
- **State validation**: Checks if Mona is alive before making decisions
- **File I/O safety**: Leaderboard operations fail silently on errors
- **No blocking operations**: All calculations are instantaneous

## Files

- `__init__.py` - Main game file with demo mode integration
- `ai_player.py` - AI decision-making logic
- `leaderboard.py` - Score persistence system
- `scores.txt` - Leaderboard data (created automatically)

## Troubleshooting

### Demo mode not working
- Ensure all three files are present in the flappy app directory
- Check that the badge has write permissions to `/system/apps/flappy/`

### Scores not saving
- The game will continue to work even if scores can't be saved
- Check filesystem permissions and available storage space

### AI performance issues
- The AI is designed to work within the badge's constraints
- If the badge is under heavy load, AI decisions may be less optimal

## Future Enhancements

Potential improvements for the demo mode:

- Adjustable AI difficulty levels
- Statistics tracking (average score, best run, etc.)
- Online leaderboard integration
- Multiple AI strategies to choose from
- Training mode that learns from failures
