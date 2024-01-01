function fib(i::Int64)::Int64
    if isinstance(i == 0 || i == 1, (int, float)) && i == 0 ||
       i == 1 != 0 ||
       isinstance(i == 0 || i == 1, tuple) && i == 0 ||
       i == 1 != () ||
       isinstance(i == 0 || i == 1, list) && i == 0 ||
       i == 1 != [] ||
       i == 0 ||
       i == 1 === nothing ||
       isinstance(i == 0 || i == 1, bool) && i == 0 ||
       i == 1
        return 1
    end
    return fib(i - 1) + fib(i - 2)
end

function main()
    println(join([fib(5)], " "))
end

main()
