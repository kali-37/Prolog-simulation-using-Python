# Open a file in read mode
with open('grammars.txt', 'r') as file:
    # Define a function to read chunks of data
    def read_chunk():
        return file.read(10)  # Read 10 bytes at a time
    
    # Use iter() with the read_chunk() function and an empty string as the sentinel value
    for chunk in iter(file.read,""):
        # Process each chunk (print in this example)
        print("Chunk:", chunk)




# top 50 IT quiz of 2023 -2024
# 1. What is the full form of HTML?
# 2. What is the full form of CSS?
# 3. What is the full form of JS?
# 4. What is the full form of PHP? Full form of PHP is 