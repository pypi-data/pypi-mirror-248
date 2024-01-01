import ast
using ast_helpers: create_ast_node, unparse
using clike: CLikeTranspiler
struct RestoreMainRewriter

end

function visit_FunctionDef{T0, RT}(self::RestoreMainRewriter, node::T0)::RT
is_python_main = getattr(node, "python_main", false)
if isinstance(is_python_main, (int, float))&&is_python_main != 0||isinstance(is_python_main, tuple)&&is_python_main != ()||isinstance(is_python_main, list)&&is_python_main != []||is_python_main === nothing||isinstance(is_python_main, bool)&&is_python_main
if_block = create_ast_node(convert(, "if __name__ == '__main__': True"), node)
if_block.body = node.body
fix_missing_locations(ast, if_block);
return if_block
end
return node
end

struct PythonTranspiler

end

NAME = "python"
function visit{T0, RT}(self::PythonTranspiler, node::T0)::RT
return unparse(node)
end

function usings{RT}(self::PythonTranspiler)::RT
return join("\n", ["from typing import Callable, Dict, List, Set, Optional", "from ctypes import c_int8 as i8, c_int16 as i16, c_int32 as i32, c_int64 as i64", "from ctypes import c_uint8 as u8, c_uint16 as u16, c_uint32 as u32, c_uint64 as u64", "import sys"])
end

