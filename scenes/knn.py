from manim import *
import numpy as np

BG = "#1C1C1C"
GREEN = "#83C167"   # paid back
RED = "#FC6255"     # didn't pay back
ACCENT = "#FFFF00"
BLUE = "#58C4DD"
MONO = "DejaVu Sans Mono"

# loan dataset in (income, wealth) feature space, axes 0..5
GREENS = [(2.0, 3.0), (2.6, 3.6), (4.2, 4.4)]   # Alice, G2, Eve
REDS = [(3.4, 1.2), (1.2, 0.8)]                 # Bob, Max
QUERY = (2.4, 2.6)
QUERY2 = (3.2, 1.6)


def make_axes():
    ax = Axes(
        x_range=[0, 5, 1], y_range=[0, 5, 1], x_length=7.2, y_length=4.4,
        axis_config={"stroke_opacity": 0.15, "include_ticks": False},
    ).shift(DOWN * 0.35)
    xl = Text("income", font_size=18, color=WHITE, opacity=0.4, font=MONO
              ).next_to(ax.x_axis, RIGHT, buff=0.15)
    yl = Text("wealth", font_size=18, color=WHITE, opacity=0.4, font=MONO
              ).next_to(ax.y_axis, UP, buff=0.15)
    return ax, xl, yl


def dots_for(ax):
    g = VGroup(*[Dot(ax.c2p(x, y), color=GREEN, radius=0.09) for x, y in GREENS])
    r = VGroup(*[Dot(ax.c2p(x, y), color=RED, radius=0.09) for x, y in REDS])
    return g, r


def title_block(title, sub):
    t = Text(title, font_size=40, color=BLUE, weight=BOLD, font=MONO
             ).to_edge(UP, buff=0.55)
    s = Text(sub, font_size=19, color=WHITE, opacity=0.5, font=MONO
             ).next_to(t, DOWN, buff=0.22)
    return t, s


class Scene1_Title(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("K-Nearest Neighbors", "how a bank decides on Joan")
        self.play(Write(t), run_time=1.3)
        self.play(FadeIn(s, shift=DOWN * 0.2), run_time=0.7)
        self.wait(1.0)
        core = Text("similar data -> similar outcomes", font_size=30,
                    color=ACCENT, weight=BOLD, font=MONO)
        self.play(FadeOut(s), Write(core), run_time=1.4)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Scene2_Data(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The loan data", "green = paid back   red = defaulted")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax, xl, yl = make_axes()
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.9)
        g, r = dots_for(ax)
        labels = VGroup(
            Text("Alice", font_size=16, color=GREEN, font=MONO).move_to(ax.c2p(2.0, 3.0) + UP * 0.28 + LEFT * 0.35),
            Text("Eve", font_size=16, color=GREEN, font=MONO).move_to(ax.c2p(4.2, 4.4) + UP * 0.28),
            Text("Bob", font_size=16, color=RED, font=MONO).move_to(ax.c2p(3.4, 1.2) + DOWN * 0.32),
            Text("Max", font_size=16, color=RED, font=MONO).move_to(ax.c2p(1.2, 0.8) + DOWN * 0.32),
        )
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in g], run_time=1.0),
                  LaggedStart(*[FadeIn(d, scale=0.5) for d in r], run_time=1.0))
        self.play(FadeIn(labels), run_time=0.6)
        self.wait(0.8)
        q = Text("?", font_size=34, color=ACCENT, weight=BOLD, font=MONO
                 ).move_to(ax.c2p(*QUERY))
        ring = Circle(radius=0.22, color=ACCENT, stroke_width=2.5
                      ).move_to(ax.c2p(*QUERY))
        self.play(FadeIn(ring, scale=2), Write(q), run_time=0.9)
        ask = Text("Joan. will she pay it back?", font_size=24, color=WHITE,
                   font=MONO).to_edge(DOWN, buff=0.5)
        self.play(Write(ask), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Scene3_K1(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("K = 1", "ask the single closest customer")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax, xl, yl = make_axes()
        g, r = dots_for(ax)
        ax.add(xl, yl)
        self.add(ax, g, r)
        q = Text("?", font_size=34, color=ACCENT, weight=BOLD, font=MONO
                 ).move_to(ax.c2p(*QUERY))
        self.add(q)
        line = Line(ax.c2p(*QUERY), ax.c2p(*GREENS[0]), color=ACCENT,
                    stroke_width=3)
        self.play(Create(line), run_time=1.0)
        near = Text("nearest: Alice (paid)", font_size=22, color=GREEN,
                    font=MONO).next_to(line.get_start() + (UP + RIGHT) * 0.5, RIGHT)
        self.play(Write(near), run_time=0.8)
        self.wait(0.8)
        verdict = Text("predict: PAID BACK", font_size=30, color=GREEN,
                       weight=BOLD, font=MONO).to_edge(DOWN, buff=0.5)
        self.play(Write(verdict), run_time=1.0)
        self.wait(1.2)
        warn = Text("...but one neighbor is fragile", font_size=20,
                    color=WHITE, opacity=0.6, font=MONO).next_to(verdict, UP, buff=0.3)
        self.play(FadeIn(warn), run_time=0.7)
        self.wait(1.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Scene4_K3(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("K = 3", "let the three closest neighbors vote")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax, xl, yl = make_axes()
        g, r = dots_for(ax)
        ax.add(xl, yl)
        self.add(ax, g, r)
        q = Text("?", font_size=34, color=ACCENT, weight=BOLD, font=MONO
                 ).move_to(ax.c2p(*QUERY))
        self.add(q)
        # three nearest: Alice (2.0,3.0), G2 (2.6,3.6), Bob (3.4,1.2)
        nbrs = [GREENS[0], GREENS[1], REDS[0]]
        lines = VGroup(*[Line(ax.c2p(*QUERY), ax.c2p(*n), color=BLUE,
                              stroke_width=2.5, stroke_opacity=0.8) for n in nbrs])
        circ = Circle(radius=float(np.linalg.norm(np.array(QUERY) - np.array(REDS[0])) * 1.02),
                      color=BLUE, stroke_width=1.5, stroke_opacity=0.4
                      ).move_to(ax.c2p(*QUERY))
        self.play(Create(circ), run_time=1.0)
        self.play(LaggedStart(*[Create(l) for l in lines], run_time=1.2))
        votes = Text("GREEN  GREEN  RED", font_size=26, font=MONO
                     ).to_edge(DOWN, buff=0.85)
        votes[0:5].set_color(GREEN)
        votes[6:11].set_color(GREEN)
        votes[13:16].set_color(RED)
        self.play(Write(votes), run_time=1.0)
        verdict = Text("majority vote -> PAID BACK", font_size=28,
                       color=GREEN, weight=BOLD, font=MONO
                       ).next_to(votes, DOWN, buff=0.3)
        self.play(Write(verdict), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Scene5_Weighted(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Weighted KNN", "closer neighbors get louder votes")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax, xl, yl = make_axes()
        g, r = dots_for(ax)
        ax.add(xl, yl)
        self.add(ax, g, r)
        q = Text("?", font_size=34, color=ACCENT, weight=BOLD, font=MONO
                 ).move_to(ax.c2p(*QUERY2))
        self.add(q)
        # neighbors of QUERY2: Bob (3.4,1.2) d=0.45, Alice d=1.84, G2 d=2.09
        nbrs = [(REDS[0], "2.2", RED, DOWN * 0.34 + RIGHT * 0.15),
                (GREENS[0], "0.5", GREEN, UP * 0.3 + LEFT * 0.55),
                (GREENS[1], "0.5", GREEN, UP * 0.3 + RIGHT * 0.15)]
        for (pt, w, col, off) in nbrs:
            line = Line(ax.c2p(*QUERY2), ax.c2p(*pt), color=col, stroke_width=3)
            tag = Text(f"w = {w}", font_size=18, color=col, font=MONO
                       ).move_to(ax.c2p(*pt) + off)
            self.play(Create(line), FadeIn(tag), run_time=0.8)
        self.wait(0.6)
        b1 = Text("standard vote:  green 2 - 1 red  ->  GREEN", font_size=21,
                  color=GREEN, font=MONO)
        b2 = Text("weighted vote:  red 2.2 - 1.0 green  ->  RED", font_size=21,
                  color=RED, font=MONO)
        bottom = VGroup(b1, b2).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.45)
        self.play(Write(b1), run_time=0.9)
        self.play(Write(b2), run_time=0.9)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Scene6_Boundaries(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Choosing K", "the decision boundary tells you everything")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        # training cloud for the panels
        pts = [(1.2, 3.4), (1.8, 2.6), (2.4, 3.8), (1.6, 1.4), (2.8, 2.2),
               (3.6, 3.2), (4.2, 4.0), (3.8, 1.8), (4.4, 2.6), (3.2, 4.2)]
        lab = [1, 1, 1, 0, 1, 0, 0, 0, 0, 1]  # 1 green, 0 red
        pts = np.array(pts)

        def classify(x, y, k):
            d = np.sqrt(((pts - np.array([x, y])) ** 2).sum(axis=1))
            idx = np.argsort(d)[:k]
            return 1 if sum(lab[i] for i in idx) * 2 > k else 0

        def panel(k, x0, name, note, col):
            gw, gh, cell = 4.0, 3.0, 0.2
            cells = VGroup()
            for i in range(int(gw / cell)):
                for j in range(int(gh / cell)):
                    x = i * cell + cell / 2
                    y = j * cell + cell / 2
                    c = GREEN if classify(x, y, k) else RED
                    sq = Rectangle(width=cell, height=cell,
                                   fill_color=c, fill_opacity=0.35,
                                   stroke_width=0).move_to(
                        np.array([x0 + x - gw / 2, y - gh / 2 - 0.15, 0]))
                    cells.add(sq)
            dots = VGroup(*[Dot(np.array([x0 + px - gw / 2, py - gh / 2 - 0.15, 0]),
                                color=(GREEN if l else RED), radius=0.05)
                            for (px, py), l in zip(pts, lab)])
            head = Text(name, font_size=24, color=col, weight=BOLD, font=MONO
                        ).move_to(np.array([x0, 1.55, 0]))
            foot = Text(note, font_size=16, color=WHITE, opacity=0.55, font=MONO
                        ).move_to(np.array([x0, -2.15, 0]))
            return VGroup(cells, dots, head, foot)

        p1 = panel(1, -3.6, "K = 1", "jagged -> memorizes noise (overfit)", RED)
        p2 = panel(10, 3.6, "K = 10 (everyone)", "flat -> ignores structure (underfit)", RED)
        self.play(LaggedStart(*[FadeIn(sq) for sq in p1[0]], lag_ratio=0.004,
                              run_time=1.6),
                  FadeIn(p1[1]), Write(p1[2]))
        self.wait(0.6)
        self.play(LaggedStart(*[FadeIn(sq) for sq in p2[0]], lag_ratio=0.004,
                              run_time=1.6),
                  FadeIn(p2[1]), Write(p2[2]))
        self.wait(0.8)
        tip = Text("try many K, graph the error, pick the dip", font_size=22,
                   color=ACCENT, font=MONO).to_edge(DOWN, buff=0.45)
        self.play(Write(p1[3]), Write(p2[3]), run_time=0.8)
        self.play(Write(tip), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Scene7_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, _ = title_block("KNN in one breath", "")
        self.play(Write(t), run_time=0.9)
        lines = VGroup(
            Text("1. store the data (lazy: no training)", font_size=24,
                 color=WHITE, font=MONO),
            Text("2. measure distance (L2 / L1 / Hamming / cosine)", font_size=24,
                 color=WHITE, font=MONO),
            Text("3. K neighbors vote (weighted = closer wins)", font_size=24,
                 color=WHITE, font=MONO),
            Text("4. K too small -> overfit,  K too big -> underfit", font_size=24,
                 color=WHITE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        lines[0][13:17].set_color(BLUE)
        lines[1][19:48].set_color(BLUE)
        lines[2][20:44].set_color(GREEN)
        lines[3][18:25].set_color(RED)
        lines[3][41:49].set_color(RED)
        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(1.0)
        nfl = Text("No Free Lunch: no algorithm wins everywhere",
                   font_size=20, color=ACCENT, opacity=0.85, font=MONO
                   ).to_edge(DOWN, buff=0.5)
        self.play(Write(nfl), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
