import ast
using ast_helpers: get_id
function get_ann_repr{T0, T1, T2, T3, RT}(node::T0, parse_func::T1, default::T2, sep::T3)::RT
if node === nothing
return default
end
if isinstance(isinstance(node, str), (int, float))&&isinstance(node, str) != 0||isinstance(isinstance(node, str), tuple)&&isinstance(node, str) != ()||isinstance(isinstance(node, str), list)&&isinstance(node, str) != []||isinstance(node, str) === nothing||isinstance(isinstance(node, str), bool)&&isinstance(node, str)
if isinstance(parse_func, (int, float))&&parse_func != 0||isinstance(parse_func, tuple)&&parse_func != ()||isinstance(parse_func, list)&&parse_func != []||parse_func === nothing||isinstance(parse_func, bool)&&parse_func
return parse_func(node)
end
return node
else

if isinstance(isinstance(node, ast.Name), (int, float))&&isinstance(node, ast.Name) != 0||isinstance(isinstance(node, ast.Name), tuple)&&isinstance(node, ast.Name) != ()||isinstance(isinstance(node, ast.Name), list)&&isinstance(node, ast.Name) != []||isinstance(node, ast.Name) === nothing||isinstance(isinstance(node, ast.Name), bool)&&isinstance(node, ast.Name)
id = get_id(node)
if isinstance(parse_func, (int, float))&&parse_func != 0||isinstance(parse_func, tuple)&&parse_func != ()||isinstance(parse_func, list)&&parse_func != []||parse_func === nothing||isinstance(parse_func, bool)&&parse_func
return parse_func(id)
end
return id
else

if isinstance(isinstance(node, ast.Call), (int, float))&&isinstance(node, ast.Call) != 0||isinstance(isinstance(node, ast.Call), tuple)&&isinstance(node, ast.Call) != ()||isinstance(isinstance(node, ast.Call), list)&&isinstance(node, ast.Call) != []||isinstance(node, ast.Call) === nothing||isinstance(isinstance(node, ast.Call), bool)&&isinstance(node, ast.Call)
func = get_ann_repr(node.func, parse_func, default, sep)
args = []
for arg in node.args
push!(args, get_ann_repr(arg, parse_func, default, sep));
end
return join("", [string(".".join(args)), ".", string(func)])
else

if isinstance(isinstance(node, ast.Attribute), (int, float))&&isinstance(node, ast.Attribute) != 0||isinstance(isinstance(node, ast.Attribute), tuple)&&isinstance(node, ast.Attribute) != ()||isinstance(isinstance(node, ast.Attribute), list)&&isinstance(node, ast.Attribute) != []||isinstance(node, ast.Attribute) === nothing||isinstance(isinstance(node, ast.Attribute), bool)&&isinstance(node, ast.Attribute)
return join("", [string(get_ann_repr(node.value, parse_func, default, sep)), ".", string(get_ann_repr(node.attr, parse_func, default, sep))])
else

if isinstance(isinstance(node, ast.Constant), (int, float))&&isinstance(node, ast.Constant) != 0||isinstance(isinstance(node, ast.Constant), tuple)&&isinstance(node, ast.Constant) != ()||isinstance(isinstance(node, ast.Constant), list)&&isinstance(node, ast.Constant) != []||isinstance(node, ast.Constant) === nothing||isinstance(isinstance(node, ast.Constant), bool)&&isinstance(node, ast.Constant)
if isinstance(parse_func, (int, float))&&parse_func != 0||isinstance(parse_func, tuple)&&parse_func != ()||isinstance(parse_func, list)&&parse_func != []||parse_func === nothing||isinstance(parse_func, bool)&&parse_func
return parse_func(node.value)
end
return join("", [string(node.value)])
else

if isinstance(isinstance(node, ast.Subscript), (int, float))&&isinstance(node, ast.Subscript) != 0||isinstance(isinstance(node, ast.Subscript), tuple)&&isinstance(node, ast.Subscript) != ()||isinstance(isinstance(node, ast.Subscript), list)&&isinstance(node, ast.Subscript) != []||isinstance(node, ast.Subscript) === nothing||isinstance(isinstance(node, ast.Subscript), bool)&&isinstance(node, ast.Subscript)
id = get_ann_repr(node.value, parse_func, default, sep);
slice_val = get_ann_repr(node.slice, parse_func, default, sep)
if isinstance(sep, (int, float))&&sep != 0||isinstance(sep, tuple)&&sep != ()||isinstance(sep, list)&&sep != []||sep === nothing||isinstance(sep, bool)&&sep
return join("", [string(id), string(sep[0]), string(slice_val), string(sep[1])])
end
return join("", [string(id), "[", string(slice_val), "]"])
else

if isinstance(isinstance(node, ast.Tuple)||isinstance(node, ast.List), (int, float))&&isinstance(node, ast.Tuple)||isinstance(node, ast.List) != 0||isinstance(isinstance(node, ast.Tuple)||isinstance(node, ast.List), tuple)&&isinstance(node, ast.Tuple)||isinstance(node, ast.List) != ()||isinstance(isinstance(node, ast.Tuple)||isinstance(node, ast.List), list)&&isinstance(node, ast.Tuple)||isinstance(node, ast.List) != []||isinstance(node, ast.Tuple)||isinstance(node, ast.List) === nothing||isinstance(isinstance(node, ast.Tuple)||isinstance(node, ast.List), bool)&&isinstance(node, ast.Tuple)||isinstance(node, ast.List)
elts = list(map((x) -> get_ann_repr(x, parse_func, default, sep), node.elts))
return join(", ", elts)
else

if isinstance(# named expr ann unimplemented on line 39:9, (int, float))&&# named expr ann unimplemented on line 39:9 != 0||isinstance(# named expr ann unimplemented on line 39:9, tuple)&&# named expr ann unimplemented on line 39:9 != ()||isinstance(# named expr ann unimplemented on line 39:9, list)&&# named expr ann unimplemented on line 39:9 != []||# named expr ann unimplemented on line 39:9 === nothing||isinstance(# named expr ann unimplemented on line 39:9, bool)&&# named expr ann unimplemented on line 39:9
if isinstance(parse_func&&# named expr parsed_ann unimplemented on line 41:27, (int, float))&&parse_func&&# named expr parsed_ann unimplemented on line 41:27 != 0||isinstance(parse_func&&# named expr parsed_ann unimplemented on line 41:27, tuple)&&parse_func&&# named expr parsed_ann unimplemented on line 41:27 != ()||isinstance(parse_func&&# named expr parsed_ann unimplemented on line 41:27, list)&&parse_func&&# named expr parsed_ann unimplemented on line 41:27 != []||parse_func&&# named expr parsed_ann unimplemented on line 41:27 === nothing||isinstance(parse_func&&# named expr parsed_ann unimplemented on line 41:27, bool)&&parse_func&&# named expr parsed_ann unimplemented on line 41:27
return parsed_ann
end
return ann
end
end
end
end
end
end
end
end
return default
end

