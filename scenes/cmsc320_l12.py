from manim import *
import numpy as np

BG = "#1C1C1C"
GREEN = "#83C167"
RED = "#FC6255"
ACCENT = "#FFFF00"
BLUE = "#58C4DD"
MONO = "DejaVu Sans Mono"

# reuse verified KNN scenes (manim only renders classes defined in this module,
# so wrap the imports in same-named subclasses)
from knn import Scene2_Data as _S2, Scene3_K1 as _S3, Scene4_K3 as _S4, \
    Scene5_Weighted as _S5, Scene6_Boundaries as _S6


class Scene2_Data(_S2):
    pass


class Scene3_K1(_S3):
    pass


class Scene4_K3(_S4):
    pass


class Scene5_Weighted(_S5):
    pass


class Scene6_Boundaries(_S6):
    pass


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


class L12_Title(Scene):
    def construct(self):
        self.camera.background_color = BG
        t = Text("Introduction to Machine Learning", font_size=42, color=BLUE,
                 weight=BOLD, font=MONO).to_edge(UP, buff=0.8)
        s = Text("CMSC 320 - lecture 12 - the full tour", font_size=20,
                 color=WHITE, opacity=0.5, font=MONO).next_to(t, DOWN, buff=0.3)
        self.play(Write(t), run_time=1.4)
        self.play(FadeIn(s, shift=DOWN * 0.2), run_time=0.7)
        self.wait(0.8)
        core = Text("turn information into knowledge", font_size=30,
                    color=ACCENT, weight=BOLD, font=MONO)
        self.play(FadeOut(s), Write(core), run_time=1.3)
        self.wait(1.8)
        agenda = Text("classification - KNN - distances - boundaries - code",
                      font_size=19, color=WHITE, opacity=0.55, font=MONO
                      ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(agenda), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L12_Classification(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Classification", "supervised: the label was known in the past")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        left = VGroup(*[Dot(np.array([-4.6 + 0.9 * i, 0.6 + 0.5 * (-1) ** i, 0]),
                            color=(GREEN if i % 2 == 0 else RED), radius=0.1)
                        for i in range(4)])
        lh = Text("historical data\nlabels KNOWN", font_size=20, color=GREEN,
                  font=MONO).move_to([-4.2, 1.9, 0])
        q = Text("?", font_size=36, color=ACCENT, weight=BOLD, font=MONO
                 ).move_to([4.2, 0.6, 0])
        ring = Circle(radius=0.24, color=ACCENT, stroke_width=2.5
                      ).move_to(q.get_center())
        rh = Text("new data\nlabel UNKNOWN", font_size=20, color=ACCENT,
                  font=MONO).move_to([4.2, 1.9, 0])
        self.play(FadeIn(lh), LaggedStart(*[FadeIn(d, scale=0.5) for d in left],
                                          run_time=1.0))
        self.play(FadeIn(rh), FadeIn(ring), Write(q), run_time=0.9)
        ar1 = Arrow([-1.7, 0.6, 0], [-1.0, 0.6, 0], buff=0.08, stroke_width=4,
                    color=BLUE, max_tip_length_to_length_ratio=0.35)
        ar2 = Arrow([1.95, 0.6, 0], [3.85, 0.6, 0], buff=0.08, stroke_width=4,
                    color=BLUE, max_tip_length_to_length_ratio=0.18)
        model = box("model f(x)", w=2.6, h=0.9, col=BLUE).move_to([0.5, 0.6, 0])
        self.play(Create(ar1), FadeIn(model), Create(ar2), run_time=1.0)
        rule = Text("f(income, wealth, job) -> Yes / No", font_size=24,
                    color=WHITE, font=MONO).to_edge(DOWN, buff=0.85)
        verdict = Text("goal: labels for data you have never seen", font_size=19,
                       color=WHITE, opacity=0.55, font=MONO
                       ).next_to(rule, DOWN, buff=0.3)
        self.play(Write(rule), run_time=1.0)
        self.play(FadeIn(verdict), run_time=0.7)
        self.wait(1.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L12_Mitchell(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("What is learning?", "Tom Mitchell, 1998")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        q1 = Text("a program LEARNS from experience E", font_size=23,
                  color=WHITE, font=MONO)
        q2 = Text("if its performance on task T, measured by P,", font_size=23,
                  color=WHITE, font=MONO)
        q3 = Text("improves with E", font_size=23, color=ACCENT, font=MONO)
        quote = VGroup(q1, q2, q3).arrange(DOWN, buff=0.3)
        quote[0][20:27].set_color(BLUE)
        quote[1][22:28].set_color(GREEN)
        quote[1][41:44].set_color(RED)
        self.play(LaggedStart(*[Write(l) for l in quote], run_time=2.0))
        self.wait(0.8)
        cards = VGroup(
            VGroup(box("T", 1.0, 1.0, GREEN, 30),
                   Text("recognize\nhandwriting", font_size=17, color=WHITE,
                        font=MONO)).arrange(DOWN, buff=0.25),
            VGroup(box("P", 1.0, 1.0, RED, 30),
                   Text("recognition\naccuracy", font_size=17, color=WHITE,
                        font=MONO)).arrange(DOWN, buff=0.25),
            VGroup(box("E", 1.0, 1.0, BLUE, 30),
                   Text("database of\nlabeled digits", font_size=17,
                        color=WHITE, font=MONO)).arrange(DOWN, buff=0.25),
        ).arrange(RIGHT, buff=1.4).to_edge(DOWN, buff=0.7)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards],
                              run_time=1.6))
        self.wait(2.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L12_TradVsML(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Traditional code vs ML", "the same pipeline, pointed the other way")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        # left: rules + data -> answers
        r1 = box("rules (human)", 2.4, 0.8, RED, 18)
        d1 = box("data", 1.4, 0.8, BLUE, 18)
        a1 = box("answers", 1.6, 0.8, GREEN, 18)
        r1.move_to([-5.4, 1.5, 0]); d1.move_to([-5.4, 0.2, 0])
        a1.move_to([-2.2, 0.85, 0])
        lh = Text("TRADITIONAL", font_size=18, color=RED, font=MONO
                  ).move_to([-4.2, 2.5, 0])
        ar1 = VGroup(Arrow([-4.0, 1.3, 0], [-3.2, 1.0, 0], stroke_width=3, color=WHITE, stroke_opacity=0.6),
                     Arrow([-4.5, 0.4, 0], [-3.2, 0.7, 0], stroke_width=3, color=WHITE, stroke_opacity=0.6))
        # right: data + answers -> rules
        d2 = box("data", 1.4, 0.8, BLUE, 18)
        a2 = box("answers", 1.6, 0.8, GREEN, 18)
        r2 = box("rules (learned)", 2.6, 0.8, ACCENT, 18)
        d2.move_to([2.2, 1.5, 0]); a2.move_to([2.2, 0.2, 0])
        r2.move_to([5.4, 0.85, 0])
        rh = Text("MACHINE LEARNING", font_size=18, color=ACCENT, font=MONO
                  ).move_to([3.8, 2.5, 0])
        ar2 = VGroup(Arrow([3.1, 1.3, 0], [4.0, 1.0, 0], stroke_width=3, color=WHITE, stroke_opacity=0.6),
                     Arrow([3.2, 0.4, 0], [4.0, 0.7, 0], stroke_width=3, color=WHITE, stroke_opacity=0.6))
        self.play(FadeIn(lh), Write(r1), Write(d1), Create(ar1), Write(a1),
                  run_time=1.6)
        self.wait(0.6)
        self.play(FadeIn(rh), Write(d2), Write(a2), Create(ar2), Write(r2),
                  run_time=1.6)
        cap = Text("ML inverts it: data + outcomes produce the rules",
                   font_size=22, color=WHITE, font=MONO).to_edge(DOWN, buff=0.7)
        self.play(Write(cap), run_time=1.1)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L12_Workflow(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("The ML pipeline", "five moves, every project")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        steps = [("collect", "gather raw data"), ("prep", "clean + split"),
                 ("train", "fit the model"), ("eval", "test unseen"),
                 ("tune", "adjust hyperparams")]
        cols = [BLUE, BLUE, GREEN, GREEN, ACCENT]
        nodes = VGroup()
        for i, ((name, note), col) in enumerate(zip(steps, cols)):
            b = box(name, 2.1, 0.85, col, 20)
            b.move_to([-5.6 + 2.8 * i, 0.6, 0])
            n = Text(note, font_size=14, color=WHITE, opacity=0.5, font=MONO
                     ).next_to(b, DOWN, buff=0.22)
            nodes.add(VGroup(b, n))
        arrows = VGroup(*[Arrow([-5.6 + 2.8 * i + 1.08, 0.6, 0],
                                [-5.6 + 2.8 * (i + 1) - 1.08, 0.6, 0],
                                stroke_width=3, color=WHITE, stroke_opacity=0.5,
                                max_tip_length_to_length_ratio=0.3)
                          for i in range(4)])
        for i, n in enumerate(nodes):
            self.play(FadeIn(n, shift=RIGHT * 0.3), run_time=0.55)
            if i < 4:
                self.play(Create(arrows[i]), run_time=0.35)
        loop = Text("tune -> retrain -> re-evaluate (repeat)", font_size=20,
                    color=ACCENT, font=MONO).to_edge(DOWN, buff=0.7)
        self.play(Write(loop), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L12_RL(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Reinforcement learning", "the third cousin: learn from consequences")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        env = box("ENVIRONMENT", 3.0, 1.1, BLUE, 22).move_to([-3.6, 0.6, 0])
        ag = box("AGENT", 2.4, 1.1, GREEN, 22).move_to([3.6, 0.6, 0])
        self.play(Write(env), Write(ag), run_time=1.0)
        top = Arrow([-1.9, 1.3, 0], [2.2, 1.3, 0], stroke_width=4, color=GREEN)
        tl = Text("action", font_size=19, color=GREEN, font=MONO
                  ).move_to([0.15, 1.75, 0])
        bot = Arrow([2.2, -0.1, 0], [-1.9, -0.1, 0], stroke_width=4, color=ACCENT)
        bl = Text("new state + reward / penalty", font_size=19, color=ACCENT,
                  font=MONO).move_to([0.15, -0.55, 0])
        self.play(Create(top), FadeIn(tl), run_time=0.9)
        self.play(Create(bot), FadeIn(bl), run_time=0.9)
        self.wait(0.6)
        # pulse the loop
        for _ in range(2):
            self.play(Indicate(top, scale_factor=1.06), run_time=0.5)
            self.play(Indicate(bot, scale_factor=1.06), run_time=0.5)
        cap = Text("trial + error, maximizing LONG-TERM reward", font_size=22,
                   color=WHITE, font=MONO).to_edge(DOWN, buff=0.7)
        self.play(Write(cap), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L12_HyperParam(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Hyperparameter vs parameter", "who sets the knob?")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        h = VGroup(
            Text("HYPERPARAMETER", font_size=24, color=ACCENT, weight=BOLD,
                 font=MONO),
            Text("you set it BEFORE training", font_size=19, color=WHITE,
                 font=MONO),
            Text("not learned from data", font_size=19, color=WHITE,
                 font=MONO),
            Text("K in KNN", font_size=21, color=ACCENT, font=MONO),
        ).arrange(DOWN, buff=0.35).move_to([-3.5, 0.2, 0])
        p = VGroup(
            Text("PARAMETER", font_size=24, color=BLUE, weight=BOLD, font=MONO),
            Text("model learns it DURING training", font_size=19, color=WHITE,
                 font=MONO),
            Text("changes as the model fits", font_size=19, color=WHITE,
                 font=MONO),
            Text("weights in linear regression", font_size=21, color=BLUE,
                 font=MONO),
        ).arrange(DOWN, buff=0.35).move_to([3.5, 0.2, 0])
        line = Line([0, 2.2, 0], [0, -1.9, 0], stroke_width=1.5, stroke_opacity=0.2)
        self.play(Create(line), run_time=0.5)
        self.play(FadeIn(h, shift=RIGHT * 0.3), run_time=1.0)
        self.play(FadeIn(p, shift=LEFT * 0.3), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L12_DistL2L1(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Distance, part 1", "same two points, two answers")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1], x_length=6.5,
                  y_length=4.2, axis_config={"stroke_opacity": 0.15,
                                             "include_ticks": False},
                  ).shift(DOWN * 0.35)
        grid = VGroup(*[Line(ax.c2p(i, 0), ax.c2p(i, 5), stroke_width=0.7,
                             stroke_opacity=0.12) for i in range(1, 5)] +
                      [Line(ax.c2p(0, i), ax.c2p(5, i), stroke_width=0.7,
                            stroke_opacity=0.12) for i in range(1, 5)])
        self.play(Create(ax), FadeIn(grid), run_time=0.9)
        A = Dot(ax.c2p(1, 1), color=WHITE, radius=0.1)
        B = Dot(ax.c2p(4, 5), color=WHITE, radius=0.1)
        la = Text("A", font_size=20, font=MONO).next_to(A, DOWN, buff=0.15)
        lb = Text("B", font_size=20, font=MONO).next_to(B, UP, buff=0.15)
        self.play(FadeIn(A), FadeIn(B), FadeIn(la), FadeIn(lb), run_time=0.6)
        euc = Line(ax.c2p(1, 1), ax.c2p(4, 5), color=BLUE, stroke_width=4)
        euc_l = Text("Euclidean L2 = 5.0", font_size=21, color=BLUE, font=MONO
                     ).to_edge(DOWN, buff=0.75).shift(LEFT * 2.8)
        self.play(Create(euc), Write(euc_l), run_time=1.2)
        self.wait(0.6)
        man = VGroup(Line(ax.c2p(1, 1), ax.c2p(4, 1), color=GREEN, stroke_width=4),
                     Line(ax.c2p(4, 1), ax.c2p(4, 5), color=GREEN, stroke_width=4))
        man_l = Text("Manhattan L1 = 3 + 4 = 7", font_size=21, color=GREEN,
                     font=MONO).to_edge(DOWN, buff=0.75).shift(RIGHT * 2.4)
        self.play(Create(man[0]), Create(man[1]), Write(man_l), run_time=1.4)
        cap = Text("L1: no diagonals, no sqrt, robust in high-D", font_size=18,
                   color=WHITE, opacity=0.55, font=MONO
                   ).next_to(man_l, DOWN, buff=0.25)
        self.play(FadeIn(cap), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L12_DistHamCos(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Distance, part 2", "strings and angles")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        # Hamming
        ha = Text("1 0 1 1 0", font_size=30, font=MONO, color=WHITE
                  ).move_to([-4.4, 1.3, 0])
        hb = Text("1 1 0 1 0", font_size=30, font=MONO, color=WHITE
                  ).move_to([-4.4, 0.6, 0])
        ha[2].set_color(RED); ha[4].set_color(RED)
        hb[2].set_color(RED); hb[4].set_color(RED)
        hh = Text("HAMMING", font_size=20, color=RED, weight=BOLD, font=MONO
                  ).move_to([-4.4, 2.1, 0])
        hd = Text("count mismatches, never subtract\nd = 2", font_size=19,
                  color=WHITE, font=MONO).move_to([-4.4, -0.35, 0])
        self.play(Write(hh), Write(ha), Write(hb), run_time=1.2)
        self.play(Write(hd), run_time=0.9)
        # Cosine
        cax = Axes(x_range=[0, 3, 1], y_range=[0, 3, 1], x_length=3.4,
                   y_length=3.0, axis_config={"stroke_opacity": 0.15,
                                              "include_ticks": False}
                   ).move_to([3.6, 0.5, 0])
        v1 = Arrow(cax.c2p(0, 0), cax.c2p(1, 1), color=BLUE, stroke_width=4,
                   max_tip_length_to_length_ratio=0.18)
        v2 = Arrow(cax.c2p(0, 0), cax.c2p(2, 2), color=GREEN, stroke_width=4,
                   max_tip_length_to_length_ratio=0.12)
        ch = Text("COSINE", font_size=20, color=GREEN, weight=BOLD, font=MONO
                  ).move_to([3.6, 2.4, 0])
        cd = Text("angle, not length: (1,1) vs (2,2)\nsimilarity = 1.0",
                  font_size=19, color=WHITE, font=MONO).move_to([3.6, -1.6, 0])
        self.play(Write(ch), Create(cax), Create(v1), run_time=1.0)
        self.play(Create(v2), Write(cd), run_time=1.0)
        cap = Text("cosine = the workhorse for text + sparse data", font_size=18,
                   color=ACCENT, opacity=0.8, font=MONO
                   ).to_edge(DOWN, buff=0.45)
        self.play(Write(cap), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L12_Sklearn(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("KNN in four lines", "scikit-learn: specify, fit, predict, score")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        code = VGroup(
            Text("model = KNeighborsClassifier(n_neighbors=3)", font_size=22,
                 color=BLUE, font=MONO),
            Text("model.fit(X_train, y_train)", font_size=22, color=GREEN,
                 font=MONO),
            Text("pred = model.predict(X_test)", font_size=22, color=ACCENT,
                 font=MONO),
            Text("score = accuracy_score(y_test, pred)", font_size=22,
                 color=WHITE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        tags = VGroup(
            Text("specify", font_size=15, color=BLUE, opacity=0.7, font=MONO),
            Text("fit", font_size=15, color=GREEN, opacity=0.7, font=MONO),
            Text("predict", font_size=15, color=ACCENT, opacity=0.7, font=MONO),
            Text("evaluate", font_size=15, color=WHITE, opacity=0.7, font=MONO),
        )
        for ln, tg in zip(code, tags):
            tg.next_to(ln, RIGHT, buff=0.5)
        for ln, tg in zip(code, tags):
            self.play(FadeIn(ln, shift=RIGHT * 0.3), FadeIn(tg), run_time=0.7)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L12_ProsCons(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("KNN: the tradeoff", "simple is not free")
        self.play(Write(t), FadeIn(s), run_time=0.9)
        pros = VGroup(
            Text("+ simple and intuitive", font_size=20, color=GREEN, font=MONO),
            Text("+ no training phase (lazy)", font_size=20, color=GREEN,
                 font=MONO),
            Text("+ wild, non-linear boundaries", font_size=20, color=GREEN,
                 font=MONO),
            Text("+ no distribution assumptions", font_size=20, color=GREEN,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.4, 0.3, 0])
        cons = VGroup(
            Text("- slow: distance to every point", font_size=20, color=RED,
                 font=MONO),
            Text("- stores the whole dataset", font_size=20, color=RED,
                 font=MONO),
            Text("- hates unscaled features", font_size=20, color=RED,
                 font=MONO),
            Text("- curse of dimensionality", font_size=20, color=RED,
                 font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.3, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in pros],
                              run_time=1.6))
        self.play(LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in cons],
                              run_time=1.6))
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L12_Extras(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, s = title_block("Two parting truths", "")
        self.play(Write(t), run_time=0.8)
        nfl = Text("No Free Lunch", font_size=32, color=ACCENT, weight=BOLD,
                   font=MONO).move_to([-3.5, 1.2, 0])
        nfl2 = Text("no single algorithm\nwins on every task", font_size=21,
                    color=WHITE, font=MONO).move_to([-3.5, 0.0, 0])
        rad = Text("Radius KNN", font_size=32, color=BLUE, weight=BOLD,
                   font=MONO).move_to([3.5, 1.2, 0])
        rad2 = Text("vote with everyone inside\na fixed radius r, not a fixed K",
                    font_size=21, color=WHITE, font=MONO).move_to([3.5, 0.0, 0])
        self.play(Write(nfl), FadeIn(nfl2), run_time=1.2)
        self.play(Write(rad), FadeIn(rad2), run_time=1.2)
        note = Text("radius KNN: bonus reading, not on the exam", font_size=18,
                    color=WHITE, opacity=0.5, font=MONO
                    ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(note), run_time=0.7)
        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class L12_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG
        t, _ = title_block("Lecture 12 in one breath", "")
        self.play(Write(t), run_time=0.9)
        lines = VGroup(
            Text("supervised learning = labels known in the past", font_size=22,
                 color=WHITE, font=MONO),
            Text("KNN: store data, K neighbors vote by distance", font_size=22,
                 color=WHITE, font=MONO),
            Text("metrics: L2 / L1 / Hamming / cosine", font_size=22,
                 color=WHITE, font=MONO),
            Text("K too small -> overfit,  K too big -> underfit", font_size=22,
                 color=WHITE, font=MONO),
            Text("next: trees, forests, neural nets, Bayes, SVMs", font_size=22,
                 color=WHITE, font=MONO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        lines[0][24:29].set_color(GREEN)
        lines[1][28:36].set_color(BLUE)
        lines[2][9:33].set_color(BLUE)
        lines[3][15:22].set_color(RED)
        lines[3][35:44].set_color(RED)
        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(2.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
