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


class L13_Title(Scene):
    def construct(self):
        self.camera.background_color = BG
        t = Text("Feature Engineering", font_size=44, color=BLUE, weight=BOLD,
                 font=MONO).to_edge(UP, buff=0.8)
        s = Text("CMSC 320 - lecture 13 - before the model, shape the data",
                 font_size=20, color=WHITE, opacity=0.5, font=MONO
                 ).next_to(t, DOWN, buff=0.3)
        self.play(Write(t), run_time=1.4)
        self.play(FadeIn(s, shift=DOWN * 0.2), run_time=0.7)
        self.wait(0.8)
        core = Text("raw data -> meaningful features", font_size=32,
                    color=ACCENT, weight=BOLD, font=MONO)
        self.play(FadeOut(s), Write(core), run_time=1.4)
        self.wait(1.2)
        key = Text("better features -> better predictions", font_size=22,
                   color=WHITE, font=MONO).next_to(core, DOWN, buff=0.5)
        self.play(FadeIn(key), run_time=0.8)
        agenda = Text("creation - transformation - encoding - binning",
                      font_size=19, color=WHITE, opacity=0.55, font=MONO
                      ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(agenda), run_time=0.8)
        self.wait(1.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L13_WhatWhy(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("What and why", "the step between cleaning and modeling")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        pipe = VGroup(
            box("preprocess", 2.3, 0.85, BLUE, 18),
            box("feature\nengineering", 2.5, 0.95, ACCENT, 18),
            box("ML model", 2.0, 0.85, GREEN, 18),
        ).arrange(RIGHT, buff=0.7).move_to([0, 1.35, 0])
        ar = VGroup(*[Arrow(pipe[i].get_right(), pipe[i + 1].get_left(),
                            stroke_width=3, color=WHITE, stroke_opacity=0.5,
                            max_tip_length_to_length_ratio=0.3)
                      for i in range(2)])
        note = Text("cleaning, missing values, outliers came first",
                    font_size=16, color=WHITE, opacity=0.5, font=MONO
                    ).next_to(pipe[0], DOWN, buff=0.3)
        self.play(FadeIn(pipe[0]), FadeIn(note), run_time=0.7)
        self.play(Create(ar[0]), FadeIn(pipe[1]), run_time=0.8)
        self.play(Create(ar[1]), FadeIn(pipe[2]), run_time=0.7)
        defn = Text("features = the columns a model reads;\nengineering transforms raw data into\nfeatures models can use well",
                    font_size=21, color=WHITE, font=MONO).move_to([-3.4, -0.9, 0])
        why = VGroup(
            Text("models don't like categorical data", font_size=19,
                 color=RED, font=MONO),
            Text("different scales hurt learning", font_size=19, color=RED,
                 font=MONO),
            Text("models are fussy in many other ways", font_size=19,
                 color=RED, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.9, 0])
        wh = Text("WHY", font_size=20, color=RED, weight=BOLD, font=MONO
                  ).move_to([3.4, 0.15, 0])
        self.play(Write(defn), run_time=1.3)
        self.play(FadeIn(wh), LaggedStart(*[FadeIn(l, shift=LEFT * 0.2)
                                            for l in why], run_time=1.5))
        goal = Text("goal: simpler transforms + higher accuracy", font_size=20,
                    color=ACCENT, font=MONO).to_edge(DOWN, buff=0.55)
        self.play(Write(goal), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L13_Menu(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The four toolboxes", "common ways to apply feature engineering")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        cards = VGroup(
            VGroup(box("1 creation", 2.9, 0.8, BLUE, 20),
                   Text("polynomial x^2\ninteraction x1*x2\nclustering (k-means)",
                        font_size=15, color=WHITE, opacity=0.7,
                        font=MONO)).arrange(DOWN, buff=0.25),
            VGroup(box("2 transformation", 2.9, 0.8, GREEN, 20),
                   Text("scaling, z-score\nlog, binning\nencoding categoricals",
                        font_size=15, color=WHITE, opacity=0.7,
                        font=MONO)).arrange(DOWN, buff=0.25),
            VGroup(box("3 selection", 2.9, 0.8, ACCENT, 20),
                   Text("keep the features\nthat actually\nhelp", font_size=15,
                        color=WHITE, opacity=0.7, font=MONO)).arrange(DOWN,
                                                                      buff=0.25),
            VGroup(box("4 reduction", 2.9, 0.8, RED, 20),
                   Text("PCA: fewer dims,\nkeep the signal\n(later topic)",
                        font_size=15, color=WHITE, opacity=0.7,
                        font=MONO)).arrange(DOWN, buff=0.25),
        ).arrange(RIGHT, buff=0.75).move_to([0, 0.15, 0])
        for c in cards:
            self.play(FadeIn(c, shift=UP * 0.3), run_time=0.7)
        text_note = Text("text data too: BoW / TF-IDF for NLP (later)",
                         font_size=18, color=WHITE, opacity=0.55, font=MONO
                         ).to_edge(DOWN, buff=0.55)
        self.play(Write(text_note), run_time=0.9)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L13_Creation(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Feature creation", "new columns from old ones")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1], x_length=5.6,
                  y_length=3.6, axis_config={"stroke_opacity": 0.15,
                                             "include_ticks": False}
                  ).move_to([-3.4, 0.1, 0])
        lin = ax.plot(lambda x: 0.9 * x, color=WHITE, stroke_width=3,
                      stroke_opacity=0.4)
        curve = ax.plot(lambda x: 0.22 * x ** 2, color=ACCENT, stroke_width=4)
        pts = VGroup(*[Dot(ax.c2p(x, 0.22 * x ** 2 + 0.18 * np.sin(2 * x)),
                           color=WHITE, radius=0.07)
                       for x in np.arange(0.8, 4.9, 0.8)])
        ph = Text("POLYNOMIAL: add x^2", font_size=21, color=ACCENT,
                  weight=BOLD, font=MONO).move_to([-3.4, 2.35, 0])
        pn = Text("house size vs price grows\nnonlinearly - x^2 captures it",
                  font_size=17, color=WHITE, opacity=0.6, font=MONO
                  ).move_to([-3.4, -2.25, 0])
        self.play(Write(ph), Create(ax), run_time=1.0)
        self.play(Create(lin), FadeIn(pts), run_time=0.9)
        self.play(Create(curve), run_time=1.0)
        self.play(FadeIn(pn), run_time=0.7)
        ih = Text("INTERACTION: x1 * x2", font_size=21, color=GREEN,
                  weight=BOLD, font=MONO).move_to([3.6, 2.35, 0])
        b1 = box("income", 1.9, 0.75, GREEN, 18).move_to([2.6, 1.0, 0])
        b2 = box("age", 1.5, 0.75, GREEN, 18).move_to([4.7, 1.0, 0])
        cross = Text("x", font_size=34, color=ACCENT, weight=BOLD, font=MONO
                     ).move_to([3.65, 1.0, 0])
        down = Arrow([3.65, 0.55, 0], [3.65, -0.15, 0], stroke_width=3,
                     color=WHITE, stroke_opacity=0.5)
        b3 = box("income x age", 2.9, 0.8, ACCENT, 18).move_to([3.65, -0.65, 0])
        inote = Text("spending power depends on BOTH\nat once, not independently",
                     font_size=17, color=WHITE, opacity=0.6, font=MONO
                     ).move_to([3.6, -1.9, 0])
        self.play(Write(ih), FadeIn(b1), FadeIn(cross), FadeIn(b2),
                  run_time=1.1)
        self.play(Create(down), FadeIn(b3), run_time=0.9)
        self.play(FadeIn(inote), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L13_Scaling(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Why scale?", "age 27-50 vs income 48,000-83,000")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = Axes(x_range=[0, 100, 25], y_range=[0, 100, 25], x_length=6.4,
                  y_length=4.0, axis_config={"stroke_opacity": 0.15,
                                             "include_ticks": False}
                  ).shift(DOWN * 0.3)
        xl = Text("income (0-100k)", font_size=16, color=WHITE, opacity=0.4,
                  font=MONO).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = Text("age", font_size=16, color=WHITE, opacity=0.4, font=MONO
                  ).next_to(ax.y_axis, UP, buff=0.1)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.9)
        q = Dot(ax.c2p(60, 35), color=ACCENT, radius=0.11)
        a = Dot(ax.c2p(55, 30), color=GREEN, radius=0.11)
        b = Dot(ax.c2p(90, 80), color=RED, radius=0.11)
        la = Text("A", font_size=18, color=GREEN, font=MONO
                  ).next_to(a, DOWN, buff=0.12)
        lb = Text("B", font_size=18, color=RED, font=MONO
                  ).next_to(b, UP, buff=0.12)
        self.play(FadeIn(q), FadeIn(a), FadeIn(la), FadeIn(b), FadeIn(lb),
                  run_time=0.8)
        d1 = Line(q.get_center(), a.get_center(), color=GREEN, stroke_width=3)
        d2 = Line(q.get_center(), b.get_center(), color=RED, stroke_width=3)
        self.play(Create(d1), Create(d2), run_time=1.1)
        cap = Text("income spans 35x more than age: the income gap\ndominates the distance, biasing k-NN toward B",
                   font_size=19, color=WHITE, font=MONO).to_edge(DOWN, buff=0.5)
        hl(cap, 0, 6, RED)
        self.play(Write(cap), run_time=1.2)
        note = Text("critical for distance / weighted-sum models: k-NN, linear regression",
                    font_size=17, color=ACCENT, opacity=0.85, font=MONO
                    ).next_to(cap, DOWN, buff=0.22)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L13_MinMax(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Min-Max normalization", "squeeze every feature into [0, 1]")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        formula = Text("Xscaled = (X - Xmin) / (Xmax - Xmin)", font_size=30,
                       color=BLUE, font=MONO).move_to([0, 1.5, 0])
        self.play(Write(formula), run_time=1.2)
        rows = VGroup(
            Text("income  0 -> 0      12.53 billion -> 1", font_size=21,
                 color=WHITE, font=MONO),
            Text("age     0 -> 0      100 -> 1", font_size=21, color=WHITE,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-2.2, 0.1, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows],
                              run_time=1.2))
        pros = VGroup(
            Text("+ no single feature dominates", font_size=18, color=GREEN,
                 font=MONO),
            Text("+ relative distances preserved", font_size=18, color=GREEN,
                 font=MONO),
            Text("+ distribution shape unchanged", font_size=18, color=GREEN,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.3, 0.15, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in pros],
                              run_time=1.3))
        con = Text("- sensitive to OUTLIERS: min/max set the range",
                   font_size=19, color=RED, font=MONO).move_to([-2.1, -1.35, 0])
        self.play(Write(con), run_time=0.9)
        code = Text("sklearn: MinMaxScaler()", font_size=20, color=ACCENT,
                    font=MONO).move_to([4.3, -1.35, 0])
        self.play(FadeIn(code), run_time=0.7)
        tip = Text("handle outliers BEFORE scaling, or the scale distorts",
                   font_size=18, color=WHITE, opacity=0.6, font=MONO
                   ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(tip), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L13_Standard(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Standardization (z-score)", "center at 0, spread at 1")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        formula = Text("X' = (X - mean) / std_dev", font_size=30, color=BLUE,
                       font=MONO).move_to([0, 1.5, 0])
        sub = Text("result: mean = 0, standard deviation = 1", font_size=20,
                   color=WHITE, opacity=0.6, font=MONO
                   ).next_to(formula, DOWN, buff=0.35)
        self.play(Write(formula), FadeIn(sub), run_time=1.2)
        pros = VGroup(
            Text("+ comparable scales, shape unchanged", font_size=18,
                 color=GREEN, font=MONO),
            Text("+ more robust to outliers than Min-Max", font_size=18,
                 color=GREEN, font=MONO),
            Text("+ no need for a bounded range", font_size=18, color=GREEN,
                 font=MONO),
            Text("+ for distance + gradient models: logistic reg, SVM",
                 font_size=18, color=GREEN, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([-2.6, -0.35, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in pros],
                              run_time=1.6))
        code = Text("sklearn:\nStandardScaler()", font_size=20, color=ACCENT,
                    font=MONO).move_to([4.0, -0.35, 0])
        self.play(FadeIn(code), run_time=0.7)
        cmp = Text("vs Min-Max: Min-Max gives a SMALLER spread;\nstandardization preserves the relative spread of data",
                   font_size=19, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.5)
        self.play(Write(cmp), run_time=1.1)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L13_Log(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Log transformation", "tame a skewed distribution")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 4, 1], x_length=5.4,
                  y_length=3.4, axis_config={"stroke_opacity": 0.15,
                                             "include_ticks": False}
                  ).move_to([-3.2, 0.15, 0])
        skew = ax.plot(lambda x: 9 * np.exp(-2.2 * x), color=RED,
                       stroke_width=4)
        bell = ax.plot(lambda x: 2.2 * np.exp(-0.9 * (x - 3.0) ** 2),
                       color=GREEN, stroke_width=4)
        h1 = Text("BEFORE: skewed right", font_size=19, color=RED, font=MONO
                  ).move_to([-3.2, 2.0, 0])
        self.play(Write(h1), Create(ax), Create(skew), run_time=1.3)
        self.play(Create(bell), run_time=1.0)
        h2 = Text("AFTER log: bell-shaped", font_size=19, color=GREEN,
                  font=MONO).move_to([-3.2, -2.15, 0])
        self.play(FadeIn(h2), run_time=0.7)
        forms = VGroup(
            Text("x' = log(x)", font_size=24, color=BLUE, font=MONO),
            Text("x' = log(x + 1)  if zeros exist", font_size=24, color=BLUE,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.6, 1.35, 0])
        self.play(LaggedStart(*[Write(f) for f in forms], run_time=1.3))
        ben = VGroup(
            Text("+ spreads values evenly", font_size=18, color=GREEN,
                 font=MONO),
            Text("+ pulls extreme tail inward", font_size=18, color=GREEN,
                 font=MONO),
            Text("+ ready for t-test / ANOVA", font_size=18, color=GREEN,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.9, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in ben],
                              run_time=1.3))
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L13_EncodingMenu(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Encoding categoricals", "models read numbers, not strings")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        bad = box('"red" "blue"', 2.6, 0.9, RED, 20).move_to([-4.6, 1.3, 0])
        ar = Arrow([-3.2, 1.3, 0], [-2.2, 1.3, 0], stroke_width=4, color=WHITE,
                   stroke_opacity=0.5)
        good = box("0 1 0", 1.8, 0.9, GREEN, 22).move_to([-1.2, 1.3, 0])
        self.play(Write(bad), run_time=0.8)
        self.play(Create(ar), FadeIn(good), run_time=0.8)
        why = Text("most ML algorithms require\nnumerical inputs", font_size=19,
                   color=WHITE, opacity=0.6, font=MONO
                   ).move_to([-4.0, 0.0, 0])
        self.play(FadeIn(why), run_time=0.7)
        menu = VGroup(
            Text("1 label      -> ordinal data", font_size=20, color=BLUE,
                 font=MONO),
            Text("2 one-hot    -> nominal data", font_size=20, color=BLUE,
                 font=MONO),
            Text("3 frequency  -> high cardinality", font_size=20, color=BLUE,
                 font=MONO),
            Text("4 target     -> mean of target per category", font_size=20,
                 color=BLUE, font=MONO),
            Text("5 probability -> frequency / total", font_size=20,
                 color=BLUE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([2.0, -0.55, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in menu],
                              run_time=2.0))
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L13_LabelOneHot(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Label vs one-hot", "when numbers lie about order")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        lh = Text("LABEL ENCODING", font_size=21, color=ACCENT, weight=BOLD,
                  font=MONO).move_to([-4.0, 1.9, 0])
        tab = VGroup(
            Text("Nurse  -> 0", font_size=20, color=WHITE, font=MONO),
            Text("Doctor -> 1", font_size=20, color=WHITE, font=MONO),
            Text("Actor  -> 2", font_size=20, color=WHITE, font=MONO),
            Text("Teacher-> 3", font_size=20, color=WHITE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-4.0, 0.55, 0])
        prob = Text("PROBLEM: jobs have no order -\n0 < 3 implies Teacher beats Nurse",
                    font_size=18, color=RED, font=MONO).move_to([-3.9, -1.35, 0])
        self.play(Write(lh), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2)
                                           for r in tab], run_time=1.4))
        self.play(Write(prob), run_time=1.0)
        rh = Text("ONE-HOT ENCODING", font_size=21, color=GREEN, weight=BOLD,
                  font=MONO).move_to([3.4, 1.9, 0])
        grid = VGroup(
            Text("        Nurse Doctor Actor Teacher", font_size=17,
                 color=WHITE, opacity=0.6, font=MONO),
            Text("Nurse    1     0      0     0", font_size=17, color=WHITE,
                 font=MONO),
            Text("Doctor   0     1      0     0", font_size=17, color=WHITE,
                 font=MONO),
            Text("Actor    0     0      1     0", font_size=17, color=WHITE,
                 font=MONO),
            Text("Teacher  0     0      0     1", font_size=17, color=WHITE,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([3.6, 0.45, 0])
        hl(grid[1], 9, 10, GREEN)
        hl(grid[2], 15, 16, GREEN)
        hl(grid[3], 22, 23, GREEN)
        hl(grid[4], 28, 29, GREEN)
        self.play(Write(rh), FadeIn(grid), run_time=1.4)
        code = Text("pandas: pd.get_dummies(s)", font_size=19, color=ACCENT,
                    font=MONO).move_to([3.4, -1.15, 0])
        down = Text("- 50 categories -> dataset explodes", font_size=18,
                    color=RED, font=MONO).move_to([-3.4, -2.25, 0])
        up = Text("+ every category treated equally", font_size=18, color=GREEN,
                  font=MONO).move_to([3.4, -2.25, 0])
        self.play(FadeIn(code), run_time=0.7)
        self.play(FadeIn(up), FadeIn(down), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L13_FreqTargetProb(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Frequency, target, probability", "count-based encodings")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        f = VGroup(
            Text("FREQUENCY", font_size=21, color=BLUE, weight=BOLD,
                 font=MONO),
            Text("replace category with\nits count: 'Nurse' x3 -> 3",
                 font_size=17, color=WHITE, font=MONO),
            Text("+ fewer dims, shows importance\n- equal counts lose uniqueness",
                 font_size=15, color=WHITE, opacity=0.6, font=MONO),
        ).arrange(DOWN, buff=0.3).move_to([-4.6, 0.35, 0])
        tg = VGroup(
            Text("TARGET (MEAN)", font_size=21, color=GREEN, weight=BOLD,
                 font=MONO),
            Text("category -> mean of the\ntarget for that category",
                 font_size=17, color=WHITE, font=MONO),
            Text("best for high-cardinality\ncategories, supervised tasks",
                 font_size=15, color=WHITE, opacity=0.6, font=MONO),
        ).arrange(DOWN, buff=0.3).move_to([0.0, 0.35, 0])
        pr = VGroup(
            Text("PROBABILITY", font_size=21, color=ACCENT, weight=BOLD,
                 font=MONO),
            Text("count / total:\n'Nurse' 3 of 6 -> 0.5", font_size=17,
                 color=WHITE, font=MONO),
            Text("use when relative proportion\nbeats the raw count",
                 font_size=15, color=WHITE, opacity=0.6, font=MONO),
        ).arrange(DOWN, buff=0.3).move_to([4.6, 0.35, 0])
        for c in (f, tg, pr):
            self.play(FadeIn(c, shift=UP * 0.3), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L13_Binning(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Binning / discretization", "continuous values -> categories")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 4, 1], x_length=7.0,
                  y_length=3.2, axis_config={"stroke_opacity": 0.15,
                                             "include_ticks": False}
                  ).move_to([0, 0.55, 0])
        self.play(Create(ax), run_time=0.7)
        ew = VGroup(*[Rectangle(width=2.0, height=0.5, fill_color=BLUE,
                                fill_opacity=0.35, stroke_width=1.5,
                                stroke_color=BLUE).move_to(ax.c2p(1 + 2 * i, 0.75))
                      for i in range(3)])
        ef = VGroup(*[Rectangle(width=w, height=0.5, fill_color=GREEN,
                                fill_opacity=0.35, stroke_width=1.5,
                                stroke_color=GREEN).move_to(ax.c2p(c, 1.6))
                      for w, c in [(1.0, 1.0), (2.0, 2.5), (4.0, 5.5),
                                   (2.0, 8.5)]])
        cu = VGroup(*[Rectangle(width=3.0, height=0.5, fill_color=ACCENT,
                                fill_opacity=0.35, stroke_width=1.5,
                                stroke_color=ACCENT).move_to(ax.c2p(1.5 + 3 * i, 2.45))
                      for i in range(3)])
        l1 = Text("EQUAL-WIDTH: same interval", font_size=17, color=BLUE,
                  font=MONO).next_to(ew, RIGHT, buff=0.35)
        l2 = Text("EQUAL-FREQUENCY: same count per bin", font_size=17,
                  color=GREEN, font=MONO).next_to(ef, RIGHT, buff=0.35)
        l3 = Text("CUSTOM: domain-knowledge bins", font_size=17, color=ACCENT,
                  font=MONO).next_to(cu, RIGHT, buff=0.35)
        self.play(FadeIn(ew), FadeIn(l1), run_time=0.9)
        self.play(FadeIn(ef), FadeIn(l2), run_time=0.9)
        self.play(FadeIn(cu), FadeIn(l3), run_time=0.9)
        man = Text("manual binning = boundaries known BEFOREHAND, not in the data:",
                   font_size=19, color=WHITE, font=MONO).move_to([0, -1.75, 0])
        ex = Text("GPA -> pass/fail (threshold 3.20)   location -> county   MPG -> car type",
                  font_size=17, color=WHITE, opacity=0.6, font=MONO
                  ).move_to([0, -2.3, 0])
        self.play(Write(man), run_time=1.0)
        self.play(FadeIn(ex), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L13_KeyConcepts(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Bridge to evaluation", "key ML concepts before we measure")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        sup = Text("supervised: learn the mapping Y = f(X)", font_size=22,
                   color=BLUE, font=MONO).move_to([-3.6, 1.6, 0])
        sup2 = Text("labels known in training (spam or not)", font_size=17,
                    color=WHITE, opacity=0.55, font=MONO
                    ).move_to([-3.6, 1.05, 0])
        self.play(Write(sup), FadeIn(sup2), run_time=1.1)
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1], x_length=3.0,
                  y_length=2.4, axis_config={"stroke_opacity": 0.15,
                                             "include_ticks": False}
                  ).move_to([3.9, 1.15, 0])
        g = VGroup(*[Dot(ax.c2p(x, y), color=GREEN, radius=0.06)
                     for x, y in [(1.2, 2.8), (1.8, 3.2), (1.0, 2.0)]])
        r = VGroup(*[Dot(ax.c2p(x, y), color=RED, radius=0.06)
                     for x, y in [(2.8, 1.2), (3.2, 2.0), (2.4, 0.8)]])
        bd = Line(ax.c2p(0.6, 0.6), ax.c2p(3.6, 3.6), color=ACCENT,
                  stroke_width=3)
        bh = Text("decision boundary: line (or hyperplane)\nseparating the classes",
                  font_size=17, color=ACCENT, font=MONO
                  ).move_to([3.9, -0.85, 0])
        self.play(Create(ax), FadeIn(g), FadeIn(r), run_time=1.0)
        self.play(Create(bd), FadeIn(bh), run_time=1.0)
        opt = Text("training = OPTIMIZATION: minimize a loss function\n(predicted vs actual gap) via gradient descent",
                   font_size=19, color=GREEN, font=MONO).move_to([-1.4, -1.7, 0])
        self.play(Write(opt), run_time=1.2)
        gen = Text("generalization = performs well on UNSEEN data, not just training",
                   font_size=19, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.45)
        self.play(Write(gen), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L13_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, _ = title_block("Lecture 13 in one breath", "")
        self.play(Write(t), run_time=0.9)
        lines = VGroup(
            Text("feature engineering: raw data -> features models love",
                 font_size=22, color=WHITE, font=MONO),
            Text("creation: x^2 and x1*x2 capture nonlinear + joint effects",
                 font_size=22, color=WHITE, font=MONO),
            Text("scaling: Min-Max -> [0,1] (outlier-prone), z-score -> mean 0 std 1",
                 font_size=22, color=WHITE, font=MONO),
            Text("log tames skew; encoding turns categories into numbers",
                 font_size=22, color=WHITE, font=MONO),
            Text("one-hot for nominal; binning for domain thresholds",
                 font_size=22, color=WHITE, font=MONO),
            Text("next: how well does the model generalize?", font_size=22,
                 color=WHITE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        hl(lines[1], 10, 23, BLUE)
        hl(lines[2], 27, 40, BLUE)
        hl(lines[2], 44, 67, GREEN)
        hl(lines[3], 5, 9, RED)
        hl(lines[4], 12, 19, GREEN)
        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(2.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
