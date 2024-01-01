import ast

using py2many::ast_helpers: get_id
struct DeclarationExtractor
self.annotated_members::Dict{String, {['String', 'Any']}}
transpiler::
class_assignments::Dict
member_assignments::Dict
typed_function_args::Dict
end

function __init__{T0}(self::DeclarationExtractor, transpiler::T0)
self.transpiler = transpiler
self.annotated_members::Dict{String, {['String', 'Any']}} = Dict()
self.class_assignments = Dict()
self.member_assignments = Dict()
self.typed_function_args = Dict()
end

function _maybe_rename_key{T0}(self::DeclarationExtractor, key::T0)::String
if key in self.transpiler._keywords
return key + "_"
else

return key
end
end

function get_declarations{RT}(self::DeclarationExtractor)::RT
typed_members = Dict(k => v[0] for (k, v) in items(self.annotated_members))
for (member, var) in items(self.member_assignments)
if member in self.annotated_members
continue;
end
if var in self.typed_function_args
typed_members[member] = self.typed_function_args[var]
end
end
for (member, value) in items(self.member_assignments)
if member not in typed_members
typed_members[member] = _typename_from_annotation(self.transpiler, value)
end
end
typed_members = Dict(_maybe_rename_key(self, k) => v for (k, v) in items(typed_members));
return typed_members
end

function get_declarations_with_defaults{RT}(self::DeclarationExtractor)::RT
typed_members = self.annotated_members
for (member, var) in items(self.member_assignments)
if member in self.annotated_members
continue;
end
if var in self.typed_function_args
typed_members[member] = (self.typed_function_args[var], nothing)
end
end
for (member, value) in items(self.member_assignments)
if member not in typed_members
typed_members[member] = (_typename_from_annotation(self.transpiler, value), nothing)
end
end
return typed_members
end

function visit_ClassDef(self::DeclarationExtractor, node::ast.ClassDef)
decorators = [get_id(d) for d in node.decorator_list]
if isinstance(length(node.decorator_list) > 0&&"dataclass" in decorators, (int, float))&&length(node.decorator_list) > 0&&"dataclass" in decorators != 0||isinstance(length(node.decorator_list) > 0&&"dataclass" in decorators, tuple)&&length(node.decorator_list) > 0&&"dataclass" in decorators != ()||isinstance(length(node.decorator_list) > 0&&"dataclass" in decorators, list)&&length(node.decorator_list) > 0&&"dataclass" in decorators != []||length(node.decorator_list) > 0&&"dataclass" in decorators === nothing||isinstance(length(node.decorator_list) > 0&&"dataclass" in decorators, bool)&&length(node.decorator_list) > 0&&"dataclass" in decorators
node.is_dataclass = true
dataclass_members = []
for child in node.body
if isinstance(isinstance(child, ast.AnnAssign), (int, float))&&isinstance(child, ast.AnnAssign) != 0||isinstance(isinstance(child, ast.AnnAssign), tuple)&&isinstance(child, ast.AnnAssign) != ()||isinstance(isinstance(child, ast.AnnAssign), list)&&isinstance(child, ast.AnnAssign) != []||isinstance(child, ast.AnnAssign) === nothing||isinstance(isinstance(child, ast.AnnAssign), bool)&&isinstance(child, ast.AnnAssign)
visit_AnnAssign(self, child);
push!(dataclass_members, child);
end
end
for m in dataclass_members
remove(node.body, m);
end
else

node.is_dataclass = false
generic_visit(self, node);
end
end

function visit_AsyncFunctionDef{T0}(self::DeclarationExtractor, node::T0)
visit_FunctionDef(self, node);
end

function visit_FunctionDef{T0}(self::DeclarationExtractor, node::T0)
types, names = visit(self.transpiler, node.args)
for i in 0:length(names) - 1
typename = types[i]
if isinstance(typename&&typename != "T", (int, float))&&typename&&typename != "T" != 0||isinstance(typename&&typename != "T", tuple)&&typename&&typename != "T" != ()||isinstance(typename&&typename != "T", list)&&typename&&typename != "T" != []||typename&&typename != "T" === nothing||isinstance(typename&&typename != "T", bool)&&typename&&typename != "T"
if names[i] not in self.typed_function_args
self.typed_function_args[names[i]] = typename
end
end
end
generic_visit(self, node);
end

function visit_AnnAssign{T0, T1}(self::DeclarationExtractor, node::T0, dataclass::T1)
target = node.target
target_id = get_id(target)
if target_id === nothing
return
end
type_str = nothing
if isinstance(isinstance(node.annotation, ast.Constant), (int, float))&&isinstance(node.annotation, ast.Constant) != 0||isinstance(isinstance(node.annotation, ast.Constant), tuple)&&isinstance(node.annotation, ast.Constant) != ()||isinstance(isinstance(node.annotation, ast.Constant), list)&&isinstance(node.annotation, ast.Constant) != []||isinstance(node.annotation, ast.Constant) === nothing||isinstance(isinstance(node.annotation, ast.Constant), bool)&&isinstance(node.annotation, ast.Constant)
type_str = node.annotation.value;
end
if type_str === nothing
type_str = _typename_from_annotation(self.transpiler, node);
end
if target_id not in self.annotated_members
self.annotated_members[target_id] = (type_str, node.value)
end
if !(is_member(self, target))
node.class_assignment = true
if target not in self.class_assignments
self.class_assignments[target] = node.value
end
end
if isinstance(dataclass, (int, float))&&dataclass != 0||isinstance(dataclass, tuple)&&dataclass != ()||isinstance(dataclass, list)&&dataclass != []||dataclass === nothing||isinstance(dataclass, bool)&&dataclass
type_str = _typename_from_annotation(self.transpiler, node);
if target_id not in self.annotated_members
self.annotated_members[target_id] = (type_str, node.value)
end
end
end

function visit_Assign{T0}(self::DeclarationExtractor, node::T0)
target = node.targets[0]
if isinstance(is_member(self, target), (int, float))&&is_member(self, target) != 0||isinstance(is_member(self, target), tuple)&&is_member(self, target) != ()||isinstance(is_member(self, target), list)&&is_member(self, target) != []||is_member(self, target) === nothing||isinstance(is_member(self, target), bool)&&is_member(self, target)
if target.attr not in self.member_assignments
self.member_assignments[target.attr] = node.value
end
else

node.class_assignment = true
target = get_id(target);
if target not in self.class_assignments
self.class_assignments[target] = node.value
end
end
end

function is_member{T0}(self::DeclarationExtractor, node::T0)::Bool
if isinstance(hasattr(node, "value"), (int, float))&&hasattr(node, "value") != 0||isinstance(hasattr(node, "value"), tuple)&&hasattr(node, "value") != ()||isinstance(hasattr(node, "value"), list)&&hasattr(node, "value") != []||hasattr(node, "value") === nothing||isinstance(hasattr(node, "value"), bool)&&hasattr(node, "value")
if visit(self.transpiler, node.value) == "self"
return true
end
end
return false
end

