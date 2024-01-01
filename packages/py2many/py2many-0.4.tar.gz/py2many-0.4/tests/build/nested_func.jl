function foo()::Int64
    function bar()::Int64
        return 1
    end

    return bar()
end

function main()
    foo()
end
