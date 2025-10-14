def compare_files(file1_path, file2_path):
    # Open both files
    with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()

    # Find the maximum number of lines
    max_len = max(len(file1_lines), len(file2_lines))

    for i in range(max_len):
        line1 = file1_lines[i].strip() if i < len(file1_lines) else "<no line>"
        line2 = file2_lines[i].strip() if i < len(file2_lines) else "<no line>"

        if line1 != line2:
            print(f"Difference on line {i+1}:")
            print(f"  File1: {line1}")
            print(f"  File2: {line2}")
            print()

if __name__ == "__main__":
    file1 = "uno_gui_revised.py"  # Replace with your file path
    file2 = "uno_gui_revised copy.py"  # Replace with your file path
    compare_files(file1, file2)
