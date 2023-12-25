__all__ = (
    'ast_to_py',
    'file_to_py',
    'parse',
    'py_to_scuff',
    'scuff_to_py',
    'unparse',
)


import os
from ast import AST, Module
from os import PathLike

from .compiler import Compiler
from .lexer import Lexer
from .parser import RecursiveDescentParser, FileParser, PyParser


type PythonData = str
type ScuffText = str


def parse(file: PathLike = None, *, string: ScuffText = None) -> Module:
    '''
    Parse Scuff text or a file containing it and return its AST.

    :param file: The file to parse
    :type file: :class:`PathLike`
    '''
    if string is None:
        return FileParser(file).parse()
    if file is None:
        return RecursiveDescentParser(string=string).parse()
    raise ValueError(
        "A `file` argument is required when `string` is not given or None."
    )


def unparse(node: AST) -> ScuffText:
    '''
    Convert an AST back into Scuff text.

    :param node: The AST to unparse
    :type node: :class:`AST`
    '''
    return Unparser().unparse(node)


def ast_to_py(node: AST) -> PythonData:
    '''
    Convert an AST to Python data.

    :param node: The AST to convert
    :type node: :class:`AST`
    '''
    return Compiler().compile(node)


def py_to_scuff(data: PythonData) -> ScuffText:
    '''
    Convert Python data to Scuff.

    :param data: The data to convert
    :type data: :class:`PythonData`
    '''
    return PyParser.to_scuff(data)


def scuff_to_py(string: ScuffText) -> PythonData:
    '''
    Convert Scuff to Python data.

    :param string: The text to parse
    :type string: :class:`ScuffText`
    '''
    module = RecursiveDescentParser(string=string).parse()
    return Compiler().compile(module)


def file_to_py(file: PathLike) -> PythonData:
    '''
    Parse a Scuff file and convert it to Python data.

    :param file: The file to parse
    :type file: :class:`PathLike`
    '''
    absolute = os.path.abspath(os.path.expanduser(file))
    module = FileParser(absolute).parse()
    return Compiler().compile(module)

