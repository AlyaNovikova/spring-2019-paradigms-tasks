#!/usr/bin/env python3
import abc


class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}

    def __getitem__(self, var_name):
        if var_name in self.variables:
            return self.variables[var_name]
        elif self.parent:
            return self.parent[var_name]
        else:
            raise KeyError(var_name)

    def __setitem__(self, var_name, value):
        self.variables[var_name] = value


class ASTNodeVisitor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def visit_number(self, number):
        pass

    def visit_function(self, function):
        pass

    def visit_function_definition(self, func_def):
        pass

    def visit_conditional(self, conditional):
        pass

    def visit_print(self, print):
        pass

    def visit_read(self, read):
        pass

    def visit_function_call(self, func_call):
        pass

    def visit_reference(self, reference):
        pass

    def visit_binary_operation(self, binary_op):
        pass

    def visit_unary_operation(self, unary_op):
        pass


class ASTNode(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def evaluate(self, scope):
        pass

    @abc.abstractmethod
    def accept(self, visitor):
        pass


class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return self.value

    def evaluate(self, scope):
        return self

    def accept(self, visitor):
        return visitor.visit_number(self)


class Function(ASTNode):
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        return self

    def accept(self, visitor):
        return visitor.visit_function(self)


class FunctionDefinition(ASTNode):
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

    def accept(self, visitor):
        return visitor.visit_function_definition(self)


class Conditional(ASTNode):
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        if self.condition.evaluate(scope) == Number(0):
            to_evaluate = self.if_false
        else:
            to_evaluate = self.if_true
        res = None
        for statement in to_evaluate or []:
            res = statement.evaluate(scope)
        return res

    def accept(self, visitor):
        return visitor.visit_conditional(self)


class Print(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        res = self.expr.evaluate(scope)
        print(res.value)
        return res

    def accept(self, visitor):
        return visitor.visit_print(self)


class Read(ASTNode):
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        val = Number(int(input()))
        scope[self.name] = val
        return val

    def accept(self, visitor):
        return visitor.visit_read(self)


class FunctionCall(ASTNode):
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for arg_name, arg_expr in zip(function.args, self.args):
            call_scope[arg_name] = arg_expr.evaluate(scope)
        res = None
        for statement in function.body:
            res = statement.evaluate(call_scope)
        return res

    def accept(self, visitor):
        return visitor.visit_function_call(self)


class Reference(ASTNode):
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

    def accept(self, visitor):
        return visitor.visit_reference(self)


class BinaryOperation(ASTNode):
    OPERATIONS = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x // y,
        '%': lambda x, y: x % y,
        '==': lambda x, y: x == y,
        '!=': lambda x, y: x != y,
        '<': lambda x, y: x < y,
        '>': lambda x, y: x > y,
        '<=': lambda x, y: x <= y,
        '>=': lambda x, y: x >= y,
        '&&': lambda x, y: x and y,
        '||': lambda x, y: x or y
    }

    def __init__(self, lhs, op, rhs):
        if op not in self.OPERATIONS:
            raise NotImplementedError(op)
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        lhs = self.lhs.evaluate(scope).value
        rhs = self.rhs.evaluate(scope).value
        return Number(int(self.OPERATIONS[self.op](lhs, rhs)))

    def accept(self, visitor):
        return visitor.visit_binary_operation(self)


class UnaryOperation(ASTNode):
    OPERATIONS = {
        '-': lambda x: -x,
        '!': lambda x: not x
    }

    def __init__(self, op, expr):
        if op not in self.OPERATIONS:
            raise NotImplementedError(op)
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        expr = self.expr.evaluate(scope).value
        return Number(int(self.OPERATIONS[self.op](expr)))

    def accept(self, visitor):
        return visitor.visit_unary_operation(self)
