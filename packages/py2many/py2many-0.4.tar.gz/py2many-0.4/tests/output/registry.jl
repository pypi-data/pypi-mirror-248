
import pathlib
using unittest::mock:Mock
using language: LanguageSettings
using python_transformer: PythonTranspiler, RestoreMainRewriter
using rewriters: InferredAnnAssignRewriter
CI = get(os.environ, "CI", "0")
if CI in ["1", "true"]
    using pycpp: settings
    using pydart: settings
    using pygo: settings
    using pyjl: settings
    using pykt: settings
    using pynim: settings
    using pyrs: settings
    using pysmt: settings
    using pyv: settings
else

    try
        using pycpp: settings
        using pydart: settings
        using pygo: settings
        using pyjl: settings
        using pykt: settings
        using pynim: settings
        using pyrs: settings
        using pysmt: settings
        using pyv: settings
    catch exn
        if exn isa ImportError
            using pycpp: settings
            using pydart: settings
            using pygo: settings
            using pyjl: settings
            using pykt: settings
            using pynim: settings
            using pyrs: settings
            using pysmt: settings
            using pyv: settings
        end
    end
end
PY2MANY_DIR = Path(pathlib, __file__).parent
ROOT_DIR = PY2MANY_DIR.parent
FAKE_ARGS = Mock(4)
function python_settings{T0,T1}(args::T0, env::T1)::LanguageSettings
    return LanguageSettings(
        PythonTranspiler(),
        ".py",
        "Python",
        ["black"],
        [RestoreMainRewriter()],
        [InferredAnnAssignRewriter()],
    )
end

ALL_SETTINGS = Dict(
    "python" => python_settings,
    "cpp" => cpp_settings,
    "rust" => rust_settings,
    "julia" => julia_settings,
    "kotlin" => kotlin_settings,
    "nim" => nim_settings,
    "dart" => dart_settings,
    "go" => go_settings,
    "vlang" => vlang_settings,
    "smt" => smt_settings,
)
function _get_all_settings{T0,T1,RT}(args::T0, env::T1)::RT
    return dict(((key, func(args, env)) for (key, func) in ALL_SETTINGS.items()))
end
