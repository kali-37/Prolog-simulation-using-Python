class ReadLine:
    def __init__(self):
        self.buffer = []
        self.history = []  # Store command history
        self.history_index = 0  # Index for navigating history

    def add_to_buffer(self, text):
        self.buffer.extend(text)

    def clear_buffer(self):
        self.buffer = []

    def delete_last_character(self):
        if self.buffer:
            self.buffer.pop()

    def get_line(self):
        return ''.join(self.buffer)

    def add_to_history(self, line):
        self.history.append(line)

    def handle_up_arrow(self):
        if self.history:
            if self.history_index > 0:
                self.history_index -= 1
            return self.history[self.history_index]
        return ''

    def handle_down_arrow(self):
        if self.history:
            if self.history_index < len(self.history) - 1:
                self.history_index += 1
            return self.history[self.history_index]
        return ''

# Example Usage:
reader = ReadLine()

while True:
    user_input = input('Enter text: ')
    
    if user_input == 'exit':
        break
    
    if user_input == 'clear':
        reader.clear_buffer()
    elif user_input == 'delete':
        reader.delete_last_character()
    elif user_input == 'up':
        current_line = reader.handle_up_arrow()
        reader.clear_buffer()
        reader.add_to_buffer(list(current_line))
    elif user_input == 'down':
        current_line = reader.handle_down_arrow()
        reader.clear_buffer()
        reader.add_to_buffer(list(current_line))
    else:
        reader.add_to_buffer(list(user_input))
        reader.add_to_history(user_input)
    
    current_line = reader.get_line()
    print(f'Current line: {current_line}')
