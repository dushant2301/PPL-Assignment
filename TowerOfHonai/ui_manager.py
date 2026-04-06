"""
UI Manager — futuristic neon glassmorphism UI with buttons, panels, and stats.
"""

import pygame
import math
from constants import *


class Button:
    """A futuristic neon-styled button with hover and click animations."""

    def __init__(self, x, y, width, height, text, color=NEON_CYAN,
                 shortcut_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.shortcut_text = shortcut_text
        self.hover = False
        self.active = False
        self.enabled = True
        self.click_anim = 0.0
        self.hover_anim = 0.0

    def update(self, dt, mouse_pos):
        """Update button animation state."""
        self.hover = self.rect.collidepoint(mouse_pos) and self.enabled

        # Smooth hover animation
        target = 1.0 if self.hover else 0.0
        self.hover_anim += (target - self.hover_anim) * dt * 12

        # Click fade
        if self.click_anim > 0:
            self.click_anim = max(0, self.click_anim - dt * 4)

    def draw(self, surface):
        """Draw the button with glassmorphism effect."""
        r = self.rect

        # Glass background
        glass_surf = pygame.Surface((r.width, r.height), pygame.SRCALPHA)

        # Background fill
        bg_alpha = int(30 + self.hover_anim * 30)
        if self.active:
            bg_alpha = 60
        bg_color = (*self.color[:3], bg_alpha)
        pygame.draw.rect(glass_surf, bg_color, (0, 0, r.width, r.height),
                         border_radius=BUTTON_RADIUS)

        # Click flash
        if self.click_anim > 0:
            flash_alpha = int(100 * self.click_anim)
            pygame.draw.rect(glass_surf, (*WHITE[:3], flash_alpha),
                             (0, 0, r.width, r.height),
                             border_radius=BUTTON_RADIUS)

        # Border glow
        border_alpha = int(80 + self.hover_anim * 120)
        if self.active:
            border_alpha = 220
        if not self.enabled:
            border_alpha = 30

        border_color = self.color if self.enabled else UI_TEXT_DIM
        pygame.draw.rect(glass_surf, (*border_color[:3], border_alpha),
                         (0, 0, r.width, r.height),
                         width=2, border_radius=BUTTON_RADIUS)

        surface.blit(glass_surf, r.topleft)

        # Text
        font = pygame.font.SysFont("Consolas", 15, bold=True)
        text_color = self.color if self.enabled else UI_TEXT_DIM
        if self.active:
            text_color = WHITE
        text_surf = font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=(r.centerx, r.centery - 2))
        surface.blit(text_surf, text_rect)

        # Shortcut hint
        if self.shortcut_text and self.hover:
            hint_font = pygame.font.SysFont("Consolas", 10)
            hint_surf = hint_font.render(self.shortcut_text, True, UI_TEXT_DIM)
            hint_rect = hint_surf.get_rect(centerx=r.centerx, top=r.bottom + 3)
            surface.blit(hint_surf, hint_rect)

    def handle_click(self, mouse_pos):
        """Check if button was clicked. Returns True if clicked."""
        if self.rect.collidepoint(mouse_pos) and self.enabled:
            self.click_anim = 1.0
            return True
        return False


class Slider:
    """A futuristic slider control for speed adjustment."""

    def __init__(self, x, y, width, values, labels, default_index=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = 30
        self.values = values
        self.labels = labels
        self.current_index = default_index
        self.dragging = False
        self.rect = pygame.Rect(x, y - 5, width, self.height + 10)

    @property
    def value(self):
        return self.values[self.current_index]

    @property
    def label(self):
        return self.labels[self.current_index]

    def set_index(self, idx):
        """Set the slider to a specific index."""
        self.current_index = max(0, min(len(self.values) - 1, idx))

    def handle_click(self, mouse_pos):
        """Handle click on the slider."""
        if self.rect.collidepoint(mouse_pos):
            # Determine which segment was clicked
            rel_x = mouse_pos[0] - self.x
            segment_width = self.width / len(self.values)
            idx = int(rel_x / segment_width)
            self.set_index(idx)
            return True
        return False

    def draw(self, surface):
        """Draw the slider."""
        n = len(self.values)
        seg_w = self.width / n

        for i in range(n):
            sx = self.x + i * seg_w
            sr = pygame.Rect(int(sx), self.y, int(seg_w), self.height)

            # Background
            is_selected = i == self.current_index
            bg_alpha = 50 if is_selected else 20
            bg_surf = pygame.Surface((sr.width, sr.height), pygame.SRCALPHA)

            color = NEON_CYAN if is_selected else UI_TEXT_DIM
            pygame.draw.rect(bg_surf, (*color[:3], bg_alpha),
                             (0, 0, sr.width, sr.height),
                             border_radius=6)
            pygame.draw.rect(bg_surf, (*color[:3], 100 if is_selected else 40),
                             (0, 0, sr.width, sr.height),
                             width=1, border_radius=6)
            surface.blit(bg_surf, sr.topleft)

            # Label
            font = pygame.font.SysFont("Consolas", 12, bold=is_selected)
            label_surf = font.render(self.labels[i], True, color)
            label_rect = label_surf.get_rect(center=sr.center)
            surface.blit(label_surf, label_rect)

        # Title
        title_font = pygame.font.SysFont("Consolas", 11)
        title_surf = title_font.render("SPEED", True, UI_TEXT_DIM)
        title_rect = title_surf.get_rect(centerx=self.x + self.width // 2,
                                         bottom=self.y - 5)
        surface.blit(title_surf, title_rect)


class DiskCounter:
    """Interactive disk count selector with +/- buttons."""

    def __init__(self, x, y, initial_count=DEFAULT_DISK_COUNT):
        self.x = x
        self.y = y
        self.count = initial_count
        self.minus_rect = pygame.Rect(x, y, 32, 32)
        self.plus_rect = pygame.Rect(x + 80, y, 32, 32)
        self.hover_minus = False
        self.hover_plus = False

    def update(self, mouse_pos):
        """Update hover states."""
        self.hover_minus = self.minus_rect.collidepoint(mouse_pos)
        self.hover_plus = self.plus_rect.collidepoint(mouse_pos)

    def handle_click(self, mouse_pos):
        """Handle click, returns new count or None."""
        if self.minus_rect.collidepoint(mouse_pos) and self.count > MIN_DISKS:
            self.count -= 1
            return self.count
        if self.plus_rect.collidepoint(mouse_pos) and self.count < MAX_DISKS:
            self.count += 1
            return self.count
        return None

    def increment(self):
        if self.count < MAX_DISKS:
            self.count += 1
            return self.count
        return None

    def decrement(self):
        if self.count > MIN_DISKS:
            self.count -= 1
            return self.count
        return None

    def draw(self, surface):
        """Draw the disk counter."""
        # Title
        title_font = pygame.font.SysFont("Consolas", 11)
        title_surf = title_font.render("DISKS", True, UI_TEXT_DIM)
        title_rect = title_surf.get_rect(centerx=self.x + 56, bottom=self.y - 5)
        surface.blit(title_surf, title_rect)

        # Minus button
        color_m = NEON_CYAN if self.hover_minus and self.count > MIN_DISKS else UI_TEXT_DIM
        btn_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, (*color_m[:3], 40 if self.hover_minus else 20),
                         (0, 0, 32, 32), border_radius=6)
        pygame.draw.rect(btn_surf, (*color_m[:3], 100), (0, 0, 32, 32),
                         width=1, border_radius=6)
        surface.blit(btn_surf, self.minus_rect.topleft)
        font = pygame.font.SysFont("Consolas", 18, bold=True)
        m_surf = font.render("−", True, color_m)
        surface.blit(m_surf, m_surf.get_rect(center=self.minus_rect.center))

        # Count display
        count_font = pygame.font.SysFont("Consolas", 22, bold=True)
        count_surf = count_font.render(str(self.count), True, NEON_CYAN)
        count_rect = count_surf.get_rect(center=(self.x + 56, self.y + 16))
        surface.blit(count_surf, count_rect)

        # Plus button
        color_p = NEON_CYAN if self.hover_plus and self.count < MAX_DISKS else UI_TEXT_DIM
        btn_surf2 = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf2, (*color_p[:3], 40 if self.hover_plus else 20),
                         (0, 0, 32, 32), border_radius=6)
        pygame.draw.rect(btn_surf2, (*color_p[:3], 100), (0, 0, 32, 32),
                         width=1, border_radius=6)
        surface.blit(btn_surf2, self.plus_rect.topleft)
        p_surf = font.render("+", True, color_p)
        surface.blit(p_surf, p_surf.get_rect(center=self.plus_rect.center))


class UIManager:
    """Manages all UI elements — panels, buttons, stats, and overlays."""

    def __init__(self):
        self.buttons = {}
        self.speed_slider = None
        self.disk_counter = None
        self.time_elapsed = 0.0
        self.show_stats = True
        self.completion_alpha = 0.0
        self.completion_active = False
        self.completion_text_scale = 0.0
        self._setup_ui()

    def _setup_ui(self):
        """Initialize all UI components."""
        # Bottom panel buttons — centered layout
        panel_center_x = SCREEN_WIDTH // 2
        btn_y = BOTTOM_PANEL_Y + 35

        # Calculate total width of all buttons
        button_configs = [
            ("auto_solve", "AUTO SOLVE", NEON_CYAN, "[S]"),
            ("step", "NEXT STEP", NEON_GREEN, "[N]"),
            ("pause", "PAUSE", NEON_ORANGE, "[SPACE]"),
            ("reset", "RESET", NEON_RED, "[R]"),
            ("sound", "SOUND: ON", NEON_PURPLE, "[M]"),
        ]

        total_width = len(button_configs) * BUTTON_WIDTH + (len(button_configs) - 1) * BUTTON_GAP
        start_x = panel_center_x - total_width // 2

        for i, (key, text, color, shortcut) in enumerate(button_configs):
            bx = start_x + i * (BUTTON_WIDTH + BUTTON_GAP)
            self.buttons[key] = Button(bx, btn_y, BUTTON_WIDTH, BUTTON_HEIGHT,
                                       text, color, shortcut)

        # Speed slider — below buttons
        slider_width = 320
        slider_x = panel_center_x - slider_width // 2
        self.speed_slider = Slider(slider_x, btn_y + BUTTON_HEIGHT + 25,
                                   slider_width, SPEED_VALUES, SPEED_LABELS, 1)

        # Disk counter — left side of bottom panel
        self.disk_counter = DiskCounter(50, btn_y + 5)

    def update(self, dt, mouse_pos, game_state):
        """Update all UI elements."""
        self.time_elapsed += dt

        for btn in self.buttons.values():
            btn.update(dt, mouse_pos)

        self.disk_counter.update(mouse_pos)

        # Update button states based on game state
        is_solving = game_state.get('is_solving', False)
        is_paused = game_state.get('is_paused', False)
        is_complete = game_state.get('is_complete', False)
        is_animating = game_state.get('is_animating', False)

        # Update pause button text
        if is_solving and not is_paused:
            self.buttons['pause'].text = "PAUSE"
        elif is_paused:
            self.buttons['pause'].text = "RESUME"
        else:
            self.buttons['pause'].text = "START"

        # Enable/disable buttons contextually
        self.buttons['step'].enabled = not is_solving or is_paused
        self.buttons['auto_solve'].active = is_solving and not is_paused
        self.buttons['auto_solve'].enabled = not is_complete

        # Disable disk counter during solving
        # (handled in click logic)

        # Completion animation
        if self.completion_active:
            self.completion_alpha = min(255, self.completion_alpha + dt * 200)
            self.completion_text_scale = min(1.0, self.completion_text_scale + dt * 3)
        else:
            self.completion_alpha = max(0, self.completion_alpha - dt * 300)
            self.completion_text_scale = max(0, self.completion_text_scale - dt * 5)

    def draw(self, surface, game_state):
        """Draw all UI elements."""
        self._draw_top_panel(surface, game_state)
        self._draw_bottom_panel(surface)
        self._draw_completion_overlay(surface)

    def _draw_top_panel(self, surface, game_state):
        """Draw the top stats panel with glassmorphism."""
        panel_rect = pygame.Rect(
            TOP_PANEL_MARGIN, TOP_PANEL_MARGIN,
            SCREEN_WIDTH - TOP_PANEL_MARGIN * 2, TOP_PANEL_HEIGHT
        )

        # Glass panel background
        panel_surf = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (15, 20, 40, 160),
                         (0, 0, panel_rect.width, panel_rect.height),
                         border_radius=15)
        # Inner glow border
        pygame.draw.rect(panel_surf, (*NEON_CYAN[:3], 40),
                         (0, 0, panel_rect.width, panel_rect.height),
                         width=1, border_radius=15)
        surface.blit(panel_surf, panel_rect.topleft)

        # Title
        title_font = pygame.font.SysFont("Consolas", 20, bold=True)
        title_text = title_font.render("TOWER OF HANOI", True, NEON_CYAN)
        surface.blit(title_text, (panel_rect.x + 20, panel_rect.y + 10))

        subtitle_font = pygame.font.SysFont("Consolas", 11)
        subtitle = subtitle_font.render("Dushant Sewatkar CS25D006", True, UI_TEXT_DIM)
        surface.blit(subtitle, (panel_rect.x + 20, panel_rect.y + 36))

        # Stats — right side
        stats_font = pygame.font.SysFont("Consolas", 14)
        stats_bold = pygame.font.SysFont("Consolas", 16, bold=True)

        move_count = game_state.get('move_count', 0)
        optimal = game_state.get('optimal_moves', 0)
        disk_count = game_state.get('disk_count', DEFAULT_DISK_COUNT)
        progress = game_state.get('progress', 0)

        stats = [
            ("MOVES", f"{move_count}", NEON_CYAN),
            ("OPTIMAL", f"{optimal}", NEON_GREEN),
            ("PROGRESS", f"{progress}%", NEON_ORANGE),
        ]

        stat_x = panel_rect.right - 100 * len(stats) - 20
        for i, (label, value, color) in enumerate(stats):
            sx = stat_x + i * 100

            # Label
            label_surf = stats_font.render(label, True, UI_TEXT_DIM)
            surface.blit(label_surf, (sx, panel_rect.y + 12))

            # Value
            value_surf = stats_bold.render(value, True, color)
            surface.blit(value_surf, (sx, panel_rect.y + 32))

        # Progress bar
        bar_y = panel_rect.bottom - 8
        bar_width = panel_rect.width - 40
        bar_x = panel_rect.x + 20

        # Background
        pygame.draw.rect(surface, (20, 25, 45),
                         (bar_x, bar_y, bar_width, 4), border_radius=2)
        # Fill
        fill_width = int(bar_width * progress / 100)
        if fill_width > 0:
            # Gradient fill
            fill_surf = pygame.Surface((fill_width, 4), pygame.SRCALPHA)
            for px in range(fill_width):
                t = px / max(1, fill_width)
                r = int(NEON_CYAN[0] * (1 - t) + NEON_GREEN[0] * t)
                g = int(NEON_CYAN[1] * (1 - t) + NEON_GREEN[1] * t)
                b = int(NEON_CYAN[2] * (1 - t) + NEON_GREEN[2] * t)
                pygame.draw.line(fill_surf, (r, g, b, 200), (px, 0), (px, 3))
            surface.blit(fill_surf, (bar_x, bar_y))

    def _draw_bottom_panel(self, surface):
        """Draw the bottom control panel."""
        panel_rect = pygame.Rect(
            TOP_PANEL_MARGIN, BOTTOM_PANEL_Y,
            SCREEN_WIDTH - TOP_PANEL_MARGIN * 2, BOTTOM_PANEL_HEIGHT
        )

        # Glass panel
        panel_surf = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (15, 20, 40, 140),
                         (0, 0, panel_rect.width, panel_rect.height),
                         border_radius=15)
        pygame.draw.rect(panel_surf, (*NEON_CYAN[:3], 30),
                         (0, 0, panel_rect.width, panel_rect.height),
                         width=1, border_radius=15)
        surface.blit(panel_surf, panel_rect.topleft)

        # Panel title
        title_font = pygame.font.SysFont("Consolas", 11)
        title = title_font.render("CONTROLS", True, UI_TEXT_DIM)
        surface.blit(title, (panel_rect.x + 20, panel_rect.y + 8))

        # Draw buttons
        for btn in self.buttons.values():
            btn.draw(surface)

        # Draw slider
        self.speed_slider.draw(surface)

        # Draw disk counter
        self.disk_counter.draw(surface)

    def _draw_completion_overlay(self, surface):
        """Draw the 'PUZZLE SOLVED' celebration overlay."""
        if self.completion_alpha <= 0:
            return

        alpha = int(self.completion_alpha)
        scale = self.completion_text_scale

        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, int(alpha * 0.3)),
                         (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(overlay, (0, 0))

        if scale <= 0:
            return

        # Main text
        font_size = max(10, int(60 * scale))
        font = pygame.font.SysFont("Consolas", font_size, bold=True)
        text = font.render("PUZZLE SOLVED!", True, NEON_CYAN)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))

        # Text glow
        glow_pulse = 0.7 + 0.3 * math.sin(self.time_elapsed * 4)
        glow_surf = pygame.Surface((text_rect.width + 40, text_rect.height + 20), pygame.SRCALPHA)
        glow_color = (*NEON_CYAN[:3], int(40 * glow_pulse * (alpha / 255)))
        pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=10)
        surface.blit(glow_surf, (text_rect.x - 20, text_rect.y - 10))

        surface.blit(text, text_rect)

        # Sub text
        sub_font = pygame.font.SysFont("Consolas", max(8, int(18 * scale)))
        sub_text = sub_font.render("Press R to reset or adjust disk count for a new challenge",
                                   True, UI_TEXT_DIM)
        sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        surface.blit(sub_text, sub_rect)

    def trigger_completion(self):
        """Trigger the completion overlay."""
        self.completion_active = True

    def hide_completion(self):
        """Hide the completion overlay."""
        self.completion_active = False
