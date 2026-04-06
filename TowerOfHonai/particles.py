"""
Particle system for visual effects — trails, bursts, ambient particles.
"""
from __future__ import annotations

import pygame
import random
import math
from typing import List
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, NEON_CYAN, NEON_PURPLE,
                       NEON_BLUE, NEON_PINK, NEON_GREEN, NEON_ORANGE,
                       NEON_YELLOW, TRAIL_FADE_RATE)


class Particle:
    """A single particle with position, velocity, color, and lifetime."""

    __slots__ = ['x', 'y', 'vx', 'vy', 'color', 'lifetime', 'max_lifetime',
                 'size', 'decay_size', 'gravity', 'alpha']

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 color: tuple, lifetime: float, size: float = 3, gravity: float = 0) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.decay_size = True
        self.gravity = gravity
        self.alpha = 255

    def update(self, dt: float) -> bool:
        """Update particle position and lifetime."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt
        self.lifetime -= dt

        # Calculate alpha based on remaining life
        life_ratio = max(0, self.lifetime / self.max_lifetime)
        self.alpha = int(255 * life_ratio)

        return self.lifetime > 0

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the particle with glow effect."""
        if self.alpha <= 5:
            return

        life_ratio = max(0, self.lifetime / self.max_lifetime)
        current_size = max(1, self.size * life_ratio) if self.decay_size else self.size

        # Outer glow
        glow_size = int(current_size * 2.5)
        if glow_size > 1:
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            glow_color = (*self.color[:3], int(self.alpha * 0.3))
            pygame.draw.circle(glow_surf, glow_color, (glow_size, glow_size), glow_size)
            surface.blit(glow_surf, (int(self.x - glow_size), int(self.y - glow_size)))

        # Core particle
        core_surf = pygame.Surface((int(current_size * 2 + 2), int(current_size * 2 + 2)), pygame.SRCALPHA)
        core_color = (*self.color[:3], min(255, self.alpha))
        pygame.draw.circle(core_surf, core_color,
                           (int(current_size + 1), int(current_size + 1)), max(1, int(current_size)))
        surface.blit(core_surf, (int(self.x - current_size - 1), int(self.y - current_size - 1)))


class TrailPoint:
    """A point in a motion trail."""

    __slots__ = ['x', 'y', 'alpha', 'color', 'size']

    def __init__(self, x: float, y: float, color: tuple, size: float = 4) -> None:
        self.x = x
        self.y = y
        self.alpha = 255
        self.color = color
        self.size = size


class ParticleSystem:
    """Manages all particles, trails, and visual effects."""

    def __init__(self) -> None:
        self.particles: List[Particle] = []
        self.trails: List[TrailPoint] = []
        self.ambient_particles: List[Particle] = []
        self._init_ambient()

    def _init_ambient(self):
        """Create ambient floating particles for the background."""
        for _ in range(30):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            vx = random.uniform(-8, 8)
            vy = random.uniform(-8, 8)
            color = random.choice([NEON_CYAN, NEON_PURPLE, NEON_BLUE, NEON_PINK])
            size = random.uniform(1, 3)
            lifetime = random.uniform(3, 8)
            p = Particle(x, y, vx, vy, color, lifetime, size)
            p.decay_size = False
            self.ambient_particles.append(p)

    def emit_burst(self, x, y, color, count=15, speed=120, lifetime=0.8, size=3):
        """Emit a burst of particles from a point."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            spd = random.uniform(speed * 0.3, speed)
            vx = math.cos(angle) * spd
            vy = math.sin(angle) * spd
            lt = random.uniform(lifetime * 0.5, lifetime)
            sz = random.uniform(size * 0.5, size * 1.5)
            # Slightly vary the color
            r = min(255, max(0, color[0] + random.randint(-20, 20)))
            g = min(255, max(0, color[1] + random.randint(-20, 20)))
            b = min(255, max(0, color[2] + random.randint(-20, 20)))
            p = Particle(x, y, vx, vy, (r, g, b), lt, sz, gravity=50)
            self.particles.append(p)

    def emit_trail(self, x, y, color, size=4):
        """Add a trail point at the given position."""
        self.trails.append(TrailPoint(x, y, color, size))
        # Limit trail length
        if len(self.trails) > 100:
            self.trails = list(self.trails[-100:])

    def emit_sparkle(self, x, y, color, count=5):
        """Emit small sparkle particles."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            spd = random.uniform(20, 60)
            vx = math.cos(angle) * spd
            vy = math.sin(angle) * spd
            lt = random.uniform(0.2, 0.5)
            p = Particle(x, y, vx, vy, color, lt, 2)
            self.particles.append(p)

    def emit_celebration(self, count=100):
        """Massive particle explosion for puzzle completion."""
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        colors = [NEON_CYAN, NEON_PINK, NEON_PURPLE, NEON_GREEN,
                  NEON_ORANGE, NEON_YELLOW, NEON_BLUE]
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            spd = random.uniform(100, 400)
            vx = math.cos(angle) * spd
            vy = math.sin(angle) * spd
            color = random.choice(colors)
            lt = random.uniform(1.0, 3.0)
            sz = random.uniform(2, 6)
            p = Particle(cx + random.randint(-50, 50),
                         cy + random.randint(-50, 50),
                         vx, vy, color, lt, sz, gravity=80)
            self.particles.append(p)

    def update(self, dt):
        """Update all particles."""
        # Update active particles
        self.particles = [p for p in self.particles if p.update(dt)]

        # Fade and remove old trail points
        new_trails = []
        for tp in self.trails:
            tp.alpha = int(tp.alpha * TRAIL_FADE_RATE)
            if tp.alpha > 5:
                new_trails.append(tp)
        self.trails = new_trails

        # Update ambient particles
        for p in self.ambient_particles:
            if not p.update(dt):
                # Respawn
                p.x = random.randint(0, SCREEN_WIDTH)
                p.y = random.randint(0, SCREEN_HEIGHT)
                p.vx = random.uniform(-8, 8)
                p.vy = random.uniform(-8, 8)
                p.lifetime = random.uniform(3, 8)
                p.max_lifetime = p.lifetime
                p.alpha = 255

            # Wrap around edges
            if p.x < 0: p.x = SCREEN_WIDTH
            if p.x > SCREEN_WIDTH: p.x = 0
            if p.y < 0: p.y = SCREEN_HEIGHT
            if p.y > SCREEN_HEIGHT: p.y = 0

    def draw_trails(self, surface):
        """Draw motion trails."""
        for tp in self.trails:
            if tp.alpha > 5:
                ts = pygame.Surface((int(tp.size * 2 + 2), int(tp.size * 2 + 2)), pygame.SRCALPHA)
                color = (*tp.color[:3], tp.alpha)
                pygame.draw.circle(ts, color, (int(tp.size + 1), int(tp.size + 1)), int(tp.size))
                surface.blit(ts, (int(tp.x - tp.size - 1), int(tp.y - tp.size - 1)))

    def draw_particles(self, surface):
        """Draw all active particles."""
        for p in self.particles:
            p.draw(surface)

    def draw_ambient(self, surface):
        """Draw ambient background particles."""
        for p in self.ambient_particles:
            p.draw(surface)

    def clear(self):
        """Clear all particles and trails."""
        self.particles.clear()
        self.trails.clear()
