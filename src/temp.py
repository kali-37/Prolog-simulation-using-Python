# Open a file in read mode
with open('grammars.txt', 'r') as file:
    # Define a function to read chunks of data
    def read_chunk():
        return file.read(10)  # Read 10 bytes at a time
    
    # Use iter() with the read_chunk() function and an empty string as the sentinel value
    for chunk in iter(file.read,""):
        # Process each chunk (print in this example)
        print("Chunk:", chunk)
