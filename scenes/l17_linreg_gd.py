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


# shared scatter data: (weight, height) of 5 people
PTS = [(62, 162), (74, 168), (85, 172), (96, 178), (108, 186)]


def reg_axes():
    ax = Axes(x_range=[50, 120, 10], y_range=[155, 195, 10], x_length=6.4,
              y_length=3.9, axis_config={"stroke_opacity": 0.15,
                                         "include_ticks": False})
    return ax


def line_fn(x):
    return 147.0 + 0.36 * x


class L17_Title(Scene):
    def construct(self):
        self.camera.background_color = BG
        t = Text("Linear Regression & Gradient Descent", font_size=38,
                 color=BLUE, weight=BOLD, font=MONO).to_edge(UP, buff=0.8)
        s = Text("CMSC 320 - lecture 17 - optimization for ML", font_size=20,
                 color=WHITE, opacity=0.5, font=MONO).next_to(t, DOWN,
                                                              buff=0.3)
        self.play(Write(t), run_time=1.4)
        self.play(FadeIn(s, shift=DOWN * 0.2), run_time=0.7)
        self.wait(0.8)
        core = Text("find the best line, descend to it", font_size=30,
                    color=ACCENT, weight=BOLD, font=MONO)
        self.play(FadeOut(s), Write(core), run_time=1.3)
        self.wait(1.8)
        agenda = Text("model - loss - gradient descent - metrics - variants",
                      font_size=19, color=WHITE, opacity=0.55, font=MONO
                      ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(agenda), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L17_Modular(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("A modular approach to ML",
                           "every algorithm = three interchangeable parts")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        b1 = box("choose a model", 2.9, 0.95, BLUE, 18).move_to([-4.5, 0.9, 0])
        b2 = box("define loss", 2.6, 0.95, GREEN, 18).move_to([0, 0.9, 0])
        b3 = box("fit & optimize", 3.0, 0.95, ACCENT, 18).move_to([4.5, 0.9, 0])
        n1 = Text("the shape of the\nrelationship", font_size=15, color=WHITE,
                  opacity=0.55, font=MONO).next_to(b1, DOWN, buff=0.25)
        n2 = Text("how bad the fit is", font_size=15, color=WHITE,
                  opacity=0.55, font=MONO).next_to(b2, DOWN, buff=0.25)
        n3 = Text("search for the best\nparameters", font_size=15, color=WHITE,
                  opacity=0.55, font=MONO).next_to(b3, DOWN, buff=0.25)
        a1 = Arrow([-2.95, 0.9, 0], [-1.45, 0.9, 0], stroke_width=3,
                   color=WHITE, stroke_opacity=0.5,
                   max_tip_length_to_length_ratio=0.3)
        a2 = Arrow([1.45, 0.9, 0], [2.9, 0.9, 0], stroke_width=3, color=WHITE,
                   stroke_opacity=0.5, max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(b1, shift=RIGHT * 0.3), run_time=0.7)
        self.play(FadeIn(n1), run_time=0.4)
        self.play(Create(a1), FadeIn(b2, shift=RIGHT * 0.3), run_time=0.7)
        self.play(FadeIn(n2), run_time=0.4)
        self.play(Create(a2), FadeIn(b3, shift=RIGHT * 0.3), run_time=0.7)
        self.play(FadeIn(n3), run_time=0.4)
        self.wait(0.8)
        cap = Text("mix and match the modules -> a whole family of ML methods",
                   font_size=21, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.7)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L17_RegVsClass(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Regression vs classification",
                           "the output type decides the task")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        h1 = Text("CLASSIFICATION", font_size=24, color=RED, weight=BOLD,
                  font=MONO).move_to([-3.6, 1.9, 0])
        d1 = Text("discrete categories", font_size=20, color=WHITE,
                  font=MONO).move_to([-3.6, 1.2, 0])
        d1b = Text("either / or, no in-between", font_size=18, color=WHITE,
                   opacity=0.6, font=MONO).move_to([-3.6, 0.6, 0])
        d1c = Text("is this email spam?", font_size=20, color=RED,
                   font=MONO).move_to([-3.6, -0.1, 0])
        h2 = Text("REGRESSION", font_size=24, color=GREEN, weight=BOLD,
                  font=MONO).move_to([3.6, 1.9, 0])
        d2 = Text("continuous values", font_size=20, color=WHITE,
                  font=MONO).move_to([3.6, 1.2, 0])
        d2b = Text("more or less correct", font_size=18, color=WHITE,
                   opacity=0.6, font=MONO).move_to([3.6, 0.6, 0])
        d2c = Text("what will the home sell for?", font_size=20, color=GREEN,
                   font=MONO).move_to([3.6, -0.1, 0])
        line = Line([0, 2.2, 0], [0, -0.6, 0], stroke_width=1.5,
                    stroke_opacity=0.2)
        self.play(Create(line), run_time=0.5)
        self.play(FadeIn(h1), Write(d1), FadeIn(d1b), Write(d1c), run_time=1.4)
        self.play(FadeIn(h2), Write(d2), FadeIn(d2b), Write(d2c), run_time=1.4)
        cap = Text("classification: which class?    regression: how much?",
                   font_size=22, color=ACCENT, font=MONO).to_edge(DOWN,
                                                                  buff=0.7)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L17_Model(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Simple linear regression",
                           "predict height (Y) from weight (X)")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = reg_axes().move_to([-3.1, -0.15, 0])
        xl = Text("weight", font_size=17, color=WHITE, opacity=0.4,
                  font=MONO).next_to(ax.x_axis, RIGHT, buff=0.12)
        yl = Text("height", font_size=17, color=WHITE, opacity=0.4,
                  font=MONO).next_to(ax.y_axis, UP, buff=0.12)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.9)
        pts = VGroup(*[Dot(ax.c2p(x, y), color=WHITE, radius=0.08)
                       for x, y in PTS])
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pts],
                              run_time=1.0))
        fit = ax.plot(line_fn, x_range=[55, 115], color=GREEN, stroke_width=4)
        self.play(Create(fit), run_time=1.2)
        f = Text("Y = b0 + b1 * X", font_size=30, color=ACCENT, weight=BOLD,
                 font=MONO).move_to([3.6, 1.5, 0])
        l1 = Text("b1 = slope", font_size=22, color=GREEN, font=MONO
                  ).move_to([3.6, 0.55, 0])
        l1b = Text("Y change per 1 unit of X", font_size=17, color=WHITE,
                   opacity=0.6, font=MONO).move_to([3.6, 0.05, 0])
        l2 = Text("b0 = intercept", font_size=22, color=BLUE, font=MONO
                  ).move_to([3.6, -0.75, 0])
        l2b = Text("value of Y when X = 0", font_size=17, color=WHITE,
                   opacity=0.6, font=MONO).move_to([3.6, -1.25, 0])
        self.play(Write(f), run_time=1.0)
        self.play(FadeIn(l1), FadeIn(l1b), run_time=0.8)
        self.play(FadeIn(l2), FadeIn(l2b), run_time=0.8)
        cap = Text("goal: the line with the least overall error", font_size=20,
                   color=WHITE, font=MONO).to_edge(DOWN, buff=0.6)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L17_Multi(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Multiple linear regression",
                           "more than one feature X")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        f = Text("Y = b0 + b1*x1 + b2*x2 + ... + bp*xp", font_size=30,
                 color=ACCENT, weight=BOLD, font=MONO).move_to([0, 1.4, 0])
        self.play(Write(f), run_time=1.3)
        cards = VGroup(
            VGroup(box("x1 ... xp", 2.2, 0.9, BLUE, 20),
                   Text("the features\n(input columns)", font_size=17,
                        color=WHITE, font=MONO)).arrange(DOWN, buff=0.3),
            VGroup(box("b0 ... bp", 2.2, 0.9, GREEN, 20),
                   Text("parameters /\ncoefficients", font_size=17,
                        color=WHITE, font=MONO)).arrange(DOWN, buff=0.3),
            VGroup(box("Y", 2.2, 0.9, RED, 20),
                   Text("the target\n(continuous)", font_size=17, color=WHITE,
                        font=MONO)).arrange(DOWN, buff=0.3),
        ).arrange(RIGHT, buff=1.6).move_to([0, -0.6, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards],
                              run_time=1.6))
        cap = Text("learning = picking the b's that fit the data best",
                   font_size=20, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.6)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L17_Residuals(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Residuals and the cost function",
                           "how wrong is the line?")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = reg_axes().move_to([-3.6, -0.35, 0])
        self.add(ax)
        pts = VGroup(*[Dot(ax.c2p(x, y), color=WHITE, radius=0.08)
                       for x, y in PTS])
        fit = ax.plot(line_fn, x_range=[55, 115], color=GREEN, stroke_width=3)
        self.add(fit)
        res = VGroup(*[Line(ax.c2p(x, y), ax.c2p(x, line_fn(x)),
                            color=RED, stroke_width=3.5)
                       for x, y in PTS])
        self.play(LaggedStart(*[Create(r) for r in res], run_time=1.2))
        e1 = Text("residual e = Y - Yhat", font_size=21, color=RED,
                  font=MONO).move_to([3.4, 1.7, 0])
        e2 = Text("loss per point = e^2", font_size=21, color=ACCENT,
                  font=MONO).move_to([3.4, 1.0, 0])
        e3 = Text("SSE = sum of e^2", font_size=21, color=BLUE,
                  font=MONO).move_to([3.4, 0.3, 0])
        e4 = Text("cost = MSE = SSE / n", font_size=21, color=GREEN,
                  font=MONO).move_to([3.4, -0.4, 0])
        self.play(Write(e1), run_time=0.8)
        self.play(Write(e2), run_time=0.8)
        self.play(Write(e3), run_time=0.8)
        self.play(Write(e4), run_time=0.8)
        note = Text("squaring punishes big errors hardest", font_size=17,
                    color=WHITE, opacity=0.6, font=MONO).move_to([3.4, -1.1, 0])
        self.play(FadeIn(note), run_time=0.6)
        cap = Text("now fitting the line IS an optimization problem: min MSE",
                   font_size=20, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.55)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L17_GDidea(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Gradient descent", "roll downhill on the cost")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        axes = Axes(x_range=[-0.5, 4.5, 1], y_range=[-0.5, 5, 1],
                    x_length=8, y_length=4.0,
                    axis_config={"stroke_opacity": 0.15,
                                 "include_ticks": False}).shift(DOWN * 0.55)
        xlab = Text("b1", font_size=19, color=WHITE, opacity=0.4,
                    font=MONO).next_to(axes.x_axis, RIGHT, buff=0.15)
        ylab = Text("cost J(b0, b1)", font_size=19, color=WHITE, opacity=0.4,
                    font=MONO).next_to(axes.y_axis, UP, buff=0.15)
        curve = axes.plot(
            lambda x: 0.28 * (x - 2.6) ** 2 + 0.4
            + 1.4 * np.sin(1.6 * x) * np.exp(-0.35 * x),
            x_range=[-0.3, 4.3], color=BLUE, stroke_width=3)
        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab), run_time=0.9)
        self.play(Create(curve), run_time=1.3)

        def loss(x):
            return (0.28 * (x - 2.6) ** 2 + 0.4
                    + 1.4 * np.sin(1.6 * x) * np.exp(-0.35 * x))

        def grad(x):
            h = 1e-5
            return (loss(x + h) - loss(x - h)) / (2 * h)

        w = 0.2
        ball = Dot(axes.c2p(w, loss(w)), color=ACCENT, radius=0.11)
        self.play(FadeIn(ball), run_time=0.4)
        eta = 0.45
        for _ in range(9):
            g = grad(w)
            w_new = min(w - eta * g, 4.2)
            nxt = Dot(axes.c2p(w_new, loss(w_new)), color=ACCENT, radius=0.11)
            arrow = Arrow(ball.get_center(), nxt.get_center(), buff=0.09,
                          stroke_width=3, color=GREEN,
                          max_tip_length_to_length_ratio=0.25)
            self.play(Transform(ball, nxt), Create(arrow), run_time=0.5)
            self.wait(0.2)
            w = w_new
        aha = Text("b -> b - alpha * gradient of J", font_size=28,
                   color=GREEN, weight=BOLD, font=MONO).to_edge(DOWN,
                                                                buff=0.5)
        self.play(Write(aha), run_time=1.1)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L17_GDsteps(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The gradient descent loop",
                           "iterate until the cost stops falling")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        steps = [("01", "initialize b0, b1", BLUE),
                 ("02", "compute the gradient", GREEN),
                 ("03", "step opposite it", ACCENT),
                 ("04", "repeat to convergence", RED)]
        nodes = VGroup()
        for i, (num, txt, col) in enumerate(steps):
            b = box(num + "  " + txt, 5.6, 0.8, col, 18)
            b.move_to([-1.9 + (i % 2) * 3.8, 1.5 - i * 1.05, 0])
            nodes.add(b)
        arrs = VGroup(
            Arrow([-1.9 + 2.85, 1.5 - 0 * 1.05, 0], [1.9 - 2.85, 1.5 - 1 * 1.05, 0],
                  stroke_width=3, color=WHITE, stroke_opacity=0.5,
                  max_tip_length_to_length_ratio=0.25),
            Arrow([1.9 - 2.85, 1.5 - 1 * 1.05, 0], [-1.9 + 2.85, 1.5 - 2 * 1.05, 0],
                  stroke_width=3, color=WHITE, stroke_opacity=0.5,
                  max_tip_length_to_length_ratio=0.25),
            Arrow([-1.9 + 2.85, 1.5 - 2 * 1.05, 0], [1.9 - 2.85, 1.5 - 3 * 1.05, 0],
                  stroke_width=3, color=WHITE, stroke_opacity=0.5,
                  max_tip_length_to_length_ratio=0.25))
        for i, n in enumerate(nodes):
            self.play(FadeIn(n, shift=RIGHT * 0.3), run_time=0.6)
            if i < 3:
                self.play(Create(arrs[i]), run_time=0.35)
        cap = Text("the gradient points uphill -> we walk downhill",
                   font_size=21, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.6)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L17_LearningRate(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Learning rate alpha", "the step size is everything")
        self.play(Write(t), FadeIn(s), run_time=0.9)

        def parab(x):
            return 0.5 * (x - 2) ** 2 + 0.3

        panels = []
        cfgs = [("too big", RED, [0.0, 4.0, 0.0, 4.0],
                 [0.0, 4.0, 0.0, 4.0]),
                ("just right", GREEN, [0.0, 4.0, 0.0, 4.0],
                 [0.6, 2.6, 1.4, 2.0]),
                ("too small", BLUE, [0.0, 4.0, 0.0, 4.0],
                 [0.6, 0.9, 1.05, 1.2])]
        for i, (name, col, xr, path) in enumerate(cfgs):
            ax = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1], x_length=3.4,
                      y_length=2.5,
                      axis_config={"stroke_opacity": 0.15,
                                   "include_ticks": False})
            ax.move_to([-4.7 + 4.7 * i, 0.15, 0])
            curve = ax.plot(parab, x_range=[0.1, 3.9], color=WHITE,
                            stroke_opacity=0.5, stroke_width=2.5)
            dots = VGroup(*[Dot(ax.c2p(x, parab(x)), color=col, radius=0.08)
                            for x in path])
            marks = VGroup(*[Line(d.get_center() + DOWN * 0.02,
                                  d.get_center() + DOWN * 0.14,
                                  stroke_width=2, color=col)
                             for d in dots[1:]])
            head = Text(name, font_size=21, color=col, weight=BOLD,
                        font=MONO).move_to([-4.7 + 4.7 * i, 1.9, 0])
            panels.append(VGroup(ax, curve, dots, marks, head))
        for p in panels:
            self.play(FadeIn(p, shift=UP * 0.2), run_time=0.8)
        self.wait(0.8)
        c1 = Text("overshoots the minimum", font_size=17, color=RED,
                  font=MONO).move_to([-4.7, -1.75, 0])
        c2 = Text("converges fast", font_size=17, color=GREEN,
                  font=MONO).move_to([0, -1.75, 0])
        c3 = Text("crawls: too many steps", font_size=17, color=BLUE,
                  font=MONO).move_to([4.7, -1.75, 0])
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(c3), run_time=0.9)
        cap = Text("common alphas: 0.001  0.01  0.1  0.3", font_size=20,
                   color=ACCENT, font=MONO).to_edge(DOWN, buff=0.55)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L17_LineLine(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The line of best fit + L.I.N.E.",
                           "when is a linear model trustworthy?")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = reg_axes().move_to([-4.0, -0.35, 0])
        xl = Text("weight", font_size=17, color=WHITE, opacity=0.4,
                  font=MONO).next_to(ax.x_axis, RIGHT, buff=0.12)
        self.add(ax, xl)
        pts = VGroup(*[Dot(ax.c2p(x, y), color=WHITE, radius=0.08)
                       for x, y in PTS])
        fit = ax.plot(line_fn, x_range=[55, 115], color=GREEN, stroke_width=4)
        self.play(FadeIn(pts), run_time=0.5)
        self.play(Create(fit), run_time=1.1)
        done = Text("gradient descent done:\nthe best-fit line", font_size=19,
                    color=GREEN, font=MONO).move_to([-4.0, 1.9, 0])
        self.play(FadeIn(done), run_time=0.7)
        items = [("L", "relationship is linear", BLUE),
                 ("I", "residuals independent", GREEN),
                 ("N", "residuals normal", ACCENT),
                 ("E", "equal residual variance", RED)]
        rows = VGroup()
        for i, (letter, txt, col) in enumerate(items):
            b = box(letter, 0.8, 0.8, col, 26)
            b.move_to([-0.6, 1.6 - i * 0.95, 0])
            tx = Text(txt, font_size=20, color=WHITE, font=MONO
                      ).next_to(b, RIGHT, buff=0.4)
            rows.add(VGroup(b, tx))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows],
                              run_time=1.8))
        cap = Text("check the assumptions before trusting predictions",
                   font_size=20, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.55)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L17_Metrics(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Evaluating a regression",
                           "how good is the fit, really?")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        m1 = VGroup(Text("MSE", font_size=26, color=BLUE, weight=BOLD,
                         font=MONO),
                    Text("mean squared error:\npenalizes big errors, lower better",
                         font_size=17, color=WHITE, font=MONO)
                    ).arrange(DOWN, buff=0.25).move_to([-3.9, 1.3, 0])
        m2 = VGroup(Text("RMSE", font_size=26, color=GREEN, weight=BOLD,
                         font=MONO),
                    Text("sqrt of MSE: same units as Y\nRMSE = $10K -> off by $10K",
                         font_size=17, color=WHITE, font=MONO)
                    ).arrange(DOWN, buff=0.25).move_to([3.9, 1.3, 0])
        m3 = VGroup(Text("MAE", font_size=26, color=ACCENT, weight=BOLD,
                         font=MONO),
                    Text("mean absolute error: robust,\nbut not differentiable at 0",
                         font_size=17, color=WHITE, font=MONO)
                    ).arrange(DOWN, buff=0.25).move_to([-3.9, -0.9, 0])
        m4 = VGroup(Text("R^2", font_size=26, color=RED, weight=BOLD,
                         font=MONO),
                    Text("variance explained, 0 to 1\nR^2 = 0.85 -> X explains 85% of Y",
                         font_size=17, color=WHITE, font=MONO)
                    ).arrange(DOWN, buff=0.25).move_to([3.9, -0.9, 0])
        self.play(FadeIn(m1), run_time=0.7)
        self.play(FadeIn(m2), run_time=0.7)
        self.play(FadeIn(m3), run_time=0.7)
        self.play(FadeIn(m4), run_time=0.7)
        cap = Text("R^2 = 0: as good as guessing the mean;  R^2 = 1: perfect",
                   font_size=19, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.55)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L17_Variants(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The regression family",
                           "same skeleton, different loss + constraints")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        rows = [
            ("polynomial", "adds x^2, x^3 terms: fits curves;\nflexible but overfits", BLUE),
            ("ridge (L2)", "shrinks coefficients, never to 0;\nbest when features are correlated", GREEN),
            ("lasso (L1)", "forces some coefficients to 0:\nfeature selection, sparse models", ACCENT),
            ("elastic net", "ridge + lasso: correlated features\nAND selection", RED),
        ]
        for i, (name, txt, col) in enumerate(rows):
            b = box(name, 2.6, 0.75, col, 18).move_to([-4.6, 1.75 - i * 1.15, 0])
            tx = Text(txt, font_size=17, color=WHITE, font=MONO
                      ).next_to(b, RIGHT, buff=0.45)
            self.play(FadeIn(b, shift=RIGHT * 0.3), FadeIn(tx), run_time=0.8)
        cap = Text("logistic = for categories (later); random forest regression\naverages many trees - the popular general-purpose pick",
                   font_size=18, color=WHITE, opacity=0.7, font=MONO
                   ).to_edge(DOWN, buff=0.5)
        self.play(Write(cap), run_time=1.1)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L17_Regularization(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Regularization strength", "lambda: the volume knob")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        f = Text("new loss = old loss + lambda * penalty", font_size=27,
                 color=ACCENT, weight=BOLD, font=MONO).move_to([0, 1.6, 0])
        self.play(Write(f), run_time=1.1)
        l1 = Text("L1 penalty = sum |b|", font_size=21, color=GREEN,
                  font=MONO).move_to([-3.6, 0.6, 0])
        l1b = Text("sparse solution, feature\nselection, multiple optima",
                   font_size=17, color=WHITE, opacity=0.65, font=MONO
                   ).move_to([-3.6, -0.15, 0])
        l2 = Text("L2 penalty = sum b^2", font_size=21, color=BLUE,
                  font=MONO).move_to([3.6, 0.6, 0])
        l2b = Text("dense solution, unique,\nhandles correlated features",
                   font_size=17, color=WHITE, opacity=0.65, font=MONO
                   ).move_to([3.6, -0.15, 0])
        self.play(FadeIn(l1), FadeIn(l1b), run_time=0.9)
        self.play(FadeIn(l2), FadeIn(l2b), run_time=0.9)
        cap = Text("lambda too big -> underfit;  too small -> overfit.\nchoose it by cross-validation / grid search (RidgeCV, LassoCV)",
                   font_size=18, color=WHITE, font=MONO).to_edge(DOWN,
                                                                 buff=0.5)
        self.play(Write(cap), run_time=1.1)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L17_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, _ = title_block("Lecture 17 in one breath", "")
        self.play(Write(t), run_time=0.9)
        lines = VGroup(
            Text("regression predicts continuous Y: 'how much?'", font_size=22,
                 color=WHITE, font=MONO),
            Text("cost = MSE over residuals e = Y - Yhat", font_size=22,
                 color=WHITE, font=MONO),
            Text("gradient descent: step opposite the gradient, rate alpha",
                 font_size=22, color=WHITE, font=MONO),
            Text("alpha too big overshoots, too small crawls", font_size=22,
                 color=WHITE, font=MONO),
            Text("check L.I.N.E.; score with MSE / RMSE / MAE / R^2",
                 font_size=22, color=WHITE, font=MONO),
            Text("ridge L2 shrinks, lasso L1 zeroes, elastic net both",
                 font_size=22, color=WHITE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        lines[1][8:11].set_color(RED)
        lines[2][35:44].set_color(GREEN)
        lines[3][5:17].set_color(RED)
        lines[3][22:28].set_color(BLUE)
        lines[5][7:15].set_color(GREEN)
        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(2.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
