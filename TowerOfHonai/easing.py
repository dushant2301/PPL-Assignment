"""
Easing functions for smooth, cinematic animations.
Provides various interpolation curves for the anti-gravity movement system.
"""

import math


def linear(t: float) -> float:
    """Linear interpolation — constant speed."""
    return max(0.0, min(1.0, t))


def ease_in_quad(t: float) -> float:
    """Quadratic ease-in — slow start."""
    t = max(0.0, min(1.0, t))
    return t * t


def ease_out_quad(t: float) -> float:
    """Quadratic ease-out — slow end."""
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) * (1 - t)


def ease_in_out_quad(t: float) -> float:
    """Quadratic ease-in-out."""
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        return 2 * t * t
    return 1 - (-2 * t + 2) ** 2 / 2


def ease_in_cubic(t: float) -> float:
    """Cubic ease-in — slower start."""
    t = max(0.0, min(1.0, t))
    return t * t * t


def ease_out_cubic(t: float) -> float:
    """Cubic ease-out — slower end."""
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    """Cubic ease-in-out — smooth start and end."""
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        return 4 * t * t * t
    return 1 - (-2 * t + 2) ** 3 / 2


def ease_out_bounce(t: float) -> float:
    """Bounce ease-out — bouncy landing effect."""
    t = max(0.0, min(1.0, t))
    n1 = 7.5625
    d1 = 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375


def ease_out_elastic(t: float) -> float:
    """Elastic ease-out — springy overshoot."""
    t = max(0.0, min(1.0, t))
    if t == 0 or t == 1:
        return t
    c4 = (2 * math.pi) / 3
    return 2 ** (-10 * t) * math.sin((t * 10 - 0.75) * c4) + 1


def ease_out_back(t: float) -> float:
    """Back ease-out — slight overshoot."""
    t = max(0.0, min(1.0, t))
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def smoothstep(t: float) -> float:
    """Hermite smoothstep — classic smooth interpolation."""
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def smoother_step(t: float) -> float:
    """Ken Perlin's smoother step — even smoother."""
    t = max(0.0, min(1.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


def ease_in_expo(t: float) -> float:
    """Exponential ease-in."""
    t = max(0.0, min(1.0, t))
    return 0 if t == 0 else 2 ** (10 * t - 10)


def ease_out_expo(t: float) -> float:
    """Exponential ease-out."""
    t = max(0.0, min(1.0, t))
    return 1 if t == 1 else 1 - 2 ** (-10 * t)


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between two values."""
    return a + (b - a) * t


def lerp_2d(p1: tuple, p2: tuple, t: float) -> tuple:
    """Linear interpolation between two 2D points."""
    return (lerp(p1[0], p2[0], t), lerp(p1[1], p2[1], t))
