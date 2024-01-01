struct A

end

B = "FOO"
function main()
    @assert(A::B == "FOO")
end
