import math
import cairo

class Viz:
    def __init__(self, hot = {}):
        self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 1280, 720)
        self.ctx = cairo.Context(self.surface)
        self.hot = hot

    def rect(self, x, y, w, h):
        ctx = self.ctx

        ctx.move_to(x, y)
        ctx.line_to(x + w, y)
        ctx.line_to(x + w, y + h)
        ctx.line_to(x, y + h)
        ctx.close_path()

    def xy(self, r, c):
        return (60 + c * 65, 600 - r * 80)

    def center(self, r, c):
        return (60 + c * 65 + (55.0 / 2), 600 - r * 80 + (70.0 / 2))

    def cell(self, r, c, label, a = 0.5):
        (x, y) = self.xy(r, c)
        ctx = self.ctx

        (w, h) = (55, 70)

        self.rect(x, y, w, h)
        ctx.fill()

        ctx.save()
        ctx.set_line_width(4)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        self.rect(x, y, w, h)
        ctx.stroke()
        ctx.set_source_rgba(1, 1, 1, 0.1)
        self.rect(x, y, w, h)
        ctx.stroke()
        ctx.restore()

        self.label(r, c, label, a)

    def label(self, r, c, label, a = 0.1):
        (x, y) = self.xy(r, c)
        ctx = self.ctx
        (w, h) = (55, 70)

        ctx.save()
        (_, _, tw, th, _, _) = ctx.text_extents(label)
        ctx.set_source_rgba(1, 1, 1, a)
        ctx.move_to(x + ((w - tw) / 2), y + ((h + th) / 2))
        ctx.show_text(label)
        ctx.restore()

    def render_recite(self, r, c, label, src, dst):
        self.render_wire(r, c, label, src, dst, 16)

    def render_wire(self, r, c, label, src, dst, width = 6):
        ctx = self.ctx
        (x, y) = self.xy(r, c)
        (w, h) = (55, 70)

        def local(dx, dy):
            return (x + dx * w, y + dy * h)
        (nx,ny) = local(.5, -.1)
        (wx,wy) = local(-.1, .5)
        (ex,ey) = local(1.1, .5)
        (sx,sy) = local(.5, 1.1)
        (cx,cy) = local(.5, .5)

        at = {
            'NORTH' : (nx,ny),
            'SOUTH' : (sx,sy),
            'EAST' : (ex,ey),
            'WEST' : (wx,wy)}

        ctx.save()
        # ctx.set_source_rgb(.8, .3, .1)
        ctx.set_source_rgb(.2, .3, .0)
        ctx.set_line_width(width)

        ctx.move_to(*at[src])
        ctx.curve_to(cx, cy, cx, cy, *at[dst])
        ctx.stroke()
        ctx.restore()

        self.label(r, c, label, 0.6)

    def render(self, pngfile):
        ctx = self.ctx

        ctx.select_font_face("helvetica")
        ctx.set_font_size(20)

        for r in range(8):
            for c in range(18):
                label = "%d%02d" % (r, c)
                if label in self.hot:
                    ra = self.hot[label].attr.get('render')
                    if ra:
                        getattr(self, "render_" + ra[0])(r, c, label, *ra[1:])
                    else:
                        ctx.set_source_rgb(0, .3, .1)
                        self.cell(r, c, label, 1.0)
                else:
                    ctx.set_source_rgb(0, .0, .1)
                    self.cell(r, c, label)

        if 0:
            ctx.set_source_rgba(1, 1, 0, 0.5)
            ctx.set_line_width(9)
            ctx.move_to(*self.center(*self.path[0]))
            for p in self.path:
                ctx.line_to(*self.center(*p))
            ctx.stroke()
        self.surface.write_to_png(pngfile)

if __name__ == '__main__':
    g = Viz()
    path = ['SOUTH', 'SOUTH', 'SOUTH', 'SOUTH', 'SOUTH', 'SOUTH', 'SOUTH', 'WEST']
    path = ['SOUTH', 'SOUTH', 'EAST', 'SOUTH', 'WEST', 'SOUTH', 'SOUTH', 'SOUTH', 'SOUTH', 'WEST']
    s6w = ['SOUTH'] * 6 + ['WEST']
    n6w = ['NORTH'] * 6 + ['WEST']
    path = (['EAST'] * 9 + ['SOUTH'] + (s6w + n6w) * 8 +
        s6w + ['NORTH'] * 7 + ['EAST'] * 7
    )
    (r, c) = (7, 8)
    pa = [(r+1,c), (r,c)]
    print path
    for d in path:
        if d == 'EAST':
            c += 1
        elif d == 'WEST':
            c -= 1
        elif d == 'NORTH':
            r += 1
        elif d == 'SOUTH':
            r -= 1
        pa.append((r,c))
    print pa
    g.path = pa
    g.render("out.png")
