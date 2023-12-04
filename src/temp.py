# # Open a file in read mode
# with open('grammars.txt', 'r') as file:
#     # Define a function to read chunks of data
#     def read_chunk():
#         return file.read(10)  # Read 10 bytes at a time
    
#     # Use iter() with the read_chunk() function and an empty string as the sentinel value
#     for chunk in iter(file.read,""):
#         # Process each chunk (print in this example)
#         print("Chunk:", chunk)


# def detect_arrow_key():
#     while True:
#         # Capture input character by character
#         key = input("Press an arrow key: ")

#         if key == '\x1b[A':  # Up arrow key ANSI escape sequence
#             print("Up arrow key pressed")
#         elif key == '\x1b[B':  # Down arrow key ANSI escape sequence
#             print("Down arrow key pressed")
#         elif key == '\x1b[C':  # Right arrow key ANSI escape sequence
#             print("Right arrow key pressed")
#         elif key == '\x1b[D':  # Left arrow key ANSI escape sequence
#             print("Left arrow key pressed")

#         elif key == 'q':  # Press 'q' to quit
#             break

# detect_arrow_key()


import sys
import tty
import termios

def detect_arrow_key():
    # Save the original terminal settings
    original_settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setcbreak(sys.stdin.fileno())  # Set the terminal to raw mode
        while True:
            key = sys.stdin.read(1)
            if key == '\x1b':  # Check for escape character
                key = sys.stdin.read(2)  # Read the next two characters for arrow keys
                if key == '[A':  # Up arrow key
                    print("\rUp arrow key pressed")
                elif key == '[B':  # Down arrow key
                    print("\rDown arrow key pressed")
                elif key == '[C':  # Right arrow key
                    print("\rRight arrow key pressed")
                elif key == '[D':  # Left arrow key
                    print("\rLeft arrow key pressed")
            elif key == 'q':  # Press 'q' to quit
                break

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_settings)  # Restore original terminal settings

detect_arrow_key()
