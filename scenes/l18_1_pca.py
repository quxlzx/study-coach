from manim import *
import numpy as np

BG = "#1C1C1C"
GREEN = "#83C167"
RED = "#FC6255"
ACCENT = "#FFFF00"
BLUE = "#58C4DD"
MONO = "DejaVu Sans Mono"


def title_block(title, sub):
    t = Text(title, font_size=40, color=BLUE, weight=BOLD, font=MONO
             ).to_edge(UP, buff=0.55)
    s = Text(sub, font_size=19, color=WHITE, opacity=0.5, font=MONO
             ).next_to(t, DOWN, buff=0.22)
    return t, s


def box(text, w=2.2, h=0.9, col=BLUE, fs=20):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h,
                         stroke_color=col, stroke_width=2.5,
                         fill_color=col, fill_opacity=0.08)
    t = Text(text, font_size=fs, color=col, font=MONO).move_to(r.get_center())
    return VGroup(r, t)


# correlated 2D cloud, centered at origin (data coords)
rng = np.random.default_rng(7)
N = 42
_base = rng.normal(0, 1, N)
CLOUD = np.stack([
    1.7 * _base + rng.normal(0, 0.28, N),
    1.15 * _base + rng.normal(0, 0.34, N),
], axis=1) / 2.4
THETA = np.arctan2(1.15, 1.7)  # direction of max variance


class P_Title(Scene):
    def construct(self):
        self.camera.background_color = BG
        t = Text("PCA: Principal Component Analysis", font_size=38,
                 color=BLUE, weight=BOLD, font=MONO).to_edge(UP, buff=0.8)
        s = Text("CMSC 320 - lecture 18.1 - unsupervised learning",
                 font_size=20, color=WHITE, opacity=0.5, font=MONO
                 ).next_to(t, DOWN, buff=0.3)
        self.play(Write(t), run_time=1.4)
        self.play(FadeIn(s, shift=DOWN * 0.2), run_time=0.7)
        self.wait(0.8)
        core = Text("view the data from its most informative angle",
                    font_size=29, color=ACCENT, weight=BOLD, font=MONO)
        self.play(FadeOut(s), Write(core), run_time=1.4)
        self.wait(1.8)
        agenda = Text("curse of dimensionality - variance - eigenvectors - projection",
                      font_size=18, color=WHITE, opacity=0.55, font=MONO
                      ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(agenda), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class P_Why(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Too many features?", "dimensionality reduction")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        defn = Text("reduce the number of features while\nkeeping the essential information",
                    font_size=24, color=ACCENT, font=MONO).move_to([0, 1.5, 0])
        self.play(Write(defn), run_time=1.1)
        cards = VGroup(
            VGroup(box("redundancy", 2.6, 0.85, RED, 19),
                   Text("correlated features\nadd noise", font_size=16,
                        color=WHITE, font=MONO)).arrange(DOWN, buff=0.3),
            VGroup(box("efficiency", 2.6, 0.85, GREEN, 19),
                   Text("fewer features =\nfaster models", font_size=16,
                        color=WHITE, font=MONO)).arrange(DOWN, buff=0.3),
            VGroup(box("sparsity", 2.6, 0.85, BLUE, 19),
                   Text("more dims = emptier\nspace, harder patterns",
                        font_size=16, color=WHITE, font=MONO)
                   ).arrange(DOWN, buff=0.3),
        ).arrange(RIGHT, buff=1.3).move_to([0, -0.6, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards],
                              run_time=1.8))
        cap = Text("simpler models, less overfitting, clearer insight",
                   font_size=20, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.6)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class P_Curse(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The curse of dimensionality",
                           "more axes, emptier space")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        # left: dense 2D box, right: same points lost in bigger box
        sm = Square(side_length=2.6, stroke_color=WHITE, stroke_opacity=0.4,
                    stroke_width=2).move_to([-3.9, 0.15, 0])
        big = Square(side_length=4.0, stroke_color=WHITE, stroke_opacity=0.4,
                     stroke_width=2).move_to([3.0, -0.15, 0])
        pts2 = VGroup(*[Dot(sm.get_center() + np.array([dx, dy, 0]),
                            color=BLUE, radius=0.07)
                        for dx, dy in [(-0.9, 0.7), (-0.3, -0.8), (0.6, 0.4),
                                       (0.9, -0.6), (0.1, 0.9), (-0.7, -0.2),
                                       (0.4, -0.1), (0.8, 0.8), (-0.2, 0.2)]])
        pts3 = VGroup(*[Dot(big.get_center() + np.array([dx, dy, 0]),
                            color=BLUE, radius=0.07)
                        for dx, dy in [(-1.9, 1.5), (-0.6, -1.7), (1.3, 0.8),
                                       (1.9, -1.3), (0.2, 1.8), (-1.5, -0.4),
                                       (0.8, -0.2), (1.7, 1.7), (-0.4, 0.4)]])
        h1 = Text("2 dimensions", font_size=20, color=WHITE, font=MONO
                  ).move_to([-3.9, 1.85, 0])
        h2 = Text("many dimensions", font_size=20, color=WHITE, font=MONO
                  ).move_to([3.0, 2.15, 0])
        self.play(Create(sm), FadeIn(h1), FadeIn(pts2), run_time=1.1)
        self.play(Create(big), FadeIn(h2), FadeIn(pts3), run_time=1.1)
        cap = Text("Hughes phenomenon: fixed samples + more dims\n= predictive power rises, then falls",
                   font_size=20, color=ACCENT, font=MONO).to_edge(DOWN,
                                                                  buff=0.5)
        self.play(Write(cap), run_time=1.1)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class P_What(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("What is PCA?", "unsupervised dimensionality reduction")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        l1 = Text("PCA simplifies a big dataset into a smaller one",
                  font_size=23, color=WHITE, font=MONO).move_to([0, 1.7, 0])
        l2 = Text("correlated features  ->  uncorrelated principal components",
                  font_size=23, color=ACCENT, font=MONO).move_to([0, 1.0, 0])
        self.play(Write(l1), run_time=1.0)
        self.play(Write(l2), run_time=1.0)
        cards = VGroup(
            box("visualize: 100 features -> 2D", 4.6, 0.8, BLUE, 18),
            box("speeds up models", 3.0, 0.8, GREEN, 18),
            box("removes redundancy", 3.6, 0.8, RED, 18),
        ).arrange(DOWN, buff=0.35).move_to([0, -1.15, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.3) for c in cards],
                              run_time=1.5))
        cap = Text("no labels needed - PCA just looks at the data itself",
                   font_size=20, color=WHITE, opacity=0.7, font=MONO
                   ).to_edge(DOWN, buff=0.6)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class P_Rotate(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The goal: maximize variance", "find the direction of widest spread")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = Axes(x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
                  x_length=6.2, y_length=4.4,
                  axis_config={"stroke_opacity": 0.15,
                               "include_ticks": False}).shift(LEFT * 2.6)
        self.play(Create(ax), run_time=0.8)
        pts = VGroup(*[Dot(ax.c2p(x, y), color=BLUE, radius=0.07)
                       for x, y in CLOUD])
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pts],
                              run_time=1.2))
        axis = Line([-1.9 * np.cos(0.15), -1.9 * np.sin(0.15), 0],
                    [1.9 * np.cos(0.15), 1.9 * np.sin(0.15), 0],
                    color=RED, stroke_width=4).move_to(ax.c2p(0, 0))
        self.play(Create(axis), run_time=0.7)
        spin = Text("rotating...", font_size=19, color=WHITE, opacity=0.6,
                    font=MONO).move_to(ax.c2p(0, 0) + DOWN * 2.05)
        self.play(FadeIn(spin), run_time=0.4)
        self.play(Rotate(axis, angle=THETA - 0.15, about_point=ax.c2p(0, 0)),
                  run_time=1.6)
        self.play(FadeOut(spin), Indicate(axis, color=ACCENT), run_time=0.8)
        pc1 = Text("PC1 = the axis where the cloud\nis most spread out",
                   font_size=21, color=ACCENT, font=MONO).move_to([4.3, 1.2, 0])
        pc2 = Text("PC2 = perpendicular to PC1,\ncatches what is left",
                   font_size=21, color=GREEN, font=MONO).move_to([4.3, -0.1, 0])
        keep = Text("keep PC1, drop PC2:\n2D -> 1D, little lost",
                    font_size=21, color=WHITE, font=MONO).move_to([4.3, -1.4, 0])
        self.play(Write(pc1), run_time=1.0)
        self.play(Write(pc2), run_time=1.0)
        self.play(Write(keep), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class P_Projection(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Projecting onto the PCs", "new coordinates, fewer numbers")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = Axes(x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
                  x_length=6.6, y_length=4.6,
                  axis_config={"stroke_opacity": 0.15,
                               "include_ticks": False}).shift(LEFT * 2.4)
        self.add(ax)
        pts = VGroup(*[Dot(ax.c2p(x, y), color=BLUE, radius=0.07)
                       for x, y in CLOUD])
        self.add(pts)
        u = np.array([np.cos(THETA), np.sin(THETA), 0])
        p1 = Line(ax.c2p(0, 0) - 2.1 * u, ax.c2p(0, 0) + 2.1 * u,
                  color=ACCENT, stroke_width=4)
        self.play(Create(p1), run_time=0.8)
        lab = Text("PC1", font_size=22, color=ACCENT, weight=BOLD, font=MONO
                   ).move_to(ax.c2p(0, 0) + 2.35 * u + DOWN * 0.25)
        self.play(FadeIn(lab), run_time=0.4)
        drops = VGroup()
        ticks = VGroup()
        for x, y in CLOUD:
            p = ax.c2p(x, y)
            foot = ax.c2p(0, 0) + (x * u[0] + y * u[1]) * u
            drops.add(Line(p, foot, stroke_width=1.4, color=WHITE,
                           stroke_opacity=0.45))
            ticks.add(Line(foot + 0.09 * np.array([-u[1], u[0], 0]),
                           foot + 0.09 * np.array([u[1], -u[0], 0]),
                           stroke_width=3, color=ACCENT))
        self.play(LaggedStart(*[Create(d) for d in drops], lag_ratio=0.04,
                              run_time=1.8))
        self.play(FadeIn(ticks), run_time=0.6)
        u2 = np.array([-u[1], u[0], 0])
        p2 = Line(ax.c2p(0, 0) - 1.1 * u2, ax.c2p(0, 0) + 1.1 * u2,
                  color=GREEN, stroke_width=4)
        self.play(Create(p2), run_time=0.7)
        lab2 = Text("PC2", font_size=22, color=GREEN, weight=BOLD, font=MONO
                    ).move_to(ax.c2p(0, 0) + 1.35 * u2 + RIGHT * 0.3)
        self.play(FadeIn(lab2), run_time=0.4)
        cap = Text("each point becomes 1 number on PC1 instead of 2",
                   font_size=20, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.55)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class P_Steps(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("How PCA works: 5 steps", "the recipe")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        steps = [("1", "standardize the data", BLUE),
                 ("2", "compute covariance matrix", GREEN),
                 ("3", "eigenvectors + eigenvalues", ACCENT),
                 ("4", "sort PCs, keep top k", RED),
                 ("5", "project data onto them", BLUE)]
        nodes = VGroup()
        for i, (num, txt, col) in enumerate(steps):
            b = box(num + ". " + txt, 4.6, 0.72, col, 18)
            b.move_to([0, 1.85 - i * 0.98, 0])
            nodes.add(b)
        for i, n in enumerate(nodes):
            self.play(FadeIn(n, shift=RIGHT * 0.3), run_time=0.55)
        cap = Text("data -> covariance -> eigenvectors -> sorted PCs -> reduced data",
                   font_size=18, color=ACCENT, font=MONO).to_edge(DOWN,
                                                                  buff=0.5)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class P_Standardize(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Step 1: standardize", "PCA listens to scale")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        l1 = Text("height in cm: 160 - 190", font_size=23, color=BLUE,
                  font=MONO).move_to([-3.6, 1.4, 0])
        l2 = Text("weight in kg: 60 - 110", font_size=23, color=GREEN,
                  font=MONO).move_to([-3.6, 0.7, 0])
        l3 = Text("age in years: 20 - 40", font_size=23, color=RED,
                  font=MONO).move_to([-3.6, 0.0, 0])
        self.play(Write(l1), run_time=0.7)
        self.play(Write(l2), run_time=0.7)
        self.play(Write(l3), run_time=0.7)
        warn = Text("big numbers dominate\nthe variance!", font_size=21,
                    color=ACCENT, font=MONO).move_to([3.9, 0.7, 0])
        self.play(FadeIn(warn), run_time=0.8)
        f = Text("x_new = (x - mean) / std", font_size=28, color=WHITE,
                 weight=BOLD, font=MONO).move_to([0, -1.15, 0])
        self.play(Write(f), run_time=1.1)
        cap = Text("every feature ends at mean 0, std 1: a fair fight",
                   font_size=20, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.55)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class P_Cov(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Step 2: covariance matrix", "who moves with whom?")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        m = 1.15
        grid = VGroup()
        cells = [["var(x1)", "cov(x1,x2)", "cov(x1,x3)"],
                 ["cov(x2,x1)", "var(x2)", "cov(x2,x3)"],
                 ["cov(x3,x1)", "cov(x3,x2)", "var(x3)"]]
        cols = [[GREEN, BLUE, BLUE], [BLUE, GREEN, BLUE], [BLUE, BLUE, GREEN]]
        for i in range(3):
            for j in range(3):
                r = Square(side_length=m, stroke_color=cols[i][j],
                           stroke_width=2, fill_color=cols[i][j],
                           fill_opacity=0.07)
                r.move_to([-4.0 + j * m, 1.2 - i * m, 0])
                tx = Text(cells[i][j], font_size=12, color=cols[i][j],
                          font=MONO).move_to(r.get_center())
                grid.add(VGroup(r, tx))
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in grid],
                              run_time=1.6))
        d1 = Text("diagonal: each feature's\nown variance (spread)",
                  font_size=19, color=GREEN, font=MONO).move_to([3.4, 1.6, 0])
        d2 = Text("off-diagonal: how pairs\nmove together", font_size=19,
                  color=BLUE, font=MONO).move_to([3.4, 0.5, 0])
        d3 = Text("+ together / - opposite / 0 none", font_size=18,
                  color=WHITE, opacity=0.7, font=MONO).move_to([3.4, -0.4, 0])
        self.play(FadeIn(d1), run_time=0.7)
        self.play(FadeIn(d2), run_time=0.7)
        self.play(FadeIn(d3), run_time=0.7)
        cap = Text("the covariance matrix hides the best directions - step 3 digs them out",
                   font_size=18, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.5)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class P_Eigen(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Step 3: eigenvectors", "solve  S v = lambda v")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        f = Text("S v = lambda v", font_size=40, color=ACCENT, weight=BOLD,
                 font=MONO).move_to([0, 1.5, 0])
        self.play(Write(f), run_time=1.1)
        r1 = VGroup(box("S", 0.9, 0.9, BLUE, 26),
                    Text("covariance matrix", font_size=18, color=BLUE,
                         font=MONO)).arrange(RIGHT, buff=0.5).move_to([-3.9, 0.3, 0])
        r2 = VGroup(box("v", 0.9, 0.9, GREEN, 26),
                    Text("eigenvector = a direction\n(the principal component)",
                         font_size=18, color=GREEN, font=MONO)
                    ).arrange(RIGHT, buff=0.5).move_to([-2.6, -0.75, 0])
        r3 = VGroup(box("lambda", 1.6, 0.9, RED, 22),
                    Text("eigenvalue = how much\nvariance lives there",
                         font_size=18, color=RED, font=MONO)
                    ).arrange(RIGHT, buff=0.5).move_to([-2.2, -1.8, 0])
        self.play(FadeIn(r1, shift=RIGHT * 0.3), run_time=0.7)
        self.play(FadeIn(r2, shift=RIGHT * 0.3), run_time=0.7)
        self.play(FadeIn(r3, shift=RIGHT * 0.3), run_time=0.7)
        # mini cloud with arrow along max-variance direction
        ax = Axes(x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
                  x_length=3.6, y_length=3.0,
                  axis_config={"stroke_opacity": 0.15,
                               "include_ticks": False}).move_to([4.3, -0.3, 0])
        pts = VGroup(*[Dot(ax.c2p(x, y), color=WHITE, radius=0.055,
                           stroke_opacity=0.6)
                       for x, y in CLOUD])
        ax.add(pts)
        u = np.array([np.cos(THETA), np.sin(THETA), 0])
        v = Arrow(ax.c2p(0, 0), ax.c2p(0, 0) + 1.9 * u, color=GREEN,
                  stroke_width=5, max_tip_length_to_length_ratio=0.16)
        self.play(Create(ax), FadeIn(pts), run_time=0.9)
        self.play(Create(v), run_time=0.8)
        vl = Text("v1: the widest direction", font_size=17, color=GREEN,
                  font=MONO).move_to([4.3, -2.15, 0])
        self.play(FadeIn(vl), run_time=0.6)
        cap = Text("eigenvectors = directions, eigenvalues = importance",
                   font_size=20, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.45)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class P_Select(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Step 4: keep the top k PCs", "explained variance decides")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        # bar chart of eigenvalues 5, 3, 2
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 6, 2], x_length=5.2,
                  y_length=3.6, axis_config={"stroke_opacity": 0.15,
                                             "include_ticks": False}
                  ).move_to([-3.4, -0.1, 0])
        self.play(Create(ax), run_time=0.7)
        vals = [5, 3, 2]
        cols = [ACCENT, BLUE, RED]
        bars = VGroup()
        labs = VGroup()
        for i, (v, c) in enumerate(zip(vals, cols)):
            bar = Rectangle(width=0.8, height=ax.c2p(i + 1, v)[1] - ax.c2p(0, 0)[1],
                            stroke_color=c, stroke_width=2, fill_color=c,
                            fill_opacity=0.35)
            bar.move_to([(ax.c2p(i + 1, 0)[0] + ax.c2p(i + 1, v)[0]) / 2,
                         (ax.c2p(i + 1, 0)[1] + ax.c2p(i + 1, v)[1]) / 2, 0])
            bars.add(bar)
            labs.add(Text(f"PC{i+1}", font_size=17, color=c, font=MONO
                          ).move_to(ax.c2p(i + 1, 0) + DOWN * 0.35))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                              run_time=1.2), FadeIn(labs), run_time=1.2)
        r1 = Text("eigenvalues 5, 3, 2 -> total 10", font_size=20,
                  color=WHITE, font=MONO).move_to([3.6, 1.7, 0])
        r2 = Text("EVR: 0.50 / 0.30 / 0.20", font_size=20, color=ACCENT,
                  font=MONO).move_to([3.6, 1.0, 0])
        r3 = Text("cumulative: 0.50 -> 0.80 -> 1.00", font_size=20,
                  color=BLUE, font=MONO).move_to([3.6, 0.3, 0])
        r4 = Text("threshold 80%? keep PC1 + PC2", font_size=20, color=GREEN,
                  font=MONO).move_to([3.6, -0.4, 0])
        self.play(Write(r1), run_time=0.8)
        self.play(Write(r2), run_time=0.8)
        self.play(Write(r3), run_time=0.8)
        self.play(Write(r4), run_time=0.8)
        cap = Text("rules of thumb: >95% cumulative variance, lambda >= 1 (Kaiser),\nor the elbow of the scree plot",
                   font_size=18, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.45)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class P_Transform(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Step 5: transform the data", "multiply by the top eigenvectors")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        f = Text("X_reduced = X_standardized * W_k", font_size=32,
                 color=ACCENT, weight=BOLD, font=MONO).move_to([0, 1.4, 0])
        self.play(Write(f), run_time=1.2)
        l1 = Text("W_k = matrix whose columns\nare the top k eigenvectors",
                  font_size=19, color=BLUE, font=MONO).move_to([-3.9, 0.1, 0])
        l2 = Text("each column of the result\nis one principal component",
                  font_size=19, color=GREEN, font=MONO).move_to([3.9, 0.1, 0])
        self.play(FadeIn(l1), run_time=0.8)
        self.play(FadeIn(l2), run_time=0.8)
        big = box("10 features", 2.6, 0.85, RED, 19).move_to([-3.4, -1.5, 0])
        small = box("2 features", 2.6, 0.85, GREEN, 19).move_to([3.4, -1.5, 0])
        ar = Arrow([-1.9, -1.5, 0], [1.9, -1.5, 0], stroke_width=4,
                   color=WHITE, stroke_opacity=0.6)
        self.play(FadeIn(big), Create(ar), FadeIn(small), run_time=1.0)
        cap = Text("fewer numbers, most of the story still intact",
                   font_size=20, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.5)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class P_ProCon(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("PCA: the tradeoff", "powerful, but not free")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        pros = VGroup(
            Text("+ shrinks features, keeps signal", font_size=20,
                 color=GREEN, font=MONO),
            Text("+ reduces noise", font_size=20, color=GREEN, font=MONO),
            Text("+ makes 100-D data viewable in 2D", font_size=20,
                 color=GREEN, font=MONO),
            Text("+ speeds up every model downstream", font_size=20,
                 color=GREEN, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.4, 0.3, 0])
        cons = VGroup(
            Text("- assumes straight-line structure", font_size=20, color=RED,
                 font=MONO),
            Text("- PCs are hard to interpret", font_size=20, color=RED,
                 font=MONO),
            Text("- variance != importance:\ncould drop the signal", font_size=20,
                 color=RED, font=MONO),
            Text("- no new features, only re-mixes", font_size=20, color=RED,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.3, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in pros],
                              run_time=1.6))
        self.play(LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in cons],
                              run_time=1.6))
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class P_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, _ = title_block("Lecture 18.1 in one breath", "")
        self.play(Write(t), run_time=0.9)
        lines = VGroup(
            Text("too many correlated features -> curse of dimensionality",
                 font_size=22, color=WHITE, font=MONO),
            Text("PCA: unsupervised, project onto axes of max variance",
                 font_size=22, color=WHITE, font=MONO),
            Text("standardize -> covariance -> solve S v = lambda v",
                 font_size=22, color=WHITE, font=MONO),
            Text("eigenvectors = directions, eigenvalues = importance",
                 font_size=22, color=WHITE, font=MONO),
            Text("keep top k by explained variance (e.g. 80-95%)",
                 font_size=22, color=WHITE, font=MONO),
            Text("data -> S -> eigenvectors -> sorted PCs -> reduced data",
                 font_size=22, color=WHITE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        lines[1][29:36].set_color(GREEN)
        lines[2][31:43].set_color(ACCENT)
        lines[3][33:43].set_color(BLUE)
        lines[4][29:37].set_color(RED)
        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(2.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
