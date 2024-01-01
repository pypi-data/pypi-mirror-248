import io

import ast

import textwrap
using tempfile: NamedTemporaryFile

try
using argparse_dataclass: dataclass
using argparse_dataclass: ArgumentParser
catch exn
if exn isa ImportError
ArgumentParser = "ArgumentParser"
ap_dataclass = "ap_dataclass"
end
end
struct JuliaTranspilerPlugins

end

function visit_argparse_dataclass{T0}(self::JuliaTranspilerPlugins, node::T0)::String
fields = []
for (declaration, typename_with_default) in items(node.declarations_with_defaults)
typename, default_value = typename_with_default
if typename === nothing
return nothing
end
if isinstance(default_value !== nothing&&typename != "bool", (int, float))&&default_value !== nothing&&typename != "bool" != 0||isinstance(default_value !== nothing&&typename != "bool", tuple)&&default_value !== nothing&&typename != "bool" != ()||isinstance(default_value !== nothing&&typename != "bool", list)&&default_value !== nothing&&typename != "bool" != []||default_value !== nothing&&typename != "bool" === nothing||isinstance(default_value !== nothing&&typename != "bool", bool)&&default_value !== nothing&&typename != "bool"
default_value = visit(self, default_value)
default_value = join("", [", default_value = \"", string(default_value), "\""])
else

default_value = ""
end
push!(fields, "".join(["#[structopt(short, long", string(default_value), ")]\npub ", string(declaration), ": ", string(typename), ","]));
end
fields = join("\n", fields);
add(self._usings, "structopt::StructOpt");
clsdef = "\n" + dedent(textwrap, "".join(["        #[derive(Debug, StructOpt)]\n        #[structopt(name = \"", string(self._module), "\", about = \"Placeholder\")]\n        struct ", string(node.name), " {\n            ", string(fields), "\n        }\n        "]))
return clsdef
end

function visit_open{T0, T1, RT}(self::JuliaTranspilerPlugins, node::T0, vargs::T1)::RT
add(self._usings, "std::fs::File");
if length(vargs) > 1
add(self._usings, "std::fs::OpenOptions");
mode = vargs[1]
opts = "OpenOptions::new()"
is_binary = "b" in mode
for c in mode
if c == "w"
if !(is_binary)
add(self._usings, "pylib::FileWriteString");
end
opts += ".write(true)"
end
if c == "r"
if !(is_binary)
add(self._usings, "pylib::FileReadString");
end
opts += ".read(true)"
end
if c == "a"
opts += ".append(true)"
end
if c == "+"
opts += ".read(true).write(true)"
end
end
node.result_type = true
return join("", [string(opts), ".open(", string(vargs[0]), ")"])
end
node.result_type = true
return join("", ["File::open(", string(vargs[0]), ")"])
end

function visit_named_temp_file{T0, T1}(self::JuliaTranspilerPlugins, node::T0, vargs::T1)::String
node.annotation = Name(ast, "tempfile._TemporaryFileWrapper")
node.result_type = true
return "NamedTempFile::new()"
end

function visit_textio_read{T0, T1, RT}(self::JuliaTranspilerPlugins, node::T0, vargs::T1)::RT
return nothing
end

function visit_textio_write{T0, T1, RT}(self::JuliaTranspilerPlugins, node::T0, vargs::T1)::RT
return nothing
end

function visit_ap_dataclass{T0, RT}(self::JuliaTranspilerPlugins, cls::T0)::RT
return cls
end

function visit_range{T0}(self::JuliaTranspilerPlugins, node::T0, vargs::Array{String})::String
start = 0
stop = 0
step = nothing
if length(vargs) == 1
stop = vargs[0 + 1]
else

start = vargs[0 + 1];
stop = vargs[1 + 1]
if length(node.args) == 3
step = vargs[2 + 1];
end
end
if isinstance(step, (int, float))&&step != 0||isinstance(step, tuple)&&step != ()||isinstance(step, list)&&step != []||step === nothing||isinstance(step, bool)&&step
return join("", [string(start), ":", string(step), ":", string(stop)])
end
return join("", [string(start), ":", string(stop)])
end

function visit_print{T0}(self::JuliaTranspilerPlugins, node::T0, vargs::Array{String})::String
args = join(", ", vargs)
return join("", ["println(join([", string(args), "], \" \"))"])
end

function visit_cast_int{T0, T1}(self::JuliaTranspilerPlugins, node::T0, vargs::T1)::String
if !(vargs)
return "0"
end
arg_type = _typename_from_annotation(self, node.args[0])
if isinstance(arg_type !== nothing&&startswith(arg_type, "Float"), (int, float))&&arg_type !== nothing&&startswith(arg_type, "Float") != 0||isinstance(arg_type !== nothing&&startswith(arg_type, "Float"), tuple)&&arg_type !== nothing&&startswith(arg_type, "Float") != ()||isinstance(arg_type !== nothing&&startswith(arg_type, "Float"), list)&&arg_type !== nothing&&startswith(arg_type, "Float") != []||arg_type !== nothing&&startswith(arg_type, "Float") === nothing||isinstance(arg_type !== nothing&&startswith(arg_type, "Float"), bool)&&arg_type !== nothing&&startswith(arg_type, "Float")
return join("", ["Int64(floor(", string(vargs[0]), "))"])
end
return join("", ["Int64(", string(vargs[0]), ")"])
end

function visit_asyncio_run{T0, T1}(node::T0, vargs::T1)::String
return join("", ["block_on(", string(vargs[0]), ")"])
end

SMALL_DISPATCH_MAP = Dict("str" => (n, vargs) -> vargs ? (join("", ["string(", string(vargs[0]), ")"])) : ("\"\""), "len" => (n, vargs) -> join("", ["length(", string(vargs[0]), ")"]), "enumerate" => (n, vargs) -> join("", [string(vargs[0]), ".iter().enumerate()"]), "sum" => (n, vargs) -> join("", [string(vargs[0]), ".iter().sum()"]), "bool" => (n, vargs) -> vargs ? (join("", ["Bool(", string(vargs[0]), ")"])) : ("false"), "floor" => (n, vargs) -> join("", ["Int64(floor(", string(vargs[0]), "))"]))
SMALL_USINGS_MAP = Dict("asyncio.run" => "futures::executor::block_on")
DISPATCH_MAP = Dict("range" => JuliaTranspilerPlugins::visit_range, "xrange" => JuliaTranspilerPlugins::visit_range, "print" => JuliaTranspilerPlugins::visit_print, "int" => JuliaTranspilerPlugins::visit_cast_int)
MODULE_DISPATCH_TABLE::Dict{String, String} = Dict()
DECORATOR_DISPATCH_TABLE = Dict(ap_dataclass => JuliaTranspilerPlugins::visit_ap_dataclass)
CLASS_DISPATCH_TABLE = Dict(ap_dataclass => JuliaTranspilerPlugins::visit_argparse_dataclass)
ATTR_DISPATCH_TABLE = Dict("temp_file.name" => (self, node, value, attr) -> join("", [string(value), ".path()"]))
FuncType = Union[(Callable, str)]
FUNC_DISPATCH_TABLE::Dict{FuncType, {['Callable', 'Bool']}} = Dict("parse_args" => ((self, node, vargs) -> "::from_args()", false), "f.read" => ((self, node, vargs) -> "f.read_string()", true), "f.write" => ((self, node, vargs) -> join("", ["f.write_string(", string(vargs[0]), ")"]), true), "f.close" => ((self, node, vargs) -> "drop(f)", false), open => (JuliaTranspilerPlugins::visit_open, true), NamedTemporaryFile => (JuliaTranspilerPlugins::visit_named_temp_file, true), io.TextIOWrapper.read => (JuliaTranspilerPlugins::visit_textio_read, true), io.TextIOWrapper.read => (JuliaTranspilerPlugins::visit_textio_write, true), os.unlink => ((self, node, vargs) -> join("", ["std::fs::remove_file(", string(vargs[0]), ")"]), true), sys.exit => ((self, node, vargs) -> join("", ["quit(", string(vargs[0]), ")"]), true))
