[translated]
module main

pub struct Foo {

}

pub struct Inner {

}

fn (self Inner) f1 () int {
    return self.f2()
}
fn (self Inner) f2 () int {
    return 20
}
fn main () {
    Foo.Inner().f1()
}
