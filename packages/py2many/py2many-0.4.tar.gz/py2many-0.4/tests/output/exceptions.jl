import ast
using ast_helpers: get_id
struct _InternalErrorBase

end


struct TypeNotSupported

end

function __init__{T0}(self::TypeNotSupported, typename::T0)
__init__(super(), "".join([string(typename), " not supported"]));
end

struct AstErrorBase
lineno::
col_offset::
end

function __init__(self::AstErrorBase, msg::String, node::ast.AST)
self.lineno = node.lineno
self.col_offset = node.col_offset
__init__(super(), msg);
end

struct AstNotImplementedError

end


struct AstUnrecognisedBinOp
lineno::
col_offset::
end

function __init__(self::AstUnrecognisedBinOp, left_id::String, right_id::String, node::ast.AST)
self.lineno = node.lineno
self.col_offset = node.col_offset
__init__(super(), "".join([string(left_id), " ", string(type_(node.op)), " ", string(right_id)]), convert(String, node));
end

struct AstClassUsedBeforeDeclaration

end

function __init__{T0}(self::AstClassUsedBeforeDeclaration, fndef::T0, node::ast.AST)
__init__(super(), "".join(["Declaration of ", string(get_id(fndef)), " not yet parsed"]), node);
end

struct AstCouldNotInfer

end

function __init__{T0}(self::AstCouldNotInfer, type_node::T0, node::ast.AST)
__init__(super(), "".join(["Could not infer: ", string(type_node)]), node);
end

struct AstTypeNotSupported

end

function __init__{T0}(self::AstTypeNotSupported, msg::T0, node::ast.AST)
__init__(super(), msg, node);
end

struct AstIncompatibleAssign

end


struct AstEmptyNodeFound

end

function __init__(self::AstEmptyNodeFound)
__init__(super());
end

