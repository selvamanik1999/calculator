import re
import sys


class EvaluatePostFix:
    def __init__(self, spreadsheet_obj):
        self.stack = []
        self.top = -1
        self.spreadsheet_obj = spreadsheet_obj

    def pop(self):
        if self.top == -1:
            return
        else:
            self.top -= 1
            return self.stack.pop()

    def push(self, i):
        self.top += 1
        self.stack.append(i)

    def evaluate(self, expression):
        for curr in [x.strip() for x in expression.split(' ')]:
            if curr.lstrip('-').isdigit():  # handle negative numbers
                num = int(curr)
                self.push(int(num))
            elif curr in ['+', '-', '/', '*']:
                val1 = self.pop()
                val2 = self.pop()
                if curr == '/':  # do div separately to avoid divide by zero error
                    if val1 == 0:
                        # raise ("Invalid input {}: arithmatic error - not divided by zero".format(expression))
                        print("Invalid expression {}\nArithmatic error - cannnot divided by zero".format(expression))
                        sys.exit(1)
                    self.push(val2 / val1)
                else:
                    switch_case = {'+': val2 + val1, '-': val2 - val1, '*': val2 * val1}
                    self.push(switch_case.get(curr))
            else:
                self.push(self.spreadsheet_obj.resolve_nested_column(curr))
        return self.pop()


class SpreadSheet:

    def __init__(self):
        self.row = 0
        self.col = 0
        self.spreadsheet = []
        self.visited = set()
        self.resolved = {}  # memoize

    def titleToNumber(self, expression):
        res = 0
        for c in expression:
            res = res * 26 + ord(c) - ord('A') + 1
        return res

    def get_row_col_for_column(self, expression):
        title, num = re.match("([a-zA-Z]+)([0-9]+)", expression).groups()
        curr_row, curr_col = int(num) - 1, int(self.titleToNumber(title)) - 1
        return curr_row, curr_col

    def get_input(self):
        self.row, self.col = map(int, input().split(" "))
        self.spreadsheet = [[""] * self.col for r in range(self.row)]
        for curr_col in range(self.col):
            for curr_row in range(self.row):
                self.spreadsheet[curr_row][curr_col] = input()

    def get_output(self):
        output = [[0] * self.col for r in range(self.row)]
        for curr_col in range(self.col):
            for curr_row in range(self.row):
                expression = self.spreadsheet[curr_row][curr_col]
                output[curr_row][curr_col] = EvaluatePostFix(self).evaluate(expression)
        return output

    def resolve_nested_column(self, column_value):
        if column_value in self.resolved:  # cache - dont resolve it again
            return self.resolved[column_value]
        if column_value in self.visited:
            # raise Exception("Cycle detected")
            print("Cycle detected")
            sys.exit(1)
        self.visited.add(column_value)
        row_val, col_val = self.get_row_col_for_column(column_value)
        result = EvaluatePostFix(self).evaluate(self.spreadsheet[row_val][col_val])
        self.visited.remove(column_value)
        return result

    def print_output(self, output):
        print(self.row, self.col)
        for curr_col in range(self.col):
            for curr_row in range(self.row):
                print("{0:.5f}".format(output[curr_row][curr_col]))

    def start(self):
        self.get_input()
        output = self.get_output()
        self.print_output(output)


if __name__ == '__main__':
    spreadsheet = SpreadSheet()
    spreadsheet.start()
