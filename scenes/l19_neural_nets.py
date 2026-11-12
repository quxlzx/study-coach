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


def sigmoid_x(x):
    return 1.0 / (1.0 + np.exp(-x))


class L19_Title(Scene):
    def construct(self):
        self.camera.background_color = BG
        t = Text("Introduction to Neural Networks", font_size=40, color=BLUE,
                 weight=BOLD, font=MONO).to_edge(UP, buff=0.8)
        s = Text("CMSC 320 - lecture 19 - from intuition to computation",
                 font_size=20, color=WHITE, opacity=0.5, font=MONO
                 ).next_to(t, DOWN, buff=0.3)
        self.play(Write(t), run_time=1.4)
        self.play(FadeIn(s, shift=DOWN * 0.2), run_time=0.7)
        self.wait(0.8)
        core = Text("weighted sum + activation, stacked in layers", font_size=29,
                    color=ACCENT, weight=BOLD, font=MONO)
        self.play(FadeOut(s), Write(core), run_time=1.4)
        self.wait(1.8)
        agenda = Text("logistic regression - neurons - perceptron - backprop",
                      font_size=18, color=WHITE, opacity=0.55, font=MONO
                      ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(agenda), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_LinearLogistic(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Linear -> logistic regression", "one sigmoid away from classification")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        lr = VGroup(
            Text("LINEAR REGRESSION", font_size=22, color=GREEN, weight=BOLD,
                 font=MONO),
            Text("yhat = w . x + b", font_size=24, color=WHITE, font=MONO),
            Text("identity activation: sigma(a) = a", font_size=19, color=WHITE,
                 font=MONO),
            Text("continuous, unbounded output", font_size=19, color=WHITE,
                 opacity=0.7, font=MONO),
        ).arrange(DOWN, buff=0.35).move_to([-4.0, 0.7, 0])
        lg = VGroup(
            Text("LOGISTIC REGRESSION", font_size=22, color=BLUE, weight=BOLD,
                 font=MONO),
            Text("yhat = sigma(w . x + b)", font_size=24, color=WHITE,
                 font=MONO),
            Text("sigmoid: sigma(a) = 1 / (1 + exp(-a))", font_size=19,
                 color=WHITE, font=MONO),
            Text("probability of class 1, bounded 0 to 1", font_size=19,
                 color=WHITE, opacity=0.7, font=MONO),
        ).arrange(DOWN, buff=0.35).move_to([0.6, 0.7, 0])
        self.play(FadeIn(lr, shift=RIGHT * 0.3), run_time=1.1)
        self.play(FadeIn(lg, shift=RIGHT * 0.3), run_time=1.1)
        ax = Axes(x_range=[-6, 6, 2], y_range=[0, 1, 0.5], x_length=4.2,
                  y_length=2.6,
                  axis_config={"stroke_opacity": 0.2, "include_ticks": False},
                  ).move_to([4.6, 0.5, 0])
        curve = ax.plot(sigmoid_x, color=ACCENT, stroke_width=4)
        yl = Text("P(y = 1 given x)", font_size=15, color=WHITE, opacity=0.5,
                  font=MONO).next_to(ax.y_axis, UP, buff=0.1)
        self.play(Create(ax), FadeIn(yl), Create(curve), run_time=1.4)
        cap = Text("used when the dependent variable is categorical: predict\nclass 1 when yhat >= 0.5, else class 0",
                   font_size=20, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.55)
        self.play(Write(cap), run_time=1.1)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_Threshold(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Training and the threshold", "the 0.5 line is a dial, not a law")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        train = VGroup(
            Text("1. train by gradient descent", font_size=21, color=GREEN,
                 font=MONO),
            Text("score z = w1 x1 + w2 x2 + ... + wn xn + b", font_size=19,
                 color=WHITE, font=MONO),
            Text("gradient descent minimizes the logistic loss", font_size=19,
                 color=WHITE, font=MONO),
            Text("2. decide: yhat >= 0.5 -> class 1, else class 0",
                 font_size=21, color=GREEN, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.6, 0.8, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in train],
                              run_time=1.6))
        ax = Axes(x_range=[-6, 6, 2], y_range=[0, 1, 0.5], x_length=4.6,
                  y_length=3.2,
                  axis_config={"stroke_opacity": 0.2, "include_ticks": False},
                  ).move_to([3.9, 0.6, 0])
        curve = ax.plot(sigmoid_x, color=BLUE, stroke_width=4)
        thr = DashedLine(ax.c2p(-6, 0.5), ax.c2p(6, 0.5), color=ACCENT,
                         stroke_width=2.5)
        tl = Text("threshold = 0.5", font_size=17, color=ACCENT, font=MONO
                  ).move_to(ax.c2p(3.4, 0.68))
        self.play(Create(ax), Create(curve), run_time=1.2)
        self.play(Create(thr), FadeIn(tl), run_time=0.8)
        hi = Text("raise threshold -> more precision, fewer false positives",
                  font_size=19, color=GREEN, font=MONO).to_edge(DOWN, buff=1.0)
        lo = Text("lower threshold -> more recall, fewer false negatives",
                  font_size=19, color=RED, font=MONO).next_to(hi, DOWN, buff=0.25)
        self.play(Write(hi), run_time=0.9)
        self.play(Write(lo), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_WhatIsNN(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("What is a neural network?", "a parametric function that learns")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        f = Text("f(x ; W) = yhat", font_size=36, color=ACCENT, weight=BOLD,
                 font=MONO).move_to([0, 1.6, 0])
        parts = VGroup(
            Text("x = input", font_size=20, color=BLUE, font=MONO),
            Text("yhat = output", font_size=20, color=GREEN, font=MONO),
            Text("W = parameters learned from data", font_size=20, color=RED,
                 font=MONO),
        ).arrange(RIGHT, buff=1.2).move_to([0, 0.6, 0])
        self.play(Write(f), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(p) for p in parts], run_time=1.2))
        d1 = Text("simple units (neurons) in layers -\n"
                  "loosely inspired by brains",
                  font_size=21, color=WHITE, font=MONO).move_to([-3.6, -0.8, 0])
        d2 = Text("learns representations from raw data -\n"
                  "no manual feature engineering",
                  font_size=21, color=WHITE, font=MONO).move_to([3.6, -0.8, 0])
        self.play(FadeIn(d1, shift=RIGHT * 0.3), FadeIn(d2, shift=LEFT * 0.3),
                  run_time=1.2)
        cap = Text("f is differentiable almost everywhere -> W is optimized\nby gradient descent",
                   font_size=19, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.5)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_Bio(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Biological inspiration", "brain cell -> math abstraction")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        # simple neuron sketch on the left
        body = Circle(radius=0.55, color=WHITE, stroke_width=3,
                      fill_color=WHITE, fill_opacity=0.06).move_to([-3.6, 0.4, 0])
        dend = VGroup(*[Line([-5.6 + 0.15 * j, 1.6 - 0.6 * j, 0],
                             body.get_center() + np.array([-0.5, 0.25 - 0.5 * j, 0]),
                             color=WHITE, stroke_width=2, stroke_opacity=0.6)
                        for j in range(3)])
        axon = Line(body.get_right(), [-0.9, 0.4, 0], color=WHITE,
                    stroke_width=3)
        self.play(Create(dend), Create(body), Create(axon), run_time=1.3)
        rows = [("dendrites", "inputs (features)", BLUE),
                ("synapse strength", "weights", GREEN),
                ("cell body", "weighted sum + activation", ACCENT),
                ("axon", "output", RED)]
        for i, (bio, math_, col) in enumerate(rows):
            b = Text(bio, font_size=20, color=col, font=MONO)
            a = Text(math_, font_size=20, color=WHITE, font=MONO)
            ar = Text("->", font_size=20, color=WHITE, opacity=0.5, font=MONO)
            row = VGroup(b, ar, a).arrange(RIGHT, buff=0.4)
            row.move_to([2.9, 1.7 - 0.75 * i, 0])
            self.play(FadeIn(row, shift=LEFT * 0.3), run_time=0.6)
        cap = Text("layers of interconnected neurons, information flows one way",
                   font_size=19, color=WHITE, opacity=0.6, font=MONO
                   ).to_edge(DOWN, buff=0.5)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_Calculus(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Calculus refresher", "partial derivatives and the gradient")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        d1 = Text("partial derivative: how f changes when ONE variable\nchanges, all others held constant",
                  font_size=21, color=WHITE, font=MONO).move_to([0, 1.7, 0])
        self.play(Write(d1), run_time=1.0)
        e1 = VGroup(
            Text("f(x) = x^2", font_size=26, color=BLUE, font=MONO),
            Text("f '(x) = 2x", font_size=26, color=BLUE, font=MONO),
            Text("the slope: how x^2 changes with x", font_size=18,
                 color=WHITE, opacity=0.6, font=MONO),
        ).arrange(DOWN, buff=0.3).move_to([-3.4, -0.3, 0])
        e2 = VGroup(
            Text("f(x, y) = 2xy", font_size=26, color=GREEN, font=MONO),
            Text("df/dx = 2y   and   df/dy = 2x", font_size=26, color=GREEN,
                 font=MONO),
            Text("gradient: grad f = (2y, 2x)", font_size=21, color=GREEN,
                 font=MONO),
        ).arrange(DOWN, buff=0.3).move_to([3.4, -0.3, 0])
        self.play(FadeIn(e1, shift=RIGHT * 0.3), run_time=1.0)
        self.play(FadeIn(e2, shift=LEFT * 0.3), run_time=1.0)
        cap = Text("grad f points in the direction of steepest ascent",
                   font_size=22, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.6)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_Structure(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Basic structure", "input - hidden - output, information flows forward")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        cols = [[-4.2, 1.4], [-4.2, 0.0], [-4.2, -1.4],
                [-0.7, 1.7], [-0.7, 0.7], [-0.7, -0.3], [-0.7, -1.3],
                [3.2, 0.9], [3.2, -0.7]]
        dots = VGroup(*[Dot(np.array([x, y, 0.0]), color=WHITE, radius=0.16)
                        for x, y in cols])
        inD, hidD, outD = dots[0:3], dots[3:7], dots[7:9]
        edges = VGroup(*[Line(a.get_center(), b.get_center(), color=WHITE,
                              stroke_width=1.6, stroke_opacity=0.3)
                         for a in list(inD) + list(hidD)
                         for b in (list(hidD) if a in inD else list(outD))])
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in inD], run_time=0.7))
        self.play(Create(edges), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in hidD], run_time=0.8))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in outD], run_time=0.7))
        li = Text("INPUT layer\nreceives data", font_size=18, color=BLUE,
                  font=MONO).move_to([-4.2, -2.35, 0])
        lh = Text("HIDDEN layer(s)\nlearn intermediate representations",
                  font_size=18, color=GREEN, font=MONO).move_to([-0.7, -2.35, 0])
        lo = Text("OUTPUT layer\nthe prediction", font_size=18, color=RED,
                  font=MONO).move_to([3.2, -2.35, 0])
        self.play(FadeIn(li), FadeIn(lh), FadeIn(lo), run_time=0.9)
        cap = Text("depth = capacity to model complexity - a directed acyclic graph",
                   font_size=19, color=ACCENT, font=MONO).to_edge(UP, buff=1.55)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_Neuron(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Inside one neuron", "weighted sum, then activation")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        xs = [(-4.4, 1.5), (-4.4, 0.5), (-4.4, -0.5), (-4.4, -1.5)]
        xvals = ["x1 = 0.5", "x2 = 1.2", "x3 = 0.8", "x4 = 2.0"]
        inD = VGroup(*[Dot(np.array([x, y, 0.0]), color=WHITE, radius=0.14)
                       for x, y in xs])
        labels = VGroup(*[Text(v, font_size=22, color=WHITE, font=MONO)
                          .next_to(d, LEFT, buff=0.35)
                          for v, d in zip(xvals, inD)])
        summ = Circle(radius=0.5, color=BLUE, stroke_width=3).move_to([-1.2, 0, 0])
        st = Text("sum", font_size=20, color=BLUE, font=MONO
                  ).move_to([-1.2, 0, 0])
        lines = VGroup(*[Line(d.get_right(), summ.get_center() + LEFT * 0.45,
                              color=WHITE, stroke_width=2.5, stroke_opacity=0.6)
                         for d in inD])
        woffs = [UP * 0.45, UP * 0.35, DOWN * 0.35, DOWN * 0.45]
        wvals = ["w1 = 0.3", "w2 = 0.2", "w3 = 0.8", "w4 = 0.6"]
        wls = VGroup(*[Text(w, font_size=21, color=GREEN, font=MONO)
                       .move_to((d.get_center() + summ.get_center()) / 2 + off)
                       for w, d, off in zip(wvals, inD, woffs)])
        self.play(LaggedStart(*[FadeIn(d) for d in inD], run_time=0.7),
                  FadeIn(labels), run_time=0.7)
        self.play(Create(lines), FadeIn(wls), run_time=1.0)
        self.play(Create(summ), FadeIn(st), run_time=0.7)
        act = RoundedRectangle(corner_radius=0.1, width=1.5, height=0.9,
                               stroke_color=ACCENT, stroke_width=3,
                               fill_color=ACCENT, fill_opacity=0.06
                               ).move_to([1.4, 0, 0])
        at = Text("act", font_size=20, color=ACCENT, font=MONO
                  ).move_to([1.4, 0, 0])
        ar1 = Arrow(summ.get_right(), act.get_left() - RIGHT * 0.05,
                    stroke_width=3, color=WHITE,
                    max_tip_length_to_length_ratio=0.3)
        zl = Text("z = w . x + b", font_size=20, color=BLUE, font=MONO
                  ).move_to([0.4, 0.85, 0])
        self.play(Create(ar1), FadeIn(act), FadeIn(at), Write(zl), run_time=1.0)
        ar2 = Arrow(act.get_right(), [4.4, 0, 0], stroke_width=3, color=WHITE,
                    max_tip_length_to_length_ratio=0.2)
        yl = Text("yhat = sigma(z)", font_size=22, color=GREEN, font=MONO
                  ).move_to([5.3, 0, 0])
        self.play(Create(ar2), Write(yl), run_time=0.9)
        cap = VGroup(
            Text("weights w: how important each input is", font_size=19,
                 color=GREEN, font=MONO),
            Text("bias b: shifts the output - adds flexibility", font_size=19,
                 color=GREEN, font=MONO),
            Text("W and b are learned to shrink the gap between yhat and y",
                 font_size=19, color=ACCENT, font=MONO),
        ).arrange(DOWN, buff=0.28).to_edge(DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(l) for l in cap], run_time=1.3))
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_History(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("A brief history", "ideas, winters, and GPUs")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = NumberLine(x_range=[1940, 2025, 10], length=11.5,
                        include_ticks=False, include_numbers=False)
        ax.set_stroke(WHITE, 2, opacity=0.35)
        ax.shift(DOWN * 0.1)
        self.play(Create(ax), run_time=0.8)
        marks = [(1943, "McCulloch + Pitts:\nfirst math neuron model", BLUE, UP, 1.05),
                 (1957, "Rosenblatt:\nthe perceptron", BLUE, DOWN, 1.05),
                 (1974, "AI winter: Minsky + Papert\nexpose limits, little compute", RED, UP, 1.05),
                 (1986, "rebirth: backpropagation", GREEN, DOWN, 1.05),
                 (1997, "boom / bust:\nSVMs take over", RED, UP, 1.95),
                 (2009, "GPUs make big\nnetworks practical", GREEN, DOWN, 1.05),
                 (2018, "renaissance: big data +\nstate-of-the-art deep learning", ACCENT, UP, 1.05)]
        for yr, note, col, side, h in marks:
            x = ax.number_to_point(yr)
            tick = Line(x, x + (UP if side is UP else DOWN) * 0.25,
                        stroke_width=2.5, color=col)
            yr_t = Text(str(yr), font_size=16, color=col, font=MONO).move_to(
                x + (DOWN if side is UP else UP) * 0.28)
            note_t = Text(note, font_size=14, color=WHITE, opacity=0.75,
                          font=MONO).move_to(x + (UP if side is UP else DOWN) * h)
            self.play(Create(tick), FadeIn(yr_t), FadeIn(note_t), run_time=0.55)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_Perceptron(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The perceptron (1957)", "the simplest neural unit")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        f = Text("yhat = step(w . x + b)", font_size=28, color=WHITE,
                 font=MONO).move_to([-3.9, 1.7, 0])
        rule = VGroup(
            Text("z >= 0 -> predict class 1", font_size=21, color=GREEN,
                 font=MONO),
            Text("z <  0 -> predict class 0", font_size=21, color=RED,
                 font=MONO),
        ).arrange(DOWN, buff=0.3).move_to([-3.9, 0.5, 0])
        self.play(Write(f), run_time=0.9)
        self.play(FadeIn(rule), run_time=0.8)
        # linear boundary panel
        p = np.array([2.6, -1.6, 0.0])
        g = VGroup(*[Dot(p + np.array([dx, dy, 0.0]), color=GREEN, radius=0.09)
                     for dx, dy in [(0.4, 1.6), (1.4, 1.2), (0.9, 0.5),
                                    (1.8, 1.9), (1.5, 0.4)]])
        r = VGroup(*[Dot(p + np.array([dx, dy, 0.0]), color=RED, radius=0.09)
                     for dx, dy in [(-1.4, -0.4), (-0.6, 0.6), (-1.8, 0.9),
                                    (-0.9, -1.2), (-1.9, 0.1)]])
        bline = Line(p + np.array([-1.9, 1.7, 0.0]), p + np.array([1.7, -1.9, 0.0]),
                     color=ACCENT, stroke_width=3)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in g], run_time=0.7),
                  LaggedStart(*[FadeIn(d, scale=0.5) for d in r], run_time=0.7))
        self.play(Create(bline), run_time=0.8)
        bl = Text("learns a LINEAR decision boundary", font_size=19,
                  color=ACCENT, font=MONO).move_to([4.3, 1.9, 0])
        self.play(Write(bl), run_time=0.7)
        train = Text("training: update ONLY on mistakes - move the boundary\nthe right way (perceptron learning rule)",
                     font_size=19, color=WHITE, font=MONO).move_to([-2.4, -1.5, 0])
        self.play(Write(train), run_time=1.0)
        lim = Text("limits: only linearly separable data - fails XOR - no hidden\nlayers - binary only",
                   font_size=19, color=RED, font=MONO).to_edge(DOWN, buff=0.45)
        self.play(Write(lim), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_Activations(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Activation functions", "the gate that adds non-linearity")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        head = Text("without activation, stacked layers collapse into ONE linear model",
                    font_size=20, color=ACCENT, font=MONO).to_edge(UP, buff=1.5)
        self.play(Write(head), run_time=0.9)

        def panel(x0, name, fn, col, note):
            ax = Axes(x_range=[-4, 4, 2], y_range=[-2, 2, 1], x_length=2.9,
                      y_length=2.0,
                      axis_config={"stroke_opacity": 0.2, "include_ticks": False},
                      ).move_to([x0, 0.35, 0])
            crv = ax.plot(fn, color=col, stroke_width=3.5)
            nm = Text(name, font_size=19, color=col, weight=BOLD, font=MONO
                      ).move_to([x0, 1.9, 0])
            nt = Text(note, font_size=14, color=WHITE, opacity=0.6, font=MONO
                      ).move_to([x0, -1.55, 0])
            return VGroup(ax, crv, nm, nt)

        relu = lambda a: np.maximum(0, a)
        leaky = lambda a: np.where(a < 0, 0.2 * a, a)
        lin = lambda a: 0.5 * a
        tanh = np.tanh
        panels = VGroup(
            panel(-5.0, "linear", lin, WHITE, "f(z) = z: still linear"),
            panel(-2.5, "sigmoid", sigmoid_x, BLUE, "0 to 1, probability"),
            panel(0.0, "tanh", tanh, GREEN, "-1 to 1, vanishing grads"),
            panel(2.5, "ReLU", relu, ACCENT, "0 if negative, else z"),
            panel(5.0, "leaky ReLU", leaky, RED, "small slope below 0:\nno dead neurons"),
        )
        for pn in panels:
            self.play(FadeIn(pn[2]), Create(pn[0]), Create(pn[1]),
                      FadeIn(pn[3]), run_time=0.75)
        foot = Text("softmax: turns outputs into probabilities for multi-class",
                    font_size=19, color=WHITE, opacity=0.7, font=MONO
                    ).to_edge(DOWN, buff=0.45)
        self.play(Write(foot), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_TrainingLoop(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Training loop", "forward, measure, backward, update, repeat")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        cols = [[-4.6, 1.2], [-4.6, 0.0], [-4.6, -1.2],
                [-1.5, 1.5], [-1.5, 0.5], [-1.5, -0.5], [-1.5, -1.5],
                [1.6, 0.7], [1.6, -0.7]]
        dots = VGroup(*[Dot(np.array([x, y, 0.0]), color=WHITE, radius=0.15)
                        for x, y in cols])
        inD, hidD, outD = dots[0:3], dots[3:7], dots[7:9]
        e1 = VGroup(*[Line(a.get_center(), b.get_center(), color=WHITE,
                           stroke_width=1.8, stroke_opacity=0.35)
                      for a in inD for b in hidD])
        e2 = VGroup(*[Line(a.get_center(), b.get_center(), color=WHITE,
                           stroke_width=1.8, stroke_opacity=0.35)
                      for a in hidD for b in outD])
        self.add(dots, e1, e2)
        # forward pulse
        pulse = VGroup()
        for src, dst in [(inD, hidD), (hidD, outD)]:
            for a in src:
                for b in dst:
                    pulse.add(Line(a.get_center(), b.get_center(),
                                   color=ACCENT, stroke_width=3))
        fwd = Text("1. FORWARD PASS: activations flow left to right",
                   font_size=21, color=ACCENT, font=MONO).to_edge(DOWN, buff=1.15)
        self.play(Write(fwd), run_time=0.7)
        self.play(LaggedStart(*[Create(l) for l in pulse], lag_ratio=0.05,
                              run_time=1.6))
        self.play(*[FadeOut(l) for l in pulse], run_time=0.4)
        loss = box("2. LOSS: compare yhat with y", 4.4, 0.8, RED, 19
                   ).to_edge(DOWN, buff=0.45)
        self.play(Transform(fwd, loss), run_time=0.7)
        # backward arrows
        back = VGroup(*[Arrow(b.get_center(), a.get_center(), color=GREEN,
                              stroke_width=3, buff=0.25,
                              max_tip_length_to_length_ratio=0.18)
                        for a, b in [(hidD[1], outD[0]), (hidD[2], outD[1])]])
        bwd = Text("3. BACKWARD PASS: gradients flow right to left (chain rule)",
                   font_size=21, color=GREEN, font=MONO).to_edge(DOWN, buff=0.45)
        self.play(Create(back), Transform(fwd, bwd), run_time=1.2)
        upd = Text("4. UPDATE: W = W - learning_rate * dL/dW, then repeat for epochs",
                   font_size=21, color=BLUE, font=MONO).to_edge(DOWN, buff=0.45)
        self.play(Transform(fwd, upd), run_time=0.9)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_Backprop(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Backpropagation + the chain rule", "who is to blame for the error?")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        d1 = Text("the network is a COMPOSITION of functions, layer by layer",
                  font_size=21, color=WHITE, font=MONO).move_to([0, 1.8, 0])
        d2 = Text("chain rule: multiply the derivatives of each layer,\nbackward from output to input",
                  font_size=21, color=WHITE, font=MONO).move_to([0, 0.7, 0])
        self.play(Write(d1), run_time=0.9)
        self.play(Write(d2), run_time=0.9)
        chain = VGroup(
            box("E total", 1.7, 0.8, RED, 19),
            Text("->", font_size=24, color=WHITE, opacity=0.6, font=MONO),
            box("output o1", 2.0, 0.8, BLUE, 19),
            Text("->", font_size=24, color=WHITE, opacity=0.6, font=MONO),
            box("net o1", 1.7, 0.8, BLUE, 19),
            Text("->", font_size=24, color=WHITE, opacity=0.6, font=MONO),
            box("weight w5", 1.9, 0.8, GREEN, 19),
        ).arrange(RIGHT, buff=0.45).move_to([0, -0.5, 0])
        cl = Text("trace the dependency chain, then differentiate each link",
                  font_size=19, color=WHITE, opacity=0.6, font=MONO
                  ).move_to([0, -1.45, 0])
        self.play(LaggedStart(*[FadeIn(m) for m in chain], run_time=1.4),
                  FadeIn(cl), run_time=0.8)
        g1 = Text("big gradient -> that weight matters a lot for the error",
                  font_size=20, color=GREEN, font=MONO).to_edge(DOWN, buff=1.0)
        g2 = Text("small gradient -> that weight barely matters", font_size=20,
                  color=RED, font=MONO).next_to(g1, DOWN, buff=0.25)
        self.play(Write(g1), run_time=0.8)
        self.play(Write(g2), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_GraphExample(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Backprop on a tiny graph", "a simplified computational graph")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        px, py, pz, pq, pf = (-4.8, 1.5), (-4.8, 0.0), (-4.8, -1.5), (-1.2, 0.75), (2.4, 0.0)
        nodes = {}
        vals = {"x": "-2", "y": "5", "z": "-4", "q": "x + y", "f": "q * z"}
        cols = {"x": WHITE, "y": WHITE, "z": WHITE, "q": BLUE, "f": ACCENT}
        for name, (x, y) in [("x", px), ("y", py), ("z", pz), ("q", pq), ("f", pf)]:
            c = Circle(radius=0.42, color=cols[name], stroke_width=3,
                       fill_color=cols[name], fill_opacity=0.08
                       ).move_to([x, y, 0])
            lt = Text(name, font_size=22, color=cols[name], font=MONO
                      ).move_to([x, y, 0])
            nodes[name] = VGroup(c, lt)
        e1 = Line(np.array([px[0] + 0.42, px[1], 0]), np.array([pq[0] - 0.42, pq[1] + 0.15, 0]),
                  color=WHITE, stroke_width=2.5, stroke_opacity=0.5)
        e2 = Line(np.array([py[0] + 0.42, py[1], 0]), np.array([pq[0] - 0.42, pq[1] - 0.15, 0]),
                  color=WHITE, stroke_width=2.5, stroke_opacity=0.5)
        e3 = Line(np.array([pq[0] + 0.42, pq[1] + 0.1, 0]), np.array([pf[0] - 0.42, pf[1] + 0.2, 0]),
                  color=WHITE, stroke_width=2.5, stroke_opacity=0.5)
        e4 = Line(np.array([pz[0] + 0.42, pz[1], 0]), np.array([pf[0] - 0.42, pf[1] - 0.2, 0]),
                  color=WHITE, stroke_width=2.5, stroke_opacity=0.5)
        self.play(LaggedStart(*[FadeIn(nodes[n], scale=0.6) for n in "xyz"],
                              run_time=0.9))
        self.play(Create(e1), Create(e2), FadeIn(nodes["q"]), run_time=0.9)
        self.play(Create(e3), Create(e4), FadeIn(nodes["f"]), run_time=0.9)
        fwd = Text("forward: f = (x + y) * z, so q = -2 + 5 = 3, f = 3 * -4 = 12",
                   font_size=21, color=BLUE, font=MONO).to_edge(DOWN, buff=1.15)
        self.play(Write(fwd), run_time=1.0)
        b1 = Text("backward: df/dz = q = 3   and   df/dq = z = -4",
                  font_size=21, color=GREEN, font=MONO).to_edge(DOWN, buff=1.15)
        self.play(Transform(fwd, b1), run_time=0.9)
        b2 = Text("chain rule for x: df/dx = df/dq * dq/dx = -4 * 1 = -4",
                  font_size=21, color=GREEN, font=MONO).to_edge(DOWN, buff=1.15)
        self.play(Transform(fwd, b2), run_time=0.9)
        note = Text("y is not wired straight to f - the chain rule carries its\ninfluence through q",
                    font_size=19, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.45)
        self.play(Write(note), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_NumericExample(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("A worked forward pass", "2 inputs, 2 hidden, 2 outputs, sigmoid")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        # mini network
        pos = {"i1": (-5.4, 1.1), "i2": (-5.4, 0.0), "h1": (-2.4, 1.4),
               "h2": (-2.4, 0.0), "o1": (0.6, 1.1), "o2": (0.6, 0.0)}
        dots = VGroup(*[Dot(np.array([x, y, 0.0]), color=WHITE, radius=0.13)
                        for x, y in pos.values()])
        edges = VGroup(*[Line(np.array([pos[a][0], pos[a][1], 0]),
                              np.array([pos[b][0], pos[b][1], 0]),
                              color=WHITE, stroke_width=1.5, stroke_opacity=0.3)
                         for a, b in [("i1", "h1"), ("i2", "h1"), ("i1", "h2"),
                                      ("i2", "h2"), ("h1", "o1"), ("h2", "o1"),
                                      ("h1", "o2"), ("h2", "o2")]])
        self.add(dots, edges)
        labs = VGroup(
            Text("i1 = 0.05  i2 = 0.10", font_size=17, color=WHITE, font=MONO
                 ).move_to([-5.4, -1.0, 0]),
            Text("targets: 0.01 and 0.99", font_size=17, color=WHITE,
                 opacity=0.6, font=MONO).move_to([-5.4, -1.5, 0]),
        )
        self.play(FadeIn(labs), run_time=0.7)
        steps = VGroup(
            Text("neth1 = w1 i1 + w2 i2 + b1 = 0.3775", font_size=19,
                 color=BLUE, font=MONO),
            Text("outh1 = sigmoid(0.3775) = 0.5933", font_size=19, color=BLUE,
                 font=MONO),
            Text("outh2 = 0.5969", font_size=19, color=BLUE, font=MONO),
            Text("neto1 = 1.1059 -> outo1 = 0.7514", font_size=19, color=GREEN,
                 font=MONO),
            Text("outo2 = 0.7729", font_size=19, color=GREEN, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.7, 0])
        for ln in steps:
            self.play(FadeIn(ln, shift=LEFT * 0.3), run_time=0.6)
        err = VGroup(
            Text("error = 1/2 (predicted - target)^2", font_size=19,
                 color=RED, font=MONO),
            Text("Eo1 = 0.2748   Eo2 = 0.0236", font_size=19, color=RED,
                 font=MONO),
            Text("E total = 0.2984", font_size=21, color=ACCENT, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.4, -2.0, 0])
        for ln in err:
            self.play(FadeIn(ln, shift=UP * 0.2), run_time=0.6)
        cap = Text("then backprop: dE/dw5 = dE/dout * dout/dnet * dnet/dw5,\nupdate w5 = w5 - alpha * dE/dw5",
                   font_size=18, color=WHITE, opacity=0.7, font=MONO
                   ).to_edge(DOWN, buff=0.35)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L19_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, _ = title_block("Lecture 19 in one breath", "")
        self.play(Write(t), run_time=0.9)
        lines = VGroup(
            Text("logistic regression = weighted sum + sigmoid + threshold",
                 font_size=22, color=WHITE, font=MONO),
            Text("a neuron: z = w . x + b, then an activation", font_size=22,
                 color=WHITE, font=MONO),
            Text("activations add non-linearity: sigmoid, tanh, ReLU, softmax",
                 font_size=22, color=WHITE, font=MONO),
            Text("perceptron alone = linear boundary only (fails XOR)",
                 font_size=22, color=RED, font=MONO),
            Text("train: forward -> loss -> backprop (chain rule) -> update W",
                 font_size=22, color=BLUE, font=MONO),
            Text("W = W - learning_rate * dL/dW, repeated over epochs",
                 font_size=22, color=ACCENT, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT * 0.3), run_time=0.7)
        note = Text("finicky: learning rate and hidden-node count need tuning",
                    font_size=19, color=WHITE, opacity=0.6, font=MONO
                    ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
