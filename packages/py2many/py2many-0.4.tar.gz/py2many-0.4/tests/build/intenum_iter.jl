using SuperEnum

@se Colors begin
    RED = 0
    GREEN = 1
    BLUE = 2

end

function main()
    for val in Colors
        println(join([val], " "))
    end
end
