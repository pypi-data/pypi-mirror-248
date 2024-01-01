


T = TypeVar("T")
E = TypeVar("E", Exception, IntEnum)
struct Ok
    value::T
end


struct Err
    error::E
end


Result = Union[(Ok[T], Err[E])]
