fun main(argv: Array<String>) {
val (foo, (baz, qux)) = Pair(4, (5, 6))
assert(foo != baz != qux)}


