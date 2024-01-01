import ast
using py2many::analysis:get_id
function detect_mutable_vars{T0,RT}(node::T0)::RT
    return visit(MutabilityTransformer(), node)
end

struct MutabilityTransformer
    var_usage_count::Dict
    lvalue::Bool
end

function __init__(self::MutabilityTransformer)
    self.var_usage_count = Dict()
    self.lvalue = false
end

function increase_use_count{T0}(self::MutabilityTransformer, name::T0)
    if !(name in self.var_usage_count)
        self.var_usage_count[name] = 0
    end
    self.var_usage_count[name] += 1
end

function visit_FunctionDef{T0,RT}(self::MutabilityTransformer, node::T0)::RT
    self.var_usage_count = Dict()
    generic_visit(self, node)
    mutable_vars = []
    for (var, count) in items(self.var_usage_count)
        if count > 1
            push!(mutable_vars, var)
        end
    end
    node.mutable_vars = mutable_vars
    return node
end

function visit_Assign{T0,RT}(self::MutabilityTransformer, node::T0)::RT
    old = self.lvalue
    self.lvalue = true
    target = node.targets[0]
    if isinstance(isinstance(target, ast.Tuple), (int, float)) &&
       isinstance(target, ast.Tuple) != 0 ||
       isinstance(isinstance(target, ast.Tuple), tuple) &&
       isinstance(target, ast.Tuple) != () ||
       isinstance(isinstance(target, ast.Tuple), list) &&
       isinstance(target, ast.Tuple) != [] ||
       isinstance(target, ast.Tuple) === nothing ||
       isinstance(isinstance(target, ast.Tuple), bool) && isinstance(target, ast.Tuple)
        for e in target.elts
            visit(self, e)
        end
    end
    visit(self, target)
    self.lvalue = old
    generic_visit(self, node)
    return node
end

function _visit_assign_target{T0}(self::MutabilityTransformer, node::T0)::ast.AST
    old = self.lvalue
    self.lvalue = true
    visit(self, node.target)
    self.lvalue = old
    generic_visit(self, node)
    return node
end

function visit_AugAssign{T0}(self::MutabilityTransformer, node::T0)::ast.AST
    return _visit_assign_target(self, node)
end

function visit_AnnAssign{T0}(self::MutabilityTransformer, node::T0)::ast.AST
    return _visit_assign_target(self, node)
end

function visit_Subscript{T0,RT}(self::MutabilityTransformer, node::T0)::RT
    visit(self, node.value)
    visit(self, node.slice)
    return node
end

function visit_Name{T0,RT}(self::MutabilityTransformer, node::T0)::RT
    if isinstance(self.lvalue, (int, float)) && self.lvalue != 0 ||
       isinstance(self.lvalue, tuple) && self.lvalue != () ||
       isinstance(self.lvalue, list) && self.lvalue != [] ||
       self.lvalue === nothing ||
       isinstance(self.lvalue, bool) && self.lvalue
        increase_use_count(self, get_id(node))
    end
    return node
end

function visit_Call{T0,RT}(self::MutabilityTransformer, node::T0)::RT
    fname = get_id(node.func)
    fndef = find(node.scopes, fname)
    if isinstance(fndef && hasattr(fndef, "args"), (int, float)) &&
       fndef && hasattr(fndef, "args") != 0 ||
       isinstance(fndef && hasattr(fndef, "args"), tuple) &&
       fndef && hasattr(fndef, "args") != () ||
       isinstance(fndef && hasattr(fndef, "args"), list) &&
       fndef && hasattr(fndef, "args") != [] ||
       fndef && hasattr(fndef, "args") === nothing ||
       isinstance(fndef && hasattr(fndef, "args"), bool) && fndef && hasattr(fndef, "args")
        for (fnarg, node_arg) in zip(fndef.args.args, node.args)
            if isinstance(
                   hasattr(fndef, "mutable_vars") && fnarg.arg in fndef.mutable_vars,
                   (int, float),
               ) &&
               hasattr(fndef, "mutable_vars") && fnarg.arg in fndef.mutable_vars != 0 ||
               isinstance(
                   hasattr(fndef, "mutable_vars") && fnarg.arg in fndef.mutable_vars,
                   tuple,
               ) &&
               hasattr(fndef, "mutable_vars") && fnarg.arg in fndef.mutable_vars != () ||
               isinstance(
                   hasattr(fndef, "mutable_vars") && fnarg.arg in fndef.mutable_vars,
                   list,
               ) &&
               hasattr(fndef, "mutable_vars") && fnarg.arg in fndef.mutable_vars != [] ||
               hasattr(fndef, "mutable_vars") &&
               fnarg.arg in fndef.mutable_vars === nothing ||
               isinstance(
                   hasattr(fndef, "mutable_vars") && fnarg.arg in fndef.mutable_vars,
                   bool,
               ) && hasattr(fndef, "mutable_vars") && fnarg.arg in fndef.mutable_vars
                increase_use_count(self, get_id(node_arg))
            end
        end
    end
    if isinstance(hasattr(node.func, "attr"), (int, float)) &&
       hasattr(node.func, "attr") != 0 ||
       isinstance(hasattr(node.func, "attr"), tuple) && hasattr(node.func, "attr") != () ||
       isinstance(hasattr(node.func, "attr"), list) && hasattr(node.func, "attr") != [] ||
       hasattr(node.func, "attr") === nothing ||
       isinstance(hasattr(node.func, "attr"), bool) && hasattr(node.func, "attr")
        if node.func.attr == "append"
            increase_use_count(self, get_id(node.func.value))
        end
    end
    generic_visit(self, node)
    return node
end
