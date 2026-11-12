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


class L16_Title(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("How to Do Classification", "CMSC 320 - lecture 16")
        self.play(Write(t), run_time=1.3)
        self.play(FadeIn(s, shift=DOWN * 0.2), run_time=0.7)
        self.wait(0.8)
        core = Text("three classifiers, one toolbox", font_size=30,
                    color=ACCENT, weight=BOLD, font=MONO)
        self.play(FadeOut(s), Write(core), run_time=1.3)
        self.wait(1.0)
        steps = ["acquire", "explore", "clean", "feature\nengineer", "train",
                 "test", "iterate", "present"]
        nodes = VGroup()
        for i, name in enumerate(steps):
            col = GREEN if name in ("train", "test") else BLUE
            b = box(name, 1.55, 0.95, col, 15)
            b.move_to([-5.9 + 1.7 * i, -0.9, 0])
            nodes.add(b)
        self.play(LaggedStart(*[FadeIn(b, scale=0.7) for b in nodes],
                              lag_ratio=0.12, run_time=1.6))
        methods = Text("today, inside train + test: Naive Bayes - SVM - Random Forest",
                       font_size=19, color=WHITE, opacity=0.7, font=MONO
                       ).to_edge(DOWN, buff=0.55)
        self.play(Write(methods), run_time=1.0)
        self.wait(1.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L16_NB(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Naive Bayes", "Bayes theorem + one naive assumption")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        bayes = Text("P(y | X) = P(y) * P(X | y) / P(X)", font_size=28,
                     color=BLUE, font=MONO).move_to([0, 1.6, 0])
        self.play(Write(bayes), run_time=1.1)
        steps = VGroup(
            Text("1. start from Bayes theorem (y = class, X = features)",
                 font_size=19, color=WHITE, font=MONO),
            Text("2. expand P(X | y) assuming features are INDEPENDENT",
                 font_size=19, color=WHITE, font=MONO),
            Text("3. drop P(X): same constant for every class", font_size=19,
                 color=WHITE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-1.2, 0.1, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in steps],
                              run_time=1.6))
        rule = Text("predict y that MAXIMIZES  P(y) * prod P(x_i | y)",
                    font_size=22, color=ACCENT, font=MONO
                    ).move_to([0, -1.35, 0])
        naive = Text("the 'naive' part: features independent GIVEN the class",
                     font_size=19, color=RED, font=MONO
                     ).to_edge(DOWN, buff=0.55)
        self.play(Write(rule), run_time=1.0)
        self.play(Write(naive), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L16_NBAssumptions(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Four assumptions", "what Naive Bayes takes on faith")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        items = [
            ("1 feature independence", "all features independent given class y"),
            ("2 equal importance", "every feature counts the same"),
            ("3 gaussian continuous", "continuous attributes ~ normal per class"),
            ("4 no missing data", "the dataset must be complete"),
        ]
        rows = VGroup()
        for name, desc in items:
            pair = VGroup(
                Text(name, font_size=20, color=BLUE, font=MONO),
                Text(desc, font_size=18, color=WHITE, opacity=0.75,
                     font=MONO),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            rows.add(pair)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([-2.6, 0.3, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows],
                              run_time=1.8))
        golf = VGroup(
            Text("golf example", font_size=20, color=GREEN, weight=BOLD,
                 font=MONO),
            Text("'Hot' does not imply 'High Humidity'\n-> independence assumed",
                 font_size=17, color=WHITE, font=MONO),
            Text("Wind counts as much as Outlook\n-> equal importance",
                 font_size=17, color=WHITE, font=MONO),
        ).arrange(DOWN, buff=0.4).move_to([3.7, 0.3, 0])
        self.play(LaggedStart(*[FadeIn(g, shift=LEFT * 0.2) for g in golf],
                              run_time=1.5))
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L16_NBText(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Naive Bayes on text", "sports or not?")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        task = Text('new text: "A very close game" -> Sports or Non-Sports?',
                    font_size=21, color=ACCENT, font=MONO
                    ).move_to([0, 1.55, 0])
        self.play(Write(task), run_time=1.0)
        docs = VGroup(
            Text("doc1  Sports", font_size=19, color=GREEN, font=MONO),
            Text("doc2  Sports", font_size=19, color=GREEN, font=MONO),
            Text("doc3  Sports", font_size=19, color=GREEN, font=MONO),
            Text("doc4  Non-Sports", font_size=19, color=RED, font=MONO),
            Text("doc5  Non-Sports", font_size=19, color=RED, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-4.0, -0.1, 0])
        self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 0.2) for d in docs],
                              run_time=1.2))
        right = VGroup(
            Text("each WORD is a feature", font_size=19, color=BLUE, font=MONO),
            Text("prior: P(Sports) = 3/5", font_size=19, color=GREEN,
                 font=MONO),
            Text("prior: P(Non) = 2/5", font_size=19, color=RED, font=MONO),
            Text("likelihood: count the words\nunder each label", font_size=18,
                 color=WHITE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([2.6, -0.1, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in right],
                              run_time=1.5))
        cap = Text("why NB loves text: high dimension, one feature per word\n(spam filtering, sentiment analysis)",
                   font_size=18, color=WHITE, opacity=0.6, font=MONO
                   ).to_edge(DOWN, buff=0.5)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L16_Laplace(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Zero counts + Laplace smoothing", "did you see any issue?")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        prod = VGroup(
            Text("P(Sports) * P(a given S) * P(very given S)\n"
                 "           * P(close given S) * P(game given S)",
                 font_size=20, color=GREEN, font=MONO),
            Text("P(Non) * P(a given N) * P(very given N)\n"
                 "           * P(close given N) * P(game given N)",
                 font_size=20, color=RED, font=MONO),
        ).arrange(DOWN, buff=0.3).move_to([0, 1.55, 0])
        self.play(Write(prod[0]), run_time=0.8)
        self.play(Write(prod[1]), run_time=0.8)
        zero = Text("'close' never appears in Non-Sports: P(close | Non) = 0/9 = 0\none zero factor kills the ENTIRE product",
                    font_size=19, color=ACCENT, font=MONO).move_to([0, -0.05, 0])
        self.play(Write(zero), run_time=1.2)
        formula = Text("Laplace: P(word | class) = (count + 1) / (total + V)",
                       font_size=24, color=BLUE, font=MONO
                       ).move_to([0, -1.3, 0])
        self.play(Write(formula), run_time=1.1)
        ex = Text("V = 14 unique words -> P(close | Non) = (0+1)/(9+14) = 1/23\nevery word keeps a NON-ZERO probability",
                  font_size=19, color=WHITE, font=MONO
                  ).to_edge(DOWN, buff=0.5)
        self.play(Write(ex), run_time=1.1)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L16_SVM(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Support Vector Machines", "find the widest street")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = Axes(x_range=[0, 8, 2], y_range=[0, 8, 2], x_length=6.2,
                  y_length=4.4, axis_config={"stroke_opacity": 0.15,
                                             "include_ticks": False},
                  ).shift(LEFT * 2.4 + DOWN * 0.3)
        self.play(Create(ax), run_time=0.8)
        rng = np.random.default_rng(3)
        greens = [(x, y) for x, y in zip(rng.uniform(0.8, 3.0, 6),
                                         rng.uniform(4.8, 7.2, 6))]
        reds = [(x, y) for x, y in zip(rng.uniform(5.0, 7.4, 6),
                                       rng.uniform(0.8, 3.2, 6))]
        gd = VGroup(*[Dot(ax.c2p(x, y), color=GREEN, radius=0.09)
                      for x, y in greens])
        rd = VGroup(*[Dot(ax.c2p(x, y), color=RED, radius=0.09)
                      for x, y in reds])
        self.play(FadeIn(gd), FadeIn(rd), run_time=0.9)
        bad = DashedLine(ax.c2p(0.5, 6.5), ax.c2p(7.5, 1.0), color=WHITE,
                         stroke_width=2, stroke_opacity=0.35)
        self.play(Create(bad), run_time=0.7)
        q = Text("many lines separate the data -\nwhich one?", font_size=19,
                 color=WHITE, opacity=0.6, font=MONO).move_to([3.9, 2.0, 0])
        self.play(Write(q), run_time=0.8)
        good = Line(ax.c2p(1.5, 7.5), ax.c2p(7.5, 1.5), color=ACCENT,
                    stroke_width=4)
        off1 = Line(ax.c2p(0.2, 6.2), ax.c2p(6.2, 0.2), color=ACCENT,
                    stroke_width=2, stroke_opacity=0.6)
        off2 = Line(ax.c2p(3.0, 8.0), ax.c2p(8.0, 3.0), color=ACCENT,
                    stroke_width=2, stroke_opacity=0.6)
        self.play(Create(good), run_time=0.9)
        self.play(Create(off1), Create(off2), run_time=0.9)
        sv1 = Circle(radius=0.16, color=BLUE, stroke_width=2.5
                     ).move_to(ax.c2p(3.0, 5.6))
        sv2 = Circle(radius=0.16, color=BLUE, stroke_width=2.5
                     ).move_to(ax.c2p(5.2, 3.4))
        self.play(FadeIn(sv1), FadeIn(sv2), run_time=0.7)
        cap = Text("maximize the MARGIN; support vectors = points\nclosest to the boundary w*x + b = 0",
                   font_size=19, color=ACCENT, font=MONO
                   ).to_edge(DOWN, buff=0.45)
        self.play(Write(cap), run_time=1.1)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L16_Hyperplane(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("What is a hyperplane?", "a boundary one dimension lower")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        rows = VGroup(
            Text("2D feature space -> a LINE", font_size=22, color=GREEN,
                 font=MONO),
            Text("y = m*x + b", font_size=20, color=WHITE, font=MONO),
            Text("3D feature space -> a PLANE", font_size=22, color=BLUE,
                 font=MONO),
            Text("x + 3y - 2z = 5", font_size=20, color=WHITE, font=MONO),
            Text("N features -> hyperplane in N-D", font_size=22, color=RED,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([-2.8, 0.2, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows],
                              run_time=1.8))
        flat = VGroup(
            Text("flat surface, one dimension\nlower than the feature space",
                 font_size=19, color=WHITE, font=MONO),
            Text("it splits the space into\ntwo regions", font_size=19,
                 color=WHITE, font=MONO),
        ).arrange(DOWN, buff=0.5).move_to([3.4, 0.4, 0])
        self.play(LaggedStart(*[FadeIn(f, shift=LEFT * 0.2) for f in flat],
                              run_time=1.2))
        cap = Text("larger margin = better generalization: a wide buffer\nzone survives noise that would flip a tight boundary",
                   font_size=19, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.5)
        self.play(Write(cap), run_time=1.1)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L16_Multiclass(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("More than 2 classes?", "SVM is binary - so compose it")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        # one-vs-all
        ova = Text("ONE-VS-ALL: 3 classifiers", font_size=20, color=BLUE,
                   weight=BOLD, font=MONO).move_to([-3.9, 1.7, 0])
        ova_rows = VGroup()
        for i, (a, b) in enumerate([("A", "not A"), ("B", "not B"),
                                    ("C", "not C")]):
            acol = GREEN if a == "A" else (RED if a == "B" else BLUE)
            r = VGroup(
                Text(a, font_size=18, color=acol, font=MONO),
                Text("vs", font_size=18, color=WHITE, font=MONO),
                Text(b, font_size=18, color=WHITE, font=MONO),
            ).arrange(RIGHT, buff=0.45).move_to([-3.9, 0.9 - 0.55 * i, 0])
            ova_rows.add(r)
        self.play(Write(ova), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(r) for r in ova_rows], run_time=1.0))
        # one-vs-one
        ovo = Text("ONE-VS-ONE: 3 pairs", font_size=20, color=GREEN,
                   weight=BOLD, font=MONO).move_to([0.6, 1.7, 0])
        ovo_rows = VGroup()
        for i, (a, b) in enumerate([("A", "B"), ("A", "C"), ("B", "C")]):
            acol = GREEN if a == "A" else (RED if a == "B" else BLUE)
            bcol = GREEN if b == "A" else (RED if b == "B" else BLUE)
            r = VGroup(
                Text(a, font_size=18, color=acol, font=MONO),
                Text("vs", font_size=18, color=WHITE, font=MONO),
                Text(b, font_size=18, color=bcol, font=MONO),
            ).arrange(RIGHT, buff=0.45).move_to([0.6, 0.9 - 0.55 * i, 0])
            ovo_rows.add(r)
        self.play(Write(ovo), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(r) for r in ovo_rows], run_time=1.0))
        # multiclass diagram: 3-class regions
        mc = Text("MULTICLASS REGIONS", font_size=20, color=ACCENT,
                  weight=BOLD, font=MONO).move_to([4.2, 1.7, 0])
        tri = VGroup(
            Polygon(np.array([4.2, 1.1, 0]), np.array([3.2, -0.6, 0]),
                    np.array([5.2, -0.6, 0]), color=GREEN, stroke_width=2,
                    fill_color=GREEN, fill_opacity=0.25),
            Polygon(np.array([3.2, -0.6, 0]), np.array([5.2, -0.6, 0]),
                    np.array([4.2, -1.9, 0]), color=RED, stroke_width=2,
                    fill_color=RED, fill_opacity=0.25),
        )
        lab = VGroup(
            Text("A", font_size=17, color=GREEN, font=MONO).move_to([4.2, 0.35, 0]),
            Text("B", font_size=17, color=RED, font=MONO).move_to([4.2, -1.15, 0]),
        )
        self.play(Write(mc), run_time=0.7)
        self.play(Create(tri[0]), Create(tri[1]), FadeIn(lab), run_time=1.0)
        cap = Text("n classes: one-vs-all needs n models, one-vs-one needs n(n-1)/2\nthe winning vote decides the label",
                   font_size=19, color=WHITE, font=MONO).to_edge(DOWN, buff=0.5)
        self.play(Write(cap), run_time=1.1)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L16_Kernel(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The kernel trick", "when no straight line will do")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        # 1D: - - + - + + on a line
        ax = NumberLine(x_range=[-3.5, 3.5, 1], length=6.0,
                        include_ticks=False).move_to([-3.6, 0.6, 0])
        ax.set_stroke(opacity=0.25)
        xs = [(-2.5, RED), (-1.5, RED), (-0.5, RED), (0.8, GREEN),
              (1.8, GREEN), (2.6, GREEN)]
        dots1 = VGroup(*[Dot(ax.number_to_point(x), color=c, radius=0.1)
                         for x, c in xs])
        h1 = Text("1D: red -2..-0.5, green +0.8..+2.6", font_size=17,
                  color=WHITE, opacity=0.6, font=MONO
                  ).move_to([-3.6, 1.9, 0])
        self.play(Write(h1), Create(ax), FadeIn(dots1), run_time=1.2)
        no = Text("no single point separates them", font_size=18, color=RED,
                  font=MONO).move_to([-3.6, -0.5, 0])
        self.play(Write(no), run_time=0.7)
        # parabola view
        pax = Axes(x_range=[-3, 3, 1], y_range=[-1, 7, 2], x_length=4.6,
                   y_length=3.6, axis_config={"stroke_opacity": 0.2,
                                              "include_ticks": False},
                   ).move_to([3.4, -0.1, 0])
        parab = pax.plot(lambda x: x * x, color=BLUE, stroke_width=3)
        pts2 = VGroup(*[Dot(pax.c2p(x, x * x), color=c, radius=0.1)
                        for x, c in xs])
        cut = DashedLine(pax.c2p(-3, 1.0), pax.c2p(3, 1.0), color=ACCENT,
                         stroke_width=3)
        h2 = Text("lift with y = x^2", font_size=17, color=BLUE, font=MONO
                  ).move_to([3.4, 1.9, 0])
        self.play(Write(h2), Create(pax), Create(parab), FadeIn(pts2),
                  run_time=1.4)
        self.play(Create(cut), run_time=0.7)
        cap = Text("kernel trick: map to higher-D where a hyperplane works;\nkernels compute inner products WITHOUT computing the map -> fast",
                   font_size=18, color=ACCENT, font=MONO
                   ).to_edge(DOWN, buff=0.45)
        self.play(Write(cap), run_time=1.2)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L16_Overfit(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Overfit vs underfit", "the two ways a model breaks")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        left = VGroup(
            Text("OVERFITTING", font_size=22, color=RED, weight=BOLD,
                 font=MONO),
            Text("KNN k=1: memorizes, hypersensitive\nto noise (high variance)",
                 font_size=18, color=WHITE, font=MONO),
            Text("decision trees: the WORST offenders -\nthey use every scrap of data",
                 font_size=18, color=WHITE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.4, 0.9, 0])
        right = VGroup(
            Text("UNDERFITTING", font_size=22, color=BLUE, weight=BOLD,
                 font=MONO),
            Text("KNN k=N: everyone votes, misses local\npatterns (high bias)",
                 font_size=18, color=WHITE, font=MONO),
            Text("too simple to capture structure", font_size=18, color=WHITE,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, 0.9, 0])
        self.play(FadeIn(left, shift=RIGHT * 0.3), run_time=1.2)
        self.play(FadeIn(right, shift=LEFT * 0.3), run_time=1.2)
        fixes = Text("fixes: tune hyperparameters (K), depth limits / early\nstopping, pruning, or ensembles of trees",
                     font_size=19, color=ACCENT, font=MONO
                     ).to_edge(DOWN, buff=0.55)
        self.play(Write(fixes), run_time=1.1)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L16_Bagging(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Bagging + Random Forest", "many trees, one vote")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        data = box("one dataset", 2.2, 0.8, BLUE, 17).move_to([-5.0, 1.3, 0])
        boots = VGroup(*[box(f"bootstrap {i+1}", 1.9, 0.62, BLUE, 13)
                         for i in range(3)])
        for i, b in enumerate(boots):
            b.move_to([-2.2, 1.9 - 0.8 * i, 0])
        trees = VGroup(*[box(f"tree {i+1}", 1.5, 0.62, GREEN, 13)
                         for i in range(3)])
        for i, tr in enumerate(trees):
            tr.move_to([0.6, 1.9 - 0.8 * i, 0])
        vote = box("majority vote /\naverage", 2.0, 0.9, ACCENT, 15
                   ).move_to([3.6, 0.7, 0])
        self.play(Write(data), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(b) for b in boots], run_time=0.9))
        self.play(LaggedStart(*[FadeIn(tr) for tr in trees], run_time=0.9))
        self.play(FadeIn(vote), run_time=0.7)
        arrows = VGroup(
            Arrow(data.get_right(), boots[1].get_left(), stroke_width=2,
                  stroke_opacity=0.5, color=WHITE,
                  max_tip_length_to_length_ratio=0.2),
            Arrow(boots[0].get_right(), trees[0].get_left(), stroke_width=2,
                  stroke_opacity=0.5, color=WHITE,
                  max_tip_length_to_length_ratio=0.25),
            Arrow(trees[1].get_right(), vote.get_left(), stroke_width=2,
                  stroke_opacity=0.5, color=WHITE,
                  max_tip_length_to_length_ratio=0.25),
        )
        self.play(Create(arrows), run_time=0.9)
        pts = VGroup(
            Text("bootstrap = sample WITH replacement\n(some repeat, some left out = OOB)",
                 font_size=17, color=WHITE, font=MONO),
            Text("random feature subsets per split ->\ndiverse trees", font_size=17,
                 color=GREEN, font=MONO),
            Text("noisy trees get outvoted -> less\noverfitting (N trees = hyperparameter)",
                 font_size=17, color=ACCENT, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(p) for p in pts], run_time=1.5))
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L16_Boosting(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Boosting", "each model fixes the last one's mistakes")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        m1 = box("weak model 1", 2.2, 0.75, BLUE, 16).move_to([-4.4, 1.2, 0])
        m2 = box("weak model 2", 2.2, 0.75, BLUE, 16).move_to([-0.6, 1.2, 0])
        m3 = box("weak model 3", 2.2, 0.75, BLUE, 16).move_to([3.2, 1.2, 0])
        a1 = Arrow(m1.get_right(), m2.get_left(), stroke_width=3, color=ACCENT,
                   max_tip_length_to_length_ratio=0.25)
        a2 = Arrow(m2.get_right(), m3.get_left(), stroke_width=3, color=ACCENT,
                   max_tip_length_to_length_ratio=0.25)
        err = Text("focus on misclassified points", font_size=17, color=RED,
                   font=MONO).move_to([-2.5, 0.45, 0])
        err2 = Text("focus harder still", font_size=17, color=RED, font=MONO
                    ).move_to([1.3, 0.45, 0])
        self.play(Write(m1), run_time=0.6)
        self.play(Create(a1), Write(m2), FadeIn(err), run_time=0.9)
        self.play(Create(a2), Write(m3), FadeIn(err2), run_time=0.9)
        pts = VGroup(
            Text("SEQUENTIAL training, weighted voting", font_size=20,
                 color=WHITE, font=MONO),
            Text("reduces BIAS (bagging reduces variance)", font_size=20,
                 color=ACCENT, font=MONO),
            Text("examples: AdaBoost, GBM, XGBoost, LightGBM", font_size=18,
                 color=BLUE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-0.6, -1.0, 0])
        self.play(LaggedStart(*[FadeIn(p) for p in pts], run_time=1.4))
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L16_Eval(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Compare models fairly", "same split, same metrics")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        code = VGroup(
            Text('models = {"Logistic": logreg, "Naive Bayes": nb,',
                 font_size=19, color=BLUE, font=MONO),
            Text('          "SVM": svm, "Random Forest": rf}', font_size=19,
                 color=BLUE, font=MONO),
            Text("for name, model in models.items():", font_size=19,
                 color=GREEN, font=MONO),
            Text("    model.fit(X_train, y_train)", font_size=19, color=WHITE,
                 font=MONO),
            Text("    pred = model.predict(X_test)", font_size=19, color=WHITE,
                 font=MONO),
            Text("    # accuracy + macro F1 for every model", font_size=19,
                 color=ACCENT, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-0.8, 0.4, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code],
                              run_time=1.8))
        cap = Text("always evaluate on a held-out set or cross-validation",
                   font_size=20, color=ACCENT, font=MONO
                   ).to_edge(DOWN, buff=0.6)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L16_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, _ = title_block("Lecture 16 in one breath", "")
        self.play(Write(t), run_time=0.9)
        def seg(*parts):
            return VGroup(*[Text(p, font_size=21, color=c, font=MONO)
                            for p, c in parts]).arrange(RIGHT, buff=0.02)
        lines = VGroup(
            seg(("Naive Bayes: priors x ", WHITE),
                ("independent likelihoods", GREEN)),
            seg(("Laplace smoothing", ACCENT),
                (" rescues zero counts: (c+1)/(n+V)", WHITE)),
            seg(("SVM: ", WHITE), ("max-margin hyperplane", BLUE),
                ("; kernels bend the space", WHITE)),
            seg(("multiclass: one-vs-all (n models) or one-vs-one (n(n-1)/2)",
                 WHITE)),
            seg(("ensembles: bagging cuts variance, ", WHITE),
                ("boosting cuts bias", RED)),
            seg(("validate on held-out data - always", WHITE)),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(2.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
