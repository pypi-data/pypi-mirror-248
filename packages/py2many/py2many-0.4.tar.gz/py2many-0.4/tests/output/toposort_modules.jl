import ast
using pathlib: Path
using toposort: toposort_flatten
using collections: defaultdict

function module_for_path(path::Path)::String
    module_ = join(".", path.parts)
    return rsplit(module_, ".", 1)[0]
end

struct ImportDependencyVisitor
    deps::_modules::_current::String
end

function __init__{T0}(self::ImportDependencyVisitor, modules::T0)
    self.deps = defaultdict(set)
    self._modules = modules
end

function visit_Module{T0}(self::ImportDependencyVisitor, node::T0)
    self._current = module_for_path(node.__file__)
    generic_visit(self, node)
end

function visit_ImportFrom{T0}(self::ImportDependencyVisitor, node::T0)
    if node.module in self._modules
        add(self.deps[self._current], node.module)
    end
    generic_visit(self, node)
end

function visit_Import{T0}(self::ImportDependencyVisitor, node::T0)
    names = [n.name for n in node.names]
    for n in names
        if n in self._modules
            add(self.deps[self._current], n)
        end
    end
    generic_visit(self, node)
end

function get_dependencies{T0,RT}(trees::T0)::RT
    modules = (module_for_path(node.__file__) for node in trees)
    visitor = ImportDependencyVisitor(modules)
    for t in trees
        visit(visitor, t)
    end
    for m in modules
        if m
            not in visitor.deps
            visitor.deps[m] = set()
        end
    end
    return visitor.deps
end

function toposort{T0}(trees::T0)::Tuple
    deps = get_dependencies(trees)
    tree_dict = Dict(module_for_path(node.__file__) => node for node in trees)
    return tuple([tree_dict[t] for t in toposort_flatten(deps, true)])
end
