import ast




using py2many::analysis: get_id
using py2many::ast_helpers: create_ast_node, unparse
using py2many::astx: LifeTime
using py2many::clike: CLikeTranspiler, class_for_typename
using py2many::exceptions: AstIncompatibleAssign, AstUnrecognisedBinOp
using py2many::tracer: is_enum
try
using typpete::inference_runner: infer
using typpete::src::context: Context
using typpete::src::z3_types: TypesSolver
catch exn
if exn isa ModuleNotFoundError
function infer_types_ast{T0, RT}(node::T0)::RT
return node
end

end
end
struct InferMeta
has_fixed_width_ints::Bool
end


function infer_types{T0}(node::T0)::InferMeta
visitor = InferTypesTransformer()
visit(visitor, node);
return InferMeta(visitor.has_fixed_width_ints)
end

function infer_types_typpete{T0}(node::T0)::InferMeta
solver = TypesSolver(node)
context = Context(node, node.body, solver)
for stmt in node.body
infer_types_ast(stmt);
end
push(solver);
return InferMeta(true)
end

function get_inferred_type{T0, RT}(node::T0)::RT
if isinstance(isinstance(node, ast.Name), (int, float))&&isinstance(node, ast.Name) != 0||isinstance(isinstance(node, ast.Name), tuple)&&isinstance(node, ast.Name) != ()||isinstance(isinstance(node, ast.Name), list)&&isinstance(node, ast.Name) != []||isinstance(node, ast.Name) === nothing||isinstance(isinstance(node, ast.Name), bool)&&isinstance(node, ast.Name)
if !(hasattr(node, "scopes"))
return nothing
end
definition = find(node.scopes, get_id(node))
if isinstance(definition != node&&definition !== nothing, (int, float))&&definition != node&&definition !== nothing != 0||isinstance(definition != node&&definition !== nothing, tuple)&&definition != node&&definition !== nothing != ()||isinstance(definition != node&&definition !== nothing, list)&&definition != node&&definition !== nothing != []||definition != node&&definition !== nothing === nothing||isinstance(definition != node&&definition !== nothing, bool)&&definition != node&&definition !== nothing
return get_inferred_type(definition)
end
else

if isinstance(isinstance(node, ast.Constant)||isinstance(node, ast.NameConstant), (int, float))&&isinstance(node, ast.Constant)||isinstance(node, ast.NameConstant) != 0||isinstance(isinstance(node, ast.Constant)||isinstance(node, ast.NameConstant), tuple)&&isinstance(node, ast.Constant)||isinstance(node, ast.NameConstant) != ()||isinstance(isinstance(node, ast.Constant)||isinstance(node, ast.NameConstant), list)&&isinstance(node, ast.Constant)||isinstance(node, ast.NameConstant) != []||isinstance(node, ast.Constant)||isinstance(node, ast.NameConstant) === nothing||isinstance(isinstance(node, ast.Constant)||isinstance(node, ast.NameConstant), bool)&&isinstance(node, ast.Constant)||isinstance(node, ast.NameConstant)
return _infer_primitive(InferTypesTransformer, node.value)
end
end
if isinstance(hasattr(node, "annotation"), (int, float))&&hasattr(node, "annotation") != 0||isinstance(hasattr(node, "annotation"), tuple)&&hasattr(node, "annotation") != ()||isinstance(hasattr(node, "annotation"), list)&&hasattr(node, "annotation") != []||hasattr(node, "annotation") === nothing||isinstance(hasattr(node, "annotation"), bool)&&hasattr(node, "annotation")
return node.annotation
end
return nothing
end

function is_reference{T0}(arg::T0)::Bool
annotation_has_ref = hasattr(arg, "annotation")&&isinstance(arg.annotation, ast.Subscript)
if isinstance(annotation_has_ref, (int, float))&&annotation_has_ref != 0||isinstance(annotation_has_ref, tuple)&&annotation_has_ref != ()||isinstance(annotation_has_ref, list)&&annotation_has_ref != []||annotation_has_ref === nothing||isinstance(annotation_has_ref, bool)&&annotation_has_ref
return true
end
inferred = get_inferred_type(arg)
annotation_has_ref = hasattr(inferred, "id")&&isinstance(inferred.id, ast.Subscript);
return annotation_has_ref
end

function bit_length(val::ast.AST)::Int64
if isinstance(isinstance(val, ast.Constant)&&isinstance(val.value, int), (int, float))&&isinstance(val, ast.Constant)&&isinstance(val.value, int) != 0||isinstance(isinstance(val, ast.Constant)&&isinstance(val.value, int), tuple)&&isinstance(val, ast.Constant)&&isinstance(val.value, int) != ()||isinstance(isinstance(val, ast.Constant)&&isinstance(val.value, int), list)&&isinstance(val, ast.Constant)&&isinstance(val.value, int) != []||isinstance(val, ast.Constant)&&isinstance(val.value, int) === nothing||isinstance(isinstance(val, ast.Constant)&&isinstance(val.value, int), bool)&&isinstance(val, ast.Constant)&&isinstance(val.value, int)
return bit_length(int)
end
return 0
end

function is_compatible{T0, T1}(cls1::T0, cls2::T1, target::Nothing{ast.AST}, source::Nothing{ast.AST})::Bool
fixed_width = InferTypesTransformer::FIXED_WIDTH_INTS
fixed_width_bit_length = InferTypesTransformer::FIXED_WIDTH_BIT_LENGTH
if isinstance(cls1 in fixed_width&&cls2 in fixed_width||cls2 === int, (int, float))&&cls1 in fixed_width&&cls2 in fixed_width||cls2 === int != 0||isinstance(cls1 in fixed_width&&cls2 in fixed_width||cls2 === int, tuple)&&cls1 in fixed_width&&cls2 in fixed_width||cls2 === int != ()||isinstance(cls1 in fixed_width&&cls2 in fixed_width||cls2 === int, list)&&cls1 in fixed_width&&cls2 in fixed_width||cls2 === int != []||cls1 in fixed_width&&cls2 in fixed_width||cls2 === int === nothing||isinstance(cls1 in fixed_width&&cls2 in fixed_width||cls2 === int, bool)&&cls1 in fixed_width&&cls2 in fixed_width||cls2 === int
target_bit_length = fixed_width_bit_length[cls1]
source_bit_length = fixed_width_bit_length[cls2]
source_value_bit_length = source !== nothing ? (bit_length(convert(ast.AST, source))) : (0)
if isinstance(source_value_bit_length, (int, float))&&source_value_bit_length != 0||isinstance(source_value_bit_length, tuple)&&source_value_bit_length != ()||isinstance(source_value_bit_length, list)&&source_value_bit_length != []||source_value_bit_length === nothing||isinstance(source_value_bit_length, bool)&&source_value_bit_length
source_bit_length = source_value_bit_length;
end
return target_bit_length >= source_bit_length
end
return true
end

struct InferTypesTransformer
elt_types::Set{String}
handling_annotation::Bool
has_fixed_width_ints::Bool
_clike::
end

TYPE_DICT = Dict(int => "int", float => "float", str => "str", bool => "bool", bytes => "bytes", complex => "complex", type_(# ...) => "...")
FIXED_WIDTH_INTS_LIST = [bool, c_int8, c_int16, c_int32, c_int64, c_uint8, c_uint16, c_uint32, c_uint64]
FIXED_WIDTH_INTS = set(FIXED_WIDTH_INTS_LIST)
FIXED_WIDTH_BIT_LENGTH = Dict(bool => 1, c_int8 => 7, c_uint8 => 8, c_int16 => 15, c_uint16 => 16, int => 31, c_int32 => 31, c_uint32 => 32, c_int64 => 63, c_uint64 => 64)
FIXED_WIDTH_INTS_NAME_LIST = ["bool", "c_int8", "c_int16", "c_int32", "c_int64", "c_uint8", "c_uint16", "c_uint32", "c_uint64", "i8", "i16", "i32", "i64", "isize", "ilong", "u8", "u16", "u32", "u64", "usize", "ulong"]
FIXED_WIDTH_INTS_NAME = set(FIXED_WIDTH_INTS_NAME_LIST)
function __init__(self::InferTypesTransformer)
self.handling_annotation = false
self.has_fixed_width_ints = false
self._clike = CLikeTranspiler()
end

function _infer_primitive{T0}(value::T0)::Nothing{ast.AST}
t = type_(value)
annotation = nothing
if t in InferTypesTransformer::TYPE_DICT
annotation = Name(ast, InferTypesTransformer::TYPE_DICT[t]);
else

if t in InferTypesTransformer::FIXED_WIDTH_INTS
annotation = Name(ast, string(t));
else

if t != type_(nothing)
throw(NotImplementedError("".join([string(t), " not found in TYPE_DICT"])))
end
end
end
return annotation
end

function visit_NameConstant{T0, RT}(self::InferTypesTransformer, node::T0)::RT
if node.value === Ellipsis
return node
end
annotation = _infer_primitive(self)
if annotation !== nothing
node.annotation = annotation
node.annotation.lifetime = type_(node.value) == str ? (LifeTime::STATIC) : (LifeTime::UNKNOWN)
end
generic_visit(self, node);
return node
end

function visit_Name{T0, RT}(self::InferTypesTransformer, node::T0)::RT
annotation = get_inferred_type(node)
if annotation !== nothing
node.annotation = annotation
end
return node
end

function visit_Constant{T0, RT}(self::InferTypesTransformer, node::T0)::RT
return visit_NameConstant(self, node)
end

function _annotate{T0}(node::T0, typename::String)
type_annotation = cast(ast.Expr, create_ast_node(typename, node)).value
node.annotation = type_annotation
end

function visit_List{T0, RT}(self::InferTypesTransformer, node::T0)::RT
generic_visit(self, node);
if length(node.elts) > 0
elements = [visit(self, e) for e in node.elts]
if isinstance(getattr(node, "is_annotation", false), (int, float))&&getattr(node, "is_annotation", false) != 0||isinstance(getattr(node, "is_annotation", false), tuple)&&getattr(node, "is_annotation", false) != ()||isinstance(getattr(node, "is_annotation", false), list)&&getattr(node, "is_annotation", false) != []||getattr(node, "is_annotation", false) === nothing||isinstance(getattr(node, "is_annotation", false), bool)&&getattr(node, "is_annotation", false)
return node
else

elt_types::Set{String} = set()
for e in elements
typ = get_inferred_type(e)
if typ !== nothing
add(elt_types, unparse(typ));
end
end
if length(elt_types) == 0
node.annotation = Name(ast, "List")
else

if length(elt_types) == 1
_annotate(self, node);
else

_annotate(self, node);
end
end
end
else

if !(hasattr(node, "annotation"))
node.annotation = Name(ast, "List")
end
end
return node
end

function visit_Set{T0, RT}(self::InferTypesTransformer, node::T0)::RT
generic_visit(self, node);
if length(node.elts) > 0
elements = [visit(self, e) for e in node.elts]
elt_types = set([get_id(get_inferred_type(e)) for e in elements])
if length(elt_types) == 1
if isinstance(hasattr(elements[0], "annotation"), (int, float))&&hasattr(elements[0], "annotation") != 0||isinstance(hasattr(elements[0], "annotation"), tuple)&&hasattr(elements[0], "annotation") != ()||isinstance(hasattr(elements[0], "annotation"), list)&&hasattr(elements[0], "annotation") != []||hasattr(elements[0], "annotation") === nothing||isinstance(hasattr(elements[0], "annotation"), bool)&&hasattr(elements[0], "annotation")
elt_type = get_id(elements[0].annotation)
_annotate(self, node);
return node
end
end
end
if !(hasattr(node, "annotation"))
node.annotation = Name(ast, "Set")
end
return node
end

function visit_Dict{T0, RT}(self::InferTypesTransformer, node::T0)::RT
generic_visit(self, node);
if length(node.keys) > 0
function typename{T0, RT}(e::T0)::RT
get_inferred_type(e);
return _generic_typename_from_annotation(self._clike, e)
end

key_types = set([typename(e) for e in node.keys])
only_key_type = next(iter(key_types))
if length(key_types) == 1
key_type = only_key_type
else

key_type = "Any"
end
value_types = set([typename(e) for e in node.values])
only_value_type = next(iter(value_types))
if length(value_types) == 1
value_type = only_value_type
else

value_type = "Any"
end
_annotate(self, node);
lifetimes = set([getattr(e.annotation, "lifetime", nothing) for e in node.values if hasattr(e, "annotation") ])
only_lifetime = length(lifetimes) == 1 ? (next(iter(lifetimes))) : (nothing)
if isinstance(length(lifetimes) == 1&&only_lifetime !== nothing, (int, float))&&length(lifetimes) == 1&&only_lifetime !== nothing != 0||isinstance(length(lifetimes) == 1&&only_lifetime !== nothing, tuple)&&length(lifetimes) == 1&&only_lifetime !== nothing != ()||isinstance(length(lifetimes) == 1&&only_lifetime !== nothing, list)&&length(lifetimes) == 1&&only_lifetime !== nothing != []||length(lifetimes) == 1&&only_lifetime !== nothing === nothing||isinstance(length(lifetimes) == 1&&only_lifetime !== nothing, bool)&&length(lifetimes) == 1&&only_lifetime !== nothing
lifetime = only_lifetime
else

lifetime = LifeTime::UNKNOWN
end
node.annotation.lifetime = lifetime
else

if !(hasattr(node, "annotation"))
node.annotation = Name(ast, "Dict")
end
end
return node
end

function visit_Assign(self::InferTypesTransformer, node::ast.Assign)::ast.AST
generic_visit(self, node);
visit(self, node.value);
annotation = getattr(node.value, "annotation", nothing)
if annotation === nothing
return node
end
for target in node.targets
target_has_annotation = hasattr(target, "annotation")
inferred = target_has_annotation ? (getattr(target.annotation, "inferred", false)) : (false)
if isinstance(!(target_has_annotation)||inferred, (int, float))&&!(target_has_annotation)||inferred != 0||isinstance(!(target_has_annotation)||inferred, tuple)&&!(target_has_annotation)||inferred != ()||isinstance(!(target_has_annotation)||inferred, list)&&!(target_has_annotation)||inferred != []||!(target_has_annotation)||inferred === nothing||isinstance(!(target_has_annotation)||inferred, bool)&&!(target_has_annotation)||inferred
target.annotation = annotation
target.annotation.inferred = true
end
end
return node
end

function visit_AnnAssign(self::InferTypesTransformer, node::ast.AnnAssign)::ast.AST
generic_visit(self, node);
node.target.annotation = node.annotation
target = node.target
target_typename = _typename_from_annotation(self._clike, target)
if target_typename in self.FIXED_WIDTH_INTS_NAME
self.has_fixed_width_ints = true
end
annotation = get_inferred_type(node.value)
value_typename = _generic_typename_from_type_node(self._clike, annotation)
target_class = class_for_typename(target_typename, nothing)
value_class = class_for_typename(value_typename, nothing)
if isinstance(!(is_compatible(target_class, value_class, target, node.value))&&target_class !== nothing, (int, float))&&!(is_compatible(target_class, value_class, target, node.value))&&target_class !== nothing != 0||isinstance(!(is_compatible(target_class, value_class, target, node.value))&&target_class !== nothing, tuple)&&!(is_compatible(target_class, value_class, target, node.value))&&target_class !== nothing != ()||isinstance(!(is_compatible(target_class, value_class, target, node.value))&&target_class !== nothing, list)&&!(is_compatible(target_class, value_class, target, node.value))&&target_class !== nothing != []||!(is_compatible(target_class, value_class, target, node.value))&&target_class !== nothing === nothing||isinstance(!(is_compatible(target_class, value_class, target, node.value))&&target_class !== nothing, bool)&&!(is_compatible(target_class, value_class, target, node.value))&&target_class !== nothing
throw(AstIncompatibleAssign("".join([string(target_class), " incompatible with ", string(value_class)]), node))
end
return node
end

function visit_AugAssign(self::InferTypesTransformer, node::ast.AugAssign)::ast.AST
generic_visit(self, node);
target = node.target
annotation = getattr(node.value, "annotation", nothing)
if isinstance(annotation !== nothing&&!(hasattr(target, "annotation")), (int, float))&&annotation !== nothing&&!(hasattr(target, "annotation")) != 0||isinstance(annotation !== nothing&&!(hasattr(target, "annotation")), tuple)&&annotation !== nothing&&!(hasattr(target, "annotation")) != ()||isinstance(annotation !== nothing&&!(hasattr(target, "annotation")), list)&&annotation !== nothing&&!(hasattr(target, "annotation")) != []||annotation !== nothing&&!(hasattr(target, "annotation")) === nothing||isinstance(annotation !== nothing&&!(hasattr(target, "annotation")), bool)&&annotation !== nothing&&!(hasattr(target, "annotation"))
target.annotation = annotation
end
return node
end

function visit_Compare{T0, RT}(self::InferTypesTransformer, node::T0)::RT
generic_visit(self, node);
node.annotation = Name(ast, "bool")
return node
end

function visit_Return{T0, RT}(self::InferTypesTransformer, node::T0)::RT
generic_visit(self, node);
new_type_str = hasattr(node.value, "annotation") ? (get_id(node.value.annotation)) : (nothing)
if new_type_str === nothing
return node
end
for scope in node.scopes
type_str = nothing
if isinstance(isinstance(scope, ast.FunctionDef), (int, float))&&isinstance(scope, ast.FunctionDef) != 0||isinstance(isinstance(scope, ast.FunctionDef), tuple)&&isinstance(scope, ast.FunctionDef) != ()||isinstance(isinstance(scope, ast.FunctionDef), list)&&isinstance(scope, ast.FunctionDef) != []||isinstance(scope, ast.FunctionDef) === nothing||isinstance(isinstance(scope, ast.FunctionDef), bool)&&isinstance(scope, ast.FunctionDef)
type_str = get_id(scope.returns);
if type_str !== nothing
if new_type_str != type_str
type_str = join("", ["Union[", string(type_str), ",", string(new_type_str), "]"]);
scope.returns.id = type_str
end
else

if scope.returns === nothing
scope.returns = Name(ast, new_type_str)
lifetime = getattr(node.value.annotation, "lifetime", nothing)
if lifetime !== nothing
scope.returns.lifetime = lifetime
end
end
end
end
end
return node
end

function visit_UnaryOp{T0, RT}(self::InferTypesTransformer, node::T0)::RT
generic_visit(self, node);
if isinstance(isinstance(node.operand, ast.Name), (int, float))&&isinstance(node.operand, ast.Name) != 0||isinstance(isinstance(node.operand, ast.Name), tuple)&&isinstance(node.operand, ast.Name) != ()||isinstance(isinstance(node.operand, ast.Name), list)&&isinstance(node.operand, ast.Name) != []||isinstance(node.operand, ast.Name) === nothing||isinstance(isinstance(node.operand, ast.Name), bool)&&isinstance(node.operand, ast.Name)
operand = find(node.scopes, get_id(node.operand))
else

operand = node.operand
end
if isinstance(hasattr(operand, "annotation"), (int, float))&&hasattr(operand, "annotation") != 0||isinstance(hasattr(operand, "annotation"), tuple)&&hasattr(operand, "annotation") != ()||isinstance(hasattr(operand, "annotation"), list)&&hasattr(operand, "annotation") != []||hasattr(operand, "annotation") === nothing||isinstance(hasattr(operand, "annotation"), bool)&&hasattr(operand, "annotation")
node.annotation = operand.annotation
end
return node
end

function _handle_overflow{T0, T1, T2}(self::InferTypesTransformer, op::T0, left_id::T1, right_id::T2)::String
widening_op = isinstance(op, ast.Add)||isinstance(op, ast.Mult)
left_class = class_for_typename(left_id, nothing)
right_class = class_for_typename(right_id, nothing)
left_idx = left_class in self.FIXED_WIDTH_INTS ? (index(self.FIXED_WIDTH_INTS_LIST, left_class)) : (-1)
right_idx = right_class in self.FIXED_WIDTH_INTS ? (index(self.FIXED_WIDTH_INTS_LIST, right_class)) : (-1)
max_idx = max(left_idx, right_idx)
cint64_idx = index(self.FIXED_WIDTH_INTS_LIST, c_int64)
if isinstance(widening_op, (int, float))&&widening_op != 0||isinstance(widening_op, tuple)&&widening_op != ()||isinstance(widening_op, list)&&widening_op != []||widening_op === nothing||isinstance(widening_op, bool)&&widening_op
if max_idx not in Set([-1, cint64_idx, length(self.FIXED_WIDTH_INTS_LIST) - 1])
return self.FIXED_WIDTH_INTS_NAME_LIST[max_idx + 1]
end
end
if isinstance(left_id == "float"||right_id == "float", (int, float))&&left_id == "float"||right_id == "float" != 0||isinstance(left_id == "float"||right_id == "float", tuple)&&left_id == "float"||right_id == "float" != ()||isinstance(left_id == "float"||right_id == "float", list)&&left_id == "float"||right_id == "float" != []||left_id == "float"||right_id == "float" === nothing||isinstance(left_id == "float"||right_id == "float", bool)&&left_id == "float"||right_id == "float"
return "float"
end
return left_idx > right_idx ? (left_id) : (right_id)
end

function visit_BinOp{T0, RT}(self::InferTypesTransformer, node::T0)::RT
generic_visit(self, node);
if isinstance(isinstance(node.left, ast.Name), (int, float))&&isinstance(node.left, ast.Name) != 0||isinstance(isinstance(node.left, ast.Name), tuple)&&isinstance(node.left, ast.Name) != ()||isinstance(isinstance(node.left, ast.Name), list)&&isinstance(node.left, ast.Name) != []||isinstance(node.left, ast.Name) === nothing||isinstance(isinstance(node.left, ast.Name), bool)&&isinstance(node.left, ast.Name)
lvar = find(node.scopes, get_id(node.left))
else

lvar = node.left
end
if isinstance(isinstance(node.right, ast.Name), (int, float))&&isinstance(node.right, ast.Name) != 0||isinstance(isinstance(node.right, ast.Name), tuple)&&isinstance(node.right, ast.Name) != ()||isinstance(isinstance(node.right, ast.Name), list)&&isinstance(node.right, ast.Name) != []||isinstance(node.right, ast.Name) === nothing||isinstance(isinstance(node.right, ast.Name), bool)&&isinstance(node.right, ast.Name)
rvar = find(node.scopes, get_id(node.right))
else

rvar = node.right
end
left = lvar&&hasattr(lvar, "annotation") ? (lvar.annotation) : (nothing)
right = rvar&&hasattr(rvar, "annotation") ? (rvar.annotation) : (nothing)
if isinstance(left === nothing&&right !== nothing, (int, float))&&left === nothing&&right !== nothing != 0||isinstance(left === nothing&&right !== nothing, tuple)&&left === nothing&&right !== nothing != ()||isinstance(left === nothing&&right !== nothing, list)&&left === nothing&&right !== nothing != []||left === nothing&&right !== nothing === nothing||isinstance(left === nothing&&right !== nothing, bool)&&left === nothing&&right !== nothing
node.annotation = right
return node
end
if isinstance(right === nothing&&left !== nothing, (int, float))&&right === nothing&&left !== nothing != 0||isinstance(right === nothing&&left !== nothing, tuple)&&right === nothing&&left !== nothing != ()||isinstance(right === nothing&&left !== nothing, list)&&right === nothing&&left !== nothing != []||right === nothing&&left !== nothing === nothing||isinstance(right === nothing&&left !== nothing, bool)&&right === nothing&&left !== nothing
node.annotation = left
return node
end
if isinstance(right === nothing&&left === nothing, (int, float))&&right === nothing&&left === nothing != 0||isinstance(right === nothing&&left === nothing, tuple)&&right === nothing&&left === nothing != ()||isinstance(right === nothing&&left === nothing, list)&&right === nothing&&left === nothing != []||right === nothing&&left === nothing === nothing||isinstance(right === nothing&&left === nothing, bool)&&right === nothing&&left === nothing
return node
end
left_id = get_id(left)
right_id = get_id(right)
if isinstance(left_id == right_id&&left_id == "int", (int, float))&&left_id == right_id&&left_id == "int" != 0||isinstance(left_id == right_id&&left_id == "int", tuple)&&left_id == right_id&&left_id == "int" != ()||isinstance(left_id == right_id&&left_id == "int", list)&&left_id == right_id&&left_id == "int" != []||left_id == right_id&&left_id == "int" === nothing||isinstance(left_id == right_id&&left_id == "int", bool)&&left_id == right_id&&left_id == "int"
if isinstance(!(isinstance(node.op, ast.Div))||getattr(node, "use_integer_div", false), (int, float))&&!(isinstance(node.op, ast.Div))||getattr(node, "use_integer_div", false) != 0||isinstance(!(isinstance(node.op, ast.Div))||getattr(node, "use_integer_div", false), tuple)&&!(isinstance(node.op, ast.Div))||getattr(node, "use_integer_div", false) != ()||isinstance(!(isinstance(node.op, ast.Div))||getattr(node, "use_integer_div", false), list)&&!(isinstance(node.op, ast.Div))||getattr(node, "use_integer_div", false) != []||!(isinstance(node.op, ast.Div))||getattr(node, "use_integer_div", false) === nothing||isinstance(!(isinstance(node.op, ast.Div))||getattr(node, "use_integer_div", false), bool)&&!(isinstance(node.op, ast.Div))||getattr(node, "use_integer_div", false)
node.annotation = left
else

node.annotation = Name(ast, "float")
end
return node
end
if left_id == "int"
left_id = "c_int32";
end
if right_id == "int"
right_id = "c_int32";
end
if isinstance(left_id in self.FIXED_WIDTH_INTS_NAME&&right_id in self.FIXED_WIDTH_INTS_NAME, (int, float))&&left_id in self.FIXED_WIDTH_INTS_NAME&&right_id in self.FIXED_WIDTH_INTS_NAME != 0||isinstance(left_id in self.FIXED_WIDTH_INTS_NAME&&right_id in self.FIXED_WIDTH_INTS_NAME, tuple)&&left_id in self.FIXED_WIDTH_INTS_NAME&&right_id in self.FIXED_WIDTH_INTS_NAME != ()||isinstance(left_id in self.FIXED_WIDTH_INTS_NAME&&right_id in self.FIXED_WIDTH_INTS_NAME, list)&&left_id in self.FIXED_WIDTH_INTS_NAME&&right_id in self.FIXED_WIDTH_INTS_NAME != []||left_id in self.FIXED_WIDTH_INTS_NAME&&right_id in self.FIXED_WIDTH_INTS_NAME === nothing||isinstance(left_id in self.FIXED_WIDTH_INTS_NAME&&right_id in self.FIXED_WIDTH_INTS_NAME, bool)&&left_id in self.FIXED_WIDTH_INTS_NAME&&right_id in self.FIXED_WIDTH_INTS_NAME
ret = _handle_overflow(self, node.op, left_id, right_id)
node.annotation = Name(ast, ret)
return node
end
if left_id == right_id
if isinstance(isinstance(node.op, ast.Div), (int, float))&&isinstance(node.op, ast.Div) != 0||isinstance(isinstance(node.op, ast.Div), tuple)&&isinstance(node.op, ast.Div) != ()||isinstance(isinstance(node.op, ast.Div), list)&&isinstance(node.op, ast.Div) != []||isinstance(node.op, ast.Div) === nothing||isinstance(isinstance(node.op, ast.Div), bool)&&isinstance(node.op, ast.Div)
if left_id == "int"
node.annotation = Name(ast, "float")
return node
end
end
node.annotation = left
return node
end
if left_id in self.FIXED_WIDTH_INTS_NAME
left_id = "int";
end
if right_id in self.FIXED_WIDTH_INTS_NAME
right_id = "int";
end
if (left_id, right_id) in Set([("int", "float"), ("float", "int")])
node.annotation = Name(ast, "float")
return node
end
if (left_id, right_id) in Set([("int", "complex"), ("complex", "int"), ("float", "complex"), ("complex", "float")])
node.annotation = Name(ast, "complex")
return node
end
if isinstance(isinstance(node.op, ast.Mult)&&Set([left_id, right_id]) in [Set(["bytes", "int"]), Set(["str", "int"]), Set(["tuple", "int"]), Set(["List", "int"])], (int, float))&&isinstance(node.op, ast.Mult)&&Set([left_id, right_id]) in [Set(["bytes", "int"]), Set(["str", "int"]), Set(["tuple", "int"]), Set(["List", "int"])] != 0||isinstance(isinstance(node.op, ast.Mult)&&Set([left_id, right_id]) in [Set(["bytes", "int"]), Set(["str", "int"]), Set(["tuple", "int"]), Set(["List", "int"])], tuple)&&isinstance(node.op, ast.Mult)&&Set([left_id, right_id]) in [Set(["bytes", "int"]), Set(["str", "int"]), Set(["tuple", "int"]), Set(["List", "int"])] != ()||isinstance(isinstance(node.op, ast.Mult)&&Set([left_id, right_id]) in [Set(["bytes", "int"]), Set(["str", "int"]), Set(["tuple", "int"]), Set(["List", "int"])], list)&&isinstance(node.op, ast.Mult)&&Set([left_id, right_id]) in [Set(["bytes", "int"]), Set(["str", "int"]), Set(["tuple", "int"]), Set(["List", "int"])] != []||isinstance(node.op, ast.Mult)&&Set([left_id, right_id]) in [Set(["bytes", "int"]), Set(["str", "int"]), Set(["tuple", "int"]), Set(["List", "int"])] === nothing||isinstance(isinstance(node.op, ast.Mult)&&Set([left_id, right_id]) in [Set(["bytes", "int"]), Set(["str", "int"]), Set(["tuple", "int"]), Set(["List", "int"])], bool)&&isinstance(node.op, ast.Mult)&&Set([left_id, right_id]) in [Set(["bytes", "int"]), Set(["str", "int"]), Set(["tuple", "int"]), Set(["List", "int"])]
node.annotation = Name(ast, left_id)
return node
end
LEGAL_COMBINATIONS = Set([("str", ast.Mod), ("List", ast.Add)])
if isinstance(left_id !== nothing&&(left_id, type_(node.op)) not in LEGAL_COMBINATIONS, (int, float))&&left_id !== nothing&&(left_id, type_(node.op)) not in LEGAL_COMBINATIONS != 0||isinstance(left_id !== nothing&&(left_id, type_(node.op)) not in LEGAL_COMBINATIONS, tuple)&&left_id !== nothing&&(left_id, type_(node.op)) not in LEGAL_COMBINATIONS != ()||isinstance(left_id !== nothing&&(left_id, type_(node.op)) not in LEGAL_COMBINATIONS, list)&&left_id !== nothing&&(left_id, type_(node.op)) not in LEGAL_COMBINATIONS != []||left_id !== nothing&&(left_id, type_(node.op)) not in LEGAL_COMBINATIONS === nothing||isinstance(left_id !== nothing&&(left_id, type_(node.op)) not in LEGAL_COMBINATIONS, bool)&&left_id !== nothing&&(left_id, type_(node.op)) not in LEGAL_COMBINATIONS
throw(AstUnrecognisedBinOp(left_id, right_id, node))
end
return node
end

function visit_ClassDef{T0, RT}(self::InferTypesTransformer, node::T0)::RT
node.annotation = Name(ast, node.name)
generic_visit(self, node);
return node
end

function visit_Attribute{T0, RT}(self::InferTypesTransformer, node::T0)::RT
value_id = get_id(node.value)
if isinstance(value_id !== nothing&&hasattr(node, "scopes"), (int, float))&&value_id !== nothing&&hasattr(node, "scopes") != 0||isinstance(value_id !== nothing&&hasattr(node, "scopes"), tuple)&&value_id !== nothing&&hasattr(node, "scopes") != ()||isinstance(value_id !== nothing&&hasattr(node, "scopes"), list)&&value_id !== nothing&&hasattr(node, "scopes") != []||value_id !== nothing&&hasattr(node, "scopes") === nothing||isinstance(value_id !== nothing&&hasattr(node, "scopes"), bool)&&value_id !== nothing&&hasattr(node, "scopes")
if isinstance(is_enum(value_id, node.scopes), (int, float))&&is_enum(value_id, node.scopes) != 0||isinstance(is_enum(value_id, node.scopes), tuple)&&is_enum(value_id, node.scopes) != ()||isinstance(is_enum(value_id, node.scopes), list)&&is_enum(value_id, node.scopes) != []||is_enum(value_id, node.scopes) === nothing||isinstance(is_enum(value_id, node.scopes), bool)&&is_enum(value_id, node.scopes)
node.annotation = find(node.scopes, value_id)
end
end
return node
end

function visit_Call{T0, RT}(self::InferTypesTransformer, node::T0)::RT
fname = get_id(node.func)
if fname !== nothing
if isinstance(startswith(fname, "self."), (int, float))&&startswith(fname, "self.") != 0||isinstance(startswith(fname, "self."), tuple)&&startswith(fname, "self.") != ()||isinstance(startswith(fname, "self."), list)&&startswith(fname, "self.") != []||startswith(fname, "self.") === nothing||isinstance(startswith(fname, "self."), bool)&&startswith(fname, "self.")
fname = split(fname, ".", 1)[1];
end
fn = find(node.scopes, fname)
if isinstance(isinstance(fn, ast.ClassDef), (int, float))&&isinstance(fn, ast.ClassDef) != 0||isinstance(isinstance(fn, ast.ClassDef), tuple)&&isinstance(fn, ast.ClassDef) != ()||isinstance(isinstance(fn, ast.ClassDef), list)&&isinstance(fn, ast.ClassDef) != []||isinstance(fn, ast.ClassDef) === nothing||isinstance(isinstance(fn, ast.ClassDef), bool)&&isinstance(fn, ast.ClassDef)
_annotate(self, node);
else

if isinstance(isinstance(fn, ast.FunctionDef), (int, float))&&isinstance(fn, ast.FunctionDef) != 0||isinstance(isinstance(fn, ast.FunctionDef), tuple)&&isinstance(fn, ast.FunctionDef) != ()||isinstance(isinstance(fn, ast.FunctionDef), list)&&isinstance(fn, ast.FunctionDef) != []||isinstance(fn, ast.FunctionDef) === nothing||isinstance(isinstance(fn, ast.FunctionDef), bool)&&isinstance(fn, ast.FunctionDef)
return_type = hasattr(fn, "returns")&&fn.returns ? (fn.returns) : (nothing)
if return_type !== nothing
node.annotation = return_type
lifetime = getattr(fn.returns, "lifetime", nothing)
if lifetime !== nothing
node.annotation.lifetime = lifetime
end
end
else

if fname in Set(["max", "min"])
return_type = get_inferred_type(node.args[0]);
if return_type !== nothing
node.annotation = return_type
end
else

if fname in values(self.TYPE_DICT)
node.annotation = Name(ast, fname)
end
end
end
end
end
generic_visit(self, node);
return node
end

function visit_Subscript{T0, RT}(self::InferTypesTransformer, node::T0)::RT
definition = find(node.scopes, get_id(node.value))
if isinstance(hasattr(definition, "annotation"), (int, float))&&hasattr(definition, "annotation") != 0||isinstance(hasattr(definition, "annotation"), tuple)&&hasattr(definition, "annotation") != ()||isinstance(hasattr(definition, "annotation"), list)&&hasattr(definition, "annotation") != []||hasattr(definition, "annotation") === nothing||isinstance(hasattr(definition, "annotation"), bool)&&hasattr(definition, "annotation")
_typename_from_annotation(self._clike, definition);
if isinstance(hasattr(definition, "container_type"), (int, float))&&hasattr(definition, "container_type") != 0||isinstance(hasattr(definition, "container_type"), tuple)&&hasattr(definition, "container_type") != ()||isinstance(hasattr(definition, "container_type"), list)&&hasattr(definition, "container_type") != []||hasattr(definition, "container_type") === nothing||isinstance(hasattr(definition, "container_type"), bool)&&hasattr(definition, "container_type")
container_type, element_type = definition.container_type
if isinstance(container_type == "Dict"||isinstance(element_type, list), (int, float))&&container_type == "Dict"||isinstance(element_type, list) != 0||isinstance(container_type == "Dict"||isinstance(element_type, list), tuple)&&container_type == "Dict"||isinstance(element_type, list) != ()||isinstance(container_type == "Dict"||isinstance(element_type, list), list)&&container_type == "Dict"||isinstance(element_type, list) != []||container_type == "Dict"||isinstance(element_type, list) === nothing||isinstance(container_type == "Dict"||isinstance(element_type, list), bool)&&container_type == "Dict"||isinstance(element_type, list)
element_type = element_type[1]
end
node.annotation = Name(ast, element_type)
if isinstance(hasattr(definition.annotation, "lifetime"), (int, float))&&hasattr(definition.annotation, "lifetime") != 0||isinstance(hasattr(definition.annotation, "lifetime"), tuple)&&hasattr(definition.annotation, "lifetime") != ()||isinstance(hasattr(definition.annotation, "lifetime"), list)&&hasattr(definition.annotation, "lifetime") != []||hasattr(definition.annotation, "lifetime") === nothing||isinstance(hasattr(definition.annotation, "lifetime"), bool)&&hasattr(definition.annotation, "lifetime")
node.annotation.lifetime = definition.annotation.lifetime
end
end
end
generic_visit(self, node);
return node
end

function visit_For{T0, RT}(self::InferTypesTransformer, node::T0)::RT
visit(self, node.target);
visit(self, node.iter);
if isinstance(hasattr(node.iter, "annotation")&&isinstance(node.iter.annotation, ast.Subscript), (int, float))&&hasattr(node.iter, "annotation")&&isinstance(node.iter.annotation, ast.Subscript) != 0||isinstance(hasattr(node.iter, "annotation")&&isinstance(node.iter.annotation, ast.Subscript), tuple)&&hasattr(node.iter, "annotation")&&isinstance(node.iter.annotation, ast.Subscript) != ()||isinstance(hasattr(node.iter, "annotation")&&isinstance(node.iter.annotation, ast.Subscript), list)&&hasattr(node.iter, "annotation")&&isinstance(node.iter.annotation, ast.Subscript) != []||hasattr(node.iter, "annotation")&&isinstance(node.iter.annotation, ast.Subscript) === nothing||isinstance(hasattr(node.iter, "annotation")&&isinstance(node.iter.annotation, ast.Subscript), bool)&&hasattr(node.iter, "annotation")&&isinstance(node.iter.annotation, ast.Subscript)
typ = _slice_value(self._clike, node.iter.annotation)
if isinstance(isinstance(node.target, ast.Name), (int, float))&&isinstance(node.target, ast.Name) != 0||isinstance(isinstance(node.target, ast.Name), tuple)&&isinstance(node.target, ast.Name) != ()||isinstance(isinstance(node.target, ast.Name), list)&&isinstance(node.target, ast.Name) != []||isinstance(node.target, ast.Name) === nothing||isinstance(isinstance(node.target, ast.Name), bool)&&isinstance(node.target, ast.Name)
node.target.annotation = typ
else

if isinstance(isinstance(node.target, ast.Tuple)&&isinstance(typ, ast.Subscript), (int, float))&&isinstance(node.target, ast.Tuple)&&isinstance(typ, ast.Subscript) != 0||isinstance(isinstance(node.target, ast.Tuple)&&isinstance(typ, ast.Subscript), tuple)&&isinstance(node.target, ast.Tuple)&&isinstance(typ, ast.Subscript) != ()||isinstance(isinstance(node.target, ast.Tuple)&&isinstance(typ, ast.Subscript), list)&&isinstance(node.target, ast.Tuple)&&isinstance(typ, ast.Subscript) != []||isinstance(node.target, ast.Tuple)&&isinstance(typ, ast.Subscript) === nothing||isinstance(isinstance(node.target, ast.Tuple)&&isinstance(typ, ast.Subscript), bool)&&isinstance(node.target, ast.Tuple)&&isinstance(typ, ast.Subscript)
typ = _slice_value(self._clike, typ);
for e in node.target.elts
e.annotation = typ
end
end
end
end
generic_visit(self, node);
return node
end

