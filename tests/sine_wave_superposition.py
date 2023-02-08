import PgfPlotter.PgfPlotter as pgf
import numpy as np


def wrapper_sine_wave(amplitude, frequency, phase):
    def sine_wave(t):
        return amplitude * np.sin(2 * np.pi * frequency * t + phase)

    return sine_wave


if __name__ == "__main__":
    t_max = 20
    sample_rate = 100
    time = np.linspace(0, t_max, sample_rate * t_max)

    wave_1 = wrapper_sine_wave(1, 1, 0)
    wave_2 = wrapper_sine_wave(.8, 1.1, np.pi / 4)

    s_1 = wave_1(time)
    s_2 = wave_2(time)
    s_sum = s_1 + s_2

    data = np.concatenate(([time], [s_1], [s_2], [s_sum]))

    plotter = pgf.Plotter(data, "sine_wave_superposition")
    plotter.legend(["$s_1(t)$", "$s_2(t)$", "$s_1(t)+s_2(t)$"])
    plotter.caption("Superposition of two sine waves with different frequencies, amplitudes and phases.")
    plotter.add_axis_optn("xlabel", "$t$")
    plotter.add_axis_optn("ylabel", "Signal")
    plotter.add_axis_optn("x unit", "\si{\second}")

    plotter.export_latex()
