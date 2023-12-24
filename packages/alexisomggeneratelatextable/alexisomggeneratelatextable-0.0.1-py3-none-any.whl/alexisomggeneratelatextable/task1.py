import ast
from functools import reduce
from typing import List, Any

def generate_latex_table(matrix: List[List[Any]]) -> str:
    if not matrix:
        return ''

    num_columns = max(max([len(row) for row in matrix]), 1)

    def create_row(row: List[Any]) -> str:
        return ' & '.join(str(item) for item in row + ['']*(num_columns-len(row))) + ' \\\\\n\\hline\n'

    def column_alignment(num_columns: int) -> str:
        return '{|' + '|'.join(['c'] * num_columns) + '|}\n\\hline\n'
    
    return '\\begin{tabular}' + reduce(
            lambda latex, row: latex + create_row(row), 
            matrix, 
            column_alignment(num_columns),
        ) + '\\end{tabular}'

def main():
    print('Enter your matrix in Python list of lists format:')
    input_str = input()
    try:
        input_matrix = ast.literal_eval(input_str)
        if not isinstance(input_matrix, list) or not all(isinstance(row, list) for row in input_matrix):
            raise ValueError
    except:
        print('Invalid matrix format.')
        exit()

    latex_code = generate_latex_table(input_matrix)
    print(latex_code)

if __name__ == '__main__':
    main()
