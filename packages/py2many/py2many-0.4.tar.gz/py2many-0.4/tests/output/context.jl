import ast
using scope: ScopeMixin
function add_list_calls{T0, RT}(node::T0)::RT
return visit(ListCallTransformer(), node)
end

function add_variable_context{T0, T1, RT}(node::T0, trees::T1)::RT
return visit(VariableTransformer(trees), node)
end

function add_assignment_context{T0, RT}(node::T0)::RT
return visit(LHSAnnotationTransformer(), node)
end

struct ListCallTransformer

end

function visit_Call{T0, RT}(self::ListCallTransformer, node::T0)::RT
if isinstance(is_list_addition(self, node), (int, float))&&is_list_addition(self, node) != 0||isinstance(is_list_addition(self, node), tuple)&&is_list_addition(self, node) != ()||isinstance(is_list_addition(self, node), list)&&is_list_addition(self, node) != []||is_list_addition(self, node) === nothing||isinstance(is_list_addition(self, node), bool)&&is_list_addition(self, node)
var = find(node.scopes, node.func.value.id)
if isinstance(var !== nothing&&is_list_assignment(self, var.assigned_from), (int, float))&&var !== nothing&&is_list_assignment(self, var.assigned_from) != 0||isinstance(var !== nothing&&is_list_assignment(self, var.assigned_from), tuple)&&var !== nothing&&is_list_assignment(self, var.assigned_from) != ()||isinstance(var !== nothing&&is_list_assignment(self, var.assigned_from), list)&&var !== nothing&&is_list_assignment(self, var.assigned_from) != []||var !== nothing&&is_list_assignment(self, var.assigned_from) === nothing||isinstance(var !== nothing&&is_list_assignment(self, var.assigned_from), bool)&&var !== nothing&&is_list_assignment(self, var.assigned_from)
if !(hasattr(var, "calls"))
var.calls = []
end
append(var.calls, node);
end
end
return node
end

function is_list_assignment{T0, RT}(self::ListCallTransformer, node::T0)::RT
return hasattr(node, "value")&&isinstance(node.value, ast.List)&&hasattr(node, "targets")&&isinstance(node.targets[0].ctx, ast.Store)
end

function is_list_addition{T0, RT}(self::ListCallTransformer, node::T0)::RT
list_operations = ["append", "extend", "insert"]
return hasattr(node.func, "ctx")&&isinstance(node.func.ctx, ast.Load)&&hasattr(node.func, "value")&&isinstance(node.func.value, ast.Name)&&hasattr(node.func, "attr")&&node.func.attr in list_operations
end

struct VariableTransformer
_trees::Dict
end

function __init__{T0}(self::VariableTransformer, trees::T0)
__init__(super());
if length(trees) == 1
self._trees = Dict()
else

self._trees = Dict(t.__file__.stem => t for t in trees)
end
end

function visit_FunctionDef{T0, RT}(self::VariableTransformer, node::T0)::RT
node.vars = []
append(None.vars, node);
for arg in node.args.args
arg.assigned_from = node
append(node.vars, arg);
end
generic_visit(self, node);
return node
end

function visit_ClassDef{T0, RT}(self::VariableTransformer, node::T0)::RT
node.vars = []
append(None.vars, node);
generic_visit(self, node);
return node
end

function visit_Import{T0, RT}(self::VariableTransformer, node::T0)::RT
for name in node.names
name.imported_from = node
end
return node
end

function visit_ImportFrom{T0, RT}(self::VariableTransformer, node::T0)::RT
module_path = node.module
names = [n.name for n in node.names]
if module_path in self._trees
m = self._trees[module_path]
resolved_names = [find(m.scopes, n) for n in names]
node.scopes[-1].vars += resolved_names
end
return node
end

function visit_If{T0, RT}(self::VariableTransformer, node::T0)::RT
node.vars = []
visit(self, node.test);
for e in node.body
visit(self, e);
end
node.body_vars = node.vars
node.vars = []
for e in node.orelse
visit(self, e);
end
node.orelse_vars = node.vars
node.vars = []
return node
end

function visit_For{T0, RT}(self::VariableTransformer, node::T0)::RT
node.target.assigned_from = node
if isinstance(isinstance(node.target, ast.Name), (int, float))&&isinstance(node.target, ast.Name) != 0||isinstance(isinstance(node.target, ast.Name), tuple)&&isinstance(node.target, ast.Name) != ()||isinstance(isinstance(node.target, ast.Name), list)&&isinstance(node.target, ast.Name) != []||isinstance(node.target, ast.Name) === nothing||isinstance(isinstance(node.target, ast.Name), bool)&&isinstance(node.target, ast.Name)
node.vars = [node.target]
else

if isinstance(isinstance(node.target, ast.Tuple), (int, float))&&isinstance(node.target, ast.Tuple) != 0||isinstance(isinstance(node.target, ast.Tuple), tuple)&&isinstance(node.target, ast.Tuple) != ()||isinstance(isinstance(node.target, ast.Tuple), list)&&isinstance(node.target, ast.Tuple) != []||isinstance(node.target, ast.Tuple) === nothing||isinstance(isinstance(node.target, ast.Tuple), bool)&&isinstance(node.target, ast.Tuple)
node.vars = [starred!(node.target.elts)/*unsupported*/]
else

node.vars = []
end
end
generic_visit(self, node);
return node
end

function visit_Module{T0, RT}(self::VariableTransformer, node::T0)::RT
node.vars = []
generic_visit(self, node);
return node
end

function visit_With{T0, RT}(self::VariableTransformer, node::T0)::RT
node.vars = []
generic_visit(self, node);
return node
end

function visit{T0, RT}(self::VariableTransformer, node::T0)::RT
if true
__tmp2 = enter_scope(self, node)
return visit(super(), node)
end
end

function visit_Assign{T0, RT}(self::VariableTransformer, node::T0)::RT
for target in node.targets
if isinstance(isinstance(target, ast.Name), (int, float))&&isinstance(target, ast.Name) != 0||isinstance(isinstance(target, ast.Name), tuple)&&isinstance(target, ast.Name) != ()||isinstance(isinstance(target, ast.Name), list)&&isinstance(target, ast.Name) != []||isinstance(target, ast.Name) === nothing||isinstance(isinstance(target, ast.Name), bool)&&isinstance(target, ast.Name)
target.assigned_from = node
append(self.scope.vars, target);
end
end
generic_visit(self, node);
return node
end

function visit_AnnAssign{T0, RT}(self::VariableTransformer, node::T0)::RT
target = node.target
if isinstance(isinstance(target, ast.Name), (int, float))&&isinstance(target, ast.Name) != 0||isinstance(isinstance(target, ast.Name), tuple)&&isinstance(target, ast.Name) != ()||isinstance(isinstance(target, ast.Name), list)&&isinstance(target, ast.Name) != []||isinstance(target, ast.Name) === nothing||isinstance(isinstance(target, ast.Name), bool)&&isinstance(target, ast.Name)
target.assigned_from = node
append(self.scope.vars, target);
end
generic_visit(self, node);
return node
end

function visit_AugAssign{T0, RT}(self::VariableTransformer, node::T0)::RT
target = node.target
if isinstance(isinstance(target, ast.Name), (int, float))&&isinstance(target, ast.Name) != 0||isinstance(isinstance(target, ast.Name), tuple)&&isinstance(target, ast.Name) != ()||isinstance(isinstance(target, ast.Name), list)&&isinstance(target, ast.Name) != []||isinstance(target, ast.Name) === nothing||isinstance(isinstance(target, ast.Name), bool)&&isinstance(target, ast.Name)
target.assigned_from = node
append(self.scope.vars, target);
end
generic_visit(self, node);
return node
end

struct LHSAnnotationTransformer
_lhs::Bool
end

function __init__(self::LHSAnnotationTransformer)
__init__(super());
self._lhs = false
end

function visit{T0, RT}(self::LHSAnnotationTransformer, node::T0)::RT
if isinstance(self._lhs, (int, float))&&self._lhs != 0||isinstance(self._lhs, tuple)&&self._lhs != ()||isinstance(self._lhs, list)&&self._lhs != []||self._lhs === nothing||isinstance(self._lhs, bool)&&self._lhs
node.lhs = self._lhs
end
return visit(super(), node)
end

function visit_Assign{T0, RT}(self::LHSAnnotationTransformer, node::T0)::RT
for target in node.targets
self._lhs = true
visit(self, target);
self._lhs = false
end
visit(self, node.value);
return node
end

function visit_AnnAssign{T0, RT}(self::LHSAnnotationTransformer, node::T0)::RT
self._lhs = true
visit(self, node.target);
self._lhs = false
visit(self, node.annotation);
if node.value !== nothing
visit(self, node.value);
end
return node
end

function visit_AugAssign{T0, RT}(self::LHSAnnotationTransformer, node::T0)::RT
self._lhs = true
visit(self, node.target);
self._lhs = false
visit(self, node.op);
visit(self, node.value);
return node
end

