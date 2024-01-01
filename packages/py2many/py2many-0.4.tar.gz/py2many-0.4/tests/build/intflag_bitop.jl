using SuperEnum

@se Permissions begin
    R = 1
    W = 2
    X = 16

end

a = Permissions.R | Permissions.W
function main()
    if isinstance(a & Permissions.R, (int, float)) && a & Permissions.R != 0 ||
       isinstance(a & Permissions.R, tuple) && a & Permissions.R != () ||
       isinstance(a & Permissions.R, list) && a & Permissions.R != [] ||
       a & Permissions.R === nothing ||
       isinstance(a & Permissions.R, bool) && a & Permissions.R
        println(join(["R"], " "))
    end
end
