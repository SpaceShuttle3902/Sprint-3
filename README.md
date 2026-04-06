# Peg Solitaire – Sprint 3

## Overview
This project is a Peg Solitaire game implemented in Python using object-oriented design principles. It supports both manual and automated gameplay, along with multiple board types and sizes.

This project was developed for CS449 to demonstrate inheritance, modularity, and software design concepts.

## Features
- Multiple board types: English, Diamond, Hexagon
- Adjustable board size
- Manual gameplay (user clicks to move pegs)
- Automated gameplay (random valid moves)
- Randomize board (manual mode only)
- Game-over detection
- GUI built with Tkinter

## Project Structure
game_logic.py   - Core game logic and class hierarchy  
gui.py          - Graphical user interface  
test_game.py    - Unit tests  

## Design
The project uses a class hierarchy:
- PegSolitaireGame (base class)
- ManualPegSolitaireGame (adds randomization)
- AutomatedPegSolitaireGame (adds auto-move)

Concepts used:
- Inheritance for code reuse
- Encapsulation to protect board state
- Separation of concerns (logic vs GUI)

## How to Run

Run the game:
python gui.py

Run tests:
python -m unittest test_game.py

## Testing
Tests include:
- Board initialization
- Valid move execution
- Game-over detection
- Automated moves
- Randomization behavior

## Author
Efren
CS449 – Sprint 3
