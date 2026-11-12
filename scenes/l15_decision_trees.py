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


def node(text, col=BLUE, w=2.0, h=0.7, fs=18):
    return box(text, w, h, col, fs)


def edge(a, b, col=WHITE, sw=2.5):
    return Line(a.get_bottom(), b.get_top(), stroke_width=sw,
                stroke_opacity=0.7, color=col)


class L15_Title(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Decision Trees", "CMSC 320 - lecture 15")
        self.play(Write(t), run_time=1.3)
        self.play(FadeIn(s, shift=DOWN * 0.2), run_time=0.7)
        self.wait(1.0)
        core = Text("learning through questions", font_size=30, color=ACCENT,
                    weight=BOLD, font=MONO)
        self.play(FadeOut(s), Write(core), run_time=1.4)
        self.wait(1.8)
        agenda = Text("structure - purity - entropy - info gain - pruning",
                      font_size=19, color=WHITE, opacity=0.55, font=MONO
                      ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(agenda), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L15_WhatIs(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("What is a decision tree?", "a flowchart that learned itself")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        pts = VGroup(
            Text("+ supervised ML: a core predictive model", font_size=21,
                 color=GREEN, font=MONO),
            Text("+ sequential questions about the data", font_size=21,
                 color=GREEN, font=MONO),
            Text("+ feature splitting at every node", font_size=21,
                 color=GREEN, font=MONO),
            Text("+ dual purpose: classification AND regression", font_size=21,
                 color=GREEN, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.4, 0.4, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in pts],
                              run_time=1.8))
        ex = box("Will a customer buy?", w=3.4, h=0.8, col=ACCENT, fs=19
                 ).move_to([3.4, 1.6, 0])
        yes = box("yes -> BUY", w=2.2, h=0.65, col=GREEN, fs=16
                  ).move_to([2.3, 0.2, 0])
        no = box("no -> SKIP", w=2.2, h=0.65, col=RED, fs=16
                 ).move_to([4.6, 0.2, 0])
        e1 = Line(ex.get_bottom() + LEFT * 0.7, yes.get_top())
        e2 = Line(ex.get_bottom() + RIGHT * 0.7, no.get_top())
        self.play(Write(ex), Create(e1), Create(e2), FadeIn(yes), FadeIn(no),
                  run_time=1.4)
        cap = Text("unlike KNN (distances), a tree learns decision RULES",
                   font_size=20, color=WHITE, font=MONO).to_edge(DOWN, buff=0.7)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L15_Terminology(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Terminology", "the anatomy of a tree")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        root = node("root node", BLUE, 2.0, 0.7, 18).move_to([0, 1.9, 0])
        i1 = node("internal node", BLUE, 2.2, 0.7, 16).move_to([-2.6, 0.4, 0])
        i2 = node("leaf node", GREEN, 1.9, 0.7, 16).move_to([2.6, 0.4, 0])
        l1 = node("leaf", GREEN, 1.3, 0.6, 15).move_to([-3.6, -1.1, 0])
        l2 = node("leaf", RED, 1.3, 0.6, 15).move_to([-1.6, -1.1, 0])
        self.play(Write(root), run_time=0.7)
        self.play(Create(edge(root, i1)), Create(edge(root, i2)),
                  FadeIn(i1), FadeIn(i2), run_time=1.0)
        self.play(Create(edge(i1, l1)), Create(edge(i1, l2)),
                  FadeIn(l1), FadeIn(l2), run_time=0.9)
        ann = VGroup(
            Text("root: start, no incoming branch", font_size=17, color=BLUE,
                 font=MONO).move_to([3.6, 1.9, 0]),
            Text("internal: tests a feature, splits", font_size=17, color=BLUE,
                 font=MONO).move_to([-4.3, 1.35, 0]),
            Text("leaf: final prediction, no splits", font_size=17, color=GREEN,
                 font=MONO).move_to([4.0, 0.4, 0]),
            Text("branch: one possible outcome", font_size=17, color=WHITE,
                 font=MONO).move_to([-4.6, -0.35, 0]),
        )
        self.play(LaggedStart(*[FadeIn(a, shift=RIGHT * 0.2) for a in ann],
                              run_time=1.6))
        foot = Text("layer = same depth from root   depth = max layers to a leaf\nbinary tree: every node has exactly 2 branches",
                    font_size=18, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.5)
        self.play(Write(foot), run_time=1.1)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L15_OutputTypes(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Two outputs", "classification trees vs regression trees")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ct = VGroup(
            Text("1. CLASSIFICATION TREE", font_size=22, color=GREEN,
                 weight=BOLD, font=MONO),
            Text("output = discrete category", font_size=19, color=WHITE,
                 font=MONO),
            Text("Yes / No, Cat / Dog", font_size=19, color=GREEN, font=MONO),
        ).arrange(DOWN, buff=0.35).move_to([-3.5, 0.9, 0])
        rt = VGroup(
            Text("2. REGRESSION TREE", font_size=22, color=BLUE, weight=BOLD,
                 font=MONO),
            Text("output = continuous number", font_size=19, color=WHITE,
                 font=MONO),
            Text("house price, temperature", font_size=19, color=BLUE,
                 font=MONO),
        ).arrange(DOWN, buff=0.35).move_to([3.5, 0.9, 0])
        self.play(FadeIn(ct, shift=RIGHT * 0.3), run_time=1.0)
        self.play(FadeIn(rt, shift=LEFT * 0.3), run_time=1.0)
        rule = Text("every root-to-leaf path = an IF-THEN rule", font_size=21,
                    color=ACCENT, font=MONO).move_to([0, -1.15, 0])
        thr = Text("continuous feature? test it against a threshold:\n'age > 30?' -> left / right",
                   font_size=18, color=WHITE, opacity=0.7, font=MONO
                   ).next_to(rule, DOWN, buff=0.4)
        self.play(Write(rule), run_time=1.0)
        self.play(FadeIn(thr), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L15_Tennis(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The tennis dataset", "play tennis on Saturday? (Tom Mitchell)")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        rows = [
            ("Day", "Outlook", "Wind", "Tennis?", None),
            ("D1", "Sunny", "Weak", "No", RED),
            ("D3", "Overcast", "Weak", "Yes", GREEN),
            ("D4", "Rain", "Weak", "Yes", GREEN),
            ("D6", "Rain", "Strong", "No", RED),
            ("D9", "Sunny", "Weak", "Yes", GREEN),
        ]
        tab = VGroup()
        for c1, c2, c3, c4, lab in rows:
            head = BLUE if lab is None else WHITE
            line = VGroup(
                Text(f"{c1:<4}", font_size=21, color=head, font=MONO),
                Text(f"{c2:<9}", font_size=21, color=head, font=MONO),
                Text(f"{c3:<7}", font_size=21, color=head, font=MONO),
                Text(c4, font_size=21, color=(lab or head), font=MONO),
            ).arrange(RIGHT, buff=0.02)
            tab.add(line)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.6, 0.2, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in tab],
                              run_time=1.6))
        facts = VGroup(
            Text("14 examples total", font_size=19, color=WHITE, font=MONO),
            Text("4 categorical features:", font_size=19, color=WHITE,
                 font=MONO),
            Text("Outlook Temp Humidity Wind", font_size=19, color=BLUE,
                 font=MONO),
            Text("target: Play vs No-Play", font_size=19, color=ACCENT,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.6, 0.4, 0])
        self.play(LaggedStart(*[FadeIn(f, shift=LEFT * 0.2) for f in facts],
                              run_time=1.4))
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L15_Purity(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Pure vs impure", "the goal: groups as pure as possible")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        pure = VGroup(
            Text("PURE node", font_size=22, color=GREEN, weight=BOLD,
                 font=MONO),
            Text("all one class: 4 Yes / 0 No", font_size=19, color=WHITE,
                 font=MONO),
            Text("no further splitting needed", font_size=19, color=WHITE,
                 font=MONO),
        ).arrange(DOWN, buff=0.35).move_to([-3.5, 0.9, 0])
        imp = VGroup(
            Text("IMPURE node", font_size=22, color=RED, weight=BOLD,
                 font=MONO),
            Text("mixed classes: 2 Yes / 3 No", font_size=19, color=WHITE,
                 font=MONO),
            Text("must split further", font_size=19, color=WHITE, font=MONO),
        ).arrange(DOWN, buff=0.35).move_to([3.5, 0.9, 0])
        self.play(FadeIn(pure, shift=RIGHT * 0.3), run_time=1.0)
        self.play(FadeIn(imp, shift=LEFT * 0.3), run_time=1.0)
        ex = Text("in tennis: 'Overcast' is PURE (all Yes)\n'Sunny' and 'Rain' are IMPURE",
                  font_size=20, color=BLUE, font=MONO).move_to([0, -1.3, 0])
        cap = Text("a good split reduces impurity - we need to MEASURE it",
                   font_size=20, color=ACCENT, font=MONO
                   ).to_edge(DOWN, buff=0.6)
        self.play(Write(ex), run_time=1.0)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L15_Entropy(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Entropy", "how mixed is this node?")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        formula = Text("H(S) = - sum p_i * log2(p_i)", font_size=28,
                       color=ACCENT, font=MONO).move_to([-3.6, 1.5, 0])
        self.play(Write(formula), run_time=1.1)
        rules = VGroup(
            Text("H = 0   pure, zero uncertainty", font_size=19, color=GREEN,
                 font=MONO),
            Text("H = 1   max impurity, 50/50 split", font_size=19, color=RED,
                 font=MONO),
            Text("more mixing -> higher entropy", font_size=19, color=WHITE,
                 font=MONO),
            Text("0 log2 0 is treated as 0", font_size=17, color=WHITE,
                 opacity=0.6, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.6, -0.1, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rules],
                              run_time=1.6))
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1.1, 0.5], x_length=4.2,
                  y_length=3.2, axis_config={"stroke_opacity": 0.2,
                                             "include_ticks": False},
                  ).move_to([3.4, 0.15, 0])
        curve = ax.plot(lambda x: -(x * np.log2(np.maximum(x, 1e-9)) +
                                    (1 - x) * np.log2(np.maximum(1 - x, 1e-9))),
                        color=BLUE, stroke_width=4)
        h0 = Text("H=0", font_size=17, color=GREEN, font=MONO
                  ).move_to(ax.c2p(0.08, 0.18))
        h1 = Text("H=1 at p=0.5", font_size=17, color=RED, font=MONO
                  ).move_to(ax.c2p(0.5, 1.02))
        cap = Text("binary entropy curve: p = fraction of one class",
                   font_size=18, color=WHITE, opacity=0.55, font=MONO
                   ).to_edge(DOWN, buff=0.55)
        self.play(Create(ax), run_time=0.8)
        self.play(Create(curve), FadeIn(h0), run_time=1.2)
        self.play(FadeIn(h1), Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L15_InfoGain(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Information gain", "how much does a split reduce entropy?")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        formula = Text("IG = H(before) - weighted H(after)", font_size=26,
                       color=ACCENT, font=MONO).move_to([0, 1.55, 0])
        self.play(Write(formula), run_time=1.0)
        root = node("S = 9+ / 5-\nH = 0.940", BLUE, 2.3, 0.95, 16
                    ).move_to([0, 0.15, 0])
        weak = node("weak\n6+ / 2-  H=0.811", GREEN, 2.5, 0.95, 15
                    ).move_to([-2.8, -1.5, 0])
        strong = node("strong\n3+ / 3-  H=1.000", RED, 2.5, 0.95, 15
                      ).move_to([2.8, -1.5, 0])
        lbl = Text("split on Wind", font_size=17, color=WHITE, opacity=0.6,
                   font=MONO).move_to([0, -0.62, 0])
        self.play(Write(root), FadeIn(lbl), run_time=0.9)
        self.play(Create(edge(root, weak)), Create(edge(root, strong)),
                  FadeIn(weak), FadeIn(strong), run_time=1.1)
        calc = Text("IG(S, wind) = 0.940 - (8/14*0.811 + 6/14*1.000) = 0.048",
                    font_size=19, color=WHITE, font=MONO
                    ).to_edge(DOWN, buff=0.85)
        self.play(Write(calc), run_time=1.1)
        rank = Text("outlook 0.246   humidity 0.151   temp 0.029   wind 0.048",
                    font_size=19, color=BLUE, font=MONO
                    ).next_to(calc, DOWN, buff=0.28)
        best = Text("^ best: outlook becomes the root", font_size=19,
                    color=ACCENT, font=MONO).next_to(rank, DOWN, buff=0.25)
        self.play(Write(rank), run_time=1.0)
        self.play(Write(best), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L15_GrowTree(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Divide and conquer", "growing the tennis tree, split by split")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        root = node("Outlook\n9+ / 5-", BLUE, 2.1, 0.9, 16).move_to([0, 2.0, 0])
        self.play(Write(root), run_time=0.8)
        sunny = node("Sunny\n2+ / 3-", BLUE, 1.7, 0.85, 15).move_to([-4.2, 0.5, 0])
        over = node("Overcast\n4+ / 0-", GREEN, 1.9, 0.85, 15).move_to([0, 0.5, 0])
        rain = node("Rain\n3+ / 2-", BLUE, 1.6, 0.85, 15).move_to([4.2, 0.5, 0])
        e1, e2, e3 = edge(root, sunny), edge(root, over), edge(root, rain)
        b1 = Text("Sunny", font_size=14, color=WHITE, opacity=0.6, font=MONO
                  ).move_to([-1.7, 1.48, 0])
        b2 = Text("Overcast", font_size=14, color=WHITE, opacity=0.6, font=MONO
                  ).move_to([0.75, 1.25, 0])
        b3 = Text("Rain", font_size=14, color=WHITE, opacity=0.6, font=MONO
                  ).move_to([2.5, 1.35, 0])
        self.play(Create(e1), Create(e2), Create(e3), FadeIn(sunny),
                  FadeIn(over), FadeIn(rain), FadeIn(b1), FadeIn(b2),
                  FadeIn(b3), run_time=1.5)
        yes = node("Yes", GREEN, 1.2, 0.6, 16).move_to([0, -0.9, 0])
        self.play(Create(edge(over, yes, GREEN)), FadeIn(yes), run_time=0.8)
        note = Text("Overcast is pure -> stop", font_size=18,
                    color=GREEN, font=MONO).move_to([0, -1.72, 0])
        self.play(FadeIn(note), run_time=0.7)
        hum = node("Humidity", BLUE, 1.9, 0.65, 15).move_to([-4.2, -0.9, 0])
        self.play(Create(edge(sunny, hum, BLUE)), FadeIn(hum), run_time=0.8)
        hn = node("High -> No", RED, 1.7, 0.6, 14).move_to([-5.1, -2.1, 0])
        hy = node("Normal -> Yes", GREEN, 2.0, 0.6, 14).move_to([-2.9, -2.1, 0])
        self.play(Create(edge(hum, hn, RED)), Create(edge(hum, hy, GREEN)),
                  FadeIn(hn), FadeIn(hy), run_time=1.0)
        wind = node("Wind", BLUE, 1.5, 0.65, 15).move_to([4.2, -0.9, 0])
        self.play(Create(edge(rain, wind, BLUE)), FadeIn(wind), run_time=0.8)
        wn = node("Strong -> No", RED, 2.0, 0.6, 14).move_to([3.1, -2.1, 0])
        wy = node("Weak -> Yes", GREEN, 1.9, 0.6, 14).move_to([5.4, -2.1, 0])
        self.play(Create(edge(wind, wn, RED)), Create(edge(wind, wy, GREEN)),
                  FadeIn(wn), FadeIn(wy), run_time=1.0)
        rule = Text("rule: at each node pick the feature with the highest IG;\nnever re-test a feature already used on the path",
                    font_size=18, color=ACCENT, font=MONO
                    ).to_edge(DOWN, buff=0.35)
        self.play(Write(rule), run_time=1.1)
        self.wait(2.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L15_Concept(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("What the tree represents", "boolean logic, one path at a time")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        left = VGroup(
            Text("each path = AND of its tests", font_size=20, color=GREEN,
                 font=MONO),
            Text("whole tree = OR of the paths", font_size=20, color=GREEN,
                 font=MONO),
            Text("can express ANY boolean function", font_size=20, color=WHITE,
                 font=MONO),
            Text("(AND, OR, XOR...)", font_size=18, color=WHITE, opacity=0.6,
                 font=MONO),
            Text("some functions need exponentially\nlarge trees", font_size=18,
                 color=RED, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.4, 0.4, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in left],
                              run_time=1.8))
        rule = VGroup(
            Text("IF (Outlook=Sunny AND Humidity=High)", font_size=18,
                 color=BLUE, font=MONO),
            Text("   OR (Outlook=Rain AND Wind=Strong)", font_size=18,
                 color=BLUE, font=MONO),
            Text("THEN Play Tennis = No", font_size=18, color=ACCENT,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.3, 0.7, 0])
        self.play(LaggedStart(*[Write(l) for l in rule], run_time=1.5))
        occ = Text("Occam's razor: prefer simpler trees ->\nfewer splits, better generalization",
                   font_size=19, color=WHITE, font=MONO).to_edge(DOWN, buff=0.55)
        self.play(Write(occ), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L15_Overfit(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Overfitting", "when the tree memorizes the noise")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2], x_length=6.0,
                  y_length=4.2, axis_config={"stroke_opacity": 0.15,
                                             "include_ticks": False},
                  ).shift(LEFT * 2.6 + DOWN * 0.25)
        self.play(Create(ax), run_time=0.8)
        rng = np.random.default_rng(7)
        greens = [(x, y) for x in rng.uniform(0.5, 3.5, 12)
                  for y in [rng.uniform(6.5, 9.5)]]
        reds = [(x, y) for x in rng.uniform(4.5, 9.5, 16)
                for y in [rng.uniform(0.5, 3.5)]]
        gd = VGroup(*[Dot(ax.c2p(x, y), color=GREEN, radius=0.07)
                      for x, y in greens])
        rd = VGroup(*[Dot(ax.c2p(x, y), color=RED, radius=0.07)
                      for x, y in reds])
        odd = Dot(ax.c2p(2.0, 1.5), color=ACCENT, radius=0.12)
        self.play(FadeIn(gd), FadeIn(rd), run_time=0.9)
        box1 = Rectangle(width=3.2, height=3.2, color=WHITE, stroke_width=2,
                         stroke_opacity=0.5).move_to(ax.c2p(2.0, 8.0))
        box2 = Rectangle(width=1.0, height=1.0, color=ACCENT, stroke_width=2.5
                         ).move_to(ax.c2p(2.0, 1.5))
        self.play(Create(box1), run_time=0.7)
        self.play(Create(box2), FadeIn(odd), run_time=0.8)
        xl = Text("attribute 1", font_size=16, color=WHITE, opacity=0.4,
                  font=MONO).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = Text("attribute 2", font_size=16, color=WHITE, opacity=0.4,
                  font=MONO).next_to(ax.y_axis, UP, buff=0.1)
        self.play(FadeIn(xl), FadeIn(yl), run_time=0.5)
        right = VGroup(
            Text("one noisy example (D15:\nSunny Hot Normal Strong -> No)",
                 font_size=18, color=ACCENT, font=MONO),
            Text("the tree grows extra deep\nsplits just to fit it", font_size=18,
                 color=RED, font=MONO),
            Text("memorizes -> poor on new data", font_size=18, color=WHITE,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.9, 0.3, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in right],
                              run_time=1.8))
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L15_Stop(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("When to stop splitting?", "don't obsess over purity")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        stops = VGroup(
            Text("node pure enough", font_size=20, color=GREEN, font=MONO),
            Text("too few samples left", font_size=20, color=GREEN, font=MONO),
            Text("max depth reached", font_size=20, color=GREEN, font=MONO),
            Text("split gains little", font_size=20, color=GREEN, font=MONO),
            Text("validation says stop", font_size=20, color=GREEN, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.5, 0.3, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in stops],
                              run_time=1.6))
        leaf = VGroup(
            Text("impure leaf is OK", font_size=22, color=ACCENT, weight=BOLD,
                 font=MONO),
            Text("predict class probabilities\n(e.g. p(green) = 80%)",
                 font_size=19, color=WHITE, font=MONO),
            Text("or just the majority label", font_size=19, color=WHITE,
                 font=MONO),
        ).arrange(DOWN, buff=0.4).move_to([3.2, 0.3, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in leaf],
                              run_time=1.4))
        cap = Text("goal: avoid overfitting while keeping the tree useful",
                   font_size=20, color=WHITE, font=MONO).to_edge(DOWN, buff=0.6)
        self.play(Write(cap), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L15_Pruning(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Pre-pruning vs post-pruning", "two ways to tame the tree")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        pre = VGroup(
            Text("PRE-PRUNING", font_size=22, color=BLUE, weight=BOLD,
                 font=MONO),
            Text("stop growth early", font_size=19, color=WHITE, font=MONO),
            Text("depth limit, min samples,\nmin gain threshold", font_size=18,
                 color=WHITE, opacity=0.7, font=MONO),
        ).arrange(DOWN, buff=0.35).move_to([-3.5, 0.9, 0])
        post = VGroup(
            Text("POST-PRUNING", font_size=22, color=GREEN, weight=BOLD,
                 font=MONO),
            Text("grow fully, then chop", font_size=19, color=WHITE, font=MONO),
            Text("remove branches that don't\nearn their keep", font_size=18,
                 color=WHITE, opacity=0.7, font=MONO),
        ).arrange(DOWN, buff=0.35).move_to([3.5, 0.9, 0])
        self.play(FadeIn(pre, shift=RIGHT * 0.3), run_time=1.0)
        self.play(FadeIn(post, shift=LEFT * 0.3), run_time=1.0)
        val = Text("decide with a validation set: prefer the simpler tree\nwhen extra complexity doesn't improve validation performance",
                   font_size=19, color=ACCENT, font=MONO).to_edge(DOWN, buff=0.7)
        self.play(Write(val), run_time=1.2)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L15_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, _ = title_block("Lecture 15 in one breath", "")
        self.play(Write(t), run_time=0.9)
        def seg(*parts):
            return VGroup(*[Text(p, font_size=21, color=c, font=MONO)
                            for p, c in parts]).arrange(RIGHT, buff=0.02)
        lines = VGroup(
            seg(("tree = ", WHITE), ("flowchart", BLUE),
                (" of feature tests -> predictions", WHITE)),
            seg(("root / internal / leaf, depth = max layers", WHITE)),
            seg(("entropy ", WHITE), ("H(S)", BLUE),
                (" measures impurity: 0 pure, 1 max", WHITE)),
            seg(("pick the split with the highest ", WHITE),
                ("information gain", GREEN)),
            seg(("deep trees overfit -> ", WHITE),
                ("pre-prune or post-prune", RED)),
            seg(("sklearn: DecisionTreeClassifier(max_depth=4)", WHITE)),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(2.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
