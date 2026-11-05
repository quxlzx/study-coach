from manim import *

BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"
MONO = "DejaVu Sans Mono"


class GradDescentPoc(Scene):
    """Proof-of-concept: gradient descent as a ball rolling down a loss curve."""

    def construct(self):
        self.camera.background_color = BG

        title = Text("Gradient Descent", font_size=44, color=PRIMARY,
                     weight=BOLD, font=MONO).to_edge(UP, buff=0.6)
        sub = Text("watch the loss choose its own path", font_size=20,
                   color=WHITE, opacity=0.5, font=MONO).next_to(title, DOWN, buff=0.25)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.8)
        self.wait(1.0)

        # axes + loss curve
        axes = Axes(
            x_range=[-0.5, 4.5, 1], y_range=[-0.5, 5, 1],
            x_length=8, y_length=4.5,
            axis_config={"stroke_opacity": 0.15, "include_ticks": False},
        ).shift(DOWN * 0.4)
        xlab = Text("weight w", font_size=20, color=WHITE, opacity=0.4,
                    font=MONO).next_to(axes.x_axis, RIGHT, buff=0.2)
        ylab = Text("loss L(w)", font_size=20, color=WHITE, opacity=0.4,
                    font=MONO).next_to(axes.y_axis, UP, buff=0.2)

        curve = axes.plot(
            lambda x: 0.28 * (x - 2.6) ** 2 + 0.4 + 1.4 * np.sin(1.6 * x) * np.exp(-0.35 * x),
            x_range=[-0.3, 4.3], color=PRIMARY, stroke_width=3,
        )

        self.play(Create(axes), run_time=1.0)
        self.play(FadeIn(xlab), FadeIn(ylab), run_time=0.5)
        self.play(Create(curve), run_time=1.5)
        self.wait(1.0)

        # the ball: walk down the gradient
        w = 0.2
        ball = Dot(axes.c2p(w, self.loss(w)), color=ACCENT, radius=0.11)
        self.play(FadeIn(ball), run_time=0.4)

        eta = 0.45
        for _ in range(9):
            g = self.grad(w)
            w_new = min(w - eta * g, 4.2)
            nxt = Dot(axes.c2p(w_new, self.loss(w_new)), color=ACCENT, radius=0.11)
            arrow = Arrow(ball.get_center(), nxt.get_center(), buff=0.09,
                          stroke_width=3, color=SECONDARY, max_tip_length_to_length_ratio=0.25)
            self.play(Transform(ball, nxt), Create(arrow), run_time=0.55)
            self.wait(0.25)
            w = w_new

        # aha moment
        aha = Text("w ← w − η · ∇L", font_size=34, color=SECONDARY,
                   weight=BOLD, font=MONO).to_edge(DOWN, buff=0.55)
        self.play(FadeOut(sub), Write(aha), run_time=1.2)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

    @staticmethod
    def loss(x):
        return 0.28 * (x - 2.6) ** 2 + 0.4 + 1.4 * np.sin(1.6 * x) * np.exp(-0.35 * x)

    @staticmethod
    def grad(x):
        h = 1e-5
        return (GradDescentPoc.loss(x + h) - GradDescentPoc.loss(x - h)) / (2 * h)
