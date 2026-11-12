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


class L182_Title(Scene):
    def construct(self):
        self.camera.background_color = BG
        t = Text("Unsupervised Learning", font_size=42, color=BLUE,
                 weight=BOLD, font=MONO).to_edge(UP, buff=0.8)
        s = Text("CMSC 320 - lecture 18.2 - clustering", font_size=20,
                 color=WHITE, opacity=0.5, font=MONO).next_to(t, DOWN, buff=0.3)
        self.play(Write(t), run_time=1.4)
        self.play(FadeIn(s, shift=DOWN * 0.2), run_time=0.7)
        self.wait(0.8)
        core = Text("no labels? the data groups itself", font_size=30,
                    color=ACCENT, weight=BOLD, font=MONO)
        self.play(FadeOut(s), Write(core), run_time=1.4)
        self.wait(1.8)
        agenda = Text("k-means - elbow - hierarchical - DBSCAN - hard vs soft",
                      font_size=18, color=WHITE, opacity=0.55, font=MONO
                      ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(agenda), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_Unsupervised(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Unsupervised learning", "real data rarely comes with labels")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        lab = VGroup(*[Dot(np.array([-4.9 + 0.8 * i, 1.6, 0]),
                           color=(GREEN if i % 2 == 0 else RED), radius=0.11)
                       for i in range(3)])
        unl = VGroup(*[Dot(np.array([3.9 + 0.8 * i, 1.6, 0]),
                           color=WHITE, radius=0.11) for i in range(3)])
        lh = Text("labeled data", font_size=20, color=GREEN, font=MONO
                  ).move_to([-4.5, 2.4, 0])
        uh = Text("unlabeled data", font_size=20, color=ACCENT, font=MONO
                  ).move_to([4.5, 2.4, 0])
        q = Text("?", font_size=30, color=ACCENT, weight=BOLD, font=MONO
                 ).move_to([4.5, 1.6, 0]).shift(RIGHT * 1.5)
        self.play(FadeIn(lh), FadeIn(lab), run_time=0.8)
        self.play(FadeIn(uh), FadeIn(unl), FadeIn(q), run_time=0.8)
        defn = Text("ML algorithms analyze and cluster\nunlabeled data sets",
                    font_size=23, color=WHITE, font=MONO).move_to([-3.6, 0.1, 0])
        defn2 = Text("discover hidden patterns or groupings,\nno human intervention",
                     font_size=23, color=BLUE, font=MONO).move_to([3.6, 0.1, 0])
        self.play(Write(defn), run_time=1.1)
        self.play(Write(defn2), run_time=1.1)
        goal = Text("goal: study the intrinsic hidden structure, segment into\nsimilar groups, or simplify the data",
                    font_size=20, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.6)
        self.play(Write(goal), run_time=1.2)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_Applications(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("What is it used for?", "three big applications")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        cards = VGroup(
            VGroup(box("cluster analysis", 3.4, 0.8, BLUE, 19),
                   Text("find natural groupings by\nshared attributes", font_size=17,
                        color=WHITE, font=MONO)).arrange(DOWN, buff=0.3),
            VGroup(box("dimensionality reduction", 3.4, 0.8, GREEN, 19),
                   Text("aggregate similar variables:\nfewer dimensions, same structure",
                        font_size=17, color=WHITE, font=MONO)).arrange(DOWN, buff=0.3),
            VGroup(box("anomaly detection", 3.4, 0.8, RED, 19),
                   Text("spot outliers that break the\nmajority pattern", font_size=17,
                        color=WHITE, font=MONO)).arrange(DOWN, buff=0.3),
        ).arrange(RIGHT, buff=1.0).move_to([0, 0.7, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards],
                              run_time=1.8))
        self.wait(0.8)
        what = Text("cluster in practice:", font_size=20, color=WHITE,
                    opacity=0.6, font=MONO).to_edge(DOWN, buff=1.35)
        items = Text("news by topic - genes by expression - users by interest -\ncustomers by purchase history",
                     font_size=19, color=ACCENT, font=MONO).next_to(what, DOWN, buff=0.25)
        self.play(FadeIn(what), Write(items), run_time=1.2)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_Objectives(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The objective of clustering", "similar inside, different outside")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        A = [(-3.4, 1.3), (-2.6, 1.8), (-3.0, 0.7), (-2.2, 1.0)]
        B = [(2.6, -0.4), (3.4, 0.1), (3.0, -1.0), (2.2, -0.8)]
        dA = VGroup(*[Dot(np.array([x, y, 0]), color=GREEN, radius=0.1) for x, y in A])
        dB = VGroup(*[Dot(np.array([x, y, 0]), color=BLUE, radius=0.1) for x, y in B])
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dA], run_time=0.9),
                  LaggedStart(*[FadeIn(d, scale=0.5) for d in dB], run_time=0.9))
        intra = VGroup(Line(np.array([A[0][0], A[0][1], 0]), np.array([A[1][0], A[1][1], 0]),
                            color=GREEN, stroke_width=3),
                       Line(np.array([A[2][0], A[2][1], 0]), np.array([A[3][0], A[3][1], 0]),
                            color=GREEN, stroke_width=3),
                       Line(np.array([B[0][0], B[0][1], 0]), np.array([B[1][0], B[1][1], 0]),
                            color=BLUE, stroke_width=3),
                       Line(np.array([B[2][0], B[2][1], 0]), np.array([B[3][0], B[3][1], 0]),
                            color=BLUE, stroke_width=3))
        inter = DashedLine(np.array([-2.8, 1.2, 0]), np.array([2.9, -0.5, 0]),
                           color=RED, stroke_width=3)
        self.play(Create(intra), run_time=1.0)
        li = Text("INTRA-cluster distance: MINIMIZED", font_size=22, color=GREEN,
                  font=MONO).to_edge(DOWN, buff=1.15)
        self.play(Write(li), run_time=0.9)
        self.play(Create(inter), run_time=0.9)
        le = Text("INTER-cluster distance: MAXIMIZED", font_size=22, color=RED,
                  font=MONO).next_to(li, DOWN, buff=0.3)
        self.play(Write(le), run_time=0.9)
        cap = Text("objects in a group are related; groups are distinct ->\neasier interpretation",
                   font_size=18, color=WHITE, opacity=0.55, font=MONO
                   ).next_to(le, DOWN, buff=0.25)
        self.play(FadeIn(cap), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_Algorithms(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The clustering lineup", "most common algorithms")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        rows = [("K-Means", "centroid-based, fast, needs K", BLUE),
                ("Hierarchical", "tree of clusters (dendrogram), no K needed", GREEN),
                ("DBSCAN", "density-based, arbitrary shapes, finds noise", RED),
                ("Gaussian Mixture (GMM)", "probabilistic soft clusters", ACCENT)]
        nodes = VGroup()
        for i, (name, note, col) in enumerate(rows):
            b = box(name, 3.6, 0.75, col, 20)
            b.move_to([-2.6, 1.8 - 1.15 * i, 0])
            n = Text(note, font_size=16, color=WHITE, opacity=0.55, font=MONO
                     ).next_to(b, RIGHT, buff=0.5)
            nodes.add(VGroup(b, n))
        for nd in nodes:
            self.play(FadeIn(nd, shift=RIGHT * 0.3), run_time=0.65)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_KMeansSteps(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("K-Means: the algorithm", "pick K, then loop two moves")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        steps = [("1. choose K", "how many clusters you expect", BLUE),
                 ("2. init centroids", "start with K random centroids", BLUE),
                 ("3. assign points", "each point joins the nearest centroid\n(by minimum distance)", GREEN),
                 ("4. re-init centroids", "new centroid = average of all points\nin that cluster", GREEN),
                 ("5. repeat 3-4", "until convergence", ACCENT)]
        nodes = VGroup()
        for i, (name, note, col) in enumerate(steps):
            b = box(name, 3.1, 0.72, col, 19)
            b.move_to([-4.3, 1.9 - 1.05 * i, 0])
            n = Text(note, font_size=15, color=WHITE, opacity=0.55, font=MONO
                     ).next_to(b, RIGHT, buff=0.45)
            nodes.add(VGroup(b, n))
        for i, nd in enumerate(nodes):
            self.play(FadeIn(nd, shift=RIGHT * 0.3), run_time=0.6)
        loop = CurvedArrow([-4.3, -2.25, 0], [-4.3, 0.35, 0], angle=1.9,
                           color=ACCENT, stroke_width=3)
        self.play(Create(loop), run_time=0.9)
        cap = Text("the algorithm starts randomly, then converges",
                   font_size=20, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.45)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_KMeansAnim(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("K-Means in motion", "K = 2: centroids chase the data")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        pts = [(-3.4, 1.5), (-2.6, 1.9), (-3.8, 0.9), (-2.9, 0.8), (-2.2, 1.4),
               (2.4, -0.2), (3.2, -0.6), (3.7, -1.2), (2.7, -1.3), (3.0, 0.2)]
        P = np.array([[x, y, 0.0] for x, y in pts])
        dots = VGroup(*[Dot(p, color=WHITE, radius=0.09) for p in P])
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots],
                              lag_ratio=0.08, run_time=1.2))
        c1 = Dot(np.array([-0.6, 1.6, 0.0]), color=RED, radius=0.16)
        c2 = Dot(np.array([0.6, -1.4, 0.0]), color=BLUE, radius=0.16)
        lc1 = Text("c1", font_size=17, color=RED, font=MONO).next_to(c1, UP, buff=0.12)
        lc2 = Text("c2", font_size=17, color=BLUE, font=MONO).next_to(c2, DOWN, buff=0.12)
        self.play(FadeIn(c1, scale=2), FadeIn(c2, scale=2),
                  FadeIn(lc1), FadeIn(lc2), run_time=0.8)
        cap = Text("random start", font_size=19, color=WHITE, opacity=0.6,
                   font=MONO).to_edge(DOWN, buff=0.5)
        self.play(Write(cap), run_time=0.6)
        centers = [c1, c2]
        cols = [RED, BLUE]
        for it in range(3):
            C = np.array([c.get_center() for c in centers])
            d = np.linalg.norm(P[:, None, :] - C[None, :, :], axis=2)
            assign = np.argmin(d, axis=1)
            lines = VGroup(*[Line(P[i], C[assign[i]], color=cols[assign[i]],
                                  stroke_width=1.4, stroke_opacity=0.4)
                             for i in range(len(P))])
            newcols = [cols[a] for a in assign]
            self.play(Create(lines),
                      *[dot.animate.set_color(nc) for dot, nc in zip(dots, newcols)],
                      run_time=1.1)
            step = Text(f"iteration {it + 1}: assign to nearest, then average",
                        font_size=19, color=WHITE, opacity=0.7, font=MONO
                        ).to_edge(DOWN, buff=0.5)
            self.play(Transform(cap, step), run_time=0.5)
            news = [P[assign == k].mean(axis=0) if (assign == k).any()
                    else C[k] for k in range(2)]
            self.play(*[c.animate.move_to(n) for c, n in zip(centers, news)],
                      *[lc.animate.move_to(c.get_center() + off)
                        for lc, c, off in [(lc1, centers[0], UP * 0.3),
                                           (lc2, centers[1], DOWN * 0.3)]],
                      run_time=1.1)
            self.play(FadeOut(lines), run_time=0.4)
        done = Text("assignments stop changing -> CONVERGED", font_size=22,
                    color=ACCENT, font=MONO).to_edge(DOWN, buff=0.5)
        self.play(Transform(cap, done), run_time=0.8)
        crit = Text("stop when: centroids stop moving - points stay put -\nor max iterations reached",
                    font_size=18, color=WHITE, opacity=0.6, font=MONO
                    ).next_to(done, DOWN, buff=0.22)
        self.play(FadeIn(crit), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_ChooseK(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("How to choose K?", "the one hyperparameter you must pick")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        pts = [(-3.0, 1.2), (-2.2, 1.6), (-2.6, 0.6), (2.4, 0.4), (3.2, 0.9),
               (2.8, -0.4), (0.2, -1.4), (-0.4, 1.8)]
        P = np.array([[x, y, 0.0] for x, y in pts])
        dots = VGroup(*[Dot(p, color=WHITE, radius=0.09) for p in P])
        self.play(FadeIn(dots), run_time=0.7)
        # K = 1: one big circle
        c1 = Circle(radius=3.1, color=GREEN, stroke_width=3, stroke_opacity=0.7
                    ).move_to([0.1, 0.4, 0])
        l1 = Text("K = 1: one big cluster for everything", font_size=20,
                  color=GREEN, font=MONO).to_edge(DOWN, buff=1.0)
        self.play(Create(c1), Write(l1), run_time=1.0)
        self.wait(0.8)
        rings = VGroup(*[Circle(radius=0.3, color=RED, stroke_width=2.5).move_to(p)
                         for p in P])
        l2 = Text("K too large: a cluster per point - defeats the purpose",
                  font_size=20, color=RED, font=MONO).to_edge(DOWN, buff=1.0)
        self.play(FadeOut(c1), FadeOut(l1), LaggedStart(*[FadeIn(r) for r in rings],
                                                       run_time=0.9), Write(l2),
                  run_time=1.2)
        self.wait(0.8)
        g1 = Circle(radius=1.15, color=GREEN, stroke_width=3).move_to([-2.6, 1.15, 0])
        g2 = Circle(radius=1.15, color=BLUE, stroke_width=3).move_to([2.8, 0.3, 0])
        g3 = Circle(radius=0.95, color=ACCENT, stroke_width=3).move_to([-0.1, -1.4, 0])
        l3 = Text("ideal K: point-to-center distance is much smaller than\ncenter-to-center distance",
                  font_size=20, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.85)
        self.play(FadeOut(rings), FadeOut(l2), Create(g1), Create(g2), Create(g3),
                  Write(l3), run_time=1.5)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_WCSS(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("What K-Means minimizes", "within-cluster sum of squares")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        f1 = Text("WCSS = inertia = sum over every point of\nd(point, its centroid) squared",
                  font_size=24, color=WHITE, font=MONO).move_to([0, 1.5, 0])
        self.play(Write(f1), run_time=1.1)
        cen = Dot(np.array([-2.6, -0.6, 0.0]), color=ACCENT, radius=0.15)
        lc = Text("centroid", font_size=17, color=ACCENT, font=MONO
                  ).next_to(cen, DOWN, buff=0.15)
        pts = [(-3.4, 0.2), (-1.8, 0.1), (-3.6, -1.3), (-1.6, -1.4)]
        ds = VGroup(*[Dot(np.array([x, y, 0.0]), color=BLUE, radius=0.09)
                      for x, y in pts])
        lines = VGroup(*[Line(np.array([x, y, 0.0]), cen.get_center(),
                              color=ACCENT, stroke_width=2, stroke_opacity=0.6)
                         for x, y in pts])
        self.play(FadeIn(cen), FadeIn(lc), FadeIn(ds), run_time=0.8)
        self.play(Create(lines), run_time=0.9)
        f2 = Text("for cluster Ci with Ni points:\nmi = average of all its points",
                  font_size=20, color=BLUE, font=MONO).move_to([2.9, -0.6, 0])
        self.play(Write(f2), run_time=0.9)
        cap = Text("objective: minimize total intra-cluster variance",
                   font_size=21, color=ACCENT, font=MONO).to_edge(DOWN, buff=1.0)
        self.play(Write(cap), run_time=0.9)
        asm = Text("assumptions: every point belongs to one of K clusters -\nclusters do not overlap - within-cluster variation minimized",
                   font_size=17, color=WHITE, opacity=0.6, font=MONO
                   ).next_to(cap, DOWN, buff=0.25)
        self.play(FadeIn(asm), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_Elbow(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Finding K: the elbow method", "plot WCSS against K")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = Axes(x_range=[0, 7, 1], y_range=[0, 10, 2], x_length=7.0,
                  y_length=4.4,
                  axis_config={"stroke_opacity": 0.2, "include_ticks": False},
                  ).shift(LEFT * 0.6 + DOWN * 0.35)
        xl = Text("K (number of clusters)", font_size=18, color=WHITE,
                  opacity=0.5, font=MONO).next_to(ax.x_axis, RIGHT, buff=0.15)
        yl = Text("WCSS", font_size=18, color=WHITE, opacity=0.5, font=MONO
                  ).next_to(ax.y_axis, UP, buff=0.15)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.9)
        vals = [(1, 9.5), (2, 6.0), (3, 3.3), (4, 2.7), (5, 2.4), (6, 2.2)]
        curve = VGroup(*[Line(ax.c2p(vals[i][0], vals[i][1]),
                              ax.c2p(vals[i + 1][0], vals[i + 1][1]),
                              color=BLUE, stroke_width=4)
                         for i in range(len(vals) - 1)])
        pts = VGroup(*[Dot(ax.c2p(x, y), color=BLUE, radius=0.08)
                       for x, y in vals])
        self.play(LaggedStart(*[Create(l) for l in curve], run_time=1.6),
                  LaggedStart(*[FadeIn(p) for p in pts], run_time=1.6))
        drop = Text("drops fast at first...", font_size=19, color=GREEN,
                    font=MONO).move_to([ax.c2p(2, 8.6)[0], ax.c2p(2, 8.6)[1], 0])
        self.play(Write(drop), run_time=0.7)
        elbow = DashedLine(ax.c2p(3, 0), ax.c2p(3, 3.3), color=ACCENT,
                           stroke_width=2.5)
        ed = Dot(ax.c2p(3, 3.3), color=ACCENT, radius=0.12)
        el = Text("the elbow: K = 3", font_size=21, color=ACCENT, font=MONO
                  ).move_to([ax.c2p(4.6, 4.6)[0], ax.c2p(4.6, 4.6)[1], 0])
        self.play(Create(elbow), FadeIn(ed), Write(el), run_time=1.1)
        slow = Text("...then slows down: that bend picks K", font_size=19,
                    color=WHITE, opacity=0.6, font=MONO
                    ).move_to([ax.c2p(4.8, 1.4)[0], ax.c2p(4.8, 1.4)[1], 0])
        self.play(Write(slow), run_time=0.7)
        alt = Text("alternative: the silhouette score method", font_size=19,
                   color=WHITE, opacity=0.55, font=MONO).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(alt), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_InitSolutions(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("K-Means weakness: bad starts", "random init can land in a poor local minimum")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        # left: two centroids both in one blob
        blobA = [(-3.6, 1.2), (-2.8, 1.6), (-3.2, 0.6), (-2.5, 0.9)]
        blobB = [(2.6, -0.6), (3.4, -0.2), (3.0, -1.4)]
        dA = VGroup(*[Dot(np.array([x, y, 0.0]), color=WHITE, radius=0.09)
                      for x, y in blobA])
        dB = VGroup(*[Dot(np.array([x, y, 0.0]), color=WHITE, radius=0.09)
                      for x, y in blobB])
        c1 = Dot(np.array([-3.4, 1.0, 0.0]), color=RED, radius=0.14)
        c2 = Dot(np.array([-2.6, 1.2, 0.0]), color=RED, radius=0.14)
        self.play(FadeIn(dA), FadeIn(dB), run_time=0.7)
        self.play(FadeIn(c1, scale=2), FadeIn(c2, scale=2), run_time=0.7)
        bad = Text("unlucky start: both centroids\nin the same blob", font_size=19,
                   color=RED, font=MONO).move_to([-3.0, -1.0, 0])
        self.play(Write(bad), run_time=0.8)
        sols = VGroup(
            Text("1. run K-Means 10-50 times with different seeds,\n    keep the lowest inertia",
                 font_size=19, color=GREEN, font=MONO),
            Text("2. K-Means++ init: spread initial centroids out\n    to cover the space",
                 font_size=19, color=GREEN, font=MONO),
            Text("3. switch algorithms: Hierarchical or DBSCAN\n    need no random centroids",
                 font_size=19, color=GREEN, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.1, 0.4, 0])
        for ln in sols:
            self.play(FadeIn(ln, shift=LEFT * 0.3), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_Hierarchical(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Hierarchical clustering", "a tree of clusters: the dendrogram")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        xs = [-5.0, -4.0, -0.8, 0.4]
        y0 = -1.6
        dots = VGroup(*[Dot(np.array([x, y0, 0.0]), color=WHITE, radius=0.1)
                        for x in xs])
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots],
                              run_time=0.9))
        st1 = Text("start: every point is its own cluster", font_size=19,
                   color=WHITE, opacity=0.6, font=MONO
                   ).to_edge(DOWN, buff=0.5)
        self.play(Write(st1), run_time=0.7)
        m1 = VGroup(Line(np.array([xs[0], y0, 0]), np.array([xs[0], -0.6, 0]),
                         color=GREEN, stroke_width=3),
                    Line(np.array([xs[1], y0, 0]), np.array([xs[1], -0.6, 0]),
                         color=GREEN, stroke_width=3),
                    Line(np.array([xs[0], -0.6, 0]), np.array([xs[1], -0.6, 0]),
                         color=GREEN, stroke_width=3),
                    Line(np.array([(xs[0] + xs[1]) / 2, -0.6, 0]),
                         np.array([(xs[0] + xs[1]) / 2, -0.2, 0]),
                         color=GREEN, stroke_width=3))
        m2 = VGroup(Line(np.array([xs[2], y0, 0]), np.array([xs[2], -0.9, 0]),
                         color=BLUE, stroke_width=3),
                    Line(np.array([xs[3], y0, 0]), np.array([xs[3], -0.9, 0]),
                         color=BLUE, stroke_width=3),
                    Line(np.array([xs[2], -0.9, 0]), np.array([xs[3], -0.9, 0]),
                         color=BLUE, stroke_width=3),
                    Line(np.array([(xs[2] + xs[3]) / 2, -0.9, 0]),
                         np.array([(xs[2] + xs[3]) / 2, -0.5, 0]),
                         color=BLUE, stroke_width=3))
        st2 = Text("agglomerative (bottom-up): merge the closest pair,\nstep by step",
                   font_size=19, color=WHITE, opacity=0.6, font=MONO
                   ).to_edge(DOWN, buff=0.5)
        self.play(Create(m1), Create(m2), Transform(st1, st2), run_time=1.4)
        m3 = VGroup(Line(np.array([(xs[0] + xs[1]) / 2, -0.2, 0]),
                         np.array([(xs[0] + xs[1]) / 2, 0.9, 0]),
                         color=ACCENT, stroke_width=3),
                    Line(np.array([(xs[2] + xs[3]) / 2, -0.5, 0]),
                         np.array([(xs[2] + xs[3]) / 2, 0.9, 0]),
                         color=ACCENT, stroke_width=3),
                    Line(np.array([(xs[0] + xs[1]) / 2, 0.9, 0]),
                         np.array([(xs[2] + xs[3]) / 2, 0.9, 0]),
                         color=ACCENT, stroke_width=3))
        st3 = Text("no need to pre-specify K - cut the tree where you want",
                   font_size=19, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.5)
        self.play(Create(m3), Transform(st1, st3), run_time=1.3)
        side = VGroup(
            Text("divisive: top-down, split recursively", font_size=16,
                 color=WHITE, opacity=0.6, font=MONO),
            Text("linkage = how cluster distance is measured:",
                 font_size=16, color=WHITE, opacity=0.6, font=MONO),
            Text("single (min) - complete (max) - average", font_size=17,
                 color=BLUE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.6, 1.0, 0])
        self.play(FadeIn(side), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_DBSCAN(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("DBSCAN", "grow clusters from dense regions")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        core = [(-3.2, 0.8), (-2.6, 1.2), (-2.9, 0.2), (-2.2, 0.7)]
        border = [(-1.7, 1.3), (-1.6, 0.1)]
        noise = [(2.6, 1.4), (3.4, -0.9)]
        dC = VGroup(*[Dot(np.array([x, y, 0.0]), color=GREEN, radius=0.11)
                      for x, y in core])
        dB = VGroup(*[Dot(np.array([x, y, 0.0]), color=BLUE, radius=0.11)
                      for x, y in border])
        dN = VGroup(*[Dot(np.array([x, y, 0.0]), color=RED, radius=0.11)
                      for x, y in noise])
        eps = Circle(radius=1.05, color=ACCENT, stroke_width=2, stroke_opacity=0.7
                     ).move_to(np.array([-2.9, 0.7, 0.0]))
        le = Text("eps: neighborhood radius", font_size=18, color=ACCENT,
                  font=MONO).move_to([-2.9, 2.15, 0])
        self.play(FadeIn(dC), run_time=0.7)
        self.play(Create(eps), FadeIn(le), run_time=0.9)
        l1 = Text("CORE point: >= minPts neighbors inside eps -\nforms and expands clusters",
                  font_size=19, color=GREEN, font=MONO).move_to([2.6, 0.9, 0])
        self.play(Write(l1), run_time=0.9)
        self.play(FadeIn(dB), run_time=0.6)
        l2 = Text("BORDER point: inside eps of a core, but too sparse\nto expand - smooths cluster edges",
                  font_size=19, color=BLUE, font=MONO).move_to([2.6, -0.1, 0])
        self.play(Write(l2), run_time=0.9)
        self.play(FadeIn(dN), run_time=0.6)
        l3 = Text("NOISE: neither core nor border - an outlier",
                  font_size=19, color=RED, font=MONO).move_to([2.6, -1.1, 0])
        self.play(Write(l3), run_time=0.9)
        cap = Text("two parameters: eps + minPts - finds arbitrary shapes\nand flags outliers",
                   font_size=20, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.45)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_HardSoft(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Hard vs soft clustering", "one cluster each, or a probability mix?")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        h = VGroup(
            Text("HARD clustering", font_size=26, color=BLUE, weight=BOLD,
                 font=MONO),
            Text("each point belongs to exactly one cluster\n(or is marked noise in DBSCAN)",
                 font_size=19, color=WHITE, font=MONO),
            Text("K-Means - Hierarchical - DBSCAN", font_size=20, color=BLUE,
                 font=MONO),
        ).arrange(DOWN, buff=0.4).move_to([-3.5, 0.6, 0])
        sd = VGroup(
            Text("SOFT clustering", font_size=26, color=ACCENT, weight=BOLD,
                 font=MONO),
            Text("each point can belong to multiple clusters\nwith probabilities",
                 font_size=19, color=WHITE, font=MONO),
            Text("Gaussian Mixture Models (GMM)", font_size=20, color=ACCENT,
                 font=MONO),
        ).arrange(DOWN, buff=0.4).move_to([3.5, 0.6, 0])
        line = Line([0, 2.3, 0], [0, -1.4, 0], stroke_width=1.5, stroke_opacity=0.2)
        self.play(Create(line), run_time=0.5)
        self.play(FadeIn(h, shift=RIGHT * 0.3), run_time=1.0)
        self.play(FadeIn(sd, shift=LEFT * 0.3), run_time=1.0)
        note = Text("flexible shape does not mean soft: Hierarchical and DBSCAN\nstill assign points deterministically -> hard",
                    font_size=18, color=WHITE, opacity=0.6, font=MONO
                    ).to_edge(DOWN, buff=0.5)
        self.play(Write(note), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L182_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, _ = title_block("Lecture 18.2 in one breath", "")
        self.play(Write(t), run_time=0.9)
        lines = VGroup(
            Text("unsupervised: find hidden structure in unlabeled data",
                 font_size=22, color=WHITE, font=MONO),
            Text("cluster goal: intra-cluster small, inter-cluster large",
                 font_size=22, color=WHITE, font=MONO),
            Text("K-Means: init, assign, average, repeat -> minimize WCSS",
                 font_size=22, color=BLUE, font=MONO),
            Text("pick K with the elbow (or silhouette); beware bad inits",
                 font_size=22, color=WHITE, font=MONO),
            Text("Hierarchical: dendrogram, no K - DBSCAN: eps + minPts, noise",
                 font_size=22, color=WHITE, font=MONO),
            Text("hard = one cluster per point; soft = probabilities (GMM)",
                 font_size=22, color=ACCENT, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(2.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
