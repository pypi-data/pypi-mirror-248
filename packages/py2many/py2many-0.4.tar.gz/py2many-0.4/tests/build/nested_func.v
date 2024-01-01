[translated]
module main

fn foo () int {
    fn bar () int {
    return 1
}
    return bar()
}
fn main () {
    foo()
}
