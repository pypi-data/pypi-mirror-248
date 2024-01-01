using SuperEnum
import ast



@se LifeTime begin
    UNKNOWN = 0
                STATIC = 1

end

struct ASTxName
lifetime::LifeTime
assigned_from::Nothing{ASTx}
end


struct ASTxClassDef
is_dataclass::Bool
end


struct ASTxFunctionDef
mutable_vars::Array{String}
python_main::Bool
end


struct ASTxModule
__file__::Nothing{String}
end


struct ASTxSubscript
container_type::Nothing{{['String', 'String']}}
generic_container_type::Nothing{{['String', 'String']}}
end


struct ASTxIf
unpack::Bool
end


struct ASTx
annotation::ASTxName
rewritten::Bool
lhs::Bool
scopes::Array{ASTx}
id::Nothing{String}
end


