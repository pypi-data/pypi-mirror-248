import io
import os
import random
import sys
import time

from tempfile import NamedTemporaryFile
from typing import Callable, Dict, List, Tuple, Union

try:
    from argparse_dataclass import dataclass as ap_dataclass
    from argparse_dataclass import ArgumentParser
except:
    ArgumentParser = "ArgumentParser"
    ap_dataclass = "ap_dataclass"


class SmtTranspilerPlugins:
    def visit_open(self, node, vargs):
        # TODO
        return None

    def visit_named_temp_file(self, node, vargs):
        # TODO
        return None

    def visit_textio_read(self, node, vargs):
        # TODO
        return None

    def visit_textio_write(self, node, vargs):
        # TODO
        return None

    def visit_ap_dataclass(self, cls):
        # Do whatever transformation the decorator does to cls here
        return cls

    def visit_range(self, node, vargs: List[str]) -> str:
        if len(node.args) == 1:
            return f"(0..{vargs[0]} - 1)"
        elif len(node.args) == 2:
            return f"({vargs[0]}..{vargs[1]} - 1)"
        elif len(node.args) == 3:
            return f"countup({vargs[0]}, {vargs[1]} - 1, {vargs[2]})"

        raise Exception(
            "encountered range() call with unknown parameters: range({})".format(vargs)
        )

    def visit_print(self, node, vargs: List[str]) -> str:
        args = []
        for n in vargs:
            args.append(n)
            args.append('" "')
        args = ", ".join(args[:-1])
        return f"echo {args}"


# small one liners are inlined here as lambdas
SMALL_DISPATCH_MAP = {
    "str": lambda n, vargs: f"$({vargs[0]})",
    "bool": lambda n, vargs: f"bool({vargs[0]})",
    "floor": lambda n, vargs: f"int(floor({vargs[0]}))",
}

SMALL_USINGS_MAP: Dict[str, str] = {}

DISPATCH_MAP = {
    "range": SmtTranspilerPlugins.visit_range,
    "xrange": SmtTranspilerPlugins.visit_range,
    "print": SmtTranspilerPlugins.visit_print,
}

MODULE_DISPATCH_TABLE: Dict[str, str] = {}

DECORATOR_DISPATCH_TABLE = {ap_dataclass: SmtTranspilerPlugins.visit_ap_dataclass}

CLASS_DISPATCH_TABLE: Dict[type, Callable] = {}

ATTR_DISPATCH_TABLE: Dict[type, Callable] = {}

FuncType = Union[Callable, str]

FUNC_DISPATCH_TABLE: Dict[FuncType, Tuple[Callable, bool]] = {
    open: (SmtTranspilerPlugins.visit_open, True),
    NamedTemporaryFile: (SmtTranspilerPlugins.visit_named_temp_file, True),
    io.TextIOWrapper.read: (SmtTranspilerPlugins.visit_textio_read, True),
    io.TextIOWrapper.read: (SmtTranspilerPlugins.visit_textio_write, True),
    os.unlink: (lambda self, node, vargs: f"std::fs::remove_file({vargs[0]})", True),
    sys.exit: (lambda self, node, vargs: f"quit({vargs[0]})", True),
}

FUNC_USINGS_MAP = {
    time.time: "pylib",
    random.seed: "pylib",
    random.random: "pylib",
}
