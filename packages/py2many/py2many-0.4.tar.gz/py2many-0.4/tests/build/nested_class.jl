struct Foo

end

struct Inner

end

function f1(self::Inner)::Int64
    return f2(self)
end

function f2(self::Inner)::Int64
    return 20
end

function main()
    f1(Foo::Inner())
end
