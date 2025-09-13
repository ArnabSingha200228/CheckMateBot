import chess
import chess.engine
import sys
import os

# --- Instructions ---
# 1. Install the required library: pip install python-chess
#
# 2. Download the Stockfish chess engine executable from:
#    https://stockfishchess.org/download/
#    Note the full path to the executable file.
#
# 3. Replace the placeholder below with the actual path to your Stockfish executable.
#    Example for Windows: "C:/Users/YourUsername/Downloads/stockfish/stockfish-windows-x86-64-avx2.exe"
#    Example for macOS/Linux: "/usr/local/bin/stockfish" or "/path/to/stockfish/stockfish"
STOCKFISH_PATH = "E:\\my programs\\chessboard\\virtual\\stockfish\\stockfish-windows-x86-64-avx2.exe"


def get_engine_reply(board, time_limit=0.1):
    """
    Connects to Stockfish, gets the best move for the current board, and returns it.

    Args:
        board (chess.Board): The current state of the chess board.
        time_limit (float): The maximum time in seconds for the engine to think.

    Returns:
        chess.Move or None: The engine's best move, or None if an error occurs.
    """
    engine = None
    try:
        # Popen_uci is a function that opens the engine process and communicates via UCI protocol.
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

        # Analyze the board with a time limit. You can adjust this for stronger play.
        result = engine.play(board, chess.engine.Limit(time=time_limit))
        return result.move
    except FileNotFoundError:
        print(f"Error: Stockfish executable not found at '{STOCKFISH_PATH}'.")
        print("Please check the path and make sure Stockfish is installed.")
        return None
    except Exception as e:
        print(f"An error occurred while communicating with the engine: {e}")
        return None
    finally:
        # Always quit the engine process to avoid resource leaks.
        if engine:
            engine.quit()


def main():
    """
    Main function to run the interactive chess game logic.
    """
    print("Welcome to the Chess Move Replier!")
    print(
        "Enter a FEN string to set the starting position, or leave blank for a new game."
    )
    fen_string = input("Enter FEN: ").strip()

    try:
        if fen_string:
            board = chess.Board(fen_string)
        else:
            board = chess.Board()

        # Main loop to take moves and get replies.
        while True:
            print("\nCurrent Board State:")
            print(board)

            if board.is_game_over():
                print("\nGame Over! Result:", board.result())
                break

            if board.turn == chess.WHITE:
                print("It's White's turn.")
            else:
                print("It's Black's turn.")

            user_move_uci = input("\nEnter your move in UCI format (e.g., e2e4): ")

            if user_move_uci.lower() in ["quit", "exit"]:
                print("Exiting game.")
                break

            try:
                # Convert the user's UCI string to a move object.
                user_move = chess.Move.from_uci(user_move_uci)

                # Check if the move is legal before pushing it to the board.
                if user_move in board.legal_moves:
                    board.push(user_move)

                    # Get the engine's reply only if the game is not over.
                    if not board.is_game_over():
                        print("Engine is thinking...")
                        engine_reply_move = get_engine_reply(board)
                        if engine_reply_move:
                            board.push(engine_reply_move)
                            print(f"\nEngine's reply move (UCI): {engine_reply_move}")
                        else:
                            # If the engine failed to reply, exit the loop.
                            break

                else:
                    print("That is not a legal move. Please try again.")

            except ValueError:
                print("Invalid UCI format. Please use a format like 'e2e4'.")

    except ValueError:
        print("Invalid FEN string. Please provide a valid FEN.")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting.")


if __name__ == "__main__":
    main()
