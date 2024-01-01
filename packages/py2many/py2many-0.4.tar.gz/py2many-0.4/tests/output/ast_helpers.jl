import ast
using py2many::astx:ASTxIf

try
    using ast: unparse
catch exn
    if exn isa ImportError
        using astor: to_source
    end
end
unparse;
function get_id{T0,RT}(var::T0)::RT
    if isinstance(isinstance(var, ast.alias), (int, float)) &&
       isinstance(var, ast.alias) != 0 ||
       isinstance(isinstance(var, ast.alias), tuple) && isinstance(var, ast.alias) != () ||
       isinstance(isinstance(var, ast.alias), list) && isinstance(var, ast.alias) != [] ||
       isinstance(var, ast.alias) === nothing ||
       isinstance(isinstance(var, ast.alias), bool) && isinstance(var, ast.alias)
        return var.name
    else

        if isinstance(isinstance(var, ast.Name), (int, float)) &&
           isinstance(var, ast.Name) != 0 ||
           isinstance(isinstance(var, ast.Name), tuple) &&
           isinstance(var, ast.Name) != () ||
           isinstance(isinstance(var, ast.Name), list) && isinstance(var, ast.Name) != [] ||
           isinstance(var, ast.Name) === nothing ||
           isinstance(isinstance(var, ast.Name), bool) && isinstance(var, ast.Name)
            return var.id
        else

            if isinstance(isinstance(var, ast.arg), (int, float)) &&
               isinstance(var, ast.arg) != 0 ||
               isinstance(isinstance(var, ast.arg), tuple) &&
               isinstance(var, ast.arg) != () ||
               isinstance(isinstance(var, ast.arg), list) &&
               isinstance(var, ast.arg) != [] ||
               isinstance(var, ast.arg) === nothing ||
               isinstance(isinstance(var, ast.arg), bool) && isinstance(var, ast.arg)
                return var.arg
            else

                if isinstance(isinstance(var, ast.FunctionDef), (int, float)) &&
                   isinstance(var, ast.FunctionDef) != 0 ||
                   isinstance(isinstance(var, ast.FunctionDef), tuple) &&
                   isinstance(var, ast.FunctionDef) != () ||
                   isinstance(isinstance(var, ast.FunctionDef), list) &&
                   isinstance(var, ast.FunctionDef) != [] ||
                   isinstance(var, ast.FunctionDef) === nothing ||
                   isinstance(isinstance(var, ast.FunctionDef), bool) &&
                   isinstance(var, ast.FunctionDef)
                    return var.name
                else

                    if isinstance(isinstance(var, ast.ClassDef), (int, float)) &&
                       isinstance(var, ast.ClassDef) != 0 ||
                       isinstance(isinstance(var, ast.ClassDef), tuple) &&
                       isinstance(var, ast.ClassDef) != () ||
                       isinstance(isinstance(var, ast.ClassDef), list) &&
                       isinstance(var, ast.ClassDef) != [] ||
                       isinstance(var, ast.ClassDef) === nothing ||
                       isinstance(isinstance(var, ast.ClassDef), bool) &&
                       isinstance(var, ast.ClassDef)
                        return var.name
                    else

                        if isinstance(isinstance(var, ast.Attribute), (int, float)) &&
                           isinstance(var, ast.Attribute) != 0 ||
                           isinstance(isinstance(var, ast.Attribute), tuple) &&
                           isinstance(var, ast.Attribute) != () ||
                           isinstance(isinstance(var, ast.Attribute), list) &&
                           isinstance(var, ast.Attribute) != [] ||
                           isinstance(var, ast.Attribute) === nothing ||
                           isinstance(isinstance(var, ast.Attribute), bool) &&
                           isinstance(var, ast.Attribute)
                            value_id = get_id(var.value)
                            return join("", [string(value_id), ".", string(var.attr)])
                        else

                            return nothing
                        end
                    end
                end
            end
        end
    end
end

function create_ast_node{T0,T1,RT}(code::T0, at_node::T1)::RT
    new_node = parse(ast, code).body[0]
    if isinstance(at_node, (int, float)) && at_node != 0 ||
       isinstance(at_node, tuple) && at_node != () ||
       isinstance(at_node, list) && at_node != [] ||
       at_node === nothing ||
       isinstance(at_node, bool) && at_node
        new_node.lineno = at_node.lineno
        new_node.col_offset = at_node.col_offset
    end
    return new_node
end

function create_ast_block{T0,T1}(body::T0, at_node::T1)::ASTxIf
    block = cast(ASTxIf, ast.If(ast.Constant(true), body, []))
    block.rewritten = true
    if isinstance(at_node, (int, float)) && at_node != 0 ||
       isinstance(at_node, tuple) && at_node != () ||
       isinstance(at_node, list) && at_node != [] ||
       at_node === nothing ||
       isinstance(at_node, bool) && at_node
        block.lineno = at_node.lineno
    end
    fix_missing_locations(ast, block)
    return block
end
