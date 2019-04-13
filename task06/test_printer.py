from textwrap import dedent

import pytest
from model import *
import printer


def test_print_printer():
    pretty_printer = printer.PrettyPrinter()
    assert Print(Number(42)).accept(pretty_printer) == ['print 42;']


def test_read_printer():
    pretty_printer = printer.PrettyPrinter()
    assert Read('x').accept(pretty_printer) == ['read x;']


def test_number_printer():
    pretty_printer = printer.PrettyPrinter()
    assert Number(10).accept(pretty_printer) == ['10;']


def test_reference_printer():
    pretty_printer = printer.PrettyPrinter()
    assert Reference('x').accept(pretty_printer) == ['x;']


def test_binary_operation_printer():
    pretty_printer = printer.PrettyPrinter()
    add = BinaryOperation(Number(2), '+', Number(3))
    mul = BinaryOperation(Number(1), '*', add)
    assert mul.accept(pretty_printer) == ['(1 * (2 + 3));']


def test_unary_operation_printer():
    pretty_printer = printer.PrettyPrinter()
    assert UnaryOperation(
        '-', Number(42)).accept(pretty_printer) == ['-42;']


def test_func_call_printer():
    pretty_printer = printer.PrettyPrinter()
    assert FunctionCall(
        Reference('foo'),
        [Number(1), Number(2), Number(3)]
    ).accept(pretty_printer) == ['foo(1, 2, 3);']


def test_conditional_printer():
    pretty_printer = printer.PrettyPrinter()
    assert Conditional(
        Number(42), [], []
    ).accept(pretty_printer) == ['if 42 {', '}']


def test_func_def_printer():
    pretty_printer = printer.PrettyPrinter()
    assert FunctionDefinition(
        "foo", Function([], [])
    ).accept(pretty_printer) == ['def foo() {', '}']


def test_end_to_end(capsys):
    printer.pretty_print(FunctionDefinition('main', Function(['arg1'], [
        Read('x'),
        Print(Reference('x')),
        Conditional(
            BinaryOperation(Number(2), '==', Number(3)),
            [
                Conditional(Number(1), [], [])
            ],
            [
                FunctionCall(Reference('exit'), [
                    UnaryOperation('-', Reference('arg1'))
                ])
            ],
        ),
    ])))

    out = capsys.readouterr().out.rstrip()
    expected = dedent('''\
        def main(arg1) {
            read x;
            print x;
            if (2 == 3) {
                if 1 {
                }
            } else {
                exit(-arg1);
            }
        }''')

    assert out.rstrip() == expected

    if __name__ == '__main__':
        pytest.main()
