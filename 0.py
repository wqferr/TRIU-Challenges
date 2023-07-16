from manim import *

config.frame_width = 16
config.frame_height = 9

class Challenge0Scene(Scene):
    def construct(self):
        ball = Circle(color='#bb3333', fill_opacity=1, radius=0.5)
        np = NumberPlane(
            y_range=(0, 6.01),
            x_range=(0, 4.01),
        ).shift(3*LEFT)

        scale = 5
        height = ValueTracker(1)
        ball.move_to(
            np.coords_to_point(2, scale * height.get_value()),
            DOWN
        )
        self.play(Create(np))
        self.play(DrawBorderThenFill(ball, run_time=1))

        def update_ball(ball):
            ball.move_to(
                np.coords_to_point(2, scale*height.get_value()),
                DOWN
            )
        ball.add_updater(update_ball)

        measurement = BraceBetweenPoints(
            ball.get_critical_point(DOWN),
            np.coords_to_point(0, 0),
            direction=LEFT,
        )
        def update_measurement(brace: Brace):
            brace_len = max(scale*height.get_value(), 0.001)
            brace.stretch_to_fit_height(
                brace_len,
                about_point=np.coords_to_point(0, 0)
            )
        measurement.add_updater(update_measurement)

        measurement_hline = Line(
            measurement.get_critical_point(UR),
            ball.get_critical_point(DOWN),
            color=WHITE
        )
        def update_measurement_hline(mobject: Line):
            mobject.put_start_and_end_on(
                measurement.get_critical_point(UR),
                ball.get_critical_point(DOWN)
            )
        measurement_hline.add_updater(update_measurement_hline)

        measurement_font_size = 40
        measurement_number = DecimalNumber(
            number=height.get_value(),
            num_decimal_places=2,
            font_size=measurement_font_size,
            stroke_width=1
        )
        measurement_text = VGroup(
            measurement_number,
            Text("m", font_size=measurement_font_size, stroke_width=0.5)
        ).arrange(RIGHT, center=False)
        measurement_text_dist = ValueTracker(0)
        def update_measurement_text(text: VGroup):
            text.next_to(measurement, LEFT)
            text.shift(measurement_text_dist.get_value() * LEFT)
            text.submobjects[0].set_value(height.get_value())
        measurement_text.add_updater(update_measurement_text)
        
        self.play(
            DrawBorderThenFill(measurement, run_time=1),
            Create(measurement_hline),
        )
        self.play(Write(measurement_text))
        
        bounce_time = 0.8
        def bounce_down(time_mul=1):
            self.play(
                height.animate(
                    run_time=bounce_time*time_mul,
                    rate_func=lambda t: t**2
                ).set_value(0)
            )

        sequence_text = None
        sequence_text_scale = 0.75
        def update_sequence_text(mob):
            mob.next_to(measurement, LEFT)

        def bounce(multiplier, time_mul=1, count=0):
            anims = []
            init_height = height.get_value()
            bounce_down(time_mul)
            if sequence_text is not None:
                new_text = (
                    Text(f"a({count})")
                        .next_to(measurement, LEFT)
                        .scale(sequence_text_scale)
                )
                anims.append(
                    ApplyMethod(sequence_text.become, new_text, run_time=min(0.3, bounce_time*time_mul-0.05))
                )
            anims.append(
                height.animate(
                    run_time=bounce_time*time_mul,
                    rate_func=lambda t: 1-(t-1)**2
                ).set_value(init_height * multiplier)
            )
            self.play(*anims)

        def reset_height():
            self.play(height.animate(run_time=1).set_value(1))

        self.wait()
        text_energy_conservation = Text("Energia é conservada").next_to(np, UP)
        strikethrough_1 = Line(
            text_energy_conservation.get_critical_point(DL),
            text_energy_conservation.get_critical_point(UR),
            color=RED
        )
        strikethrough_2 = Line(
            text_energy_conservation.get_critical_point(UL),
            text_energy_conservation.get_critical_point(DR),
            color=RED
        )
        self.play(Write(text_energy_conservation, run_time=1))
        bounce(1)
        bounce(1)
        bounce(1)

        self.play(Create(strikethrough_1), Create(strikethrough_2))
        self.wait(0.5)

        bounce(0.68)
        bounce(0.68)
        bounce(0.68)
        self.wait(1)

        reset_height()
        self.play(
            measurement_text_dist.animate(run_time=1).set_value(10),
            Unwrite(text_energy_conservation),
            Uncreate(strikethrough_1),
            Uncreate(strikethrough_2),
            run_time=1
        )
        text_90_percent_restitution = (
            Text("10% da energia é perdida a cada quicada")
                .scale(0.8)
                .next_to(np, UP)
                .shift(2*RIGHT)
        )
        self.play(Write(text_90_percent_restitution))
        sequence_text = (
            Text("a(0) = 1.00")
                .scale(0.5)
                .next_to(measurement, LEFT)
        )
        sequence_text.add_updater(update_sequence_text)
        self.play(Write(sequence_text))
        bounce(0.9, 1, 1)

        question_text_scale = 0.6
        question_a_text = (
            Text("a) Encontre a(1), a altura máxima\napós a primeira quicada")
                .scale(question_text_scale)
                .next_to(np, RIGHT)
                .align_to(np, UP)
        )
        self.play(Write(question_a_text))
        self.wait(1)

        bounce(0.9, 0.5, 2)
        bounce(0.9, 0.5, 3)
        bounce(0.9, 0.5, 4)
        bounce(0.9, 0.5, 5)
        question_b_text = (
            Text("b) Encontre a(5), a altura máxima\napós a quinta quicada")
                .scale(question_text_scale)
                .next_to(question_a_text, DOWN)
                .align_to(question_a_text, LEFT)
        )
        self.play(Write(question_b_text))
        self.wait(1)

        bounce(0.9, 0.25, 6)
        bounce(0.9, 0.25, 7)
        bounce(0.9, 0.25, 8)
        bounce(0.9, 0.25, 9)
        bounce(0.9, 0.25, 10)
        question_c_text = (
            Text("c) Encontre a(10), a altura máxima\napós a décima quicada*")
                .scale(question_text_scale)
                .next_to(question_b_text, DOWN)
                .align_to(question_b_text, LEFT)
        )
        self.play(Write(question_c_text))

        self.wait(1)
        question_c_hint = (
            Text("*Essa questão não é tão tediosa quanto parece.\nLembre-se das propriedades de potências.")
                .scale(question_text_scale * 0.75)
                .next_to(np, RIGHT)
                .align_to(np, DOWN)
        )
        self.play(Write(question_c_hint))
        self.wait(3)

        considerations = (
            Text("Considere que a bola começa a 1 m do\nchão,\nem repouso")
                .scale(question_text_scale)
                .next_to(np, RIGHT)
                .next_to(question_c_text, DOWN)
                .shift(0.25 * DOWN)
                .align_to(question_c_text, LEFT)
        )
        self.play(Write(considerations))

        self.wait(10)
