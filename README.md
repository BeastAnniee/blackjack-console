# blackjack-console
A console-based two-player Blackjack game implemented in Python, showcasing object-oriented programming and basic game logic.

## Overview
This project is a modular, console-based Blackjack game written in Python. It focuses on clean separation of concerns and maintainability. The game supports human input, an automated random player, and an AI player that uses simplified card counting (Hi-Lo) and a Monte Carlo simulation to inform decisions.

## Features
- Modular architecture:
  - `cartas.py`: Card and deck (Baraja)
  - `jugadores.py`: Player types (User, Random, AI, Dealer)
  - `motor.py`: Game engine (round flow, betting, dealing, settlement)
  - `estadisticas.py`: Text and optional graphical statistics
  - `juego_modular.py`: Entry point
- Players:
  - User: interact via console (hit/stand)
  - Random: makes random hit/stand decisions and random bets within limits
  - AI: Hi-Lo card counting + Monte Carlo simulation (N≈600 per decision) for informed hit/stand
  - Dealer: standard rules (hits until 17)
- Betting system with balances, wins/losses tracking
- Optional final statistics chart (requires `matplotlib`), with safe fallback to text
- Configurable delay between actions to simulate pacing; can be disabled for fast runs

## Project Structure
```
blackjack-console/
├─ requirements.txt
└─ src/
   ├─ cartas.py          # Card (Carta) and Deck (Baraja)
   ├─ jugadores.py       # Player classes: Usuario, JugadorAleatorio, JugadorIA, Crupier
   ├─ motor.py           # Blackjack engine (rounds, turns, settlement)
   ├─ estadisticas.py    # Stats printing and optional matplotlib bar chart
   └─ juego_modular.py   # Main entry point
```

## Requirements
- Python 3.9+
- Optional: `matplotlib` for charts

Install optional dependencies:
```bash
pip install -r requirements.txt
```

The game runs without `matplotlib`; you will still get textual statistics.

## Running
From the `src/` directory:
```bash
python juego_modular.py
```

Gameplay flow:
1. Place your bet (minimum 5, must not exceed your current balance).
2. Decide on each turn: `s` (hit) or `n` (stand).
3. Random and AI players take their turns, then the dealer.
4. Bets are settled and you can choose to play another round.

## Configuration
You can control pacing via the `usar_retrasos` flag in `src/juego_modular.py`:
```python
from motor import Blackjack

if __name__ == "__main__":
    # Fast mode (no artificial delays)
    juego = Blackjack(usar_retrasos=False)
    juego.iniciar_juego()
```

Other engine behaviors:
- The deck is automatically reshuffled when it reaches a minimum threshold.
- The AI adjusts bets using a simple true count derived from the Hi-Lo count and remaining deck size.

## Troubleshooting
- No charts appear / backend errors: If `matplotlib` is not installed or a display backend is unavailable, the game will print statistics in text and continue. Install matplotlib or configure an appropriate backend to see charts.
- Encoding / locale in console: Ensure your terminal supports UTF‑8 to display Spanish suits names correctly (Corazones, Diamantes, Tréboles, Picas).

## Contributing
Feel free to open issues or submit pull requests. Ideas welcome:
- Add split/double-down rules
- Multiple decks and shoe penetration settings
- Improve AI with basic strategy tables and more efficient simulations
- Unit tests for hand evaluation and settlement logic

## License
MIT License

---
Enjoy the game!
