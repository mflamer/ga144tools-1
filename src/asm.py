import sys
from ga144 import GA144

prg708 = r"""
    @p b! @p @p
    0x15d
    0x80
    63
    push a!
\ : dump
\     @+ call emit18
\     next dump

\    @p a!
\    -d--
\    @ call emit18

    @p a!
        SOUTH
    @p push
        25
: dump
    @
    call emit18
    drop next dump

    @p call emit18
    0x00947

: again
    jump again

: emit18 ( x -- x)
    @p call emit
    0xa5
    drop call emit
    call emit
: emit
    @p call bit
    0
    @p push
    7
: bloop
    dup call bit
    2/ next bloop

    call bit1
: bit1
    @p
    1
: bit
    @p and @p @p
    1
    3
    3460
    push or !b
    unext ;
"""

prg608 = r"""
    @p a! @p
        SOUTH
        NORTH
    b!
: again
    @ 2* !b
    jump again
"""

prg508 = prg608
prg408 = prg608
prg308 = prg608
prg208 = prg608
prg108 = prg608

prg008 = r"""
    @p a! @p @p
        NORTH
        1
        1
    @p b!
        io
\ : ok
\     @p
\         2
\     !b @p
\         3
\     !b jump ok
    jump fwd
: again
    over over . +
: fwd
    dup !
    jump again
"""

prg007 = r"""
    @p a! @p
        EAST
        0
: loop
    - dup !
    jump loop
"""

prg007 = r"""
    @p b!
        0x141
: ok
    @p
        0x3ffff
    !b @p
        0
    !b jump ok
"""

xprg008 = r"""
    @p a!
        WEST
    @p b!
        NORTH
: loop
    @ !b
    jump loop
"""

if __name__ == '__main__':
    g = GA144()
    if 0:
        g.node['708'].load(prg708)
        g.node['608'].load(prg608)
        g.node['508'].load(prg508)
        g.node['408'].load(prg408)
        g.node['308'].load(prg308)
        g.node['208'].load(prg208)
        g.node['108'].load(prg108)
        g.node['008'].load(prg008)
        g.node['007'].load(prg007)
        g.node['009'].load(prg007)
    else:
        code = {}
        c = []
        for l in open(sys.argv[2]):
            if l[0] == '-':
                n = l.split()[1]
                c = []
                code[n] = c
            else:
                c.append(l)
        for n,c in sorted(code.items()):
            g.node[n].load("".join(c))
    g.download(sys.argv[1], 460800)
