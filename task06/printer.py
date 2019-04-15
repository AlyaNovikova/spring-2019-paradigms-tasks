import model


class PrettyPrinter(model.ASTNodeVisitor):
    @staticmethod
    def _add_indent_level(exprs):
        return ['    ' + expr for expr in exprs]

    def visit_number(self, number):
        return [f'{number.value};']

    def visit_function(self, function):
        raise TypeError('Function node can not be processed')

    def visit_function_definition(self, func_def):
        args_str = ', '.join(func_def.function.args)
        body = sum((expr.accept(self) for expr in func_def.function.body), [])

        res = [f'def {func_def.name}({args_str}) {{']
        res += self._add_indent_level(body)
        res.append('}')

        return res

    def visit_conditional(self, conditional):
        cond = conditional.condition.accept(self)[0][:-1]
        if_true = sum((expr.accept(self)
                       for expr in conditional.if_true or []), [])
        if_false = sum((expr.accept(self)
                        for expr in conditional.if_false or []), [])

        res = [f'if ({cond}) {{']
        res += self._add_indent_level(if_true)
        if if_false:
            res.append('} else {')
            res += self._add_indent_level(if_false)
        res += '}'

        return res

    def visit_print(self, print_):
        expr = print_.expr.accept(self)
        return [f'print {expr[0]}']

    def visit_read(self, read):
        return [f'read {read.name};']

    def visit_function_call(self, func_call):
        func = func_call.fun_expr.accept(self)[0][:-1]
        args = [arg.accept(self)[0][:-1] for arg in func_call.args]
        return [f'{func}({", ".join(args)});']

    def visit_reference(self, reference):
        return [f'{reference.name};']

    def visit_binary_operation(self, binary_op):
        lhs = binary_op.lhs.accept(self)[0][:-1]
        rhs = binary_op.rhs.accept(self)[0][:-1]
        return [f'({lhs} {binary_op.op} {rhs});']

    def visit_unary_operation(self, unary_op):
        expr = unary_op.expr.accept(self)[0][:-1]
        return [f'{unary_op.op}({expr});']


def pretty_print(expr):
    print('\n'.join(expr.accept(PrettyPrinter())))
