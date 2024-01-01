import ast


using clike: CLikeTranspiler
struct LanguageSettings
    transpiler::CLikeTranspiler
    ext::String
    display_name::String
    formatter::Nothing{Array{String}}
    indent::Nothing{Int64}
    rewriters::Array{ast.NodeVisitor}
    transformers::Array{Callable}
    post_rewriters::Array{ast.NodeVisitor}
    linter::Nothing{Array{String}}
    create_project::Nothing{Array{String}}
    project_subdir::Nothing{String}
end

function __hash__{RT}(self::LanguageSettings)::RT
    f = self.formatter !== nothing ? (tuple(self.formatter)) : (())
    l = self.linter !== nothing ? (tuple(self.linter)) : (())
    return hash((self.transpiler, f, l))
end
