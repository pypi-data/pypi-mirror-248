import ast
using ast_helpers: get_id
get_id;
IGNORED_MODULE_SET = set(["typing", "enum", "dataclasses", "ctypes", "math", "__future__", "asyncio", "sys", "os", "adt", "py2many.result", "py2many.smt"])
function add_imports{T0, RT}(node::T0)::RT
return visit(ImportTransformer(), node)
end

function is_void_function{T0, RT}(fun::T0)::RT
finder = ReturnFinder()
visit(finder, fun);
return !(finder.returns||fun.returns !== nothing)
end

function is_global{T0, RT}(target::T0)::RT
return isinstance(target.scopes[-1], ast.Module)
end

function is_mutable{T0, T1}(scopes::T0, target::T1)::Bool
for scope in scopes
if isinstance(isinstance(scope, ast.FunctionDef), (int, float))&&isinstance(scope, ast.FunctionDef) != 0||isinstance(isinstance(scope, ast.FunctionDef), tuple)&&isinstance(scope, ast.FunctionDef) != ()||isinstance(isinstance(scope, ast.FunctionDef), list)&&isinstance(scope, ast.FunctionDef) != []||isinstance(scope, ast.FunctionDef) === nothing||isinstance(isinstance(scope, ast.FunctionDef), bool)&&isinstance(scope, ast.FunctionDef)
if target in scope.mutable_vars
return true
end
end
end
return false
end

function is_ellipsis{T0, RT}(node::T0)::RT
return isinstance(node, ast.Expr)&&isinstance(node.value, ast.Constant)&&node.value.value == # ...
end

struct ReturnFinder
returns::Bool
end

returns = false
function visit_Return{T0}(self::ReturnFinder, node::T0)
if node.value !== nothing
self.returns = true
end
end

struct FunctionTransformer

end

function visit_FunctionDef{T0, RT}(self::FunctionTransformer, node::T0)::RT
node.defined_functions = []
append(None.defined_functions, node);
generic_visit(self, node);
return node
end

function _visit_Scoped{T0, RT}(self::FunctionTransformer, node::T0)::RT
node.defined_functions = []
generic_visit(self, node);
return node
end

function visit_Module{T0, RT}(self::FunctionTransformer, node::T0)::RT
return _visit_Scoped(self, node)
end

function visit_ClassDef{T0, RT}(self::FunctionTransformer, node::T0)::RT
return _visit_Scoped(self, node)
end

function visit_For{T0, RT}(self::FunctionTransformer, node::T0)::RT
return _visit_Scoped(self, node)
end

function visit_If{T0, RT}(self::FunctionTransformer, node::T0)::RT
return _visit_Scoped(self, node)
end

function visit_With{T0, RT}(self::FunctionTransformer, node::T0)::RT
return _visit_Scoped(self, node)
end

function visit_ImportFrom{T0, RT}(self::FunctionTransformer, node::T0)::RT
for name in node.names
if node.module not in IGNORED_MODULE_SET
append(None.defined_functions, name);
end
end
return node
end

struct CalledWithTransformer

end

function visit_Assign{T0, RT}(self::CalledWithTransformer, node::T0)::RT
for target in node.targets
target.called_with = []
end
return node
end

function visit_FunctionDef{T0, RT}(self::CalledWithTransformer, node::T0)::RT
node.called_with = []
generic_visit(self, node);
return node
end

function visit_Call{T0, RT}(self::CalledWithTransformer, node::T0)::RT
for arg in node.args
if isinstance(isinstance(arg, ast.Name), (int, float))&&isinstance(arg, ast.Name) != 0||isinstance(isinstance(arg, ast.Name), tuple)&&isinstance(arg, ast.Name) != ()||isinstance(isinstance(arg, ast.Name), list)&&isinstance(arg, ast.Name) != []||isinstance(arg, ast.Name) === nothing||isinstance(isinstance(arg, ast.Name), bool)&&isinstance(arg, ast.Name)
var = find(node.scopes, arg.id)
append(var.called_with, node);
end
end
generic_visit(self, node);
return node
end

struct AttributeCallTransformer

end

function visit_Assign{T0, RT}(self::AttributeCallTransformer, node::T0)::RT
for target in node.targets
target.calls = []
end
return node
end

function visit_Call{T0, RT}(self::AttributeCallTransformer, node::T0)::RT
if isinstance(isinstance(node.func, ast.Attribute), (int, float))&&isinstance(node.func, ast.Attribute) != 0||isinstance(isinstance(node.func, ast.Attribute), tuple)&&isinstance(node.func, ast.Attribute) != ()||isinstance(isinstance(node.func, ast.Attribute), list)&&isinstance(node.func, ast.Attribute) != []||isinstance(node.func, ast.Attribute) === nothing||isinstance(isinstance(node.func, ast.Attribute), bool)&&isinstance(node.func, ast.Attribute)
var = find(node.scopes, node.func.value.id)
append(var.calls, node);
end
return node
end

struct ImportTransformer

end

function visit_ImportFrom{T0, RT}(self::ImportTransformer, node::T0)::RT
for name in node.names
name.imported_from = node
scope = name.scopes[-1]
if isinstance(hasattr(scope, "imports"), (int, float))&&hasattr(scope, "imports") != 0||isinstance(hasattr(scope, "imports"), tuple)&&hasattr(scope, "imports") != ()||isinstance(hasattr(scope, "imports"), list)&&hasattr(scope, "imports") != []||hasattr(scope, "imports") === nothing||isinstance(hasattr(scope, "imports"), bool)&&hasattr(scope, "imports")
append(scope.imports, name);
end
end
return node
end

function visit_Module{T0, RT}(self::ImportTransformer, node::T0)::RT
node.imports = []
generic_visit(self, node);
return node
end

