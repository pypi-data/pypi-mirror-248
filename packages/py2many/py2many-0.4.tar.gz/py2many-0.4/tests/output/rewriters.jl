import ast

import textwrap
using py2many::analysis: get_id
using py2many::ast_helpers: create_ast_block, create_ast_node
using py2many::astx: ASTxFunctionDef
using py2many::clike: CLikeTranspiler
using py2many::inference: get_inferred_type
using py2many::scope: ScopeList

using py2many::tracer: find_node_by_type
struct InferredAnnAssignRewriter

end

function visit_Assign{T0, RT}(self::InferredAnnAssignRewriter, node::T0)::RT
target = node.targets[0]
if isinstance(isinstance(target, ast.Subscript), (int, float))&&isinstance(target, ast.Subscript) != 0||isinstance(isinstance(target, ast.Subscript), tuple)&&isinstance(target, ast.Subscript) != ()||isinstance(isinstance(target, ast.Subscript), list)&&isinstance(target, ast.Subscript) != []||isinstance(target, ast.Subscript) === nothing||isinstance(isinstance(target, ast.Subscript), bool)&&isinstance(target, ast.Subscript)
return node
end
annotation = getattr(target, "annotation", false)
if !(annotation)
return node
end
if isinstance(isinstance(annotation, ast.ClassDef), (int, float))&&isinstance(annotation, ast.ClassDef) != 0||isinstance(isinstance(annotation, ast.ClassDef), tuple)&&isinstance(annotation, ast.ClassDef) != ()||isinstance(isinstance(annotation, ast.ClassDef), list)&&isinstance(annotation, ast.ClassDef) != []||isinstance(annotation, ast.ClassDef) === nothing||isinstance(isinstance(annotation, ast.ClassDef), bool)&&isinstance(annotation, ast.ClassDef)
annotation = Name(ast, get_id(annotation));
end
col_offset = getattr(node, "col_offset", nothing)
assigns = []
for assign_target in node.targets
definition = find(node.scopes.parent_scopes, get_id(assign_target))
if definition === nothing
definition = find(node.scopes, get_id(assign_target));
end
if definition !== assign_target
previous_type = get_inferred_type(definition)
if get_id(previous_type) == get_id(annotation)
if length(node.targets) == 1
return node
else

new_node = Assign(ast, [assign_target], node.value, node.lineno, col_offset)
push!(assigns, new_node);
continue;
end
end
end
new_node = AnnAssign(ast, assign_target, node.value, node.lineno, col_offset, true, annotation)
push!(assigns, new_node);
end
if length(assigns) == 1
return assigns[0]
end
return create_ast_block(assigns, node)
end

struct ComplexDestructuringRewriter
_disable::Bool
_no_underscore::Bool
_temp::Int64
end

function __init__{T0}(self::ComplexDestructuringRewriter, language::T0)
__init__(super());
self._disable = false
if language in Set(["cpp", "julia", "dart", "v"])
self._disable = true
end
self._no_underscore = false
if language in Set(["nim"])
self._no_underscore = true
end
self._temp = 0
end

function _get_temp{RT}(self::ComplexDestructuringRewriter)::RT
self._temp += 1
if isinstance(self._no_underscore, (int, float))&&self._no_underscore != 0||isinstance(self._no_underscore, tuple)&&self._no_underscore != ()||isinstance(self._no_underscore, list)&&self._no_underscore != []||self._no_underscore === nothing||isinstance(self._no_underscore, bool)&&self._no_underscore
return join("", ["tmp", string(self._temp)])
end
return join("", ["__tmp", string(self._temp)])
end

function visit_Assign{T0, RT}(self::ComplexDestructuringRewriter, node::T0)::RT
if isinstance(self._disable, (int, float))&&self._disable != 0||isinstance(self._disable, tuple)&&self._disable != ()||isinstance(self._disable, list)&&self._disable != []||self._disable === nothing||isinstance(self._disable, bool)&&self._disable
return node
end
target = node.targets[0]
if isinstance(isinstance(target, ast.Tuple)&&!(isinstance(target.elts[0], ast.Name)), (int, float))&&isinstance(target, ast.Tuple)&&!(isinstance(target.elts[0], ast.Name)) != 0||isinstance(isinstance(target, ast.Tuple)&&!(isinstance(target.elts[0], ast.Name)), tuple)&&isinstance(target, ast.Tuple)&&!(isinstance(target.elts[0], ast.Name)) != ()||isinstance(isinstance(target, ast.Tuple)&&!(isinstance(target.elts[0], ast.Name)), list)&&isinstance(target, ast.Tuple)&&!(isinstance(target.elts[0], ast.Name)) != []||isinstance(target, ast.Tuple)&&!(isinstance(target.elts[0], ast.Name)) === nothing||isinstance(isinstance(target, ast.Tuple)&&!(isinstance(target.elts[0], ast.Name)), bool)&&isinstance(target, ast.Tuple)&&!(isinstance(target.elts[0], ast.Name))
temps = []
orig = [nothing]*length(target.elts)
body = [node]
for i in 0:length(target.elts) - 1
push!(temps, ast.Name(self._get_temp(), node.lineno));
target.elts[i], orig[i] = (temps[i], target.elts[i])
push!(body, ast.Assign([orig[i]], temps[i], node.lineno));
end
return create_ast_block(body, node)
end
return node
end

struct RenameTransformer
_old_name::
_new_name::
end

function __init__{T0, T1}(self::RenameTransformer, old_name::T0, new_name::T1)
__init__(super());
self._old_name = old_name
self._new_name = new_name
end

function visit_Name{T0, RT}(self::RenameTransformer, node::T0)::RT
if node.id == self._old_name
node.id = self._new_name
end
return node
end

function visit_FunctionDef{T0, RT}(self::RenameTransformer, node::T0)::RT
if node.name == self._old_name
node.name = self._new_name
end
generic_visit(self, node);
return node
end

function visit_Call{T0, RT}(self::RenameTransformer, node::T0)::RT
if isinstance(isinstance(node.func, ast.Name)&&node.func.id == self._old_name, (int, float))&&isinstance(node.func, ast.Name)&&node.func.id == self._old_name != 0||isinstance(isinstance(node.func, ast.Name)&&node.func.id == self._old_name, tuple)&&isinstance(node.func, ast.Name)&&node.func.id == self._old_name != ()||isinstance(isinstance(node.func, ast.Name)&&node.func.id == self._old_name, list)&&isinstance(node.func, ast.Name)&&node.func.id == self._old_name != []||isinstance(node.func, ast.Name)&&node.func.id == self._old_name === nothing||isinstance(isinstance(node.func, ast.Name)&&node.func.id == self._old_name, bool)&&isinstance(node.func, ast.Name)&&node.func.id == self._old_name
node.func.id = self._new_name
end
generic_visit(self, node);
return node
end

struct WithToBlockTransformer
_no_underscore::Bool
_temp::Int64
end

function __init__{T0}(self::WithToBlockTransformer, language::T0)
__init__(super());
self._no_underscore = false
if language in Set(["nim"])
self._no_underscore = true
end
self._temp = 0
end

function _get_temp{RT}(self::WithToBlockTransformer)::RT
self._temp += 1
if isinstance(self._no_underscore, (int, float))&&self._no_underscore != 0||isinstance(self._no_underscore, tuple)&&self._no_underscore != ()||isinstance(self._no_underscore, list)&&self._no_underscore != []||self._no_underscore === nothing||isinstance(self._no_underscore, bool)&&self._no_underscore
return join("", ["tmp", string(self._temp)])
end
return join("", ["__tmp", string(self._temp)])
end

function visit_With{T0, RT}(self::WithToBlockTransformer, node::T0)::RT
generic_visit(self, node);
stmts = []
for i in node.items
if isinstance(i.optional_vars, (int, float))&&i.optional_vars != 0||isinstance(i.optional_vars, tuple)&&i.optional_vars != ()||isinstance(i.optional_vars, list)&&i.optional_vars != []||i.optional_vars === nothing||isinstance(i.optional_vars, bool)&&i.optional_vars
target = i.optional_vars
else

target = Name(ast, self._get_temp(), node.lineno)
end
stmt = Assign(ast, [target], i.context_expr, node.lineno)
push!(stmts, stmt);
end
node.body = stmts + node.body
ret = create_ast_block(node.body, node)
ret.unpack = false
return ret
end

function capitalize_first{T0, RT}(name::T0)::RT
first = upper(name[0])
remainder = list(name)
remove(remainder, name[0]);
remainder = join("", remainder);
return first + remainder
end

function camel_case{T0, RT}(name::T0)::RT
if "_" not in name
return name
end
if isinstance(startswith(name, "__")&&endswith(name, "__"), (int, float))&&startswith(name, "__")&&endswith(name, "__") != 0||isinstance(startswith(name, "__")&&endswith(name, "__"), tuple)&&startswith(name, "__")&&endswith(name, "__") != ()||isinstance(startswith(name, "__")&&endswith(name, "__"), list)&&startswith(name, "__")&&endswith(name, "__") != []||startswith(name, "__")&&endswith(name, "__") === nothing||isinstance(startswith(name, "__")&&endswith(name, "__"), bool)&&startswith(name, "__")&&endswith(name, "__")
return name
end
return join("", (part ? (capitalize_first(part)) : ("") for part in name.split("_")))
end

function rename{T0, T1, T2}(scope::T0, old_name::T1, new_name::T2)
tx = RenameTransformer(old_name, new_name)
visit(tx, scope);
end

struct PythonMainRewriter
main_signature_arg_names::
end

function __init__{T0}(self::PythonMainRewriter, main_signature_arg_names::T0)
self.main_signature_arg_names = set(main_signature_arg_names)
__init__(super());
end

function visit_If{T0, RT}(self::PythonMainRewriter, node::T0)::RT
is_main = isinstance(node.test, ast.Compare)&&isinstance(node.test.left, ast.Name)&&node.test.left.id == "__name__"&&isinstance(node.test.ops[0], ast.Eq)&&isinstance(node.test.comparators[0], ast.Constant)&&node.test.comparators[0].value == "__main__"
if isinstance(is_main, (int, float))&&is_main != 0||isinstance(is_main, tuple)&&is_main != ()||isinstance(is_main, list)&&is_main != []||is_main === nothing||isinstance(is_main, bool)&&is_main
if isinstance(hasattr(node, "scopes")&&length(node.scopes) > 1, (int, float))&&hasattr(node, "scopes")&&length(node.scopes) > 1 != 0||isinstance(hasattr(node, "scopes")&&length(node.scopes) > 1, tuple)&&hasattr(node, "scopes")&&length(node.scopes) > 1 != ()||isinstance(hasattr(node, "scopes")&&length(node.scopes) > 1, list)&&hasattr(node, "scopes")&&length(node.scopes) > 1 != []||hasattr(node, "scopes")&&length(node.scopes) > 1 === nothing||isinstance(hasattr(node, "scopes")&&length(node.scopes) > 1, bool)&&hasattr(node, "scopes")&&length(node.scopes) > 1
rename(node.scopes[-2], convert(, "main"), convert(, "main_func"));
end
if self.main_signature_arg_names == Set(["argc", "argv"])
ret = cast(ast.FunctionDef, create_ast_node("def main(argc: int, argv: List[str]) -> int: True", node))
else

if self.main_signature_arg_names == Set(["argv"])
ret = create_ast_node("def main(argv: List[str]): True", node)
else

ret = create_ast_node("def main(): True")
end
end
ret = cast(ASTxFunctionDef, ret)
ret.lineno = node.lineno
ret.body = node.body
ret.python_main = true
return ret
end
return node
end

struct FStringJoinRewriter

end

function __init__{T0}(self::FStringJoinRewriter, language::T0)
__init__(super());
end

function visit_JoinedStr{T0, RT}(self::FStringJoinRewriter, node::T0)::RT
new_node = cast(ast.Expr, create_ast_node("\"\".join([])", node)).value
new_node = cast(ast.Call, new_node);
args = new_node.args
arg0 = cast(ast.List, args[0])
for v in node.values
if isinstance(isinstance(v, ast.Constant), (int, float))&&isinstance(v, ast.Constant) != 0||isinstance(isinstance(v, ast.Constant), tuple)&&isinstance(v, ast.Constant) != ()||isinstance(isinstance(v, ast.Constant), list)&&isinstance(v, ast.Constant) != []||isinstance(v, ast.Constant) === nothing||isinstance(isinstance(v, ast.Constant), bool)&&isinstance(v, ast.Constant)
append(arg0.elts, v);
else

if isinstance(isinstance(v, ast.FormattedValue), (int, float))&&isinstance(v, ast.FormattedValue) != 0||isinstance(isinstance(v, ast.FormattedValue), tuple)&&isinstance(v, ast.FormattedValue) != ()||isinstance(isinstance(v, ast.FormattedValue), list)&&isinstance(v, ast.FormattedValue) != []||isinstance(v, ast.FormattedValue) === nothing||isinstance(isinstance(v, ast.FormattedValue), bool)&&isinstance(v, ast.FormattedValue)
append(arg0.elts, ast.Call(ast.Name("str", "Load"), [v.value], []));
end
end
end
new_node.lineno = node.lineno
new_node.col_offset = node.col_offset
fix_missing_locations(ast, new_node);
return new_node
end

struct DocStringToCommentRewriter
_docstrings::
_docstring_parent::Dict
end

function __init__{T0}(self::DocStringToCommentRewriter, language::T0)
__init__(super());
self._docstrings = set()
self._docstring_parent = Dict()
end

function _get_doc_node{T0}(self::DocStringToCommentRewriter, node::T0)::Nothing{ast.AST}
if !(node.body&&isinstance(node.body[0], ast.Expr))
return nothing
end
node = node.body[0].value;
if isinstance(isinstance(node, ast.Str), (int, float))&&isinstance(node, ast.Str) != 0||isinstance(isinstance(node, ast.Str), tuple)&&isinstance(node, ast.Str) != ()||isinstance(isinstance(node, ast.Str), list)&&isinstance(node, ast.Str) != []||isinstance(node, ast.Str) === nothing||isinstance(isinstance(node, ast.Str), bool)&&isinstance(node, ast.Str)
return node
else

if isinstance(isinstance(node, ast.Constant)&&isinstance(node.value, str), (int, float))&&isinstance(node, ast.Constant)&&isinstance(node.value, str) != 0||isinstance(isinstance(node, ast.Constant)&&isinstance(node.value, str), tuple)&&isinstance(node, ast.Constant)&&isinstance(node.value, str) != ()||isinstance(isinstance(node, ast.Constant)&&isinstance(node.value, str), list)&&isinstance(node, ast.Constant)&&isinstance(node.value, str) != []||isinstance(node, ast.Constant)&&isinstance(node.value, str) === nothing||isinstance(isinstance(node, ast.Constant)&&isinstance(node.value, str), bool)&&isinstance(node, ast.Constant)&&isinstance(node.value, str)
return node
end
end
return nothing
end

function _visit_documentable{T0, RT}(self::DocStringToCommentRewriter, node::T0)::RT
doc_node = _get_doc_node(self, node)
add(self._docstrings, doc_node);
self._docstring_parent[doc_node] = node
generic_visit(self, node);
return node
end

function visit_FunctionDef{T0, RT}(self::DocStringToCommentRewriter, node::T0)::RT
return _visit_documentable(self, node)
end

function visit_ClassDef{T0, RT}(self::DocStringToCommentRewriter, node::T0)::RT
return _visit_documentable(self, node)
end

function visit_Module{T0, RT}(self::DocStringToCommentRewriter, node::T0)::RT
return _visit_documentable(self, node)
end

function visit_Constant{T0, RT}(self::DocStringToCommentRewriter, node::T0)::RT
if node in self._docstrings
parent = self._docstring_parent[node]
parent.docstring_comment = Constant(ast, node.value)
return nothing
end
return node
end

function visit_Expr{T0, RT}(self::DocStringToCommentRewriter, node::T0)::RT
generic_visit(self, node);
if !(hasattr(node, "value"))
return nothing
end
return node
end

struct PrintBoolRewriter
_language::
end

function __init__{T0}(self::PrintBoolRewriter, language::T0)
__init__(super());
self._language = language
end

function _do_other_rewrite{T0}(self::PrintBoolRewriter, node::T0)::ast.AST
ifexpr = cast(ast.Expr, create_ast_node("'True' if true else 'False'", node)).value
ifexpr = cast(ast.IfExp, ifexpr);
ifexpr.test = node.args[0]
ifexpr.lineno = node.lineno
ifexpr.col_offset = node.col_offset
fix_missing_locations(ast, ifexpr);
node.args[0] = ifexpr
return node
end

function _do_go_rewrite{T0}(self::PrintBoolRewriter, node::T0)::ast.AST
if_stmt = create_ast_node(textwrap.dedent("            if True:\n                print('True')\n            else:\n                print('False')\n        "), node)
if_stmt = cast(ast.If, if_stmt);
if_stmt.test = node.args[0]
if_stmt.lineno = node.lineno
if_stmt.col_offset = node.col_offset
fix_missing_locations(ast, if_stmt);
return if_stmt
end

function visit_Call{T0}(self::PrintBoolRewriter, node::T0)::ast.AST
if get_id(node.func) == "print"
if length(node.args) == 1
anno = getattr(node.args[0], "annotation", nothing)
if get_id(anno) == "bool"
if self._language == "go"
return _do_go_rewrite(self, node)
else

return _do_other_rewrite(self, node)
end
end
end
end
return node
end

struct StrStrRewriter
_language::
end

function __init__{T0}(self::StrStrRewriter, language::T0)
__init__(super());
self._language = language
end

function visit_Compare{T0, RT}(self::StrStrRewriter, node::T0)::RT
if self._language in Set(["dart", "kotlin", "nim", "python"])
return node
end
if isinstance(isinstance(node.ops[0], ast.In), (int, float))&&isinstance(node.ops[0], ast.In) != 0||isinstance(isinstance(node.ops[0], ast.In), tuple)&&isinstance(node.ops[0], ast.In) != ()||isinstance(isinstance(node.ops[0], ast.In), list)&&isinstance(node.ops[0], ast.In) != []||isinstance(node.ops[0], ast.In) === nothing||isinstance(isinstance(node.ops[0], ast.In), bool)&&isinstance(node.ops[0], ast.In)
left = node.left
right = node.comparators[0]
left_type = get_id(get_inferred_type(left))
right_type = get_id(get_inferred_type(right))
if isinstance(left_type == "str"&&right_type == "str", (int, float))&&left_type == "str"&&right_type == "str" != 0||isinstance(left_type == "str"&&right_type == "str", tuple)&&left_type == "str"&&right_type == "str" != ()||isinstance(left_type == "str"&&right_type == "str", list)&&left_type == "str"&&right_type == "str" != []||left_type == "str"&&right_type == "str" === nothing||isinstance(left_type == "str"&&right_type == "str", bool)&&left_type == "str"&&right_type == "str"
if self._language == "julia"
ret = parse(ast, "findfirst(a, b) != Nothing").body[0].value
ret.left.args[0] = left
ret.left.args[1] = right
else

if self._language == "go"
ret = parse(ast, "StringsContains(a, b)").body[0].value;
ret.args[0] = right
ret.args[1] = left
else

if self._language == "cpp"
ret = parse(ast, "a.find(b) != string.npos").body[0].value
ret.left.func.value = right
ret.left.args[0] = left
else

ret = parse(ast, "a.contains(b)").body[0].value
ret.func.value = right
ret.args[0] = left
end
end
end
ret.lineno = node.lineno
fix_missing_locations(ast, ret);
return ret
end
end
return node
end

struct IgnoredAssignRewriter
_language::
_disable::Bool
_unpack::Bool
end

function __init__{T0}(self::IgnoredAssignRewriter, language::T0)
__init__(super());
self._language = language
self._disable = language in Set(["nim", "v"])
self._unpack = language in Set(["cpp", "dart", "go", "rust"])
end

function _visit_assign_unpack_all{T0, RT}(self::IgnoredAssignRewriter, node::T0)::RT
keep_ignored = self._language == "go"
body = []
target = node.targets[0]
for i in 0:length(target.elts) - 1
elt = target.elts[i]
if isinstance(isinstance(elt, ast.Name), (int, float))&&isinstance(elt, ast.Name) != 0||isinstance(isinstance(elt, ast.Name), tuple)&&isinstance(elt, ast.Name) != ()||isinstance(isinstance(elt, ast.Name), list)&&isinstance(elt, ast.Name) != []||isinstance(elt, ast.Name) === nothing||isinstance(isinstance(elt, ast.Name), bool)&&isinstance(elt, ast.Name)
name = get_id(elt)
if isinstance(name == "_"&&!(keep_ignored), (int, float))&&name == "_"&&!(keep_ignored) != 0||isinstance(name == "_"&&!(keep_ignored), tuple)&&name == "_"&&!(keep_ignored) != ()||isinstance(name == "_"&&!(keep_ignored), list)&&name == "_"&&!(keep_ignored) != []||name == "_"&&!(keep_ignored) === nothing||isinstance(name == "_"&&!(keep_ignored), bool)&&name == "_"&&!(keep_ignored)
push!(body, ast.Expr(node.value.elts[i]));
body[-1].unused = true
continue;
end
end
push!(body, ast.Assign([target.elts[i]], node.value.elts[i]));
end
return create_ast_block(body, node)
end

function visit_Assign{T0, RT}(self::IgnoredAssignRewriter, node::T0)::RT
if isinstance(self._disable, (int, float))&&self._disable != 0||isinstance(self._disable, tuple)&&self._disable != ()||isinstance(self._disable, list)&&self._disable != []||self._disable === nothing||isinstance(self._disable, bool)&&self._disable
return node
end
target = node.targets[0]
if isinstance(isinstance(target, ast.Tuple)&&isinstance(node.value, ast.Tuple), (int, float))&&isinstance(target, ast.Tuple)&&isinstance(node.value, ast.Tuple) != 0||isinstance(isinstance(target, ast.Tuple)&&isinstance(node.value, ast.Tuple), tuple)&&isinstance(target, ast.Tuple)&&isinstance(node.value, ast.Tuple) != ()||isinstance(isinstance(target, ast.Tuple)&&isinstance(node.value, ast.Tuple), list)&&isinstance(target, ast.Tuple)&&isinstance(node.value, ast.Tuple) != []||isinstance(target, ast.Tuple)&&isinstance(node.value, ast.Tuple) === nothing||isinstance(isinstance(target, ast.Tuple)&&isinstance(node.value, ast.Tuple), bool)&&isinstance(target, ast.Tuple)&&isinstance(node.value, ast.Tuple)
names = [get_id(elt) for elt in target.elts if isinstance(elt, ast.Name) ]
has_ignored = "_" in names
if isinstance(self._unpack&&has_ignored, (int, float))&&self._unpack&&has_ignored != 0||isinstance(self._unpack&&has_ignored, tuple)&&self._unpack&&has_ignored != ()||isinstance(self._unpack&&has_ignored, list)&&self._unpack&&has_ignored != []||self._unpack&&has_ignored === nothing||isinstance(self._unpack&&has_ignored, bool)&&self._unpack&&has_ignored
return _visit_assign_unpack_all(self, node)
end
if !(has_ignored)
return node
end
body = [node]
to_eval = []
for i in 0:length(target.elts) - 1
if names[i] == "_"
target.elts[i].drop()
push!(to_eval, node.value.elts[i]);
node.value.elts[i].drop()
end
end
body = [Expr(ast, e) for e in to_eval] + body;
return create_ast_block(body, node)
end
return node
end

struct UnpackScopeRewriter
_language::
end

function __init__{T0}(self::UnpackScopeRewriter, language::T0)
__init__(super());
self._language = language
end

function _visit_body{T0}(self::UnpackScopeRewriter, body::T0)::List
unpacked = []
for s in body
do_unpack = getattr(s, "unpack", true)
if isinstance(isinstance(s, ast.If)&&is_block(CLikeTranspiler, s)&&do_unpack, (int, float))&&isinstance(s, ast.If)&&is_block(CLikeTranspiler, s)&&do_unpack != 0||isinstance(isinstance(s, ast.If)&&is_block(CLikeTranspiler, s)&&do_unpack, tuple)&&isinstance(s, ast.If)&&is_block(CLikeTranspiler, s)&&do_unpack != ()||isinstance(isinstance(s, ast.If)&&is_block(CLikeTranspiler, s)&&do_unpack, list)&&isinstance(s, ast.If)&&is_block(CLikeTranspiler, s)&&do_unpack != []||isinstance(s, ast.If)&&is_block(CLikeTranspiler, s)&&do_unpack === nothing||isinstance(isinstance(s, ast.If)&&is_block(CLikeTranspiler, s)&&do_unpack, bool)&&isinstance(s, ast.If)&&is_block(CLikeTranspiler, s)&&do_unpack
extend(unpacked, self._visit_body(s.body));
else

push!(unpacked, s);
end
end
return unpacked
end

function _visit_assign_node_body{T0, RT}(self::UnpackScopeRewriter, node::T0)::RT
node.body = _visit_body(self, node.body)
return node
end

function visit_FunctionDef(self::UnpackScopeRewriter, node::ast.FunctionDef)::ast.FunctionDef
return _visit_assign_node_body(self, convert(, node))
end

function visit_For(self::UnpackScopeRewriter, node::ast.For)::ast.For
return _visit_assign_node_body(self, convert(, node))
end

function visit_If(self::UnpackScopeRewriter, node::ast.If)::ast.If
return _visit_assign_node_body(self, convert(, node))
end

function visit_With(self::UnpackScopeRewriter, node::ast.With)::ast.With
return _visit_assign_node_body(self, convert(, node))
end

function visit_While(self::UnpackScopeRewriter, node::ast.With)::ast.With
return _visit_assign_node_body(self, convert(, node))
end

struct LoopElseRewriter
_language::
_has_break_var_name::String
end

function __init__{T0}(self::LoopElseRewriter, language::T0)::
__init__(super());
self._language = language
self._has_break_var_name = "has_break"
end

function visit_Module(self::LoopElseRewriter, node::ast.Module)::Union[Union[Any,ast.Module],ast.Module]
_visit_Scope(self, convert(, node));
return node
end

function visit_FunctionDef(self::LoopElseRewriter, node::ast.FunctionDef)::Union[Union[Any,ast.FunctionDef],ast.FunctionDef]
_visit_Scope(self, convert(, node));
return node
end

function visit_If(self::LoopElseRewriter, node::ast.If)::Union[Union[Any,ast.If],ast.If]
_visit_Scope(self, convert(, node));
return node
end

function visit_With(self::LoopElseRewriter, node::ast.With)::Union[Union[Any,ast.With],ast.With]
_visit_Scope(self, convert(, node));
return node
end

function visit_For(self::LoopElseRewriter, node::ast.For)::Union[Union[Any,ast.For],ast.For]
_generic_loop_visit(self, convert(, node));
_visit_Scope(self, convert(, node));
return node
end

function visit_While(self::LoopElseRewriter, node::ast.While)::Union[Union[Any,ast.While],ast.While]
_generic_loop_visit(self, convert(, node));
_visit_Scope(self, convert(, node));
return node
end

function _generic_loop_visit(self::LoopElseRewriter, node::)
scopes = getattr(node, "scopes", ScopeList())
if length(node.orelse) > 0
lineno = node.orelse[0].lineno
if_expr = If(ast, ast.Compare(ast.Name(self._has_break_var_name), [ast.NotEq()], [ast.Constant(true, scopes)], scopes), [oe for oe in node.orelse], [], lineno, scopes)
node.if_expr = if_expr
end
end

function _visit_Scope{T0}(self::LoopElseRewriter, node::T0)::Any
generic_visit(self, node);
scopes = getattr(node, "scopes", ScopeList())
assign = Assign(ast, [ast.Name(self._has_break_var_name)], nothing, scopes)
fix_missing_locations(ast, assign);
body = []
for n in node.body
if isinstance(hasattr(n, "if_expr"), (int, float))&&hasattr(n, "if_expr") != 0||isinstance(hasattr(n, "if_expr"), tuple)&&hasattr(n, "if_expr") != ()||isinstance(hasattr(n, "if_expr"), list)&&hasattr(n, "if_expr") != []||hasattr(n, "if_expr") === nothing||isinstance(hasattr(n, "if_expr"), bool)&&hasattr(n, "if_expr")
assign.value = Constant(ast, false, scopes)
push!(body, assign);
push!(body, n);
push!(body, n.if_expr);
else

if isinstance(isinstance(n, ast.Break), (int, float))&&isinstance(n, ast.Break) != 0||isinstance(isinstance(n, ast.Break), tuple)&&isinstance(n, ast.Break) != ()||isinstance(isinstance(n, ast.Break), list)&&isinstance(n, ast.Break) != []||isinstance(n, ast.Break) === nothing||isinstance(isinstance(n, ast.Break), bool)&&isinstance(n, ast.Break)
for_node = find_node_by_type((ast.For, ast.While), scopes)
if isinstance(hasattr(for_node, "if_expr"), (int, float))&&hasattr(for_node, "if_expr") != 0||isinstance(hasattr(for_node, "if_expr"), tuple)&&hasattr(for_node, "if_expr") != ()||isinstance(hasattr(for_node, "if_expr"), list)&&hasattr(for_node, "if_expr") != []||hasattr(for_node, "if_expr") === nothing||isinstance(hasattr(for_node, "if_expr"), bool)&&hasattr(for_node, "if_expr")
assign.value = Constant(ast, true, scopes)
push!(body, assign);
end
push!(body, n);
else

push!(body, n);
end
end
end
node.body = body
end

