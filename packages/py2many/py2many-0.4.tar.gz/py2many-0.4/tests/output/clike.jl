import ast
import importlib
import logging


import random

import time
using pathlib: Path


ilong = i64
ulong = u64
isize = i64
usize = u64
c_int8 = i8
c_int16 = i16
c_int32 = i32
c_int64 = i64
c_uint8 = u8
c_uint16 = u16
c_uint32 = u32
c_uint64 = u64
using py2many::analysis: get_id, IGNORED_MODULE_SET
using py2many::astx: LifeTime
using py2many::exceptions: AstCouldNotInfer, AstEmptyNodeFound, AstNotImplementedError, AstTypeNotSupported, TypeNotSupported


os.path;
math.pi;
time.time;
random.random;
Result;
symbols = Dict(ast.Eq => "==", ast.Is => "==", ast.NotEq => "!=", ast.Mult => "*", ast.Add => "+", ast.Sub => "-", ast.Div => "/", ast.FloorDiv => "/", ast.Mod => "%", ast.Lt => "<", ast.Gt => ">", ast.GtE => ">=", ast.LtE => "<=", ast.LShift => "<<", ast.RShift => ">>", ast.BitXor => "^", ast.BitOr => "|", ast.BitAnd => "&", ast.Not => "!", ast.IsNot => "!=", ast.USub => "-", ast.And => "&&", ast.Or => "||", ast.In => "in")
_AUTO = "auto"
_AUTO_INVOKED = "auto()"
logger = Logger(logging, "py2many")
function class_for_typename{T0, T1, T2}(typename::T0, default_type::T1, locals::T2)::
if typename === nothing
return nothing
end
if isinstance(typename == "super"||startswith(typename, "super()"), (int, float))&&typename == "super"||startswith(typename, "super()") != 0||isinstance(typename == "super"||startswith(typename, "super()"), tuple)&&typename == "super"||startswith(typename, "super()") != ()||isinstance(typename == "super"||startswith(typename, "super()"), list)&&typename == "super"||startswith(typename, "super()") != []||typename == "super"||startswith(typename, "super()") === nothing||isinstance(typename == "super"||startswith(typename, "super()"), bool)&&typename == "super"||startswith(typename, "super()")
return nothing
end
try
typeclass = eval(typename, globals(), locals)
if isinstance(hasattr(typeclass, "__self__")&&!(isinstance(typeclass.__self__, type_(sys))), (int, float))&&hasattr(typeclass, "__self__")&&!(isinstance(typeclass.__self__, type_(sys))) != 0||isinstance(hasattr(typeclass, "__self__")&&!(isinstance(typeclass.__self__, type_(sys))), tuple)&&hasattr(typeclass, "__self__")&&!(isinstance(typeclass.__self__, type_(sys))) != ()||isinstance(hasattr(typeclass, "__self__")&&!(isinstance(typeclass.__self__, type_(sys))), list)&&hasattr(typeclass, "__self__")&&!(isinstance(typeclass.__self__, type_(sys))) != []||hasattr(typeclass, "__self__")&&!(isinstance(typeclass.__self__, type_(sys))) === nothing||isinstance(hasattr(typeclass, "__self__")&&!(isinstance(typeclass.__self__, type_(sys))), bool)&&hasattr(typeclass, "__self__")&&!(isinstance(typeclass.__self__, type_(sys)))
return getattr(typeclass.__self__.__class__, typeclass.__name__)
end
if !(isinstance(typeclass, (type_, type_(open), type_(class_for_typename))))
return typeclass.__class__
end
return typeclass
catch exn
if exn isa (NameError, SyntaxError, AttributeError, TypeError)
info(logger, "".join(["could not evaluate ", string(typename)]));
return default_type
end
end
end

function c_symbol{T0}(node::T0)::String
symbol_type = type_(node)
return symbols[symbol_type]
end

struct CLikeTranspiler
NAME::String
self._imported_names::
body_dict::Dict{ast.AST, String}
_type_map::Dict
_headers::
_usings::
_features::
_container_type_map::Dict
_default_type::String
_statement_separator::String
_main_signature_arg_names::List
_extension::Bool
_ignored_module_set::
_module::
_dispatch_map::Dict
_small_dispatch_map::Dict
_small_usings_map::Dict
_func_dispatch_table::Dict
_func_usings_map::Dict
_attr_dispatch_table::Dict
_keywords::Dict
_throw_on_unimplemented::Bool
_imported_names::Dict
end

NAME::String = None
builtin_constants = frozenset(["True", "False"])
function __init__(self::CLikeTranspiler)
self._type_map = Dict()
self._headers = set([])
self._usings = set([])
self._imported_names = Dict()
self._features = set([])
self._container_type_map = Dict()
self._default_type = _AUTO
self._statement_separator = ";"
self._main_signature_arg_names = []
self._extension = false
self._ignored_module_set = copy(IGNORED_MODULE_SET)
self._module = nothing
self._dispatch_map = Dict()
self._small_dispatch_map = Dict()
self._small_usings_map = Dict()
self._func_dispatch_table = Dict()
self._func_usings_map = Dict()
self._attr_dispatch_table = Dict()
self._keywords = Dict()
self._throw_on_unimplemented = true
end

function headers{T0}(self::CLikeTranspiler, meta::T0)::String
return ""
end

function usings(self::CLikeTranspiler)::String
return ""
end

function features(self::CLikeTranspiler)::String
return ""
end

function extension{RT}(self::CLikeTranspiler)::RT
return self._extension
end

function extension_module(self::CLikeTranspiler)::String
return ""
end

function comment{T0, RT}(self::CLikeTranspiler, text::T0)::RT
return join("", ["/* ", string(text), " */"])
end

function _cast{T0}(self::CLikeTranspiler, name::String, to::T0)::String
return join("", ["(", string(to), ") ", string(name)])
end

function _slice_value{RT}(self::CLikeTranspiler, node::ast.Subscript)::RT
if sys.version_info < (3, 9, 0)
if isinstance(isinstance(node.slice, ast.Index), (int, float))&&isinstance(node.slice, ast.Index) != 0||isinstance(isinstance(node.slice, ast.Index), tuple)&&isinstance(node.slice, ast.Index) != ()||isinstance(isinstance(node.slice, ast.Index), list)&&isinstance(node.slice, ast.Index) != []||isinstance(node.slice, ast.Index) === nothing||isinstance(isinstance(node.slice, ast.Index), bool)&&isinstance(node.slice, ast.Index)
slice_value = node.slice.value
else

slice_value = node.slice
end
else

if isinstance(isinstance(node.slice, ast.Slice), (int, float))&&isinstance(node.slice, ast.Slice) != 0||isinstance(isinstance(node.slice, ast.Slice), tuple)&&isinstance(node.slice, ast.Slice) != ()||isinstance(isinstance(node.slice, ast.Slice), list)&&isinstance(node.slice, ast.Slice) != []||isinstance(node.slice, ast.Slice) === nothing||isinstance(isinstance(node.slice, ast.Slice), bool)&&isinstance(node.slice, ast.Slice)
throw(AstNotImplementedError("Advanced Slicing not supported", node))
end
slice_value = node.slice
end
return slice_value
end

function _map_type{T0, T1}(self::CLikeTranspiler, typename::T0, lifetime::T1)::String
if isinstance(isinstance(typename, list), (int, float))&&isinstance(typename, list) != 0||isinstance(isinstance(typename, list), tuple)&&isinstance(typename, list) != ()||isinstance(isinstance(typename, list), list)&&isinstance(typename, list) != []||isinstance(typename, list) === nothing||isinstance(isinstance(typename, list), bool)&&isinstance(typename, list)
throw(NotImplementedError("".join([string(typename), " not supported in this context"])))
end
typeclass = class_for_typename(typename, self._default_type)
return get(self._type_map, typeclass, typename)
end

function _map_types(self::CLikeTranspiler, typenames::Array{String})::Array{String}
return [_map_type(self, e) for e in typenames]
end

function _map_container_type{T0}(self::CLikeTranspiler, typename::T0)::String
return get(self._container_type_map, typename, self._default_type)
end

function _combine_value_index{T0, T1}(self::CLikeTranspiler, value_type::T0, index_type::T1)::String
return join("", [string(value_type), "<", string(index_type), ">"])
end

function _visit_container_type(self::CLikeTranspiler, typename::Tuple)::String
value_type, index_type = typename
if isinstance(isinstance(index_type, List), (int, float))&&isinstance(index_type, List) != 0||isinstance(isinstance(index_type, List), tuple)&&isinstance(index_type, List) != ()||isinstance(isinstance(index_type, List), list)&&isinstance(index_type, List) != []||isinstance(index_type, List) === nothing||isinstance(isinstance(index_type, List), bool)&&isinstance(index_type, List)
index_contains_default = "Any" in index_type
if !(index_contains_default)
if isinstance(any((t === nothing for t in index_type)), (int, float))&&any((t === nothing for t in index_type)) != 0||isinstance(any((t === nothing for t in index_type)), tuple)&&any((t === nothing for t in index_type)) != ()||isinstance(any((t === nothing for t in index_type)), list)&&any((t === nothing for t in index_type)) != []||any((t === nothing for t in index_type)) === nothing||isinstance(any((t === nothing for t in index_type)), bool)&&any((t === nothing for t in index_type))
throw(TypeNotSupported(typename))
end
index_type = join(", ", index_type)
end
else

index_contains_default = index_type == "Any"
end
if isinstance(index_contains_default||value_type == self._default_type, (int, float))&&index_contains_default||value_type == self._default_type != 0||isinstance(index_contains_default||value_type == self._default_type, tuple)&&index_contains_default||value_type == self._default_type != ()||isinstance(index_contains_default||value_type == self._default_type, list)&&index_contains_default||value_type == self._default_type != []||index_contains_default||value_type == self._default_type === nothing||isinstance(index_contains_default||value_type == self._default_type, bool)&&index_contains_default||value_type == self._default_type
return self._default_type
end
return _combine_value_index(self, value_type, index_type)
end

function _typename_from_type_node{T0}(self::CLikeTranspiler, node::T0)::
if isinstance(isinstance(node, ast.Name), (int, float))&&isinstance(node, ast.Name) != 0||isinstance(isinstance(node, ast.Name), tuple)&&isinstance(node, ast.Name) != ()||isinstance(isinstance(node, ast.Name), list)&&isinstance(node, ast.Name) != []||isinstance(node, ast.Name) === nothing||isinstance(isinstance(node, ast.Name), bool)&&isinstance(node, ast.Name)
return _map_type(self, get_id(node), getattr(node, "lifetime", LifeTime::UNKNOWN))
else

if isinstance(isinstance(node, ast.Constant)&&node.value !== nothing, (int, float))&&isinstance(node, ast.Constant)&&node.value !== nothing != 0||isinstance(isinstance(node, ast.Constant)&&node.value !== nothing, tuple)&&isinstance(node, ast.Constant)&&node.value !== nothing != ()||isinstance(isinstance(node, ast.Constant)&&node.value !== nothing, list)&&isinstance(node, ast.Constant)&&node.value !== nothing != []||isinstance(node, ast.Constant)&&node.value !== nothing === nothing||isinstance(isinstance(node, ast.Constant)&&node.value !== nothing, bool)&&isinstance(node, ast.Constant)&&node.value !== nothing
return node.value
else

if isinstance(isinstance(node, ast.ClassDef), (int, float))&&isinstance(node, ast.ClassDef) != 0||isinstance(isinstance(node, ast.ClassDef), tuple)&&isinstance(node, ast.ClassDef) != ()||isinstance(isinstance(node, ast.ClassDef), list)&&isinstance(node, ast.ClassDef) != []||isinstance(node, ast.ClassDef) === nothing||isinstance(isinstance(node, ast.ClassDef), bool)&&isinstance(node, ast.ClassDef)
return get_id(node)
else

if isinstance(isinstance(node, ast.Tuple), (int, float))&&isinstance(node, ast.Tuple) != 0||isinstance(isinstance(node, ast.Tuple), tuple)&&isinstance(node, ast.Tuple) != ()||isinstance(isinstance(node, ast.Tuple), list)&&isinstance(node, ast.Tuple) != []||isinstance(node, ast.Tuple) === nothing||isinstance(isinstance(node, ast.Tuple), bool)&&isinstance(node, ast.Tuple)
return [_typename_from_type_node(self, e) for e in node.elts]
else

if isinstance(isinstance(node, ast.Attribute), (int, float))&&isinstance(node, ast.Attribute) != 0||isinstance(isinstance(node, ast.Attribute), tuple)&&isinstance(node, ast.Attribute) != ()||isinstance(isinstance(node, ast.Attribute), list)&&isinstance(node, ast.Attribute) != []||isinstance(node, ast.Attribute) === nothing||isinstance(isinstance(node, ast.Attribute), bool)&&isinstance(node, ast.Attribute)
node_id = get_id(node)
if isinstance(startswith(node_id, "typing."), (int, float))&&startswith(node_id, "typing.") != 0||isinstance(startswith(node_id, "typing."), tuple)&&startswith(node_id, "typing.") != ()||isinstance(startswith(node_id, "typing."), list)&&startswith(node_id, "typing.") != []||startswith(node_id, "typing.") === nothing||isinstance(startswith(node_id, "typing."), bool)&&startswith(node_id, "typing.")
node_id = split(node_id, ".")[1];
end
return node_id
else

if isinstance(isinstance(node, ast.Subscript), (int, float))&&isinstance(node, ast.Subscript) != 0||isinstance(isinstance(node, ast.Subscript), tuple)&&isinstance(node, ast.Subscript) != ()||isinstance(isinstance(node, ast.Subscript), list)&&isinstance(node, ast.Subscript) != []||isinstance(node, ast.Subscript) === nothing||isinstance(isinstance(node, ast.Subscript), bool)&&isinstance(node, ast.Subscript)
slice_value = _slice_value(self, node)
value_type, index_type = tuple(map(self._typename_from_type_node, (node.value, slice_value)))
value_type = _map_container_type(self, convert(, value_type))
node.container_type = (value_type, index_type)
return _combine_value_index(self, convert(, value_type), index_type)
end
end
end
end
end
end
return self._default_type
end

function _generic_typename_from_type_node{T0}(self::CLikeTranspiler, node::T0)::
if isinstance(isinstance(node, ast.Name), (int, float))&&isinstance(node, ast.Name) != 0||isinstance(isinstance(node, ast.Name), tuple)&&isinstance(node, ast.Name) != ()||isinstance(isinstance(node, ast.Name), list)&&isinstance(node, ast.Name) != []||isinstance(node, ast.Name) === nothing||isinstance(isinstance(node, ast.Name), bool)&&isinstance(node, ast.Name)
return get_id(node)
else

if isinstance(isinstance(node, ast.Constant), (int, float))&&isinstance(node, ast.Constant) != 0||isinstance(isinstance(node, ast.Constant), tuple)&&isinstance(node, ast.Constant) != ()||isinstance(isinstance(node, ast.Constant), list)&&isinstance(node, ast.Constant) != []||isinstance(node, ast.Constant) === nothing||isinstance(isinstance(node, ast.Constant), bool)&&isinstance(node, ast.Constant)
return node.value
else

if isinstance(isinstance(node, ast.ClassDef), (int, float))&&isinstance(node, ast.ClassDef) != 0||isinstance(isinstance(node, ast.ClassDef), tuple)&&isinstance(node, ast.ClassDef) != ()||isinstance(isinstance(node, ast.ClassDef), list)&&isinstance(node, ast.ClassDef) != []||isinstance(node, ast.ClassDef) === nothing||isinstance(isinstance(node, ast.ClassDef), bool)&&isinstance(node, ast.ClassDef)
return get_id(node)
else

if isinstance(isinstance(node, ast.Tuple), (int, float))&&isinstance(node, ast.Tuple) != 0||isinstance(isinstance(node, ast.Tuple), tuple)&&isinstance(node, ast.Tuple) != ()||isinstance(isinstance(node, ast.Tuple), list)&&isinstance(node, ast.Tuple) != []||isinstance(node, ast.Tuple) === nothing||isinstance(isinstance(node, ast.Tuple), bool)&&isinstance(node, ast.Tuple)
return [_generic_typename_from_type_node(self, e) for e in node.elts]
else

if isinstance(isinstance(node, ast.Attribute), (int, float))&&isinstance(node, ast.Attribute) != 0||isinstance(isinstance(node, ast.Attribute), tuple)&&isinstance(node, ast.Attribute) != ()||isinstance(isinstance(node, ast.Attribute), list)&&isinstance(node, ast.Attribute) != []||isinstance(node, ast.Attribute) === nothing||isinstance(isinstance(node, ast.Attribute), bool)&&isinstance(node, ast.Attribute)
node_id = get_id(node)
if isinstance(startswith(node_id, "typing."), (int, float))&&startswith(node_id, "typing.") != 0||isinstance(startswith(node_id, "typing."), tuple)&&startswith(node_id, "typing.") != ()||isinstance(startswith(node_id, "typing."), list)&&startswith(node_id, "typing.") != []||startswith(node_id, "typing.") === nothing||isinstance(startswith(node_id, "typing."), bool)&&startswith(node_id, "typing.")
node_id = split(node_id, ".")[1];
end
return node_id
else

if isinstance(isinstance(node, ast.Subscript), (int, float))&&isinstance(node, ast.Subscript) != 0||isinstance(isinstance(node, ast.Subscript), tuple)&&isinstance(node, ast.Subscript) != ()||isinstance(isinstance(node, ast.Subscript), list)&&isinstance(node, ast.Subscript) != []||isinstance(node, ast.Subscript) === nothing||isinstance(isinstance(node, ast.Subscript), bool)&&isinstance(node, ast.Subscript)
slice_value = _slice_value(self, node)
value_type, index_type = tuple(map(self._generic_typename_from_type_node, (node.value, slice_value)))
node.generic_container_type = (value_type, index_type)
return join("", [string(value_type), "[", string(index_type), "]"])
end
end
end
end
end
end
return self._default_type
end

function _typename_from_annotation{T0, T1}(self::CLikeTranspiler, node::T0, attr::T1)::String
default_type = self._default_type
typename = default_type
if isinstance(hasattr(node, attr), (int, float))&&hasattr(node, attr) != 0||isinstance(hasattr(node, attr), tuple)&&hasattr(node, attr) != ()||isinstance(hasattr(node, attr), list)&&hasattr(node, attr) != []||hasattr(node, attr) === nothing||isinstance(hasattr(node, attr), bool)&&hasattr(node, attr)
type_node = getattr(node, attr)
typename = _typename_from_type_node(self, type_node);
if isinstance(isinstance(type_node, ast.Subscript), (int, float))&&isinstance(type_node, ast.Subscript) != 0||isinstance(isinstance(type_node, ast.Subscript), tuple)&&isinstance(type_node, ast.Subscript) != ()||isinstance(isinstance(type_node, ast.Subscript), list)&&isinstance(type_node, ast.Subscript) != []||isinstance(type_node, ast.Subscript) === nothing||isinstance(isinstance(type_node, ast.Subscript), bool)&&isinstance(type_node, ast.Subscript)
node.container_type = type_node.container_type
try
return _visit_container_type(self, type_node.container_type)
catch exn
 let e = exn
if e isa TypeNotSupported
throw(AstTypeNotSupported(string(e), node))
end
end
end
end
if typename === nothing
throw(AstCouldNotInfer(type_node, node))
end
end
return typename
end

function _generic_typename_from_annotation{T0, T1}(self::CLikeTranspiler, node::T0, attr::T1)::Nothing{String}
typename = nothing
if isinstance(hasattr(node, attr), (int, float))&&hasattr(node, attr) != 0||isinstance(hasattr(node, attr), tuple)&&hasattr(node, attr) != ()||isinstance(hasattr(node, attr), list)&&hasattr(node, attr) != []||hasattr(node, attr) === nothing||isinstance(hasattr(node, attr), bool)&&hasattr(node, attr)
type_node = getattr(node, attr)
ret = _generic_typename_from_type_node(self, type_node)
if isinstance(isinstance(type_node, ast.Subscript), (int, float))&&isinstance(type_node, ast.Subscript) != 0||isinstance(isinstance(type_node, ast.Subscript), tuple)&&isinstance(type_node, ast.Subscript) != ()||isinstance(isinstance(type_node, ast.Subscript), list)&&isinstance(type_node, ast.Subscript) != []||isinstance(type_node, ast.Subscript) === nothing||isinstance(isinstance(type_node, ast.Subscript), bool)&&isinstance(type_node, ast.Subscript)
node.generic_container_type = type_node.generic_container_type
end
return ret
end
return typename
end

function visit{T0}(self::CLikeTranspiler, node::T0)::String
if node === nothing
throw(AstEmptyNodeFound)
end
if type_(node) in keys(symbols)
return c_symbol(node)
else

try
return visit(super(), node)
catch exn
if exn isa AstNotImplementedError
error()
end
 let e = exn
if e isa Exception
throw(AstNotImplementedError(e, node))
end
end
end
end
end

function visit_Pass{T0}(self::CLikeTranspiler, node::T0)::String
return comment(self, convert(, "pass"))
end

function visit_Module{T0}(self::CLikeTranspiler, node::T0)::String
docstring = getattr(node, "docstring_comment", nothing)
buf = docstring !== nothing ? ([comment(self, docstring.value)]) : ([])
filename = getattr(node, "__file__", nothing)
if filename !== nothing
self._module = Path(filename).stem
end
self._imported_names = Dict()
clear(self._usings);
body_dict::Dict{ast.AST, String} = OrderedDict()
for b in node.body
if !(isinstance(b, ast.FunctionDef))
body_dict[b] = visit(self, b)
end
end
for b in node.body
if isinstance(isinstance(b, ast.FunctionDef), (int, float))&&isinstance(b, ast.FunctionDef) != 0||isinstance(isinstance(b, ast.FunctionDef), tuple)&&isinstance(b, ast.FunctionDef) != ()||isinstance(isinstance(b, ast.FunctionDef), list)&&isinstance(b, ast.FunctionDef) != []||isinstance(b, ast.FunctionDef) === nothing||isinstance(isinstance(b, ast.FunctionDef), bool)&&isinstance(b, ast.FunctionDef)
body_dict[b] = visit(self, b)
end
end
buf += [body_dict[b] for b in node.body]
return join("\n", buf)
end

function visit_alias{T0, RT}(self::CLikeTranspiler, node::T0)::RT
return (node.name, node.asname)
end

function _import(self::CLikeTranspiler, name::String)::String
# ...
end

function _import_from(self::CLikeTranspiler, module_name::String, names::Array{String}, level::Int64)::String
# ...
end

function visit_Import{T0}(self::CLikeTranspiler, node::T0)::String
names = [visit(self, n) for n in node.names]
imports = [_import(self, name) for (name, alias) in names if name not in self._ignored_module_set ]
for (name, asname) in names
if asname !== nothing
try
imported_name = import_module(importlib, name)
catch exn
if exn isa ImportError
imported_name = name;
end
end
self._imported_names[asname] = imported_name
end
end
return join("\n", imports)
end

function visit_ImportFrom{T0}(self::CLikeTranspiler, node::T0)::String
if node.module in self._ignored_module_set
return ""
end
imported_name = node.module
imported_module = nothing
if isinstance(node.module, (int, float))&&node.module != 0||isinstance(node.module, tuple)&&node.module != ()||isinstance(node.module, list)&&node.module != []||node.module === nothing||isinstance(node.module, bool)&&node.module
try
imported_module = import_module(importlib, node.module);
catch exn
if exn isa ImportError
# pass
end
end
else

imported_name = ".";
end
names = [visit(self, n) for n in node.names]
for (name, asname) in names
asname = asname !== nothing ? (asname) : (name);
if isinstance(imported_module, (int, float))&&imported_module != 0||isinstance(imported_module, tuple)&&imported_module != ()||isinstance(imported_module, list)&&imported_module != []||imported_module === nothing||isinstance(imported_module, bool)&&imported_module
self._imported_names[asname] = getattr(imported_module, name, nothing)
else

self._imported_names[asname] = (imported_name, name)
end
end
names = [n for (n, _) in names];
return _import_from(self, imported_name, names, node.level)
end

function visit_Name{T0}(self::CLikeTranspiler, node::T0)::String
if node.id in self.builtin_constants
return lower(node.id)
end
return node.id
end

function visit_Ellipsis{T0}(self::CLikeTranspiler, node::T0)::String
return comment(self, convert(, "..."))
end

function visit_NameConstant{T0}(self::CLikeTranspiler, node::T0)::String
if node.value === true
return "true"
else

if node.value === false
return "false"
else

if node.value === nothing
return "NULL"
else

if node.value === Ellipsis
return visit_Ellipsis(self, node)
else

return node.value
end
end
end
end
end

function visit_Constant{T0}(self::CLikeTranspiler, node::T0)::String
if isinstance(isinstance(node.value, str), (int, float))&&isinstance(node.value, str) != 0||isinstance(isinstance(node.value, str), tuple)&&isinstance(node.value, str) != ()||isinstance(isinstance(node.value, str), list)&&isinstance(node.value, str) != []||isinstance(node.value, str) === nothing||isinstance(isinstance(node.value, str), bool)&&isinstance(node.value, str)
return visit_Str(self, node)
else

if isinstance(isinstance(node.value, bytes), (int, float))&&isinstance(node.value, bytes) != 0||isinstance(isinstance(node.value, bytes), tuple)&&isinstance(node.value, bytes) != ()||isinstance(isinstance(node.value, bytes), list)&&isinstance(node.value, bytes) != []||isinstance(node.value, bytes) === nothing||isinstance(isinstance(node.value, bytes), bool)&&isinstance(node.value, bytes)
return visit_Bytes(self, node)
end
end
return string(self.visit_NameConstant(node))
end

function visit_Expr{T0}(self::CLikeTranspiler, node::T0)::String
s = visit(self, node.value)
if isinstance(isinstance(node.value, ast.Constant)&&node.value.value === Ellipsis, (int, float))&&isinstance(node.value, ast.Constant)&&node.value.value === Ellipsis != 0||isinstance(isinstance(node.value, ast.Constant)&&node.value.value === Ellipsis, tuple)&&isinstance(node.value, ast.Constant)&&node.value.value === Ellipsis != ()||isinstance(isinstance(node.value, ast.Constant)&&node.value.value === Ellipsis, list)&&isinstance(node.value, ast.Constant)&&node.value.value === Ellipsis != []||isinstance(node.value, ast.Constant)&&node.value.value === Ellipsis === nothing||isinstance(isinstance(node.value, ast.Constant)&&node.value.value === Ellipsis, bool)&&isinstance(node.value, ast.Constant)&&node.value.value === Ellipsis
return s
end
if !(s)
return ""
end
s = strip(s);
if !(endswith(s, self._statement_separator))
s += self._statement_separator
end
if s == self._statement_separator
return ""
else

return s
end
end

function visit_Str{T0}(self::CLikeTranspiler, node::T0)::String
node_str = node.value
node_str = replace(node_str, "\"", "\\"");
node_str = replace(node_str, "\n", "\n");
node_str = replace(node_str, "\r", "\r");
node_str = replace(node_str, "\t", "\t");
return join("", ["\"", string(node_str), "\""])
end

function visit_Bytes{T0}(self::CLikeTranspiler, node::T0)::String
bytes_str = node.s
byte_array = join(", ", [hex(c) for c in bytes_str])
return join("", ["{", string(byte_array), "}"])
end

function visit_arguments{T0}(self::CLikeTranspiler, node::T0)::
args = [visit(self, arg) for arg in node.args]
if args == []
return ([], [])
end
typenames, args = map(list, zip(starred!(args)/*unsupported*/))
return (typenames, args)
end

function visit_Return{T0}(self::CLikeTranspiler, node::T0)::String
if isinstance(node.value, (int, float))&&node.value != 0||isinstance(node.value, tuple)&&node.value != ()||isinstance(node.value, list)&&node.value != []||node.value === nothing||isinstance(node.value, bool)&&node.value
return format("return {0};", self.visit(node.value))
end
return "return;"
end

function _make_block{T0, RT}(self::CLikeTranspiler, node::T0)::RT
buf = []
push!(buf, "({");
extend(buf, [self.visit(child) for child in node.body]);
push!(buf, "})");
return join("\n", buf)
end

function is_block{T0, RT}(node::T0)::RT
return isinstance(node.test, ast.Constant)&&node.test.value == true&&node.orelse == []&&hasattr(node, "rewritten")&&node.rewritten
end

function visit_If{T0, T1}(self::CLikeTranspiler, node::T0, use_parens::T1)::String
buf = []
make_block = is_block(self)
if isinstance(make_block, (int, float))&&make_block != 0||isinstance(make_block, tuple)&&make_block != ()||isinstance(make_block, list)&&make_block != []||make_block === nothing||isinstance(make_block, bool)&&make_block
return _make_block(self, node)
else

if isinstance(use_parens, (int, float))&&use_parens != 0||isinstance(use_parens, tuple)&&use_parens != ()||isinstance(use_parens, list)&&use_parens != []||use_parens === nothing||isinstance(use_parens, bool)&&use_parens
push!(buf, "if({0}) {{".format(self.visit(node.test)));
else

push!(buf, "if {0} {{".format(self.visit(node.test)));
end
end
body = [visit(self, child) for child in node.body]
body = [b for b in body if b !== nothing ];
extend(buf, body);
orelse = [visit(self, child) for child in node.orelse]
if isinstance(orelse, (int, float))&&orelse != 0||isinstance(orelse, tuple)&&orelse != ()||isinstance(orelse, list)&&orelse != []||orelse === nothing||isinstance(orelse, bool)&&orelse
push!(buf, "} else {");
extend(buf, orelse);
push!(buf, "}");
else

push!(buf, "}");
end
return join("\n", buf)
end

function visit_Continue{T0}(self::CLikeTranspiler, node::T0)::String
return "continue;"
end

function visit_Break{T0}(self::CLikeTranspiler, node::T0)::String
return "break;"
end

function visit_While{T0, T1}(self::CLikeTranspiler, node::T0, use_parens::T1)::String
buf = []
if isinstance(use_parens, (int, float))&&use_parens != 0||isinstance(use_parens, tuple)&&use_parens != ()||isinstance(use_parens, list)&&use_parens != []||use_parens === nothing||isinstance(use_parens, bool)&&use_parens
push!(buf, "while ({0}) {{".format(self.visit(node.test)));
else

push!(buf, "while {0} {{".format(self.visit(node.test)));
end
extend(buf, [self.visit(n) for n in node.body]);
push!(buf, "}");
return join("\n", buf)
end

function visit_Compare{T0}(self::CLikeTranspiler, node::T0)::String
if isinstance(isinstance(node.ops[0], ast.In), (int, float))&&isinstance(node.ops[0], ast.In) != 0||isinstance(isinstance(node.ops[0], ast.In), tuple)&&isinstance(node.ops[0], ast.In) != ()||isinstance(isinstance(node.ops[0], ast.In), list)&&isinstance(node.ops[0], ast.In) != []||isinstance(node.ops[0], ast.In) === nothing||isinstance(isinstance(node.ops[0], ast.In), bool)&&isinstance(node.ops[0], ast.In)
return visit_In(self, node)
end
left = visit(self, node.left)
op = visit(self, node.ops[0])
right = visit(self, node.comparators[0])
return format("{0} {1} {2}", left, op, right)
end

function visit_BoolOp{T0}(self::CLikeTranspiler, node::T0)::String
op = visit(self, node.op)
return join(op, [self.visit(v) for v in node.values])
end

function visit_UnaryOp{T0}(self::CLikeTranspiler, node::T0)::String
return format("{0}({1})", self.visit(node.op), self.visit(node.operand))
end

function _visit_AssignOne{T0, T1}(self::CLikeTranspiler, node::T0, target::T1)::String
# ...
end

function visit_Assign{T0}(self::CLikeTranspiler, node::T0)::String
return join("\n", [self._visit_AssignOne(node, target) for target in node.targets])
end

function visit_AugAssign{T0}(self::CLikeTranspiler, node::T0)::String
target = visit(self, node.target)
op = visit(self, node.op)
val = visit(self, node.value)
return format("{0} {1}= {2};", target, op, val)
end

function visit_AnnAssign{T0, RT}(self::CLikeTranspiler, node::T0)::RT
target = visit(self, node.target)
if isinstance(hasattr(node.target, "annotation")&&isinstance(node.target.annotation, ast.Subscript)&&get_id(node.target.annotation.value) == "Callable", (int, float))&&hasattr(node.target, "annotation")&&isinstance(node.target.annotation, ast.Subscript)&&get_id(node.target.annotation.value) == "Callable" != 0||isinstance(hasattr(node.target, "annotation")&&isinstance(node.target.annotation, ast.Subscript)&&get_id(node.target.annotation.value) == "Callable", tuple)&&hasattr(node.target, "annotation")&&isinstance(node.target.annotation, ast.Subscript)&&get_id(node.target.annotation.value) == "Callable" != ()||isinstance(hasattr(node.target, "annotation")&&isinstance(node.target.annotation, ast.Subscript)&&get_id(node.target.annotation.value) == "Callable", list)&&hasattr(node.target, "annotation")&&isinstance(node.target.annotation, ast.Subscript)&&get_id(node.target.annotation.value) == "Callable" != []||hasattr(node.target, "annotation")&&isinstance(node.target.annotation, ast.Subscript)&&get_id(node.target.annotation.value) == "Callable" === nothing||isinstance(hasattr(node.target, "annotation")&&isinstance(node.target.annotation, ast.Subscript)&&get_id(node.target.annotation.value) == "Callable", bool)&&hasattr(node.target, "annotation")&&isinstance(node.target.annotation, ast.Subscript)&&get_id(node.target.annotation.value) == "Callable"
type_str = self._default_type
else

type_str = _typename_from_annotation(self, node)
end
val = node.value !== nothing ? (visit(self, node.value)) : (nothing)
return (target, type_str, val)
end

function set_continue_on_unimplemented(self::CLikeTranspiler)
self._throw_on_unimplemented = false
end

function visit_unsupported_body{T0, T1, T2}(self::CLikeTranspiler, node::T0, name::T1, body::T2)::String
if isinstance(self._throw_on_unimplemented, (int, float))&&self._throw_on_unimplemented != 0||isinstance(self._throw_on_unimplemented, tuple)&&self._throw_on_unimplemented != ()||isinstance(self._throw_on_unimplemented, list)&&self._throw_on_unimplemented != []||self._throw_on_unimplemented === nothing||isinstance(self._throw_on_unimplemented, bool)&&self._throw_on_unimplemented
throw(AstNotImplementedError("".join([string(name), " not implemented"]), node))
else

return comment(self, "".join([string(name), " unimplemented on line ", string(node.lineno), ":", string(node.col_offset)]))
end
end

function visit_NamedExpr{T0}(self::CLikeTranspiler, node::T0)::String
target = visit(self, node.target)
return visit_unsupported_body(self, node, "".join(["named expr ", string(target)]), node.value)
end

function visit_Delete{T0}(self::CLikeTranspiler, node::T0)::String
body = [visit(self, t) for t in node.targets]
return visit_unsupported_body(self, node, convert(, "del"), body)
end

function visit_Await{T0}(self::CLikeTranspiler, node::T0)::String
return visit_unsupported_body(self, node, convert(, "await"), node.value)
end

function visit_AsyncFor{T0}(self::CLikeTranspiler, node::T0)::String
target = visit(self, node.target)
iter = visit(self, node.iter)
return visit_unsupported_body(self, node, "".join(["async for ", string(target), " in ", string(iter)]), node.body)
end

function visit_AsyncWith{T0}(self::CLikeTranspiler, node::T0)::String
items = [visit(self, i) for i in node.items]
return visit_unsupported_body(self, node, "".join(["async with ", string(items)]), node.body)
end

function visit_YieldFrom{T0}(self::CLikeTranspiler, node::T0)::String
return visit_unsupported_body(self, node, convert(, "yield from"), node.value)
end

function visit_AsyncFunctionDef{T0}(self::CLikeTranspiler, node::T0)::String
return visit_unsupported_body(self, node, convert(, "async def"), node.body)
end

function visit_Nonlocal{T0}(self::CLikeTranspiler, node::T0)::String
return visit_unsupported_body(self, node, convert(, "nonlocal"), node.names)
end

function visit_DictComp{T0}(self::CLikeTranspiler, node::T0)::String
key = visit(self, node.key)
value = visit(self, node.value)
return visit_unsupported_body(self, node, "".join(["dict comprehension (", string(key), ", ", string(value), ")"]), node.generators)
end

function visit_ListComp{T0}(self::CLikeTranspiler, node::T0)::String
return visit_GeneratorExp(self, node)
end

function visit_SetComp{T0}(self::CLikeTranspiler, node::T0)::String
return visit_GeneratorExp(self, node)
end

function visit_ClassDef{T0}(self::CLikeTranspiler, node::T0)::String
bases = [get_id(base) for base in node.bases]
if set(bases) == Set(["Enum", "str"])
return visit_StrEnum(self, node)
end
if length(bases) != 1
return nothing
end
if !(bases[0] in Set(["Enum", "IntEnum", "IntFlag"]))
return nothing
end
if isinstance(bases == ["IntEnum"]||bases == ["Enum"], (int, float))&&bases == ["IntEnum"]||bases == ["Enum"] != 0||isinstance(bases == ["IntEnum"]||bases == ["Enum"], tuple)&&bases == ["IntEnum"]||bases == ["Enum"] != ()||isinstance(bases == ["IntEnum"]||bases == ["Enum"], list)&&bases == ["IntEnum"]||bases == ["Enum"] != []||bases == ["IntEnum"]||bases == ["Enum"] === nothing||isinstance(bases == ["IntEnum"]||bases == ["Enum"], bool)&&bases == ["IntEnum"]||bases == ["Enum"]
return visit_IntEnum(self, node)
end
if bases == ["IntFlag"]
return visit_IntFlag(self, node)
end
end

function visit_StrEnum{T0}(self::CLikeTranspiler, node::T0)::String
throw(Exception("Unimplemented"))
end

function visit_IntEnum{T0}(self::CLikeTranspiler, node::T0)::String
throw(Exception("Unimplemented"))
end

function visit_IntFlag{T0}(self::CLikeTranspiler, node::T0)::String
throw(Exception("Unimplemented"))
end

function visit_IfExp{T0}(self::CLikeTranspiler, node::T0)::String
body = visit(self, node.body)
orelse = visit(self, node.orelse)
test = visit(self, node.test)
return join("", ["(", string(test), "? ({ ", string(body), "; }) : ({ ", string(orelse), "; }))"])
end

function _func_for_lookup{T0}(self::CLikeTranspiler, fname::T0)::
func = class_for_typename(fname, nothing, self._imported_names)
if func === nothing
return nothing
end
try
hash(func);
catch exn
if exn isa TypeError
debug(logger, "".join([string(func), " is not hashable"]));
return nothing
end
end
return func
end

function _func_name_split(self::CLikeTranspiler, fname::String)::
splits = rsplit(fname, ".", 1)
if length(splits) == 2
return tuple(splits)
else

return ("", splits[0])
end
end

function _dispatch{T0}(self::CLikeTranspiler, node::T0, fname::String, vargs::Array{String})::Nothing{String}
if fname in self._dispatch_map
try
return self._dispatch_map[fname](self, node, vargs)
catch exn
if exn isa IndexError
return nothing
end
end
end
if fname in self._small_dispatch_map
if fname in self._small_usings_map
add(self._usings, self._small_usings_map[fname]);
end
try
return self._small_dispatch_map[fname](node, vargs)
catch exn
if exn isa IndexError
return nothing
end
end
end
func = _func_for_lookup(self, convert(, fname))
if isinstance(func !== nothing&&func in self._func_dispatch_table, (int, float))&&func !== nothing&&func in self._func_dispatch_table != 0||isinstance(func !== nothing&&func in self._func_dispatch_table, tuple)&&func !== nothing&&func in self._func_dispatch_table != ()||isinstance(func !== nothing&&func in self._func_dispatch_table, list)&&func !== nothing&&func in self._func_dispatch_table != []||func !== nothing&&func in self._func_dispatch_table === nothing||isinstance(func !== nothing&&func in self._func_dispatch_table, bool)&&func !== nothing&&func in self._func_dispatch_table
if func in self._func_usings_map
add(self._usings, self._func_usings_map[func]);
end
ret, node.result_type = self._func_dispatch_table[func]
try
return ret(self, node, vargs)
catch exn
if exn isa IndexError
return nothing
end
end
end
fname_stem, fname_leaf = _func_name_split(self, fname)
if fname_leaf in self._func_dispatch_table
ret, node.result_type = self._func_dispatch_table[fname_leaf]
try
return fname_stem + ret(self, node, vargs)
catch exn
if exn isa IndexError
return nothing
end
end
end
return nothing
end

