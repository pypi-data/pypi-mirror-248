import ast
using contextlib: contextmanager
using py2many::analysis: get_id
function add_scope_context{T0, RT}(node::T0)::RT
return visit(ScopeTransformer(), node)
end

struct ScopeMixin

end

scopes = []
function enter_scope{T0}(self::ScopeMixin, node::T0)
if isinstance(_is_scopable_node(self, node), (int, float))&&_is_scopable_node(self, node) != 0||isinstance(_is_scopable_node(self, node), tuple)&&_is_scopable_node(self, node) != ()||isinstance(_is_scopable_node(self, node), list)&&_is_scopable_node(self, node) != []||_is_scopable_node(self, node) === nothing||isinstance(_is_scopable_node(self, node), bool)&&_is_scopable_node(self, node)
append(self.scopes, node);
//yield is unimplemented;
pop(self.scopes);
else

//yield is unimplemented;
end
end

function scope{RT}(self::ScopeMixin)::RT
try
return self.scopes[-1]
catch exn
if exn isa IndexError
return nothing
end
end
end

function _is_scopable_node{T0}(self::ScopeMixin, node::T0)::Bool
scopes = [ast.Module, ast.ClassDef, ast.FunctionDef, ast.For, ast.If, ast.With];
return length([s for s in scopes if isinstance(node, s) ]) > 0
end

struct ScopeList

end

function find{T0, RT}(self::ScopeList, lookup::T0)::RT
function find_definition{T0, T1, RT}(scope::T0, var_attr::T1)::RT
for var in getattr(scope, var_attr)
if get_id(var) == lookup
return var
end
end
end

for scope in reversed(self)
defn = nothing
if isinstance(!(defn)&&hasattr(scope, "vars"), (int, float))&&!(defn)&&hasattr(scope, "vars") != 0||isinstance(!(defn)&&hasattr(scope, "vars"), tuple)&&!(defn)&&hasattr(scope, "vars") != ()||isinstance(!(defn)&&hasattr(scope, "vars"), list)&&!(defn)&&hasattr(scope, "vars") != []||!(defn)&&hasattr(scope, "vars") === nothing||isinstance(!(defn)&&hasattr(scope, "vars"), bool)&&!(defn)&&hasattr(scope, "vars")
defn = find_definition(scope, convert(, "vars"));
end
if isinstance(!(defn)&&hasattr(scope, "body_vars"), (int, float))&&!(defn)&&hasattr(scope, "body_vars") != 0||isinstance(!(defn)&&hasattr(scope, "body_vars"), tuple)&&!(defn)&&hasattr(scope, "body_vars") != ()||isinstance(!(defn)&&hasattr(scope, "body_vars"), list)&&!(defn)&&hasattr(scope, "body_vars") != []||!(defn)&&hasattr(scope, "body_vars") === nothing||isinstance(!(defn)&&hasattr(scope, "body_vars"), bool)&&!(defn)&&hasattr(scope, "body_vars")
defn = find_definition(scope, convert(, "body_vars"));
end
if isinstance(!(defn)&&hasattr(scope, "orelse_vars"), (int, float))&&!(defn)&&hasattr(scope, "orelse_vars") != 0||isinstance(!(defn)&&hasattr(scope, "orelse_vars"), tuple)&&!(defn)&&hasattr(scope, "orelse_vars") != ()||isinstance(!(defn)&&hasattr(scope, "orelse_vars"), list)&&!(defn)&&hasattr(scope, "orelse_vars") != []||!(defn)&&hasattr(scope, "orelse_vars") === nothing||isinstance(!(defn)&&hasattr(scope, "orelse_vars"), bool)&&!(defn)&&hasattr(scope, "orelse_vars")
defn = find_definition(scope, convert(, "orelse_vars"));
end
if isinstance(!(defn)&&hasattr(scope, "body"), (int, float))&&!(defn)&&hasattr(scope, "body") != 0||isinstance(!(defn)&&hasattr(scope, "body"), tuple)&&!(defn)&&hasattr(scope, "body") != ()||isinstance(!(defn)&&hasattr(scope, "body"), list)&&!(defn)&&hasattr(scope, "body") != []||!(defn)&&hasattr(scope, "body") === nothing||isinstance(!(defn)&&hasattr(scope, "body"), bool)&&!(defn)&&hasattr(scope, "body")
defn = find_definition(scope, convert(, "body"));
end
if isinstance(defn, (int, float))&&defn != 0||isinstance(defn, tuple)&&defn != ()||isinstance(defn, list)&&defn != []||defn === nothing||isinstance(defn, bool)&&defn
return defn
end
end
end

function find_import{T0, RT}(self::ScopeList, lookup::T0)::RT
for scope in reversed(self)
if isinstance(hasattr(scope, "imports"), (int, float))&&hasattr(scope, "imports") != 0||isinstance(hasattr(scope, "imports"), tuple)&&hasattr(scope, "imports") != ()||isinstance(hasattr(scope, "imports"), list)&&hasattr(scope, "imports") != []||hasattr(scope, "imports") === nothing||isinstance(hasattr(scope, "imports"), bool)&&hasattr(scope, "imports")
for imp in scope.imports
if imp.name == lookup
return imp
end
end
end
end
end

function parent_scopes(self::ScopeList)::ScopeList
scopes = list(self)
pop(scopes);
return ScopeList(scopes)
end

struct ScopeTransformer

end

function visit{T0, RT}(self::ScopeTransformer, node::T0)::RT
if true
__tmp1 = enter_scope(self, node)
node.scopes = ScopeList(self.scopes)
return visit(super(), node)
end
end

