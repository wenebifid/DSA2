class SparseMatrix:
    def __init__(self, matrix_file_path=None, num_rows=0, num_cols=0):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.data = {}

        if matrix_file_path:
            self.load_from_file(matrix_file_path)
        else:
            self.data = {}

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()

            # Remove whitespaces and ignore empty lines
            lines = [line.strip() for line in lines if line.strip()]
            if len(lines) < 2:
                raise ValueError("Input file has wrong format")

            # First two lines: rows and columns
            self.num_rows = int(lines[0].split('=')[1])
            self.num_cols = int(lines[1].split('=')[1])

            for line in lines[2:]:
                if not (line.startswith("(") and line.endswith(")")):
                    raise ValueError("Input file has wrong format")
                
                content = line[1:-1].strip()
                parts = content.split(',')
                if len(parts) != 3:
                    raise ValueError("Input file has wrong format")
                
                row, col, value = map(int, parts)
                self.set_element(row, col, value)

        except Exception as e:
            raise ValueError("Input file has wrong format") from e

    def get_element(self, curr_row, curr_col):
        return self.data.get((curr_row, curr_col), 0)

    def set_element(self, curr_row, curr_col, value):
        if value != 0:
            self.data[(curr_row, curr_col)] = value
        elif (curr_row, curr_col) in self.data:
            del self.data[(curr_row, curr_col)]

    def add(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices dimensions do not match for addition")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        
        for (row, col), value in self.data.items():
            result.set_element(row, col, value + other.get_element(row, col))
        
        return result

    def subtract(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices dimensions do not match for subtraction")

        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)

        for (row, col), value in self.data.items():
            result.set_element(row, col, value - other.get_element(row, col))

        return result

    def multiply(self, other):
        if self.num_cols != other.num_rows:
            raise ValueError("Matrices dimensions do not match for multiplication")

        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)

        for (row1, col1), value1 in self.data.items():
            for col2 in range(other.num_cols):
                value2 = other.get_element(col1, col2)
                if value2 != 0:
                    result_value = result.get_element(row1, col2) + (value1 * value2)
                    result.set_element(row1, col2, result_value)

        return result

def main():
    import sys
    
    print("Select an operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    choice = input("Enter choice (1/2/3): ")

    matrix1_path = input("Enter path for first matrix: ")
    matrix2_path = input("Enter path for second matrix: ")

    matrix1 = SparseMatrix(matrix1_path)
    matrix2 = SparseMatrix(matrix2_path)

    result = None

    if choice == '1':
        result = matrix1.add(matrix2)
    elif choice == '2':
        result = matrix1.subtract(matrix2)
    elif choice == '3':
        result = matrix1.multiply(matrix2)
    else:
        print("Invalid choice")
        return

    # Print result
    print("Result Sparse Matrix:")
    for (row, col), value in result.data.items():
        print(f"({row}, {col}, {value})")

if __name__ == "__main__":
    main()
