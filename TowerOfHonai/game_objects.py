"""
Disk and Tower classes — core game objects.
"""

import pygame
import math
from constants import *


class Disk:
    """A single disk in the Tower of Hanoi puzzle."""

    def __init__(self, size_index, total_disks):
        """
        Args:
            size_index: 0 = smallest, total_disks-1 = largest
            total_disks: total number of disks in the puzzle
        """
        self.size_index = size_index
        self.total_disks = total_disks

        # Calculate width based on size
        t = size_index / max(1, total_disks - 1) if total_disks > 1 else 0.5
        self.width = int(MIN_DISK_WIDTH + t * (MAX_DISK_WIDTH - MIN_DISK_WIDTH))
        self.height = DISK_HEIGHT

        # Color from palette
        color_idx = size_index % len(DISK_COLORS)
        self.base_color = DISK_COLORS[color_idx]

        # Position (set externally)
        self.x = 0.0
        self.y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0

        # Animation state
        self.is_active = False       # Currently being animated
        self.is_dragging = False     # Being dragged by user
        self.glow_time = 0.0
        self.shake_time = 0.0
        self.shake_amount = 0.0
        self.bounce_velocity = 0.0
        self.settled = True

    def get_rect(self):
        """Get the disk's bounding rectangle."""
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width, self.height
        )

    def contains_point(self, px, py):
        """Check if a point is inside this disk."""
        return self.get_rect().collidepoint(px, py)

    def update(self, dt):
        """Update disk animations."""
        if self.is_active:
            self.glow_time += dt * GLOW_PULSE_SPEED

        if self.shake_time > 0:
            self.shake_time -= dt
            if self.shake_time <= 0:
                self.shake_time = 0
                self.shake_amount = 0

    def start_shake(self):
        """Trigger the error shake animation."""
        self.shake_time = 0.4
        self.shake_amount = 8

    def draw(self, surface, time_elapsed):
        """Draw the disk with glow, gradient, and effects."""
        rect = self.get_rect()

        # Apply shake offset
        shake_offset = 0
        if self.shake_time > 0:
            shake_offset = math.sin(self.shake_time * 40) * self.shake_amount * self.shake_time

        draw_x = rect.x + int(shake_offset)
        draw_rect = pygame.Rect(draw_x, rect.y, rect.width, rect.height)

        # Draw glow aura when active
        if self.is_active or self.is_dragging:
            glow_pulse = 0.6 + 0.4 * math.sin(self.glow_time)
            glow_alpha = int(GLOW_INTENSITY * glow_pulse)
            glow_r = GLOW_RADIUS + int(5 * glow_pulse)

            glow_surf = pygame.Surface(
                (rect.width + glow_r * 2, rect.height + glow_r * 2),
                pygame.SRCALPHA
            )
            glow_color = (*self.base_color[:3], glow_alpha)
            glow_rect = pygame.Rect(glow_r // 2, glow_r // 2,
                                    rect.width + glow_r, rect.height + glow_r)
            pygame.draw.rect(glow_surf, glow_color, glow_rect,
                             border_radius=DISK_CORNER_RADIUS + 4)
            surface.blit(glow_surf, (draw_x - glow_r, rect.y - glow_r))

        # Draw shadow
        shadow_surf = pygame.Surface((rect.width + 6, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 50), shadow_surf.get_rect())
        surface.blit(shadow_surf, (draw_x - 3, rect.bottom + 2))

        # Draw the main disk body with gradient effect
        disk_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

        # Bottom layer (darker)
        dark_color = tuple(max(0, c - 40) for c in self.base_color[:3])
        pygame.draw.rect(disk_surf, dark_color,
                         (0, 0, rect.width, rect.height),
                         border_radius=DISK_CORNER_RADIUS)

        # Top gradient (lighter top half)
        highlight_color = tuple(min(255, c + 60) for c in self.base_color[:3])
        highlight_rect = pygame.Rect(2, 2, rect.width - 4, rect.height // 2)
        highlight_surf = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(highlight_surf, (*highlight_color, 120),
                         (0, 0, highlight_rect.width, highlight_rect.height),
                         border_radius=DISK_CORNER_RADIUS - 2)
        disk_surf.blit(highlight_surf, (highlight_rect.x, highlight_rect.y))

        # Glowing edge/border
        border_alpha = 200 if self.is_active else 130
        if self.is_active:
            glow_pulse = 0.7 + 0.3 * math.sin(self.glow_time)
            border_alpha = int(border_alpha * glow_pulse)
        border_color = (*self.base_color[:3], border_alpha)
        pygame.draw.rect(disk_surf, border_color,
                         (0, 0, rect.width, rect.height),
                         width=2, border_radius=DISK_CORNER_RADIUS)

        surface.blit(disk_surf, (draw_x, rect.y))


class Tower:
    """A tower/peg in the Tower of Hanoi puzzle."""

    def __init__(self, index, x_pos):
        self.index = index
        self.x = x_pos
        self.base_y = TOWER_BASE_Y
        self.top_y = TOWER_BASE_Y - TOWER_HEIGHT
        self.disks = []  # Stack of Disk objects (bottom to top)
        self.labels = ["SOURCE", "AUXILIARY", "TARGET"]
        self.highlight = 0.0  # Hover/active highlight intensity

    def push(self, disk):
        """Push a disk onto this tower."""
        self.disks.append(disk)
        self._position_disk(disk, len(self.disks) - 1)

    def pop(self):
        """Pop the top disk from this tower."""
        if self.disks:
            return self.disks.pop()
        return None

    def peek(self):
        """Look at the top disk without removing it."""
        return self.disks[-1] if self.disks else None

    def can_place(self, disk):
        """Check if a disk can be legally placed on this tower."""
        if not self.disks:
            return True
        return disk.size_index < self.disks[-1].size_index

    def get_top_y(self):
        """Get the Y position for the next disk placement."""
        stack_height = len(self.disks) * (DISK_HEIGHT + DISK_GAP)
        return self.base_y - stack_height - DISK_HEIGHT / 2

    def _position_disk(self, disk, stack_index):
        """Position a disk at the given stack index."""
        disk.x = self.x
        disk.y = self.base_y - stack_index * (DISK_HEIGHT + DISK_GAP) - DISK_HEIGHT / 2

    def position_all_disks(self):
        """Reposition all disks on this tower."""
        for i, disk in enumerate(self.disks):
            self._position_disk(disk, i)

    def draw(self, surface, time_elapsed):
        """Draw the tower rod and base."""
        # Draw the rod with glow
        rod_rect = pygame.Rect(
            self.x - TOWER_WIDTH // 2,
            int(self.top_y),
            TOWER_WIDTH,
            int(self.base_y - self.top_y)
        )

        # Rod glow
        glow_intensity = 0.3 + 0.1 * math.sin(time_elapsed * 1.5 + self.index)
        glow_surf = pygame.Surface(
            (TOWER_WIDTH + 16, rod_rect.height + 10), pygame.SRCALPHA
        )
        glow_color = (*NEON_CYAN[:3], int(30 * glow_intensity + self.highlight * 40))
        pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(),
                         border_radius=4)
        surface.blit(glow_surf, (rod_rect.x - 8, rod_rect.y - 5))

        # Rod body
        rod_color = (40, 60, 90)
        pygame.draw.rect(surface, rod_color, rod_rect, border_radius=4)

        # Rod border
        border_alpha = int(80 + self.highlight * 100)
        rod_border_surf = pygame.Surface(
            (rod_rect.width + 2, rod_rect.height + 2), pygame.SRCALPHA
        )
        pygame.draw.rect(rod_border_surf, (*NEON_CYAN[:3], border_alpha),
                         (0, 0, rod_rect.width + 2, rod_rect.height + 2),
                         width=1, border_radius=4)
        surface.blit(rod_border_surf, (rod_rect.x - 1, rod_rect.y - 1))

        # Draw base platform
        base_rect = pygame.Rect(
            self.x - TOWER_BASE_WIDTH // 2,
            self.base_y,
            TOWER_BASE_WIDTH,
            TOWER_BASE_HEIGHT
        )

        # Base glow
        base_glow = pygame.Surface(
            (base_rect.width + 10, base_rect.height + 8), pygame.SRCALPHA
        )
        base_glow_color = (*NEON_CYAN[:3], int(20 + self.highlight * 30))
        pygame.draw.rect(base_glow, base_glow_color, base_glow.get_rect(),
                         border_radius=5)
        surface.blit(base_glow, (base_rect.x - 5, base_rect.y - 4))

        base_color = (30, 45, 70)
        pygame.draw.rect(surface, base_color, base_rect, border_radius=5)
        pygame.draw.rect(surface, (*NEON_CYAN[:3], 80), base_rect,
                         width=1, border_radius=5)

        # Draw label
        font = pygame.font.SysFont("Consolas", 14)
        label = self.labels[self.index] if self.index < 3 else f"TOWER {self.index + 1}"
        label_surf = font.render(label, True, UI_TEXT_DIM)
        label_rect = label_surf.get_rect(centerx=self.x, top=self.base_y + 18)
        surface.blit(label_surf, label_rect)

        # Draw disks
        for disk in self.disks:
            disk.draw(surface, time_elapsed)
