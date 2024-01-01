import ast
using py2many::analysis: get_id
using py2many::clike: CLikeTranspiler
using py2many::exceptions: AstNotImplementedError

function decltype{T0}(node::T0)
# pass
end

function _lookup_class_or_module{T0, T1}(name::T0, scopes::T1)::Nothing{ast.ClassDef}
for scope in scopes
for entry in scope.body
if isinstance(isinstance(entry, ast.ClassDef), (int, float))&&isinstance(entry, ast.ClassDef) != 0||isinstance(isinstance(entry, ast.ClassDef), tuple)&&isinstance(entry, ast.ClassDef) != ()||isinstance(isinstance(entry, ast.ClassDef), list)&&isinstance(entry, ast.ClassDef) != []||isinstance(entry, ast.ClassDef) === nothing||isinstance(isinstance(entry, ast.ClassDef), bool)&&isinstance(entry, ast.ClassDef)
if entry.name == name
return entry
end
end
end
if isinstance(hasattr(scope, "imports"), (int, float))&&hasattr(scope, "imports") != 0||isinstance(hasattr(scope, "imports"), tuple)&&hasattr(scope, "imports") != ()||isinstance(hasattr(scope, "imports"), list)&&hasattr(scope, "imports") != []||hasattr(scope, "imports") === nothing||isinstance(hasattr(scope, "imports"), bool)&&hasattr(scope, "imports")
for entry in scope.imports
if entry.name == name
return entry
end
end
end
end
return nothing
end

function is_class_or_module{T0, T1}(name::T0, scopes::T1)::Bool
entry = _lookup_class_or_module(name, scopes)
return entry !== nothing
end

function is_enum{T0, T1}(name::T0, scopes::T1)::Bool
entry = _lookup_class_or_module(name, scopes)
if isinstance(entry&&hasattr(entry, "bases"), (int, float))&&entry&&hasattr(entry, "bases") != 0||isinstance(entry&&hasattr(entry, "bases"), tuple)&&entry&&hasattr(entry, "bases") != ()||isinstance(entry&&hasattr(entry, "bases"), list)&&entry&&hasattr(entry, "bases") != []||entry&&hasattr(entry, "bases") === nothing||isinstance(entry&&hasattr(entry, "bases"), bool)&&entry&&hasattr(entry, "bases")
bases = set([get_id(base) for base in entry.bases])
enum_bases = Set(["Enum", "IntEnum", "IntFlag"])
return bases & enum_bases
end
return false
end

function is_self_arg{T0, T1}(name::T0, scopes::T1)::Bool
for scope in scopes
for entry in scope.body
if isinstance(isinstance(entry, ast.FunctionDef), (int, float))&&isinstance(entry, ast.FunctionDef) != 0||isinstance(isinstance(entry, ast.FunctionDef), tuple)&&isinstance(entry, ast.FunctionDef) != ()||isinstance(isinstance(entry, ast.FunctionDef), list)&&isinstance(entry, ast.FunctionDef) != []||isinstance(entry, ast.FunctionDef) === nothing||isinstance(isinstance(entry, ast.FunctionDef), bool)&&isinstance(entry, ast.FunctionDef)
if isinstance(length(entry.args.args), (int, float))&&length(entry.args.args) != 0||isinstance(length(entry.args.args), tuple)&&length(entry.args.args) != ()||isinstance(length(entry.args.args), list)&&length(entry.args.args) != []||length(entry.args.args) === nothing||isinstance(length(entry.args.args), bool)&&length(entry.args.args)
first_arg = entry.args.args[0]
if isinstance(get_id(first_arg) == name&&hasattr(entry, "self_type"), (int, float))&&get_id(first_arg) == name&&hasattr(entry, "self_type") != 0||isinstance(get_id(first_arg) == name&&hasattr(entry, "self_type"), tuple)&&get_id(first_arg) == name&&hasattr(entry, "self_type") != ()||isinstance(get_id(first_arg) == name&&hasattr(entry, "self_type"), list)&&get_id(first_arg) == name&&hasattr(entry, "self_type") != []||get_id(first_arg) == name&&hasattr(entry, "self_type") === nothing||isinstance(get_id(first_arg) == name&&hasattr(entry, "self_type"), bool)&&get_id(first_arg) == name&&hasattr(entry, "self_type")
return true
end
end
end
end
end
return false
end

function is_list{T0}(node::T0)::Bool
if isinstance(isinstance(node, ast.List), (int, float))&&isinstance(node, ast.List) != 0||isinstance(isinstance(node, ast.List), tuple)&&isinstance(node, ast.List) != ()||isinstance(isinstance(node, ast.List), list)&&isinstance(node, ast.List) != []||isinstance(node, ast.List) === nothing||isinstance(isinstance(node, ast.List), bool)&&isinstance(node, ast.List)
return true
else

if isinstance(isinstance(node, ast.Assign), (int, float))&&isinstance(node, ast.Assign) != 0||isinstance(isinstance(node, ast.Assign), tuple)&&isinstance(node, ast.Assign) != ()||isinstance(isinstance(node, ast.Assign), list)&&isinstance(node, ast.Assign) != []||isinstance(node, ast.Assign) === nothing||isinstance(isinstance(node, ast.Assign), bool)&&isinstance(node, ast.Assign)
return is_list(node.value)
else

if isinstance(isinstance(node, ast.Name), (int, float))&&isinstance(node, ast.Name) != 0||isinstance(isinstance(node, ast.Name), tuple)&&isinstance(node, ast.Name) != ()||isinstance(isinstance(node, ast.Name), list)&&isinstance(node, ast.Name) != []||isinstance(node, ast.Name) === nothing||isinstance(isinstance(node, ast.Name), bool)&&isinstance(node, ast.Name)
var = find(node.scopes, get_id(node))
return hasattr(var, "assigned_from")&&!(isinstance(var.assigned_from, ast.FunctionDef))&&!(isinstance(var.assigned_from, ast.For))&&is_list(var.assigned_from.value)
else

return false
end
end
end
end

function find_node_by_type{T0, T1, RT}(node_type::T0, scopes::T1)::RT
c_node = nothing
for i in -1 - 1:-1:length(scopes) - 1
sc = scopes[i]
if isinstance(isinstance(sc, node_type), (int, float))&&isinstance(sc, node_type) != 0||isinstance(isinstance(sc, node_type), tuple)&&isinstance(sc, node_type) != ()||isinstance(isinstance(sc, node_type), list)&&isinstance(sc, node_type) != []||isinstance(sc, node_type) === nothing||isinstance(isinstance(sc, node_type), bool)&&isinstance(sc, node_type)
c_node = sc;
break;
end
if isinstance(hasattr(sc, "body"), (int, float))&&hasattr(sc, "body") != 0||isinstance(hasattr(sc, "body"), tuple)&&hasattr(sc, "body") != ()||isinstance(hasattr(sc, "body"), list)&&hasattr(sc, "body") != []||hasattr(sc, "body") === nothing||isinstance(hasattr(sc, "body"), bool)&&hasattr(sc, "body")
c_node = find_in_body(sc.body, (x) -> isinstance(x, node_type));
if c_node !== nothing
break;
end
end
end
return c_node
end

function find_in_body{T0, T1, RT}(body::T0, fn::T1)::RT
for i in -1 - 1:-1:length(body) - 1
node = body[i]
if isinstance(fn(node), (int, float))&&fn(node) != 0||isinstance(fn(node), tuple)&&fn(node) != ()||isinstance(fn(node), list)&&fn(node) != []||fn(node) === nothing||isinstance(fn(node), bool)&&fn(node)
return node
else

if isinstance(isinstance(node, ast.Expr)&&hasattr(node, "value")&&fn(node.value), (int, float))&&isinstance(node, ast.Expr)&&hasattr(node, "value")&&fn(node.value) != 0||isinstance(isinstance(node, ast.Expr)&&hasattr(node, "value")&&fn(node.value), tuple)&&isinstance(node, ast.Expr)&&hasattr(node, "value")&&fn(node.value) != ()||isinstance(isinstance(node, ast.Expr)&&hasattr(node, "value")&&fn(node.value), list)&&isinstance(node, ast.Expr)&&hasattr(node, "value")&&fn(node.value) != []||isinstance(node, ast.Expr)&&hasattr(node, "value")&&fn(node.value) === nothing||isinstance(isinstance(node, ast.Expr)&&hasattr(node, "value")&&fn(node.value), bool)&&isinstance(node, ast.Expr)&&hasattr(node, "value")&&fn(node.value)
return node.value
else

if isinstance(hasattr(node, "iter")&&fn(node.iter), (int, float))&&hasattr(node, "iter")&&fn(node.iter) != 0||isinstance(hasattr(node, "iter")&&fn(node.iter), tuple)&&hasattr(node, "iter")&&fn(node.iter) != ()||isinstance(hasattr(node, "iter")&&fn(node.iter), list)&&hasattr(node, "iter")&&fn(node.iter) != []||hasattr(node, "iter")&&fn(node.iter) === nothing||isinstance(hasattr(node, "iter")&&fn(node.iter), bool)&&hasattr(node, "iter")&&fn(node.iter)
return node.iter
else

if isinstance(hasattr(node, "test")&&fn(node.test), (int, float))&&hasattr(node, "test")&&fn(node.test) != 0||isinstance(hasattr(node, "test")&&fn(node.test), tuple)&&hasattr(node, "test")&&fn(node.test) != ()||isinstance(hasattr(node, "test")&&fn(node.test), list)&&hasattr(node, "test")&&fn(node.test) != []||hasattr(node, "test")&&fn(node.test) === nothing||isinstance(hasattr(node, "test")&&fn(node.test), bool)&&hasattr(node, "test")&&fn(node.test)
return node.test
else

if isinstance(hasattr(node, "body"), (int, float))&&hasattr(node, "body") != 0||isinstance(hasattr(node, "body"), tuple)&&hasattr(node, "body") != ()||isinstance(hasattr(node, "body"), list)&&hasattr(node, "body") != []||hasattr(node, "body") === nothing||isinstance(hasattr(node, "body"), bool)&&hasattr(node, "body")
ret = find_in_body(node.body, fn)
if isinstance(ret, (int, float))&&ret != 0||isinstance(ret, tuple)&&ret != ()||isinstance(ret, list)&&ret != []||ret === nothing||isinstance(ret, bool)&&ret
return ret
end
end
end
end
end
end
end
return nothing
end

function value_expr{T0, RT}(node::T0)::RT
return visit(ValueExpressionVisitor(), node)
end

function value_type{T0, RT}(node::T0)::RT
return visit(ValueTypeVisitor(), node)
end

struct ValueExpressionVisitor
_stack::List
end

function __init__(self::ValueExpressionVisitor)
__init__(super());
self._stack = []
end

function visit_Constant{T0}(self::ValueExpressionVisitor, node::T0)::String
return string(node.n)
end

function visit_Str{T0, RT}(self::ValueExpressionVisitor, node::T0)::RT
return node.s
end

function visit_Name{T0, RT}(self::ValueExpressionVisitor, node::T0)::RT
name = get_id(node)
if name in self._stack
return name
end
append(self._stack, name);
try
return _visit_Name(self, node)
finally
pop(self._stack);
end
end

function _visit_Name{T0, RT}(self::ValueExpressionVisitor, node::T0)::RT
name = get_id(node)
var = find(node.scopes, name)
if !(var)
return name
end
if isinstance(hasattr(var, "assigned_from"), (int, float))&&hasattr(var, "assigned_from") != 0||isinstance(hasattr(var, "assigned_from"), tuple)&&hasattr(var, "assigned_from") != ()||isinstance(hasattr(var, "assigned_from"), list)&&hasattr(var, "assigned_from") != []||hasattr(var, "assigned_from") === nothing||isinstance(hasattr(var, "assigned_from"), bool)&&hasattr(var, "assigned_from")
if isinstance(isinstance(var.assigned_from, ast.For), (int, float))&&isinstance(var.assigned_from, ast.For) != 0||isinstance(isinstance(var.assigned_from, ast.For), tuple)&&isinstance(var.assigned_from, ast.For) != ()||isinstance(isinstance(var.assigned_from, ast.For), list)&&isinstance(var.assigned_from, ast.For) != []||isinstance(var.assigned_from, ast.For) === nothing||isinstance(isinstance(var.assigned_from, ast.For), bool)&&isinstance(var.assigned_from, ast.For)
it = var.assigned_from.iter
return format("std::declval<typename decltype({0})::value_type>()", self.visit(it))
else

if isinstance(isinstance(var.assigned_from, ast.FunctionDef), (int, float))&&isinstance(var.assigned_from, ast.FunctionDef) != 0||isinstance(isinstance(var.assigned_from, ast.FunctionDef), tuple)&&isinstance(var.assigned_from, ast.FunctionDef) != ()||isinstance(isinstance(var.assigned_from, ast.FunctionDef), list)&&isinstance(var.assigned_from, ast.FunctionDef) != []||isinstance(var.assigned_from, ast.FunctionDef) === nothing||isinstance(isinstance(var.assigned_from, ast.FunctionDef), bool)&&isinstance(var.assigned_from, ast.FunctionDef)
return get_id(var)
else

return visit(self, var.assigned_from.value)
end
end
else

return name
end
end

function visit_Call{T0, RT}(self::ValueExpressionVisitor, node::T0)::RT
arg_strings = [visit(self, arg) for arg in node.args]
arg_strings = [a for a in arg_strings if a !== nothing ];
params = join(",", arg_strings)
return format("{0}({1})", self.visit(node.func), params)
end

function visit_Assign{T0, RT}(self::ValueExpressionVisitor, node::T0)::RT
return visit(self, node.value)
end

function visit_BinOp{T0, RT}(self::ValueExpressionVisitor, node::T0)::RT
return format("{0} {1} {2}", self.visit(node.left), CLikeTranspiler().visit(node.op), self.visit(node.right))
end

struct ValueTypeVisitor

end

function generic_visit{T0}(self::ValueTypeVisitor, node::T0)::String
return "auto"
end

function visit_Constant{T0, RT}(self::ValueTypeVisitor, node::T0)::RT
return value_expr(node)
end

function visit_Str{T0, RT}(self::ValueTypeVisitor, node::T0)::RT
return value_expr(node)
end

function visit_Name{T0, RT}(self::ValueTypeVisitor, node::T0)::RT
if isinstance(node.id == "True"||node.id == "False", (int, float))&&node.id == "True"||node.id == "False" != 0||isinstance(node.id == "True"||node.id == "False", tuple)&&node.id == "True"||node.id == "False" != ()||isinstance(node.id == "True"||node.id == "False", list)&&node.id == "True"||node.id == "False" != []||node.id == "True"||node.id == "False" === nothing||isinstance(node.id == "True"||node.id == "False", bool)&&node.id == "True"||node.id == "False"
return visit(CLikeTranspiler(), node)
end
var = find(node.scopes, node.id)
if !(var)
return get_id(node)
end
if isinstance(defined_before(var, node), (int, float))&&defined_before(var, node) != 0||isinstance(defined_before(var, node), tuple)&&defined_before(var, node) != ()||isinstance(defined_before(var, node), list)&&defined_before(var, node) != []||defined_before(var, node) === nothing||isinstance(defined_before(var, node), bool)&&defined_before(var, node)
return get_id(node)
else

return visit(self, var.assigned_from.value)
end
end

function visit_NameConstant{T0, RT}(self::ValueTypeVisitor, node::T0)::RT
return visit(CLikeTranspiler(), node)
end

function visit_Call{T0, RT}(self::ValueTypeVisitor, node::T0)::RT
params = [visit(self, arg) for arg in node.args]
if isinstance(any((t === nothing for t in params)), (int, float))&&any((t === nothing for t in params)) != 0||isinstance(any((t === nothing for t in params)), tuple)&&any((t === nothing for t in params)) != ()||isinstance(any((t === nothing for t in params)), list)&&any((t === nothing for t in params)) != []||any((t === nothing for t in params)) === nothing||isinstance(any((t === nothing for t in params)), bool)&&any((t === nothing for t in params))
throw(AstNotImplementedError("".join(["Call(", string(params), ") not implemented"]), node))
end
params = join(",", params);
return format("{0}({1})", self.visit(node.func), params)
end

function visit_Attribute{T0, RT}(self::ValueTypeVisitor, node::T0)::RT
value_id = get_id(node.value)
return join("", [string(value_id), ".", string(node.attr)])
end

function visit_Assign{T0, RT}(self::ValueTypeVisitor, node::T0)::RT
if isinstance(isinstance(node.value, ast.List), (int, float))&&isinstance(node.value, ast.List) != 0||isinstance(isinstance(node.value, ast.List), tuple)&&isinstance(node.value, ast.List) != ()||isinstance(isinstance(node.value, ast.List), list)&&isinstance(node.value, ast.List) != []||isinstance(node.value, ast.List) === nothing||isinstance(isinstance(node.value, ast.List), bool)&&isinstance(node.value, ast.List)
if length(node.value.elts) > 0
val = node.value.elts[0]
return visit(self, val)
else

target = node.targets[0]
var = find(node.scopes, get_id(target))
if isinstance(hasattr(var, "calls"), (int, float))&&hasattr(var, "calls") != 0||isinstance(hasattr(var, "calls"), tuple)&&hasattr(var, "calls") != ()||isinstance(hasattr(var, "calls"), list)&&hasattr(var, "calls") != []||hasattr(var, "calls") === nothing||isinstance(hasattr(var, "calls"), bool)&&hasattr(var, "calls")
first_added_value = var.calls[0].args[0]
return value_expr(first_added_value)
else

return nothing
end
end
else

return visit(self, node.value)
end
end

function defined_before{T0, T1}(node1::T0, node2::T1)::Bool
return node1.lineno < node2.lineno
end

function is_list_assignment{T0, RT}(node::T0)::RT
return isinstance(node.value, ast.List)&&isinstance(node.targets[0].ctx, ast.Store)
end

function is_list_addition{T0, RT}(node::T0)::RT
list_operations = ["append", "extend", "insert"]
return isinstance(node.func.ctx, ast.Load)&&hasattr(node.func, "value")&&isinstance(node.func.value, ast.Name)&&node.func.attr in list_operations
end

function is_recursive{T0, RT}(fun::T0)::RT
finder = RecursionFinder()
visit(finder, fun);
return finder.recursive
end

struct RecursionFinder
function_name::
recursive::
end

function_name = nothing
recursive = false
function visit_FunctionDef{T0}(self::RecursionFinder, node::T0)
self.function_name = node.name
generic_visit(self, node);
end

function visit_Call{T0}(self::RecursionFinder, node::T0)
self.recursive = isinstance(node.func, ast.Name)&&get_id(node.func) == self.function_name
generic_visit(self, node);
end

