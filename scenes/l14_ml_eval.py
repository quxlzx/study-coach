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


def hl(t, a, b, col):
    # Text submobjects skip spaces, so string slices must be re-indexed
    src = t.original_text
    sa = a - src[:a].count(" ") - src[:a].count("\n")
    sb = b - src[:b].count(" ") - src[:b].count("\n")
    t[sa:sb].set_color(col)


class L14_Title(Scene):
    def construct(self):
        self.camera.background_color = BG
        t = Text("ML Model Evaluation", font_size=44, color=BLUE, weight=BOLD,
                 font=MONO).to_edge(UP, buff=0.8)
        s = Text("CMSC 320 - lecture 14 - from overfitting to reliable predictions",
                 font_size=20, color=WHITE, opacity=0.5, font=MONO
                 ).next_to(t, DOWN, buff=0.3)
        self.play(Write(t), run_time=1.4)
        self.play(FadeIn(s, shift=DOWN * 0.2), run_time=0.7)
        self.wait(0.8)
        core = Text("a model is only as good as its UNSEEN data score",
                    font_size=28, color=ACCENT, weight=BOLD, font=MONO)
        self.play(FadeOut(s), Write(core), run_time=1.4)
        self.wait(1.2)
        agenda = VGroup(
            box("FIT", 1.6, 0.8, BLUE, 22),
            Text("over/underfit,\nbias-variance", font_size=15, color=WHITE,
                 opacity=0.6, font=MONO),
            box("EVALUATE", 2.2, 0.8, GREEN, 22),
            Text("splits,\ncross-validation", font_size=15, color=WHITE,
                 opacity=0.6, font=MONO),
            box("MEASURE", 2.2, 0.8, ACCENT, 22),
            Text("accuracy, precision,\nrecall, F1, log loss", font_size=15,
                 color=WHITE, opacity=0.6, font=MONO),
        )
        pairs = VGroup(agenda[0:2], agenda[2:4], agenda[4:6])
        for p in pairs:
            p.arrange(DOWN, buff=0.25)
        pairs.arrange(RIGHT, buff=1.6).to_edge(DOWN, buff=0.7)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.3) for p in pairs],
                              run_time=1.6))
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L14_Overfit(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Overfitting", "memorizing instead of learning")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1], x_length=5.2,
                  y_length=3.6, axis_config={"stroke_opacity": 0.15,
                                             "include_ticks": False}
                  ).move_to([-3.3, 0.2, 0])
        pts = VGroup(*[Dot(ax.c2p(x, 2.2 + 0.45 * x + 0.55 * np.sin(2.5 * x)),
                           color=WHITE, radius=0.07)
                       for x in np.arange(0.5, 4.8, 0.42)])
        wiggle = ax.plot(lambda x: 2.2 + 0.45 * x + 0.55 * np.sin(2.5 * x)
                         + 0.5 * np.sin(9 * x), color=RED, stroke_width=3)
        trend = ax.plot(lambda x: 2.2 + 0.45 * x, color=GREEN, stroke_width=3,
                        stroke_opacity=0.7)
        self.play(Create(ax), FadeIn(pts), run_time=0.9)
        self.play(Create(wiggle), run_time=1.3)
        cap = Text("twists through every point -\nincluding the noise",
                   font_size=18, color=RED, font=MONO
                   ).move_to([-3.3, -2.2, 0])
        self.play(Create(trend), FadeIn(cap), run_time=1.0)
        right = VGroup(
            Text("learns training data TOO closely,\nnoise included",
                 font_size=20, color=WHITE, font=MONO),
            Text("great on TRAIN, poor on NEW data", font_size=20, color=RED,
                 font=MONO),
            Text("causes: noisy data | too complex |\ntoo little data",
                 font_size=18, color=WHITE, opacity=0.6, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.4, 0.6, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in right],
                              run_time=1.8))
        fix = Text("fix: more diverse data - cross-validation - simplify / regularize",
                   font_size=19, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.45)
        self.play(Write(fix), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L14_Underfit(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Underfitting", "when the model is too simple")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1], x_length=5.2,
                  y_length=3.6, axis_config={"stroke_opacity": 0.15,
                                             "include_ticks": False}
                  ).move_to([-3.3, 0.2, 0])
        pts = VGroup(*[Dot(ax.c2p(x, 0.9 + 0.7 * x + 0.55 * np.sin(2.5 * x)),
                           color=WHITE, radius=0.07)
                       for x in np.arange(0.5, 4.8, 0.42)])
        flat = ax.plot(lambda x: 2.4 + 0.25 * x, color=RED, stroke_width=3)
        self.play(Create(ax), FadeIn(pts), run_time=0.9)
        self.play(Create(flat), run_time=0.9)
        cap = Text("a straight line through a curved truth:\nmisses the pattern, poor on TRAIN and TEST",
                   font_size=18, color=RED, font=MONO
                   ).move_to([-3.3, -2.2, 0])
        self.play(Write(cap), run_time=1.1)
        right = VGroup(
            Text("fails to capture important patterns", font_size=20,
                 color=WHITE, font=MONO),
            Text("poor on BOTH training and new data", font_size=20,
                 color=RED, font=MONO),
            Text("example: admissions decided\nby GPA alone", font_size=18,
                 color=WHITE, opacity=0.6, font=MONO),
            Text("causes: too simple | missed features", font_size=18,
                 color=WHITE, opacity=0.6, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.4, 0.5, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in right],
                              run_time=1.8))
        fix = Text("fix: raise complexity - more layers/neurons, higher polynomial degree",
                   font_size=19, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.45)
        self.play(Write(fix), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L14_BiasVariance(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Bias vs variance", "the two ways a model can be wrong")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        line = Line([0, 2.1, 0], [0, -1.6, 0], stroke_width=1.5,
                    stroke_opacity=0.2)
        self.play(Create(line), run_time=0.4)
        bias = VGroup(
            Text("BIAS", font_size=26, color=BLUE, weight=BOLD, font=MONO),
            Text("error from approximating a complex\nworld with a SIMPLIFIED model",
                 font_size=18, color=WHITE, font=MONO),
            Text("how far predictions sit from the\nactual (expected) values",
                 font_size=17, color=WHITE, opacity=0.6, font=MONO),
            Text("HIGH bias -> oversimplified ->\nunderfits", font_size=18,
                 color=RED, font=MONO),
        ).arrange(DOWN, buff=0.42).move_to([-3.5, 0.15, 0])
        var = VGroup(
            Text("VARIANCE", font_size=26, color=GREEN, weight=BOLD,
                 font=MONO),
            Text("error from being overly sensitive to\nfluctuations in the training set",
                 font_size=18, color=WHITE, font=MONO),
            Text("spread of predictions for one point\nacross different training subsets",
                 font_size=17, color=WHITE, opacity=0.6, font=MONO),
            Text("HIGH variance -> too complex ->\noverfits: great train, poor test",
                 font_size=18, color=RED, font=MONO),
        ).arrange(DOWN, buff=0.42).move_to([3.5, 0.15, 0])
        self.play(FadeIn(bias, shift=RIGHT * 0.3), run_time=1.4)
        self.play(FadeIn(var, shift=LEFT * 0.3), run_time=1.4)
        cap = Text("we minimize error on train AND validation: the tradeoff",
                   font_size=20, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.45)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L14_SeeDiff(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("See the difference", "same data, three models")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        xs = np.arange(0.5, 4.6, 0.45)
        ys = 1.2 + 0.6 * xs + 0.6 * np.sin(2.2 * xs)

        def panel(x0, name, note, col, f):
            ax = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1], x_length=3.4,
                      y_length=2.6, axis_config={"stroke_opacity": 0.15,
                                                 "include_ticks": False}
                      ).move_to([x0, 0.15, 0])
            pts = VGroup(*[Dot(ax.c2p(x, y), color=WHITE, radius=0.055)
                           for x, y in zip(xs, ys)])
            curve = ax.plot(f, color=col, stroke_width=3)
            head = Text(name, font_size=21, color=col, weight=BOLD, font=MONO
                        ).move_to([x0, 2.15, 0])
            foot = Text(note, font_size=15, color=WHITE, opacity=0.55,
                        font=MONO).move_to([x0, -1.85, 0])
            return VGroup(ax, pts, curve, head, foot)

        p1 = panel(-4.5, "UNDERFIT", "misses patterns", BLUE,
                   lambda x: 2.6 + 0.2 * x)
        p2 = panel(0.0, "GOOD FIT", "learns useful structure", GREEN,
                   lambda x: 1.2 + 0.6 * x + 0.6 * np.sin(2.2 * x))
        p3 = panel(4.5, "OVERFIT", "follows noise", RED,
                   lambda x: 1.2 + 0.6 * x + 0.6 * np.sin(2.2 * x)
                   + 0.45 * np.sin(8.5 * x))
        for p in (p1, p2, p3):
            self.play(Create(p[0]), FadeIn(p[1]), run_time=0.7)
            self.play(Create(p[2]), Write(p[3]), FadeIn(p[4]), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L14_Diagnosis(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Diagnose the error", "train vs test tells you which fix")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        cells = VGroup(
            box("high bias\nlow variance\n(underfit)", 3.0, 1.35, BLUE, 17),
            box("low bias\nlow variance\nIDEAL", 3.0, 1.35, GREEN, 17),
            box("high bias\nhigh variance\n(worst)", 3.0, 1.35, RED, 17),
            box("low bias\nhigh variance\n(overfit)", 3.0, 1.35, RED, 17),
        ).arrange_in_grid(rows=2, cols=2, buff=0.5).move_to([-3.1, -0.05, 0])
        yl = Text("test error HIGH / LOW", font_size=15, color=WHITE,
                  opacity=0.45, font=MONO).move_to([-6.35, -0.05, 0]).rotate(PI / 2)
        xl = Text("training error HIGH -> LOW", font_size=15, color=WHITE,
                  opacity=0.45, font=MONO).move_to([-3.1, -1.95, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in cells],
                              run_time=1.8), FadeIn(yl), FadeIn(xl))
        bayes = Text("even the best model can't beat the\nBayes error (here ~0%: human error)",
                     font_size=16, color=WHITE, opacity=0.55, font=MONO
                     ).move_to([-3.1, 1.95, 0])
        self.play(FadeIn(bayes), run_time=0.8)
        rec = VGroup(
            Text("RECIPE", font_size=21, color=ACCENT, weight=BOLD,
                 font=MONO),
            Text("training looks bad (HIGH BIAS)?", font_size=18, color=WHITE,
                 font=MONO),
            Text("-> bigger network, train longer", font_size=18, color=BLUE,
                 font=MONO),
            Text("test looks bad (HIGH VARIANCE)?", font_size=18, color=WHITE,
                 font=MONO),
            Text("-> more data, regularization", font_size=18, color=GREEN,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([3.6, 0.15, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in rec],
                              run_time=2.0))
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L14_Holdout(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Holdout: train / validate / test", "hide data to test honestly")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        bar = Rectangle(width=9.6, height=0.85, stroke_width=2,
                        stroke_color=WHITE, stroke_opacity=0.4).move_to([0, 1.7, 0])
        segs = VGroup(
            Rectangle(width=5.8, height=0.85, fill_color=GREEN,
                      fill_opacity=0.35, stroke_width=0).move_to([-1.9, 1.7, 0]),
            Rectangle(width=1.9, height=0.85, fill_color=BLUE,
                      fill_opacity=0.35, stroke_width=0).move_to([1.95, 1.7, 0]),
            Rectangle(width=1.9, height=0.85, fill_color=ACCENT,
                      fill_opacity=0.35, stroke_width=0).move_to([3.85, 1.7, 0]),
        )
        lab = VGroup(
            Text("TRAIN ~60%", font_size=17, color=GREEN, font=MONO
                 ).move_to([-1.9, 1.7, 0]),
            Text("VALID ~20%", font_size=17, color=BLUE, font=MONO
                 ).move_to([1.95, 1.7, 0]),
            Text("TEST ~20%", font_size=17, color=ACCENT, font=MONO
                 ).move_to([3.85, 1.7, 0]),
        )
        self.play(Create(bar), FadeIn(segs), FadeIn(lab), run_time=1.2)
        rows = VGroup(
            Text("train: fit the model", font_size=19, color=GREEN, font=MONO),
            Text("validate: try many settings, pick the best model",
                 font_size=19, color=BLUE, font=MONO),
            Text("test: ONE final score, kept untouched until the end",
                 font_size=19, color=ACCENT, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-1.2, 0.15, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows],
                              run_time=1.8))
        warn = Text("why validate? tuning on the TEST set biases the result",
                    font_size=19, color=RED, font=MONO).move_to([0, -1.35, 0])
        self.play(Write(warn), run_time=0.9)
        goal = Text("the real goal: generalize beyond past applicants (bank lending)",
                    font_size=18, color=WHITE, opacity=0.6, font=MONO
                    ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(goal), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L14_KFold(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("K-Fold cross-validation", "one split can mislead")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        note = Text("a single split may misrepresent the data",
                    font_size=19, color=WHITE, opacity=0.6, font=MONO
                    ).move_to([0, 1.9, 0])
        self.play(Write(note), run_time=0.8)
        K = 5
        w, h = 1.55, 0.55
        x0 = -5.0
        rows = VGroup()
        for r in range(K):
            row = VGroup()
            for c in range(K):
                val = (c == r)
                sq = Rectangle(width=w, height=h,
                               fill_color=(ACCENT if val else BLUE),
                               fill_opacity=(0.55 if val else 0.18),
                               stroke_width=1.5,
                               stroke_color=(ACCENT if val else BLUE),
                               stroke_opacity=0.7)
                sq.move_to([x0 + c * (w + 0.12), 1.15 - r * (h + 0.12), 0])
                row.add(sq)
            tag = Text(f"round {r + 1}", font_size=14, color=WHITE,
                       opacity=0.5, font=MONO
                       ).next_to(row, RIGHT, buff=0.3)
            rows.add(VGroup(row, tag))
        self.play(LaggedStart(*[FadeIn(rw, shift=RIGHT * 0.2) for rw in rows],
                              run_time=2.0))
        leg = VGroup(
            Rectangle(width=0.4, height=0.25, fill_color=BLUE,
                      fill_opacity=0.18, stroke_color=BLUE, stroke_width=1.5),
            Text("train", font_size=14, color=BLUE, font=MONO),
            Rectangle(width=0.4, height=0.25, fill_color=ACCENT,
                      fill_opacity=0.55, stroke_color=ACCENT, stroke_width=1.5),
            Text("validate", font_size=14, color=ACCENT, font=MONO),
        ).arrange(RIGHT, buff=0.25).move_to([5.1, 1.9, 0])
        self.play(FadeIn(leg), run_time=0.7)
        pts = VGroup(
            Text("train on K-1 folds, validate on the held-out fold",
                 font_size=18, color=WHITE, font=MONO),
            Text("each fold validates exactly once; K = 5 or 10 typical",
                 font_size=18, color=WHITE, font=MONO),
            Text("average the K scores; keep the test set separate",
                 font_size=18, color=GREEN, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0.4, -2.35, 0])
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in pts],
                              run_time=1.8))
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L14_StratLOO(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Variants", "stratified folds, leave-one-out")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        st = VGroup(
            Text("STRATIFIED K-FOLD", font_size=22, color=GREEN, weight=BOLD,
                 font=MONO),
            Text("every fold keeps the same class\nproportions as the full data",
                 font_size=18, color=WHITE, font=MONO),
            Text("plain KFold: class counts may vary per fold", font_size=16,
                 color=WHITE, opacity=0.55, font=MONO),
            Text("recommended for classification,\nespecially imbalanced data",
                 font_size=18, color=ACCENT, font=MONO),
        ).arrange(DOWN, buff=0.4).move_to([-3.5, 0.2, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in st],
                              run_time=1.8))
        lo = VGroup(
            Text("LEAVE-ONE-OUT (LOOCV)", font_size=22, color=BLUE,
                 weight=BOLD, font=MONO),
            Text("K = N: train on N-1, validate on 1,\nrepeat N times",
                 font_size=18, color=WHITE, font=MONO),
            Text("uses nearly all data; high precision", font_size=18,
                 color=GREEN, font=MONO),
            Text("but expensive + slow on large datasets", font_size=18,
                 color=RED, font=MONO),
        ).arrange(DOWN, buff=0.4).move_to([3.5, 0.2, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in lo],
                              run_time=1.8))
        extra = Text("also: time-series split for sequential data, repeated K-fold for stability",
                     font_size=17, color=WHITE, opacity=0.55, font=MONO
                     ).to_edge(DOWN, buff=0.45)
        self.play(Write(extra), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L14_AccuracyTrap(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Accuracy - and its trap", "how often correct?")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        f = Text("accuracy = correct / total", font_size=30, color=BLUE,
                 font=MONO).move_to([0, 1.6, 0])
        ex = Text("90 correct out of 100 -> 90%", font_size=21, color=WHITE,
                  font=MONO).move_to([0, 0.85, 0])
        self.play(Write(f), FadeIn(ex), run_time=1.2)
        trap = VGroup(
            Text("THE TRAP", font_size=21, color=RED, weight=BOLD, font=MONO),
            Text("90% of examples are negative:", font_size=19, color=WHITE,
                 font=MONO),
            Text("always guess 'negative' -> 90% accuracy", font_size=19,
                 color=RED, font=MONO),
            Text("but it catches 0% of positives", font_size=19, color=RED,
                 font=MONO),
        ).arrange(DOWN, buff=0.38).move_to([-3.3, -0.7, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in trap],
                              run_time=1.7))
        imb = VGroup(
            Text("class imbalance:", font_size=19, color=ACCENT, weight=BOLD,
                 font=MONO),
            Text("fraud: most transactions clean", font_size=17, color=WHITE,
                 opacity=0.7, font=MONO),
            Text("disease: most patients healthy", font_size=17, color=WHITE,
                 opacity=0.7, font=MONO),
            Text("purchases: most visitors don't buy", font_size=17,
                 color=WHITE, opacity=0.7, font=MONO),
        ).arrange(DOWN, buff=0.32).move_to([3.3, -0.7, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in imb],
                              run_time=1.7))
        cap = Text("rare positive signal inside many negatives -> accuracy misleads",
                   font_size=18, color=WHITE, opacity=0.6, font=MONO
                   ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L14_Confusion(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The confusion matrix", "four outcomes, two axes")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        cells = VGroup(
            box("true positive\n(TP)\ncaught it", 2.9, 1.3, GREEN, 17),
            box("false positive\n(FP)\nfalse alarm", 2.9, 1.3, RED, 17),
            box("false negative\n(FN)\nmissed it", 2.9, 1.3, RED, 17),
            box("true negative\n(TN)\nall clear", 2.9, 1.3, GREEN, 17),
        ).arrange_in_grid(rows=2, cols=2, buff=0.5).move_to([0, 0.05, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in cells],
                              run_time=1.8))
        colh = VGroup(
            Text("predicted +", font_size=16, color=WHITE, opacity=0.5,
                 font=MONO).move_to([-1.55, 1.55, 0]),
            Text("predicted -", font_size=16, color=WHITE, opacity=0.5,
                 font=MONO).move_to([1.55, 1.55, 0]),
        )
        rowh = VGroup(
            Text("actual +", font_size=16, color=WHITE, opacity=0.5,
                 font=MONO).move_to([-3.55, 0.55, 0]),
            Text("actual -", font_size=16, color=WHITE, opacity=0.5,
                 font=MONO).move_to([-3.55, -0.55, 0]),
        )
        self.play(FadeIn(colh), FadeIn(rowh), run_time=0.7)
        cap = Text("first letter = truth, second letter = the model's claim",
                   font_size=19, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.45)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L14_PrecRec(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Precision vs recall", "which mistake do you fear?")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        p = VGroup(
            Text("PRECISION = TP / (TP + FP)", font_size=22, color=BLUE,
                 weight=BOLD, font=MONO),
            Text("of the alerts we raised, how many\nwere real? minimize FALSE POSITIVES",
                 font_size=17, color=WHITE, font=MONO),
            Text("costly false alarms: hiring - only hire\npeople who WILL succeed (Google)",
                 font_size=17, color=WHITE, opacity=0.65, font=MONO),
            Text("1.0 = never wrong when it says positive", font_size=16,
                 color=WHITE, opacity=0.55, font=MONO),
        ).arrange(DOWN, buff=0.4).move_to([-3.5, 0.25, 0])
        r = VGroup(
            Text("RECALL = TP / (TP + FN)", font_size=22, color=GREEN,
                 weight=BOLD, font=MONO),
            Text("of all real positives, how many did\nwe catch? minimize FALSE NEGATIVES",
                 font_size=17, color=WHITE, font=MONO),
            Text("costly misses: cancer screening, fraud,\na contagious super plague",
                 font_size=17, color=WHITE, opacity=0.65, font=MONO),
            Text("1.0 = never misses the target class", font_size=16,
                 color=WHITE, opacity=0.55, font=MONO),
        ).arrange(DOWN, buff=0.4).move_to([3.5, 0.25, 0])
        self.play(FadeIn(p, shift=RIGHT * 0.3), run_time=1.5)
        self.play(FadeIn(r, shift=LEFT * 0.3), run_time=1.5)
        cap = Text("cancer: recall - fraud alerts: recall - loans: precision",
                   font_size=19, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.45)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L14_F1LogLoss(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("F1 and log loss", "one balance score, one confidence score")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        f1 = VGroup(
            Text("F1 = 2PR / (P + R)", font_size=24, color=BLUE, weight=BOLD,
                 font=MONO),
            Text("harmonic balance: high F1 needs BOTH\nprecision and recall strong",
                 font_size=17, color=WHITE, font=MONO),
            Text("precision up usually pushes recall down", font_size=16,
                 color=WHITE, opacity=0.55, font=MONO),
            Text("use when FPs AND FNs matter: flagging\nharmful content; imbalanced data",
                 font_size=17, color=WHITE, opacity=0.65, font=MONO),
        ).arrange(DOWN, buff=0.4).move_to([-3.5, 0.25, 0])
        ll = VGroup(
            Text("LOG LOSS", font_size=24, color=GREEN, weight=BOLD,
                 font=MONO),
            Text("a 99% confident WRONG call hurts more\nthan a 60% confident one",
                 font_size=17, color=WHITE, font=MONO),
            Text("accuracy ignores probabilities;\nlog loss grades confidence",
                 font_size=17, color=WHITE, font=MONO),
            Text("lower is better, 0 is ideal; works for\nmulticlass (N rows, M classes)",
                 font_size=17, color=WHITE, opacity=0.65, font=MONO),
        ).arrange(DOWN, buff=0.4).move_to([3.5, 0.25, 0])
        self.play(FadeIn(f1, shift=RIGHT * 0.3), run_time=1.5)
        self.play(FadeIn(ll, shift=LEFT * 0.3), run_time=1.5)
        cap = Text("precision cuts false alarms - recall cuts misses - F1 balances - log loss judges confidence",
                   font_size=17, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.4)
        self.play(Write(cap), run_time=1.1)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L14_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, _ = title_block("Lecture 14 in one breath", "")
        self.play(Write(t), run_time=0.9)
        lines = VGroup(
            Text("overfit = memorized noise: great train, poor test",
                 font_size=22, color=WHITE, font=MONO),
            Text("underfit = too simple: poor everywhere", font_size=22,
                 color=WHITE, font=MONO),
            Text("high bias -> bigger model; high variance -> more data / regularize",
                 font_size=22, color=WHITE, font=MONO),
            Text("hold out test data; cross-validate with K folds (stratified if imbalanced)",
                 font_size=22, color=WHITE, font=MONO),
            Text("accuracy lies under imbalance: use precision, recall, F1, log loss",
                 font_size=22, color=WHITE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        hl(lines[0], 41, 50, RED)
        hl(lines[2], 13, 29, BLUE)
        hl(lines[2], 31, 64, GREEN)
        hl(lines[3], 45, 55, ACCENT)
        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(2.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
