import ast
import textwrap
using clike: CLikeTranspiler
using plugins: ATTR_DISPATCH_TABLE, CLASS_DISPATCH_TABLE, FUNC_DISPATCH_TABLE, MODULE_DISPATCH_TABLE, DISPATCH_MAP, SMALL_DISPATCH_MAP, SMALL_USINGS_MAP
using py2many::analysis: get_id, is_void_function
using py2many::declaration_extractor: DeclarationExtractor
using py2many::clike: _AUTO_INVOKED, class_for_typename
using py2many::tracer: is_list, defined_before, is_class_or_module, is_enum

struct JuliaMethodCallRewriter

end

function visit_Call{T0, RT}(self::JuliaMethodCallRewriter, node::T0)::RT
fname = node.func
if isinstance(isinstance(fname, ast.Attribute), (int, float))&&isinstance(fname, ast.Attribute) != 0||isinstance(isinstance(fname, ast.Attribute), tuple)&&isinstance(fname, ast.Attribute) != ()||isinstance(isinstance(fname, ast.Attribute), list)&&isinstance(fname, ast.Attribute) != []||isinstance(fname, ast.Attribute) === nothing||isinstance(isinstance(fname, ast.Attribute), bool)&&isinstance(fname, ast.Attribute)
if isinstance(is_list(node.func.value)&&fname.attr == "append", (int, float))&&is_list(node.func.value)&&fname.attr == "append" != 0||isinstance(is_list(node.func.value)&&fname.attr == "append", tuple)&&is_list(node.func.value)&&fname.attr == "append" != ()||isinstance(is_list(node.func.value)&&fname.attr == "append", list)&&is_list(node.func.value)&&fname.attr == "append" != []||is_list(node.func.value)&&fname.attr == "append" === nothing||isinstance(is_list(node.func.value)&&fname.attr == "append", bool)&&is_list(node.func.value)&&fname.attr == "append"
new_func_name = "push!"
else

new_func_name = fname.attr
end
if isinstance(get_id(fname.value), (int, float))&&get_id(fname.value) != 0||isinstance(get_id(fname.value), tuple)&&get_id(fname.value) != ()||isinstance(get_id(fname.value), list)&&get_id(fname.value) != []||get_id(fname.value) === nothing||isinstance(get_id(fname.value), bool)&&get_id(fname.value)
node0 = Name(ast, get_id(fname.value), node.lineno)
else

node0 = fname.value
end
node.args = [node0] + node.args
node.func = Name(ast, new_func_name, node.lineno, fname.ctx)
end
return node
end

struct JuliaTranspiler
_headers::
_default_type::String
_container_type_map::
_dispatch_map::Dict{String, }
_small_dispatch_map::Dict{String, }
_small_usings_map::Dict{String, String}
_func_dispatch_table::Dict{FuncType, {['Callable', 'Bool']}}
_attr_dispatch_table::Dict{String, }
end

NAME = "julia"
CONTAINER_TYPE_MAP = Dict("List" => "Array", "Dict" => "Dict", "Set" => "Set", "Optional" => "Nothing")
function __init__(self::JuliaTranspiler)
__init__(super());
self._headers = set([])
self._default_type = ""
self._container_type_map = self.CONTAINER_TYPE_MAP
self._dispatch_map = DISPATCH_MAP
self._small_dispatch_map = SMALL_DISPATCH_MAP
self._small_usings_map = SMALL_USINGS_MAP
self._func_dispatch_table = FUNC_DISPATCH_TABLE
self._attr_dispatch_table = ATTR_DISPATCH_TABLE
end

function usings{RT}(self::JuliaTranspiler)::RT
usings = sorted(list(set(self._usings)));
uses = join("\n", ("".join(["using ", string(mod)]) for mod in usings))
return uses
end

function comment{T0, RT}(self::JuliaTranspiler, text::T0)::RT
return join("", ["# ", string(text)])
end

function _combine_value_index{T0, T1}(self::JuliaTranspiler, value_type::T0, index_type::T1)::String
return join("", [string(value_type), "{", string(index_type), "}"])
end

function visit_Constant{T0}(self::JuliaTranspiler, node::T0)::String
if node.value === true
return "true"
else

if node.value === false
return "false"
else

if node.value === nothing
return "nothing"
else

if isinstance(isinstance(node.value, complex), (int, float))&&isinstance(node.value, complex) != 0||isinstance(isinstance(node.value, complex), tuple)&&isinstance(node.value, complex) != ()||isinstance(isinstance(node.value, complex), list)&&isinstance(node.value, complex) != []||isinstance(node.value, complex) === nothing||isinstance(isinstance(node.value, complex), bool)&&isinstance(node.value, complex)
str_value = string(node.value)
return endswith(str_value, "j") ? (replace(str_value, "j", "im")) : (str_value)
else

return visit_Constant(super(), node)
end
end
end
end
end

function visit_FunctionDef{T0}(self::JuliaTranspiler, node::T0)::String
body = join("\n", [self.visit(n) for n in node.body])
typenames, args = visit(self, node.args)
args_list = []
typedecls = []
index = 0
is_python_main = getattr(node, "python_main", false)
if isinstance(length(typenames)&&typenames[0] === nothing&&hasattr(node, "self_type"), (int, float))&&length(typenames)&&typenames[0] === nothing&&hasattr(node, "self_type") != 0||isinstance(length(typenames)&&typenames[0] === nothing&&hasattr(node, "self_type"), tuple)&&length(typenames)&&typenames[0] === nothing&&hasattr(node, "self_type") != ()||isinstance(length(typenames)&&typenames[0] === nothing&&hasattr(node, "self_type"), list)&&length(typenames)&&typenames[0] === nothing&&hasattr(node, "self_type") != []||length(typenames)&&typenames[0] === nothing&&hasattr(node, "self_type") === nothing||isinstance(length(typenames)&&typenames[0] === nothing&&hasattr(node, "self_type"), bool)&&length(typenames)&&typenames[0] === nothing&&hasattr(node, "self_type")
typenames[0] = node.self_type
end
for i in 0:length(args) - 1
typename = typenames[i]
arg = args[i]
if typename == "T"
typename = format("T{0}", index);
push!(typedecls, typename);
index += 1
end
push!(args_list, "{0}::{1}".format(arg, typename));
end
return_type = ""
if !(is_void_function(node))
if isinstance(node.returns, (int, float))&&node.returns != 0||isinstance(node.returns, tuple)&&node.returns != ()||isinstance(node.returns, list)&&node.returns != []||node.returns === nothing||isinstance(node.returns, bool)&&node.returns
typename = _typename_from_annotation(self, node, "returns")
return_type = join("", ["::", string(typename)])
else

return_type = "::RT"
push!(typedecls, "RT");
end
end
template = ""
if length(typedecls) > 0
template = format("{{{0}}}", ", ".join(typedecls));
end
args = join(", ", args_list)
funcdef = join("", ["function ", string(node.name), string(template), "(", string(args), ")", string(return_type)])
maybe_main = ""
if isinstance(is_python_main, (int, float))&&is_python_main != 0||isinstance(is_python_main, tuple)&&is_python_main != ()||isinstance(is_python_main, list)&&is_python_main != []||is_python_main === nothing||isinstance(is_python_main, bool)&&is_python_main
maybe_main = "\nmain()";
end
return join("", [string(funcdef), "\n", string(body), "\nend\n", string(maybe_main)])
end

function visit_Return{T0}(self::JuliaTranspiler, node::T0)::String
if isinstance(node.value, (int, float))&&node.value != 0||isinstance(node.value, tuple)&&node.value != ()||isinstance(node.value, list)&&node.value != []||node.value === nothing||isinstance(node.value, bool)&&node.value
return format("return {0}", self.visit(node.value))
end
return "return"
end

function visit_arg{T0, RT}(self::JuliaTranspiler, node::T0)::RT
id = get_id(node)
if id == "self"
return (nothing, "self")
end
typename = "T"
if isinstance(node.annotation, (int, float))&&node.annotation != 0||isinstance(node.annotation, tuple)&&node.annotation != ()||isinstance(node.annotation, list)&&node.annotation != []||node.annotation === nothing||isinstance(node.annotation, bool)&&node.annotation
typename = _typename_from_annotation(self, node);
end
return (typename, id)
end

function visit_Lambda{T0}(self::JuliaTranspiler, node::T0)::String
_, args = visit(self, node.args)
args_string = join(", ", args)
body = visit(self, node.body)
return format("({0}) -> {1}", args_string, body)
end

function visit_Attribute{T0}(self::JuliaTranspiler, node::T0)::String
attr = node.attr
value_id = visit(self, node.value)
if !(value_id)
value_id = "";
end
if value_id == "sys"
if attr == "argv"
return "append!([PROGRAM_FILE], ARGS)"
end
end
if isinstance(is_enum(value_id, node.scopes), (int, float))&&is_enum(value_id, node.scopes) != 0||isinstance(is_enum(value_id, node.scopes), tuple)&&is_enum(value_id, node.scopes) != ()||isinstance(is_enum(value_id, node.scopes), list)&&is_enum(value_id, node.scopes) != []||is_enum(value_id, node.scopes) === nothing||isinstance(is_enum(value_id, node.scopes), bool)&&is_enum(value_id, node.scopes)
return join("", [string(value_id), ".", string(attr)])
end
if isinstance(is_class_or_module(value_id, node.scopes), (int, float))&&is_class_or_module(value_id, node.scopes) != 0||isinstance(is_class_or_module(value_id, node.scopes), tuple)&&is_class_or_module(value_id, node.scopes) != ()||isinstance(is_class_or_module(value_id, node.scopes), list)&&is_class_or_module(value_id, node.scopes) != []||is_class_or_module(value_id, node.scopes) === nothing||isinstance(is_class_or_module(value_id, node.scopes), bool)&&is_class_or_module(value_id, node.scopes)
return join("", [string(value_id), "::", string(attr)])
end
return join("", [string(value_id), ".", string(attr)])
end

function visit_range{T0}(self::JuliaTranspiler, node::T0, vargs::Array{String})::String
if length(node.args) == 1
return join("", ["(0:", string(vargs[0 + 1]), " - 1)"])
else

if length(node.args) == 2
return join("", ["(", string(vargs[0 + 1]), ":", string(vargs[1 + 1]), " - 1)"])
else

if length(node.args) == 3
return join("", ["(", string(vargs[0 + 1]), ":", string(vargs[2 + 1]), ":", string(vargs[1 + 1]), "-1)"])
end
end
end
throw(Exception("encountered range() call with unknown parameters: range({})".format(vargs)))
end

function _visit_print{T0}(self::JuliaTranspiler, node::T0, vargs::Array{String})::String
args = join(", ", vargs)
return join("", ["println(join([", string(args), "], \" \"))"])
end

function visit_Call{T0}(self::JuliaTranspiler, node::T0)::String
fname = visit(self, node.func)
fndef = find(node.scopes, fname)
vargs = []
if isinstance(node.args, (int, float))&&node.args != 0||isinstance(node.args, tuple)&&node.args != ()||isinstance(node.args, list)&&node.args != []||node.args === nothing||isinstance(node.args, bool)&&node.args
vargs += [visit(self, a) for a in node.args]
end
if isinstance(node.keywords, (int, float))&&node.keywords != 0||isinstance(node.keywords, tuple)&&node.keywords != ()||isinstance(node.keywords, list)&&node.keywords != []||node.keywords === nothing||isinstance(node.keywords, bool)&&node.keywords
vargs += [visit(self, kw.value) for kw in node.keywords]
end
ret = _dispatch(self, node, fname, vargs)
if ret !== nothing
return ret
end
if isinstance(fndef&&hasattr(fndef, "args"), (int, float))&&fndef&&hasattr(fndef, "args") != 0||isinstance(fndef&&hasattr(fndef, "args"), tuple)&&fndef&&hasattr(fndef, "args") != ()||isinstance(fndef&&hasattr(fndef, "args"), list)&&fndef&&hasattr(fndef, "args") != []||fndef&&hasattr(fndef, "args") === nothing||isinstance(fndef&&hasattr(fndef, "args"), bool)&&fndef&&hasattr(fndef, "args")
converted = []
for (varg, fnarg, node_arg) in zip(vargs, fndef.args.args, node.args)
actual_type = _typename_from_annotation(self, node_arg)
declared_type = _typename_from_annotation(self, fnarg)
if isinstance(actual_type != declared_type&&actual_type != self._default_type, (int, float))&&actual_type != declared_type&&actual_type != self._default_type != 0||isinstance(actual_type != declared_type&&actual_type != self._default_type, tuple)&&actual_type != declared_type&&actual_type != self._default_type != ()||isinstance(actual_type != declared_type&&actual_type != self._default_type, list)&&actual_type != declared_type&&actual_type != self._default_type != []||actual_type != declared_type&&actual_type != self._default_type === nothing||isinstance(actual_type != declared_type&&actual_type != self._default_type, bool)&&actual_type != declared_type&&actual_type != self._default_type
push!(converted, "".join(["convert(", string(declared_type), ", ", string(varg), ")"]));
else

push!(converted, varg);
end
end
else

converted = vargs
end
args = join(", ", converted)
return join("", [string(fname), "(", string(args), ")"])
end

function visit_For{T0}(self::JuliaTranspiler, node::T0)::String
target = visit(self, node.target)
it = visit(self, node.iter)
buf = []
push!(buf, "for {0} in {1}".format(target, it));
extend(buf, [self.visit(c) for c in node.body]);
push!(buf, "end");
return join("\n", buf)
end

function visit_Str{T0}(self::JuliaTranspiler, node::T0)::String
return ("" + visit_Str(super(), node)) + ""
end

function visit_Bytes{T0}(self::JuliaTranspiler, node::T0)::String
bytes_str = node.s
bytes_str = replace(bytes_str, b"\"", b"\\"");
return ("b\"" + decode(bytes_str, "ascii", "backslashreplace")) + "\""
end

function visit_Compare{T0}(self::JuliaTranspiler, node::T0)::String
left = visit(self, node.left)
right = visit(self, node.comparators[0])
if isinstance(hasattr(node.comparators[0], "annotation"), (int, float))&&hasattr(node.comparators[0], "annotation") != 0||isinstance(hasattr(node.comparators[0], "annotation"), tuple)&&hasattr(node.comparators[0], "annotation") != ()||isinstance(hasattr(node.comparators[0], "annotation"), list)&&hasattr(node.comparators[0], "annotation") != []||hasattr(node.comparators[0], "annotation") === nothing||isinstance(hasattr(node.comparators[0], "annotation"), bool)&&hasattr(node.comparators[0], "annotation")
_generic_typename_from_annotation(self, node.comparators[0]);
value_type = getattr(node.comparators[0].annotation, "generic_container_type", nothing)
if isinstance(value_type&&value_type[0] == "Dict", (int, float))&&value_type&&value_type[0] == "Dict" != 0||isinstance(value_type&&value_type[0] == "Dict", tuple)&&value_type&&value_type[0] == "Dict" != ()||isinstance(value_type&&value_type[0] == "Dict", list)&&value_type&&value_type[0] == "Dict" != []||value_type&&value_type[0] == "Dict" === nothing||isinstance(value_type&&value_type[0] == "Dict", bool)&&value_type&&value_type[0] == "Dict"
right = join("", ["keys(", string(right), ")"]);
end
end
if isinstance(isinstance(node.ops[0], ast.In), (int, float))&&isinstance(node.ops[0], ast.In) != 0||isinstance(isinstance(node.ops[0], ast.In), tuple)&&isinstance(node.ops[0], ast.In) != ()||isinstance(isinstance(node.ops[0], ast.In), list)&&isinstance(node.ops[0], ast.In) != []||isinstance(node.ops[0], ast.In) === nothing||isinstance(isinstance(node.ops[0], ast.In), bool)&&isinstance(node.ops[0], ast.In)
return format("{0} in {1}", left, right)
else

if isinstance(isinstance(node.ops[0], ast.NotIn), (int, float))&&isinstance(node.ops[0], ast.NotIn) != 0||isinstance(isinstance(node.ops[0], ast.NotIn), tuple)&&isinstance(node.ops[0], ast.NotIn) != ()||isinstance(isinstance(node.ops[0], ast.NotIn), list)&&isinstance(node.ops[0], ast.NotIn) != []||isinstance(node.ops[0], ast.NotIn) === nothing||isinstance(isinstance(node.ops[0], ast.NotIn), bool)&&isinstance(node.ops[0], ast.NotIn)
return format("{0} not in {1}", left, right)
end
end
return visit_Compare(super(), node)
end

function visit_Name{T0}(self::JuliaTranspiler, node::T0)::String
if node.id == "None"
return "None"
else

return visit_Name(super(), node)
end
end

function visit_NameConstant{T0}(self::JuliaTranspiler, node::T0)::String
if node.value === true
return "true"
else

if node.value === false
return "false"
else

if node.value === nothing
return "None"
else

return visit_NameConstant(super(), node)
end
end
end
end

function visit_If{T0}(self::JuliaTranspiler, node::T0)::String
body_vars = set([get_id(v) for v in node.scopes[-1].body_vars])
orelse_vars = set([get_id(v) for v in node.scopes[-1].orelse_vars])
node.common_vars = intersection(body_vars, orelse_vars)
buf = []
cond = visit(self, node.test)
push!(buf, "".join(["if ", string(cond)]));
extend(buf, [self.visit(child) for child in node.body]);
orelse = [visit(self, child) for child in node.orelse]
if isinstance(orelse, (int, float))&&orelse != 0||isinstance(orelse, tuple)&&orelse != ()||isinstance(orelse, list)&&orelse != []||orelse === nothing||isinstance(orelse, bool)&&orelse
push!(buf, "else\n");
extend(buf, orelse);
push!(buf, "end");
else

push!(buf, "end");
end
return join("\n", buf)
end

function visit_While{T0}(self::JuliaTranspiler, node::T0)::String
buf = []
push!(buf, "while {0}".format(self.visit(node.test)));
extend(buf, [self.visit(n) for n in node.body]);
push!(buf, "end");
return join("\n", buf)
end

function visit_UnaryOp{T0}(self::JuliaTranspiler, node::T0)::String
if isinstance(isinstance(node.op, ast.USub), (int, float))&&isinstance(node.op, ast.USub) != 0||isinstance(isinstance(node.op, ast.USub), tuple)&&isinstance(node.op, ast.USub) != ()||isinstance(isinstance(node.op, ast.USub), list)&&isinstance(node.op, ast.USub) != []||isinstance(node.op, ast.USub) === nothing||isinstance(isinstance(node.op, ast.USub), bool)&&isinstance(node.op, ast.USub)
if isinstance(isinstance(node.operand, (ast.Call, ast.Num)), (int, float))&&isinstance(node.operand, (ast.Call, ast.Num)) != 0||isinstance(isinstance(node.operand, (ast.Call, ast.Num)), tuple)&&isinstance(node.operand, (ast.Call, ast.Num)) != ()||isinstance(isinstance(node.operand, (ast.Call, ast.Num)), list)&&isinstance(node.operand, (ast.Call, ast.Num)) != []||isinstance(node.operand, (ast.Call, ast.Num)) === nothing||isinstance(isinstance(node.operand, (ast.Call, ast.Num)), bool)&&isinstance(node.operand, (ast.Call, ast.Num))
return format("-{0}", self.visit(node.operand))
else

return format("-({0})", self.visit(node.operand))
end
else

return visit_UnaryOp(super(), node)
end
end

function visit_BinOp{T0}(self::JuliaTranspiler, node::T0)::String
if isinstance(isinstance(node.left, ast.List)&&isinstance(node.op, ast.Mult)&&isinstance(node.right, ast.Num), (int, float))&&isinstance(node.left, ast.List)&&isinstance(node.op, ast.Mult)&&isinstance(node.right, ast.Num) != 0||isinstance(isinstance(node.left, ast.List)&&isinstance(node.op, ast.Mult)&&isinstance(node.right, ast.Num), tuple)&&isinstance(node.left, ast.List)&&isinstance(node.op, ast.Mult)&&isinstance(node.right, ast.Num) != ()||isinstance(isinstance(node.left, ast.List)&&isinstance(node.op, ast.Mult)&&isinstance(node.right, ast.Num), list)&&isinstance(node.left, ast.List)&&isinstance(node.op, ast.Mult)&&isinstance(node.right, ast.Num) != []||isinstance(node.left, ast.List)&&isinstance(node.op, ast.Mult)&&isinstance(node.right, ast.Num) === nothing||isinstance(isinstance(node.left, ast.List)&&isinstance(node.op, ast.Mult)&&isinstance(node.right, ast.Num), bool)&&isinstance(node.left, ast.List)&&isinstance(node.op, ast.Mult)&&isinstance(node.right, ast.Num)
return format("std::vector ({0},{1})", self.visit(node.right), self.visit(node.left.elts[0]))
else

if isinstance(isinstance(node.op, ast.MatMult), (int, float))&&isinstance(node.op, ast.MatMult) != 0||isinstance(isinstance(node.op, ast.MatMult), tuple)&&isinstance(node.op, ast.MatMult) != ()||isinstance(isinstance(node.op, ast.MatMult), list)&&isinstance(node.op, ast.MatMult) != []||isinstance(node.op, ast.MatMult) === nothing||isinstance(isinstance(node.op, ast.MatMult), bool)&&isinstance(node.op, ast.MatMult)
return format("({0}*{1})", self.visit(node.left), self.visit(node.right))
else

return visit_BinOp(super(), node)
end
end
end

function visit_ClassDef{T0}(self::JuliaTranspiler, node::T0)::String
extractor = DeclarationExtractor(JuliaTranspiler())
visit(extractor, node);
declarations = get_declarations(extractor)
node.declarations = get_declarations(extractor)
node.class_assignments = extractor.class_assignments
ret = visit_ClassDef(super(), node)
if ret !== nothing
return ret
end
decorators = [get_id(d) for d in node.decorator_list]
decorators = [class_for_typename(t, nothing, self._imported_names) for t in decorators];
for d in decorators
if d in keys(CLASS_DISPATCH_TABLE)
ret = CLASS_DISPATCH_TABLE[d](self, node);
if ret !== nothing
return ret
end
end
end
fields = []
index = 0
for (declaration, typename) in items(declarations)
if typename === nothing
typename = format("ST{0}", index);
index += 1
end
push!(fields, "".join([string(declaration), "::", string(typename)]));
end
fields = join("\n", fields);
struct_def = join("", ["struct ", string(node.name), "\n", string(fields), "\nend\n"])
for b in node.body
if isinstance(isinstance(b, ast.FunctionDef), (int, float))&&isinstance(b, ast.FunctionDef) != 0||isinstance(isinstance(b, ast.FunctionDef), tuple)&&isinstance(b, ast.FunctionDef) != ()||isinstance(isinstance(b, ast.FunctionDef), list)&&isinstance(b, ast.FunctionDef) != []||isinstance(b, ast.FunctionDef) === nothing||isinstance(isinstance(b, ast.FunctionDef), bool)&&isinstance(b, ast.FunctionDef)
b.self_type = node.name
end
end
body = join("\n", [self.visit(b) for b in node.body])
return join("", [string(struct_def), "\n", string(body)])
end

function _visit_enum{T0}(self::JuliaTranspiler, node::T0, typename::String, fields::Array{Tuple})::String
add(self._usings, "SuperEnum");
fields_list = []
sep = typename == "String" ? ("=>") : ("=")
for (field, value) in fields
fields_list += [join("", ["                ", string(field), " ", string(sep), " ", string(value), "\n            "])]
end
fields_str = join("", fields_list)
return dedent(textwrap, "".join(["            @se ", string(node.name), " begin\n", string(fields_str), "\n            end\n            "]))
end

function visit_StrEnum{T0}(self::JuliaTranspiler, node::T0)::String
fields = []
for (i, (member, var)) in node.class_assignments.items().iter().enumerate()
var = visit(self, var)
if var == _AUTO_INVOKED
var = join("", ["\"", string(member), "\""]);
end
push!(fields, (member, var));
end
return _visit_enum(self, node, "String", convert(Array{Tuple}, fields))
end

function visit_IntEnum{T0}(self::JuliaTranspiler, node::T0)::String
fields = []
for (i, (member, var)) in node.class_assignments.items().iter().enumerate()
var = visit(self, var)
if var == _AUTO_INVOKED
var = i;
end
push!(fields, (member, var));
end
return _visit_enum(self, node, "Int64", convert(Array{Tuple}, fields))
end

function visit_IntFlag{T0}(self::JuliaTranspiler, node::T0)::String
fields = []
for (i, (member, var)) in node.class_assignments.items().iter().enumerate()
var = visit(self, var)
if var == _AUTO_INVOKED
var = 1 << i;
end
push!(fields, (member, var));
end
return _visit_enum(self, node, "Int64", convert(Array{Tuple}, fields))
end

function _import(self::JuliaTranspiler, name::String)::String
return join("", ["import ", string(name)])
end

function _import_from(self::JuliaTranspiler, module_name::String, names::Array{String}, level::Int64)::String
if length(names) == 1
name = names[0 + 1]
lookup = join("", [string(module_name), ".", string(name)])
if lookup in keys(MODULE_DISPATCH_TABLE)
jl_module_name, jl_name = MODULE_DISPATCH_TABLE[lookup]
jl_module_name = replace(jl_module_name, ".", "::")
return join("", ["using ", string(jl_module_name), ": ", string(jl_name)])
end
end
module_name = replace(module_name, ".", "::");
names = join(", ", names);
return join("", ["using ", string(module_name), ": ", string(names)])
end

function visit_List{T0}(self::JuliaTranspiler, node::T0)::String
elements = [visit(self, e) for e in node.elts]
elements_str = join(", ", elements)
return join("", ["[", string(elements_str), "]"])
end

function visit_Set{T0}(self::JuliaTranspiler, node::T0)::String
elements = [visit(self, e) for e in node.elts]
elements_str = join(", ", elements)
return join("", ["Set([", string(elements_str), "])"])
end

function visit_Dict{T0}(self::JuliaTranspiler, node::T0)::String
keys = [visit(self, k) for k in node.keys]
values = [visit(self, k) for k in node.values]
kv_pairs = join(", ", ["".join([string(k), " => ", string(v)]) for (k, v) in zip(keys, values)])
return join("", ["Dict(", string(kv_pairs), ")"])
end

function visit_Subscript{T0}(self::JuliaTranspiler, node::T0)::String
value = visit(self, node.value)
index = visit(self, node.slice)
if isinstance(hasattr(node, "is_annotation"), (int, float))&&hasattr(node, "is_annotation") != 0||isinstance(hasattr(node, "is_annotation"), tuple)&&hasattr(node, "is_annotation") != ()||isinstance(hasattr(node, "is_annotation"), list)&&hasattr(node, "is_annotation") != []||hasattr(node, "is_annotation") === nothing||isinstance(hasattr(node, "is_annotation"), bool)&&hasattr(node, "is_annotation")
if value in self.CONTAINER_TYPE_MAP
value = self.CONTAINER_TYPE_MAP[value];
end
if value == "Tuple"
return format("({0})", index)
end
return format("{0}{{{1}}}", value, index)
end
_generic_typename_from_annotation(self, node.value);
if isinstance(hasattr(node.value, "annotation"), (int, float))&&hasattr(node.value, "annotation") != 0||isinstance(hasattr(node.value, "annotation"), tuple)&&hasattr(node.value, "annotation") != ()||isinstance(hasattr(node.value, "annotation"), list)&&hasattr(node.value, "annotation") != []||hasattr(node.value, "annotation") === nothing||isinstance(hasattr(node.value, "annotation"), bool)&&hasattr(node.value, "annotation")
value_type = getattr(node.value.annotation, "generic_container_type", nothing)
if isinstance(value_type !== nothing&&value_type[0] == "List", (int, float))&&value_type !== nothing&&value_type[0] == "List" != 0||isinstance(value_type !== nothing&&value_type[0] == "List", tuple)&&value_type !== nothing&&value_type[0] == "List" != ()||isinstance(value_type !== nothing&&value_type[0] == "List", list)&&value_type !== nothing&&value_type[0] == "List" != []||value_type !== nothing&&value_type[0] == "List" === nothing||isinstance(value_type !== nothing&&value_type[0] == "List", bool)&&value_type !== nothing&&value_type[0] == "List"
return format("{0}[{1} + 1]", value, index)
end
end
return format("{0}[{1}]", value, index)
end

function visit_Index{T0}(self::JuliaTranspiler, node::T0)::String
return visit(self, node.value)
end

function visit_Slice{T0}(self::JuliaTranspiler, node::T0)::String
lower = ""
if isinstance(node.lower, (int, float))&&node.lower != 0||isinstance(node.lower, tuple)&&node.lower != ()||isinstance(node.lower, list)&&node.lower != []||node.lower === nothing||isinstance(node.lower, bool)&&node.lower
lower = visit(self, node.lower);
end
upper = ""
if isinstance(node.upper, (int, float))&&node.upper != 0||isinstance(node.upper, tuple)&&node.upper != ()||isinstance(node.upper, list)&&node.upper != []||node.upper === nothing||isinstance(node.upper, bool)&&node.upper
upper = visit(self, node.upper);
end
return format("{0}..{1}", lower, upper)
end

function visit_Tuple{T0}(self::JuliaTranspiler, node::T0)::String
elts = [visit(self, e) for e in node.elts]
elts = join(", ", elts);
if isinstance(hasattr(node, "is_annotation"), (int, float))&&hasattr(node, "is_annotation") != 0||isinstance(hasattr(node, "is_annotation"), tuple)&&hasattr(node, "is_annotation") != ()||isinstance(hasattr(node, "is_annotation"), list)&&hasattr(node, "is_annotation") != []||hasattr(node, "is_annotation") === nothing||isinstance(hasattr(node, "is_annotation"), bool)&&hasattr(node, "is_annotation")
return elts
end
return format("({0})", elts)
end

function visit_Try{T0, T1}(self::JuliaTranspiler, node::T0, finallybody::T1)::String
buf = []
push!(buf, "try");
extend(buf, [self.visit(child) for child in node.body]);
if length(node.handlers) > 0
push!(buf, "catch exn");
for handler in node.handlers
push!(buf, self.visit(handler));
end
end
if isinstance(node.finalbody, (int, float))&&node.finalbody != 0||isinstance(node.finalbody, tuple)&&node.finalbody != ()||isinstance(node.finalbody, list)&&node.finalbody != []||node.finalbody === nothing||isinstance(node.finalbody, bool)&&node.finalbody
push!(buf, "finally");
extend(buf, [self.visit(child) for child in node.finalbody]);
end
push!(buf, "end");
return join("\n", buf)
end

function visit_ExceptHandler{T0}(self::JuliaTranspiler, node::T0)::String
buf = []
name = "exn"
if isinstance(node.name, (int, float))&&node.name != 0||isinstance(node.name, tuple)&&node.name != ()||isinstance(node.name, list)&&node.name != []||node.name === nothing||isinstance(node.name, bool)&&node.name
push!(buf, "".join([" let ", string(node.name), " = ", string(name)]));
name = node.name;
end
if isinstance(node.type, (int, float))&&node.type != 0||isinstance(node.type, tuple)&&node.type != ()||isinstance(node.type, list)&&node.type != []||node.type === nothing||isinstance(node.type, bool)&&node.type
type_str = visit(self, node.type)
push!(buf, "".join(["if ", string(name), " isa ", string(type_str)]));
end
extend(buf, [self.visit(child) for child in node.body]);
if isinstance(node.type, (int, float))&&node.type != 0||isinstance(node.type, tuple)&&node.type != ()||isinstance(node.type, list)&&node.type != []||node.type === nothing||isinstance(node.type, bool)&&node.type
push!(buf, "end");
end
if isinstance(node.name, (int, float))&&node.name != 0||isinstance(node.name, tuple)&&node.name != ()||isinstance(node.name, list)&&node.name != []||node.name === nothing||isinstance(node.name, bool)&&node.name
push!(buf, "end");
end
return join("\n", buf)
end

function visit_Assert{T0}(self::JuliaTranspiler, node::T0)::String
return format("@assert({0})", self.visit(node.test))
end

function visit_AnnAssign{T0}(self::JuliaTranspiler, node::T0)::String
target, type_str, val = visit_AnnAssign(super(), node)
if type_str == self._default_type
return join("", [string(target), " = ", string(val)])
end
return join("", [string(target), "::", string(type_str), " = ", string(val)])
end

function visit_AugAssign{T0}(self::JuliaTranspiler, node::T0)::String
target = visit(self, node.target)
op = visit(self, node.op)
val = visit(self, node.value)
return format("{0} {1}= {2}", target, op, val)
end

function _visit_AssignOne{T0, T1}(self::JuliaTranspiler, node::T0, target::T1)::String
if isinstance(isinstance(target, ast.Tuple), (int, float))&&isinstance(target, ast.Tuple) != 0||isinstance(isinstance(target, ast.Tuple), tuple)&&isinstance(target, ast.Tuple) != ()||isinstance(isinstance(target, ast.Tuple), list)&&isinstance(target, ast.Tuple) != []||isinstance(target, ast.Tuple) === nothing||isinstance(isinstance(target, ast.Tuple), bool)&&isinstance(target, ast.Tuple)
elts = [visit(self, e) for e in target.elts]
value = visit(self, node.value)
return format("{0} = {1}", ", ".join(elts), value)
end
if isinstance(isinstance(node.scopes[-1], ast.If), (int, float))&&isinstance(node.scopes[-1], ast.If) != 0||isinstance(isinstance(node.scopes[-1], ast.If), tuple)&&isinstance(node.scopes[-1], ast.If) != ()||isinstance(isinstance(node.scopes[-1], ast.If), list)&&isinstance(node.scopes[-1], ast.If) != []||isinstance(node.scopes[-1], ast.If) === nothing||isinstance(isinstance(node.scopes[-1], ast.If), bool)&&isinstance(node.scopes[-1], ast.If)
outer_if = node.scopes[-1]
target_id = visit(self, target)
if target_id in outer_if.common_vars
value = visit(self, node.value)
return format("{0} = {1}", target_id, value)
end
end
if isinstance(isinstance(target, ast.Subscript)||isinstance(target, ast.Attribute), (int, float))&&isinstance(target, ast.Subscript)||isinstance(target, ast.Attribute) != 0||isinstance(isinstance(target, ast.Subscript)||isinstance(target, ast.Attribute), tuple)&&isinstance(target, ast.Subscript)||isinstance(target, ast.Attribute) != ()||isinstance(isinstance(target, ast.Subscript)||isinstance(target, ast.Attribute), list)&&isinstance(target, ast.Subscript)||isinstance(target, ast.Attribute) != []||isinstance(target, ast.Subscript)||isinstance(target, ast.Attribute) === nothing||isinstance(isinstance(target, ast.Subscript)||isinstance(target, ast.Attribute), bool)&&isinstance(target, ast.Subscript)||isinstance(target, ast.Attribute)
target = visit(self, target);
value = visit(self, node.value)
if value === nothing
value = "None";
end
return format("{0} = {1}", target, value)
end
definition = find(node.scopes.parent_scopes, get_id(target))
if definition === nothing
definition = find(node.scopes, get_id(target));
end
if isinstance(isinstance(target, ast.Name)&&defined_before(definition, node), (int, float))&&isinstance(target, ast.Name)&&defined_before(definition, node) != 0||isinstance(isinstance(target, ast.Name)&&defined_before(definition, node), tuple)&&isinstance(target, ast.Name)&&defined_before(definition, node) != ()||isinstance(isinstance(target, ast.Name)&&defined_before(definition, node), list)&&isinstance(target, ast.Name)&&defined_before(definition, node) != []||isinstance(target, ast.Name)&&defined_before(definition, node) === nothing||isinstance(isinstance(target, ast.Name)&&defined_before(definition, node), bool)&&isinstance(target, ast.Name)&&defined_before(definition, node)
target_str = visit(self, target)
value = visit(self, node.value)
return join("", [string(target_str), " = ", string(value), ";"])
else

target = visit(self, target);
value = visit(self, node.value)
return join("", [string(target), " = ", string(value)])
end
end

function visit_Delete{T0}(self::JuliaTranspiler, node::T0)::String
target = node.targets[0]
return format("{0}.drop()", self.visit(target))
end

function visit_Raise{T0}(self::JuliaTranspiler, node::T0)::String
if node.exc !== nothing
return format("throw({0})", self.visit(node.exc))
end
return "error()"
end

function visit_Await{T0}(self::JuliaTranspiler, node::T0)::String
return format("await!({0})", self.visit(node.value))
end

function visit_AsyncFunctionDef{T0}(self::JuliaTranspiler, node::T0)::String
return format("#[async]\n{0}", self.visit_FunctionDef(node))
end

function visit_Yield{T0}(self::JuliaTranspiler, node::T0)::String
return "//yield is unimplemented"
end

function visit_Print{T0}(self::JuliaTranspiler, node::T0)::String
buf = []
for n in node.values
value = visit(self, n)
push!(buf, "println(\"{{:?}}\",{0})".format(value));
end
return join("\n", buf)
end

function visit_GeneratorExp{T0}(self::JuliaTranspiler, node::T0)::String
elt = visit(self, node.elt)
generators = node.generators
gen_expr = _visit_generators(self, generators)
return join("", ["(", string(elt), " ", string(gen_expr), ")"])
end

function visit_ListComp{T0}(self::JuliaTranspiler, node::T0)::String
elt = visit(self, node.elt)
generators = node.generators
list_comp = _visit_generators(self, generators)
return join("", ["[", string(elt), " ", string(list_comp), "]"])
end

function visit_DictComp(self::JuliaTranspiler, node::ast.DictComp)::String
key = visit(self, node.key)
value = visit(self, node.value)
generators = node.generators
dict_comp = join("", [string(key), " => ", string(value), " "]) + _visit_generators(self, generators)
return join("", ["Dict(", string(dict_comp), ")"])
end

function _visit_generators{T0, RT}(self::JuliaTranspiler, generators::T0)::RT
gen_exp = []
for i in 0:length(generators) - 1
generator = generators[i]
target = visit(self, generator.target)
iter = visit(self, generator.iter)
exp = join("", ["for ", string(target), " in ", string(iter)])
i == 0 ? (push!(gen_exp, exp)) : (push!(gen_exp, "".join([" ", string(exp)])));
filter_str = ""
if length(generator.ifs) == 1
filter_str += join("", [" if ", string(self.visit(generator.ifs[0])), " "])
else

for i in 0:length(generator.ifs) - 1
gen_if = generator.ifs[i]
filter_str += i == 0 ? (join("", [" if ", string(self.visit(gen_if))])) : (join("", [" && ", string(self.visit(gen_if)), " "]))
end
end
push!(gen_exp, filter_str);
end
return join("", gen_exp)
end

function visit_Global{T0}(self::JuliaTranspiler, node::T0)::String
return format("//global {0}", ", ".join(node.names))
end

function visit_Starred{T0}(self::JuliaTranspiler, node::T0)::String
return format("starred!({0})/*unsupported*/", self.visit(node.value))
end

function visit_IfExp{T0}(self::JuliaTranspiler, node::T0)::String
body = visit(self, node.body)
orelse = visit(self, node.orelse)
test = visit(self, node.test)
return join("", [string(test), " ? (", string(body), ") : (", string(orelse), ")"])
end

