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


class ASTNode(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def evaluate(self, scope):
        """
        Запускает вычисление текущего узла синтаксического дерева
        в заданной области видимости и возвращает результат вычисления.
        """


class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return self.value

    def evaluate(self, scope):
        return self


class Function(ASTNode):
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        return self


class FunctionDefinition(ASTNode):
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


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


class Print(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        res = self.expr.evaluate(scope)
        print(res.value)
        return res


class Read(ASTNode):
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        val = Number(int(input()))
        scope[self.name] = val
        return val


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


class Reference(ASTNode):
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


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
