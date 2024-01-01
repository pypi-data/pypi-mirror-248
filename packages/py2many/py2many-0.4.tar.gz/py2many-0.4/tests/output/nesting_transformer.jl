import ast
function detect_nesting_levels{T0,RT}(node::T0)::RT
    return visit(NestingTransformer(), node)
end

struct NestingTransformer
    level::Int64
end

function __init__(self::NestingTransformer)
    self.level = 0
end

function _visit_level{T0}(self::NestingTransformer, node::T0)::ast.AST
    node.level = self.level
    self.level += 1
    generic_visit(self, node)
    self.level -= 1
    return node
end

function visit_FunctionDef{T0}(self::NestingTransformer, node::T0)::ast.AST
    return _visit_level(self, node)
end

function visit_ClassDef{T0}(self::NestingTransformer, node::T0)::ast.AST
    return _visit_level(self, node)
end

function visit_If{T0}(self::NestingTransformer, node::T0)::ast.AST
    return _visit_level(self, node)
end

function visit_While{T0}(self::NestingTransformer, node::T0)::ast.AST
    return _visit_level(self, node)
end

function visit_For{T0}(self::NestingTransformer, node::T0)::ast.AST
    return _visit_level(self, node)
end

function visit_Assign{T0,RT}(self::NestingTransformer, node::T0)::RT
    node.level = self.level
    generic_visit(self, node)
    return node
end
