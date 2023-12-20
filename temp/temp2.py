import threading

class CommandHistory:
    def __init__(self):
        self.history = []
        self.index = 0

    def add_command(self, command):
        self.history.append(command)
        self.index = len(self.history)

    def get_previous_command(self):
        if self.history:
            self.index = max(0, self.index - 1)
            return self.history[self.index]
        return None

    def get_next_command(self):
        if self.history:
            self.index = min(len(self.history) - 1, self.index + 1)
            return self.history[self.index]
        return None

command_history = CommandHistory()

def handle_command(command):
    # Add your command handling code here
    print(f"Executing command: {command}")

def command_loop():
    while True:
        command = input("Enter command: ")
        if command == 'up':
            command = command_history.get_previous_command()
        elif command == 'down':
            command = command_history.get_next_command()
        else:
            command_history.add_command(command)
        if command:
            handle_command(command)

command_thread = threading.Thread(target=command_loop)
command_thread.start()