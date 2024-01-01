import ast
function add_annotation_flags{T0,RT}(node::T0)::RT
    return visit(AnnotationTransformer(), node)
end

struct AnnotationTransformer
    handling_annotation::Bool
end

function __init__(self::AnnotationTransformer)
    self.handling_annotation = false
end

function visit_arg{T0,RT}(self::AnnotationTransformer, node::T0)::RT
    if isinstance(node.annotation, (int, float)) && node.annotation != 0 ||
       isinstance(node.annotation, tuple) && node.annotation != () ||
       isinstance(node.annotation, list) && node.annotation != [] ||
       node.annotation === nothing ||
       isinstance(node.annotation, bool) && node.annotation
        self.handling_annotation = true
        visit(self, node.annotation)
        self.handling_annotation = false
    end
    return node
end

function visit_FunctionDef{T0,RT}(self::AnnotationTransformer, node::T0)::RT
    if isinstance(node.returns, (int, float)) && node.returns != 0 ||
       isinstance(node.returns, tuple) && node.returns != () ||
       isinstance(node.returns, list) && node.returns != [] ||
       node.returns === nothing ||
       isinstance(node.returns, bool) && node.returns
        self.handling_annotation = true
        visit(self, node.returns)
        self.handling_annotation = false
    end
    generic_visit(self, node)
    return node
end

function _visit_record_handling_annotation{T0}(
    self::AnnotationTransformer,
    node::T0,
)::ast.AST
    if isinstance(self.handling_annotation, (int, float)) &&
       self.handling_annotation != 0 ||
       isinstance(self.handling_annotation, tuple) && self.handling_annotation != () ||
       isinstance(self.handling_annotation, list) && self.handling_annotation != [] ||
       self.handling_annotation === nothing ||
       isinstance(self.handling_annotation, bool) && self.handling_annotation
        node.is_annotation = true
    end
    generic_visit(self, node)
    return node
end

function visit_Tuple{T0}(self::AnnotationTransformer, node::T0)::ast.AST
    return _visit_record_handling_annotation(self, node)
end

function visit_List{T0}(self::AnnotationTransformer, node::T0)::ast.AST
    return _visit_record_handling_annotation(self, node)
end

function visit_Name{T0}(self::AnnotationTransformer, node::T0)::ast.AST
    return _visit_record_handling_annotation(self, node)
end

function visit_Subscript{T0}(self::AnnotationTransformer, node::T0)::ast.AST
    return _visit_record_handling_annotation(self, node)
end

function visit_AnnAssign{T0,RT}(self::AnnotationTransformer, node::T0)::RT
    self.handling_annotation = true
    visit(self, node.target)
    self.handling_annotation = false
    generic_visit(self, node)
    return node
end
