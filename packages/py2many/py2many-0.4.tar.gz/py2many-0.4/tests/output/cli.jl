using pylib::FileWriteString
using std::fs::File
using std::fs::OpenOptions
import argparse
import ast


import tempfile
using functools: lru_cache
using pathlib: Path
using subprocess: run

using analysis: add_imports
using annotation_transformer: add_annotation_flags
using context: add_assignment_context, add_variable_context, add_list_calls
using exceptions: AstErrorBase
using inference: infer_types, infer_types_typpete
using language: LanguageSettings
using mutability_transformer: detect_mutable_vars
using nesting_transformer: detect_nesting_levels
using registry: _get_all_settings, ALL_SETTINGS, FAKE_ARGS
using scope: add_scope_context
using toposort_modules: toposort
using py2many::rewriters: ComplexDestructuringRewriter, FStringJoinRewriter, LoopElseRewriter, PythonMainRewriter, DocStringToCommentRewriter, PrintBoolRewriter, StrStrRewriter, WithToBlockTransformer, IgnoredAssignRewriter, UnpackScopeRewriter
PY2MANY_DIR = Path(__file__).parent
ROOT_DIR = PY2MANY_DIR.parent
STDIN = "-"
STDOUT = "-"
CWD = cwd(Path)
function core_transformers{T0, T1, T2, RT}(tree::T0, trees::T1, args::T2)::RT
add_variable_context(tree, trees);
add_scope_context(tree);
add_assignment_context(tree);
add_list_calls(tree);
detect_mutable_vars(tree);
detect_nesting_levels(tree);
add_annotation_flags(tree);
infer_meta = args&&args.typpete ? (infer_types_typpete(tree)) : (infer_types(tree))
add_imports(tree);
return (tree, infer_meta)
end

function _transpile{T0, RT}(filenames::Array{Path}, sources::Array{String}, settings::LanguageSettings, args::Nothing{argparse.Namespace}, _suppress_exceptions::T0)::RT
transpiler = settings.transpiler
rewriters = settings.rewriters
transformers = settings.transformers
post_rewriters = settings.post_rewriters
tree_list = []
for (filename, source) in zip(filenames, sources)
tree = parse(ast, source)
tree.__file__ = filename
push!(tree_list, tree);
end
trees = toposort(convert(, tree_list))
topo_filenames = [t.__file__ for t in trees]
language = transpiler.NAME
generic_rewriters = [ComplexDestructuringRewriter(language), PythonMainRewriter(settings.transpiler._main_signature_arg_names), FStringJoinRewriter(language), DocStringToCommentRewriter(language), WithToBlockTransformer(language), IgnoredAssignRewriter(language)]
generic_post_rewriters = [PrintBoolRewriter(language), StrStrRewriter(language), UnpackScopeRewriter(language)]
if settings.ext != ".py"
push!(generic_post_rewriters, LoopElseRewriter(language));
end
rewriters = generic_rewriters + rewriters;
post_rewriters = generic_post_rewriters + post_rewriters;
outputs = Dict()
successful = []
for (filename, tree) in zip(topo_filenames, trees)
try
output = _transpile_one(convert(, trees), tree, transpiler, rewriters, transformers, post_rewriters, convert(, args))
push!(successful, filename);
outputs[filename] = output
catch exn
 let e = exn
if e isa Exception
import traceback
formatted_lines = splitlines(traceback.format_exc())
if isinstance(isinstance(e, AstErrorBase), (int, float))&&isinstance(e, AstErrorBase) != 0||isinstance(isinstance(e, AstErrorBase), tuple)&&isinstance(e, AstErrorBase) != ()||isinstance(isinstance(e, AstErrorBase), list)&&isinstance(e, AstErrorBase) != []||isinstance(e, AstErrorBase) === nothing||isinstance(isinstance(e, AstErrorBase), bool)&&isinstance(e, AstErrorBase)
println(join(["".join([string(filename), ":", string(e.lineno), ":", string(e.col_offset), ": ", string(formatted_lines[-1])])], " "));
else

println(join(["".join([string(filename), ": ", string(formatted_lines[-1])])], " "));
end
if isinstance(!(_suppress_exceptions)||!(isinstance(e, _suppress_exceptions)), (int, float))&&!(_suppress_exceptions)||!(isinstance(e, _suppress_exceptions)) != 0||isinstance(!(_suppress_exceptions)||!(isinstance(e, _suppress_exceptions)), tuple)&&!(_suppress_exceptions)||!(isinstance(e, _suppress_exceptions)) != ()||isinstance(!(_suppress_exceptions)||!(isinstance(e, _suppress_exceptions)), list)&&!(_suppress_exceptions)||!(isinstance(e, _suppress_exceptions)) != []||!(_suppress_exceptions)||!(isinstance(e, _suppress_exceptions)) === nothing||isinstance(!(_suppress_exceptions)||!(isinstance(e, _suppress_exceptions)), bool)&&!(_suppress_exceptions)||!(isinstance(e, _suppress_exceptions))
error()
end
outputs[filename] = "FAILED"
end
end
end
end
output_list = [outputs[f] for f in filenames]
return (output_list, successful)
end

function _transpile_one{T0, T1, T2, T3, T4, T5, T6, RT}(trees::T0, tree::T1, transpiler::T2, rewriters::T3, transformers::T4, post_rewriters::T5, args::T6)::RT
add_scope_context(tree);
for rewriter in rewriters
tree = visit(rewriter, tree);
end
tree, infer_meta = core_transformers(tree, trees, args)
for tx in transformers
tx(tree);
end
for rewriter in post_rewriters
tree = visit(rewriter, tree);
end
tree, infer_meta = core_transformers(tree, trees, args)
out = []
code = visit(transpiler, tree) + "\n"
headers = headers(transpiler, infer_meta)
features = features(transpiler)
if isinstance(features, (int, float))&&features != 0||isinstance(features, tuple)&&features != ()||isinstance(features, list)&&features != []||features === nothing||isinstance(features, bool)&&features
push!(out, features);
end
if isinstance(headers, (int, float))&&headers != 0||isinstance(headers, tuple)&&headers != ()||isinstance(headers, list)&&headers != []||headers === nothing||isinstance(headers, bool)&&headers
push!(out, headers);
end
usings = usings(transpiler)
if isinstance(usings, (int, float))&&usings != 0||isinstance(usings, tuple)&&usings != ()||isinstance(usings, list)&&usings != []||usings === nothing||isinstance(usings, bool)&&usings
push!(out, usings);
end
push!(out, code);
if isinstance(transpiler.extension, (int, float))&&transpiler.extension != 0||isinstance(transpiler.extension, tuple)&&transpiler.extension != ()||isinstance(transpiler.extension, list)&&transpiler.extension != []||transpiler.extension === nothing||isinstance(transpiler.extension, bool)&&transpiler.extension
push!(out, transpiler.extension_module(tree));
end
return join("\n", out)
end

function _process_one_data{T0, T1, T2, RT}(source_data::T0, filename::T1, settings::T2)::RT
return _transpile(convert(Array{Path}, [filename]), convert(Array{String}, [source_data]), settings)[0][0]
end

function _create_cmd{T0, T1, RT}(parts::T0, filename::T1)::RT
cmd = [format(arg, filename, kw) for arg in parts]
if cmd != parts
return cmd
end
return [starred!(parts)/*unsupported*/, string(filename)]
end

function _relative_to_cwd{T0, RT}(absolute_path::T0)::RT
return Path(os.path.relpath(absolute_path, CWD))
end

function _get_output_path{T0, T1, T2, RT}(filename::T0, ext::T1, outdir::T2)::RT
if filename.name == STDIN
return Path(STDOUT)
end
directory = outdir / filename.parent
if !(is_dir(directory))
mkdir(directory, true);
end
output_path = directory / (filename.stem + ext)
if isinstance(ext == ".kt"&&is_absolute(output_path), (int, float))&&ext == ".kt"&&is_absolute(output_path) != 0||isinstance(ext == ".kt"&&is_absolute(output_path), tuple)&&ext == ".kt"&&is_absolute(output_path) != ()||isinstance(ext == ".kt"&&is_absolute(output_path), list)&&ext == ".kt"&&is_absolute(output_path) != []||ext == ".kt"&&is_absolute(output_path) === nothing||isinstance(ext == ".kt"&&is_absolute(output_path), bool)&&ext == ".kt"&&is_absolute(output_path)
output_path = _relative_to_cwd(output_path);
end
return output_path
end

function _process_one{T0, T1}(settings::LanguageSettings, filename::Path, outdir::String, args::T0, env::T1)::Bool
suffix = args.suffix !== nothing ? (join("", [".", string(args.suffix)])) : (settings.ext)
output_path = _get_output_path(filename.relative_to(filename.parent), suffix, convert(, outdir))
if filename.name == STDIN
output = _process_one_data(sys.stdin.read(), Path("test.py"), convert(, settings))
tmp_name = nothing
try
if true
f = NamedTemporaryFile(tempfile, settings.ext, false)
tmp_name = f.name;
write(f, output.encode("utf-8"));
end
if isinstance(_format_one(convert(, settings), tmp_name, env), (int, float))&&_format_one(convert(, settings), tmp_name, env) != 0||isinstance(_format_one(convert(, settings), tmp_name, env), tuple)&&_format_one(convert(, settings), tmp_name, env) != ()||isinstance(_format_one(convert(, settings), tmp_name, env), list)&&_format_one(convert(, settings), tmp_name, env) != []||_format_one(convert(, settings), tmp_name, env) === nothing||isinstance(_format_one(convert(, settings), tmp_name, env), bool)&&_format_one(convert(, settings), tmp_name, env)
write(sys.stdout, File::open(tmp_name).read());
else

write(sys.stderr, "Formatting failed");
end
finally
if tmp_name !== nothing
remove(os, tmp_name);
end
end
return (Set([filename]), Set([filename]))
end
if isinstance(resolve(filename) == resolve(output_path)&&!(args.force), (int, float))&&resolve(filename) == resolve(output_path)&&!(args.force) != 0||isinstance(resolve(filename) == resolve(output_path)&&!(args.force), tuple)&&resolve(filename) == resolve(output_path)&&!(args.force) != ()||isinstance(resolve(filename) == resolve(output_path)&&!(args.force), list)&&resolve(filename) == resolve(output_path)&&!(args.force) != []||resolve(filename) == resolve(output_path)&&!(args.force) === nothing||isinstance(resolve(filename) == resolve(output_path)&&!(args.force), bool)&&resolve(filename) == resolve(output_path)&&!(args.force)
println(join(["".join(["Refusing to overwrite ", string(filename), ". Use --force to overwrite"])], " "));
return false
end
println(join(["".join([string(filename), " ... ", string(output_path)])], " "));
if true
f = File::open(filename)
source_data = read(f)
end
dunder_init = filename.stem == "__init__"
if isinstance(dunder_init&&!(source_data), (int, float))&&dunder_init&&!(source_data) != 0||isinstance(dunder_init&&!(source_data), tuple)&&dunder_init&&!(source_data) != ()||isinstance(dunder_init&&!(source_data), list)&&dunder_init&&!(source_data) != []||dunder_init&&!(source_data) === nothing||isinstance(dunder_init&&!(source_data), bool)&&dunder_init&&!(source_data)
println(join(["Detected empty __init__; skipping"], " "));
return true
end
result = _transpile([filename], convert(Array{String}, [source_data]), settings, args)
if true
f = OpenOptions::new().write(true).open(output_path)
write(f, result[0][0].encode("utf-8"));
end
if isinstance(settings.formatter, (int, float))&&settings.formatter != 0||isinstance(settings.formatter, tuple)&&settings.formatter != ()||isinstance(settings.formatter, list)&&settings.formatter != []||settings.formatter === nothing||isinstance(settings.formatter, bool)&&settings.formatter
return _format_one(convert(, settings), output_path, env)
end
return true
end

function _format_one{T0, T1, T2}(settings::T0, output_path::T1, env::T2)::Bool
try
restore_cwd = false
if isinstance(settings.ext == ".kt"&&output_path.parts[0] == "..", (int, float))&&settings.ext == ".kt"&&output_path.parts[0] == ".." != 0||isinstance(settings.ext == ".kt"&&output_path.parts[0] == "..", tuple)&&settings.ext == ".kt"&&output_path.parts[0] == ".." != ()||isinstance(settings.ext == ".kt"&&output_path.parts[0] == "..", list)&&settings.ext == ".kt"&&output_path.parts[0] == ".." != []||settings.ext == ".kt"&&output_path.parts[0] == ".." === nothing||isinstance(settings.ext == ".kt"&&output_path.parts[0] == "..", bool)&&settings.ext == ".kt"&&output_path.parts[0] == ".."
restore_cwd = CWD;
chdir(os, output_path.parent);
output_path = output_path.name;
end
cmd = _create_cmd(settings.formatter)
proc = run(cmd, env, true)
if isinstance(proc.returncode, (int, float))&&proc.returncode != 0||isinstance(proc.returncode, tuple)&&proc.returncode != ()||isinstance(proc.returncode, list)&&proc.returncode != []||proc.returncode === nothing||isinstance(proc.returncode, bool)&&proc.returncode
if settings.ext == ".jl"
if proc.stderr !== nothing
println(join(["".join([string(cmd), " (code: ", string(proc.returncode), "):\n", string(proc.stderr), string(proc.stdout)])], " "));
if b"ERROR: " in proc.stderr
return false
end
end
return true
end
println(join(["".join(["Error: ", string(cmd), " (code: ", string(proc.returncode), "):\n", string(proc.stderr), string(proc.stdout)])], " "));
if restore_cwd
chdir(os, restore_cwd);
end
return false
end
if settings.ext == ".kt"
if isinstance(run(cmd, env).returncode, (int, float))&&run(cmd, env).returncode != 0||isinstance(run(cmd, env).returncode, tuple)&&run(cmd, env).returncode != ()||isinstance(run(cmd, env).returncode, list)&&run(cmd, env).returncode != []||run(cmd, env).returncode === nothing||isinstance(run(cmd, env).returncode, bool)&&run(cmd, env).returncode
println(join(["".join(["Error: Could not reformat: ", string(cmd)])], " "));
if restore_cwd
chdir(os, restore_cwd);
end
return false
end
end
if restore_cwd
chdir(os, restore_cwd);
end
catch exn
 let e = exn
if e isa Exception
println(join(["".join(["Error: Could not format: ", string(output_path)])], " "));
println(join(["".join(["Due to: ", string(e.__class__.__name__), " ", string(e)])], " "));
return false
end
end
end
return true
end

FileSet = Set[Path]
function _process_many{T0, T1, T2, T3, T4, T5}(settings::T0, basedir::T1, filenames::T2, outdir::T3, env::T4, _suppress_exceptions::T5)::
set_continue_on_unimplemented(settings.transpiler);
source_data = []
for filename in filenames
if true
f = File::open(basedir / filename)
push!(source_data, f.read());
end
end
outputs, successful = _transpile(filenames, convert(Array{String}, source_data), settings)
output_paths = [_get_output_path(filename, settings.ext, outdir) for filename in filenames]
for (filename, output, output_path) in zip(filenames, outputs, output_paths)
if true
f = OpenOptions::new().write(true).open(output_path)
write(f, output);
end
end
successful = set(successful)
format_errors = set()
if isinstance(settings.formatter, (int, float))&&settings.formatter != 0||isinstance(settings.formatter, tuple)&&settings.formatter != ()||isinstance(settings.formatter, list)&&settings.formatter != []||settings.formatter === nothing||isinstance(settings.formatter, bool)&&settings.formatter
for (filename, output_path) in zip(filenames, output_paths)
if isinstance(filename in successful&&!(_format_one(settings, output_path, env)), (int, float))&&filename in successful&&!(_format_one(settings, output_path, env)) != 0||isinstance(filename in successful&&!(_format_one(settings, output_path, env)), tuple)&&filename in successful&&!(_format_one(settings, output_path, env)) != ()||isinstance(filename in successful&&!(_format_one(settings, output_path, env)), list)&&filename in successful&&!(_format_one(settings, output_path, env)) != []||filename in successful&&!(_format_one(settings, output_path, env)) === nothing||isinstance(filename in successful&&!(_format_one(settings, output_path, env)), bool)&&filename in successful&&!(_format_one(settings, output_path, env))
add(format_errors, Path(filename));
end
end
end
return (successful, format_errors)
end

function _process_dir{T0, T1, T2, T3, T4, T5, RT}(settings::T0, source::T1, outdir::T2, project::T3, env::T4, _suppress_exceptions::T5)::RT
println(join(["".join(["Transpiling whole directory to ", string(outdir), ":"])], " "));
if isinstance(settings.create_project !== nothing&&project, (int, float))&&settings.create_project !== nothing&&project != 0||isinstance(settings.create_project !== nothing&&project, tuple)&&settings.create_project !== nothing&&project != ()||isinstance(settings.create_project !== nothing&&project, list)&&settings.create_project !== nothing&&project != []||settings.create_project !== nothing&&project === nothing||isinstance(settings.create_project !== nothing&&project, bool)&&settings.create_project !== nothing&&project
cmd = settings.create_project + [join("", [string(outdir)])]
proc = run(cmd, env, true)
if isinstance(proc.returncode, (int, float))&&proc.returncode != 0||isinstance(proc.returncode, tuple)&&proc.returncode != ()||isinstance(proc.returncode, list)&&proc.returncode != []||proc.returncode === nothing||isinstance(proc.returncode, bool)&&proc.returncode
cmd_str = join(" ", cmd)
println(join(["".join(["Error: running ", string(cmd_str), ": ", string(proc.stderr)])], " "));
return (set(), set(), set())
end
if settings.project_subdir !== nothing
outdir = outdir / settings.project_subdir;
end
end
successful = []
failures = []
input_paths = []
for path in rglob(source, "*.py")
if path.suffix != ".py"
continue;
end
if path.parent.name == "__pycache__"
continue;
end
relative_path = relative_to(path, source)
target_path = outdir / relative_path
target_dir = target_path.parent
makedirs(os, target_dir, true);
push!(input_paths, relative_path);
end
successful, format_errors = _process_many(settings, source, convert(, input_paths), outdir)
failures = set(input_paths) - set(successful);
println(join(["\nFinished!"], " "));
println(join(["".join(["Successful: ", string(length(successful))])], " "));
if isinstance(format_errors, (int, float))&&format_errors != 0||isinstance(format_errors, tuple)&&format_errors != ()||isinstance(format_errors, list)&&format_errors != []||format_errors === nothing||isinstance(format_errors, bool)&&format_errors
println(join(["".join(["Failed to reformat: ", string(length(format_errors))])], " "));
end
println(join(["".join(["Failed to convert: ", string(length(failures))])], " "));
println(join([], " "));
return (successful, format_errors, failures)
end

function main{T0, T1}(args::T0, env::T1)::Int64
parser = ArgumentParser(argparse)
LANGS = _get_all_settings(FAKE_ARGS)
for (lang, settings) in items(LANGS)
add_argument(parser, "".join(["--", string(lang)]), bool, false, "".join(["Generate ", string(settings.display_name), " code"]));
end
add_argument(parser, "--outdir", nothing, "Output directory");
add_argument(parser, "-i", "--indent", int, nothing, "Indentation to use in languages that care");
add_argument(parser, "--comment-unsupported", false, "store_true", "Place unsupported constructs in comments");
add_argument(parser, "--extension", "store_true", false, "Build a python extension");
add_argument(parser, "--suffix", nothing, "Alternate suffix to use instead of the default one for the language");
add_argument(parser, "--no-prologue", "store_true", false, "");
add_argument(parser, "--force", "store_true", false, "When output and input are the same file, force overwriting");
add_argument(parser, "--typpete", "store_true", false, "Use typpete for inference");
add_argument(parser, "--project", true, "Create a project when using directory mode");
args, rest = parse_known_args(parser, args)
if isinstance(args.extension&&!(args.rust), (int, float))&&args.extension&&!(args.rust) != 0||isinstance(args.extension&&!(args.rust), tuple)&&args.extension&&!(args.rust) != ()||isinstance(args.extension&&!(args.rust), list)&&args.extension&&!(args.rust) != []||args.extension&&!(args.rust) === nothing||isinstance(args.extension&&!(args.rust), bool)&&args.extension&&!(args.rust)
println(join(["extension supported only with rust via pyo3"], " "));
return -1
end
settings_func = ALL_SETTINGS["cpp"]
for (lang, func) in items(ALL_SETTINGS)
arg = getattr(args, lang)
if isinstance(arg, (int, float))&&arg != 0||isinstance(arg, tuple)&&arg != ()||isinstance(arg, list)&&arg != []||arg === nothing||isinstance(arg, bool)&&arg
settings_func = func;
break;
end
end
settings = settings_func(args, env)
if isinstance(args.comment_unsupported, (int, float))&&args.comment_unsupported != 0||isinstance(args.comment_unsupported, tuple)&&args.comment_unsupported != ()||isinstance(args.comment_unsupported, list)&&args.comment_unsupported != []||args.comment_unsupported === nothing||isinstance(args.comment_unsupported, bool)&&args.comment_unsupported
println(join(["Wrapping unimplemented in comments"], " "));
settings.transpiler._throw_on_unimplemented = false
end
for filename in rest
source = Path(filename)
if args.outdir === nothing
outdir = source.parent
else

outdir = Path(args.outdir)
end
if isinstance(is_file(source)||source.name == STDIN, (int, float))&&is_file(source)||source.name == STDIN != 0||isinstance(is_file(source)||source.name == STDIN, tuple)&&is_file(source)||source.name == STDIN != ()||isinstance(is_file(source)||source.name == STDIN, list)&&is_file(source)||source.name == STDIN != []||is_file(source)||source.name == STDIN === nothing||isinstance(is_file(source)||source.name == STDIN, bool)&&is_file(source)||source.name == STDIN
println(join(["".join(["Writing to: ", string(outdir)]), sys.stderr], " "));
try
rv = _process_one(settings, source, outdir, args, env)
catch exn
 let e = exn
if e isa Exception
import traceback
formatted_lines = splitlines(traceback.format_exc())
if isinstance(isinstance(e, AstErrorBase), (int, float))&&isinstance(e, AstErrorBase) != 0||isinstance(isinstance(e, AstErrorBase), tuple)&&isinstance(e, AstErrorBase) != ()||isinstance(isinstance(e, AstErrorBase), list)&&isinstance(e, AstErrorBase) != []||isinstance(e, AstErrorBase) === nothing||isinstance(isinstance(e, AstErrorBase), bool)&&isinstance(e, AstErrorBase)
println(join(["".join([string(source), ":", string(e.lineno), ":", string(e.col_offset), ": ", string(formatted_lines[-1])]), sys.stderr], " "));
else

println(join(["".join([string(source), ": ", string(formatted_lines[-1])]), sys.stderr], " "));
end
rv = false
end
end
end
else

if args.outdir === nothing
outdir = source.parent / join("", [string(source.name), "-py2many"])
end
successful, format_errors, failures = _process_dir(settings, source, outdir, args.project)
rv = !(failures||format_errors)
end
rv = rv === true ? (0) : (1)
return rv
end
end

