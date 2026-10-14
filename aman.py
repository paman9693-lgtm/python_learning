#f= open('n!.txt','x')
f= open('n1.txt','a')
print(f.mode)
print(f.name)
print(f.writable())
print(f.readable())
print(f.closed)
print(f.encoding)
def create_and_write_file(filename):
    # 1. Create and write to a file ('w' mode overwrites existing content)
    print(f"Creating and writing to '{filename}'...")
    
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Hello, World!\n")
        file.write("This is a new file created using Python.\n")
        file.write("File handling is simple and efficient.\n")
    
    print("File written successfully.\n")


def read_file(filename):
    # 2. Read from the file ('r' mode reads content)
    print(f"Reading contents of '{filename}':")
    print("-" * 30)
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    
    print("-" * 30)


def append_to_file(filename):
    # 3. Append new data to the file ('a' mode adds to the end without overwriting)
    print(f"Appending new text to '{filename}'...")
    
    with open(filename, "a", encoding="utf-8") as file:
        file.write("This line was appended later.\n")
        
    print("Data appended successfully.\n")


if __name__ == "__main__":
    file_name = "sample.txt"
    
    # Run the file operations
    create_and_write_file(file_name)
    read_file(file_name)
    append_to_file(file_name)
    
    # Read again to see the appended changes
    print("Reading file after append:")
    read_file(file_name)