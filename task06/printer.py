import model


class PrettyPrinter(model.ASTNodeVisitor):
    def visit_number(self, number):
        return [str(number.value)]

    def visit_function(self, function):
        pass

    def visit_function_definition(self, func_def):
        pass

    def visit_conditional(self, conditional):
        pass

    def visit_print(self, prnt):
        expr = prnt.expr.accept(self)
        return [f'print {expr[0]}']

    def visit_read(self, read):
        return [f'read {read.name}']

    def visit_function_call(self, func_call):
        pass

    def visit_reference(self, reference):
        return [reference.name]

    def visit_binary_operation(self, binary_op):
        lhs = binary_op.lhs.accept(self)
        rhs = binary_op.rhs.accept(self)
        return [f'({lhs[0]} {binary_op.op} {rhs[0]})']

    def visit_unary_operation(self, unary_op):
        expr = unary_op.expr.accept(self)
        return [f'{unary_op.op}{expr[0]}']
