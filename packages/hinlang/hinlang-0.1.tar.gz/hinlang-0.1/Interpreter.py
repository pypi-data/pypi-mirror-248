class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def interpret_file(self, file_path):
        with open(file_path, 'r') as file:
            code = file.read()
            self.interpret(code)

    def interpret(self, code):
        statements = code.split(';')
        for statement in statements:
            self.execute_statement(statement)

    def execute_statement(self, statement):
        statement = statement.strip()
        if statement.startswith("कार्यः"):
            self.execute_function_declaration(statement)
        elif "=" in statement:
            self.execute_variable_assignment(statement)
        elif statement.startswith("छापो"):
            self.execute_print_statement(statement)
        elif statement.startswith("यदि"):
            self.execute_if_statement(statement)
        elif statement.startswith("अन्यथा यदि"):
            self.execute_elif_statement(statement)
        elif statement.startswith("for"):
            self.execute_for_loop(statement)
        elif statement.startswith("while"):
            self.execute_while_loop(statement)

    def execute_variable_assignment(self, statement):
        variable, value = statement.split("=")
        variable = variable.strip()
        value = value.strip()
        if "संख्या" in value:
            value = int(value.split("संख्या")[1].strip())
        elif "शब्द" in value:
            value = value.split("शब्द")[1].strip().strip('"')
        elif "अक्षर" in value:
            value = value.split("अक्षर")[1].strip().strip("'")
        elif "सत्यासत्य" in value:
            value = True if value.split("सत्यासत्य")[1].strip().lower() == "सत्य" else False
        self.variables[variable] = value

    def execute_print_statement(self, statement):
        _, variable = statement.split("(")
        variable = variable.strip(");")
        if variable in self.variables:
            print(self.variables[variable])
        else:
            print(f"Error: Variable '{variable}' not found.")

    def execute_function_declaration(self, statement):
        _, function_body = statement.split("{")
        function_body = function_body.strip("}")
        self.functions["कार्यः"] = function_body

    def execute_if_statement(self, statement):
        _, condition, if_body = statement.split("{")
        condition = condition.strip("यदि").strip()
        if self.evaluate_condition(condition):
            self.execute_statement(if_body)
        elif "अन्यथा यदि" in statement:
            elif_body = statement.split("अन्यथा यदि")[1].split("{")[1].strip("}")
            self.execute_statement(elif_body)
        elif "अन्यथा" in statement:
            else_body = statement.split("अन्यथा")[1].strip("{").strip("}")
            self.execute_statement(else_body)

    def execute_elif_statement(self, statement):
        _, condition, elif_body = statement.split("{")
        condition = condition.strip("अन्यथा यदि").strip()
        if self.evaluate_condition(condition):
            self.execute_statement(elif_body)

    def execute_for_loop(self, statement):
        _, loop_params, loop_body = statement.split("{")
        start, end = map(int, loop_params.strip("for").strip().split("से"))
        for i in range(start, end + 1):
            self.variables["परिवर्तनशील"] = i
            self.execute_statement(loop_body)

    def execute_while_loop(self, statement):
        _, condition, loop_body = statement.split("{")
        condition = condition.strip("while").strip()
        while self.evaluate_condition(condition):
            self.execute_statement(loop_body)

    def evaluate_condition(self, condition):
        # A simple evaluation for conditions (assumes conditions involve variables and comparison operators)
        variable, operator, value = condition.split()
        variable = variable.strip()
        value = int(value) if "संख्या" in value else value
        if operator == "<" and self.variables[variable] < value:
            return True
        elif operator == ">" and self.variables[variable] > value:
            return True
        elif operator == "==" and self.variables[variable] == value:
            return True
        return False
