

function comb_sort(seq::Array{Int64})::Array{Int64}
    gap = length(seq)
    swap = true
    while isinstance(gap > 1 || swap, (int, float)) && gap > 1 ||
              swap != 0 ||
              isinstance(gap > 1 || swap, tuple) && gap > 1 ||
              swap != () ||
              isinstance(gap > 1 || swap, list) && gap > 1 ||
              swap != [] ||
              gap > 1 ||
              swap === nothing ||
              isinstance(gap > 1 || swap, bool) && gap > 1 ||
              swap
        gap = max(1, Int64(floor(gap / 1.25)))
        swap = false
        for i = 0:length(seq)-gap-1
            if seq[i+1] > seq[i+gap+1]
                seq[i+1], seq[i+gap+1] = (seq[i+gap+1], seq[i+1])
                swap = true
            end
        end
    end
    return seq
end

function main()
    unsorted = [14, 11, 19, 5, 16, 10, 19, 12, 5, 12]
    expected = [5, 5, 10, 11, 12, 12, 14, 16, 19, 19]
    @assert(comb_sort(unsorted) == expected)
    println(join(["OK"], " "))
end

main()
