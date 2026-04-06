"""
Tower of Hanoi 
Main game controller that orchestrates all systems.

Premium interactive simulation with cinematic animations,
particle effects, and a futuristic neon UI.

Controls:
  SPACE   - Start / Pause / Resume auto-solve
  S       - Toggle auto-solve
  N       - Next step (manual mode)
  R       - Reset puzzle
  UP/DOWN - Adjust disk count
  1-4     - Speed: Slow / Normal / Fast / Ultra
  M       - Toggle sound
  ESC     - Quit

Drag-and-drop: Click and drag disks to move them manually.
"""

import pygame
import sys
import math
import random
from constants import *
from game_objects import Disk, Tower
from animator import Animator
from particles import ParticleSystem
from ui_manager import UIManager
from sound_manager import SoundManager


class Game:
    """Main game controller for the Tower of Hanoi simulator."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # Display setup — internal surface for fixed-resolution rendering
        self.window_width = SCREEN_WIDTH
        self.window_height = SCREEN_HEIGHT
        self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption(TITLE)
        # Internal render surface at fixed resolution
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Time tracking
        self.time_elapsed = 0.0
        self.delta_time = 0.0

        # Core systems
        self.particle_system = ParticleSystem()
        self.sound_manager = SoundManager()
        self.towers = []
        self.animator = None
        self.ui = UIManager()

        # Game state
        self.disk_count = DEFAULT_DISK_COUNT
        self.move_count = 0
        self.optimal_moves = 0
        self.move_history = []
        self.solution_moves = []

        # Control state
        self.is_solving = False
        self.is_paused = False
        self.is_complete = False
        self.auto_solve = False

        # Drag-and-drop state
        self.dragging_disk = None
        self.drag_source_tower = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Background surfaces
        self._grid_surface = None
        self._bg_surface = None
        self._init_background()

        # Initialize the puzzle
        self._reset_puzzle()

    def _init_background(self):
        """Create the pre-cached background surfaces."""
        # Pre-render gradient background
        self._bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 2):
            t = y / SCREEN_HEIGHT
            r = int(DARK_BG[0] * (1 - t) + DARK_BG_2[0] * t)
            g = int(DARK_BG[1] * (1 - t) + DARK_BG_2[1] * t)
            b = int(DARK_BG[2] * (1 - t) + DARK_BG_2[2] * t)
            pygame.draw.rect(self._bg_surface, (r, g, b),
                             (0, y, SCREEN_WIDTH, 2))

        # Pre-render grid overlay
        self._grid_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        grid_spacing = 50
        for x in range(0, SCREEN_WIDTH, grid_spacing):
            alpha = 12 + int(8 * math.sin(x * 0.02))
            pygame.draw.line(self._grid_surface, (40, 60, 100, alpha),
                             (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, grid_spacing):
            alpha = 12 + int(8 * math.sin(y * 0.02))
            pygame.draw.line(self._grid_surface, (40, 60, 100, alpha),
                             (0, y), (SCREEN_WIDTH, y))

    def _reset_puzzle(self):
        """Reset the puzzle with the current disk count."""
        # Clear state
        self.move_count = 0
        self.optimal_moves = (2 ** self.disk_count) - 1
        self.move_history.clear()
        self.solution_moves.clear()
        self.is_solving = False
        self.is_paused = False
        self.is_complete = False
        self.auto_solve = False

        # Clear particles
        self.particle_system.clear()

        # Create towers
        self.towers = []
        for i in range(3):
            self.towers.append(Tower(i, TOWER_POSITIONS[i]))

        # Create animator
        self.animator = Animator(self.towers, self.particle_system, self.sound_manager)
        self.animator.set_speed(self.ui.speed_slider.value)
        self.animator.on_move_complete = self._on_move_complete

        # Create and place disks on the first tower (largest at bottom)
        for i in range(self.disk_count - 1, -1, -1):
            disk = Disk(i, self.disk_count)
            self.towers[0].push(disk)

        # Pre-compute solution
        self._compute_solution(self.disk_count, 0, 2, 1)

        # Update UI disk counter
        self.ui.disk_counter.count = self.disk_count
        self.ui.hide_completion()

        # Drag state
        self.dragging_disk = None
        self.drag_source_tower = None

    def _compute_solution(self, n, source, target, auxiliary):
        """Compute the Tower of Hanoi solution using recursion."""
        if n == 0:
            return
        self._compute_solution(n - 1, source, auxiliary, target)
        self.solution_moves.append((source, target))
        self._compute_solution(n - 1, auxiliary, target, source)

    def _start_auto_solve(self):
        """Begin the auto-solve animation."""
        if self.is_complete:
            return

        self.is_solving = True
        self.is_paused = False
        self.auto_solve = True

        # Queue all remaining moves
        self.animator.clear_queue()
        start_idx = self.move_count
        for move in self.solution_moves[start_idx:]:
            self.animator.queue_move(move[0], move[1])

    def _step_solve(self):
        """Execute the next move in the solution."""
        if self.is_complete or self.move_count >= len(self.solution_moves):
            return

        if self.animator.busy:
            return

        move = self.solution_moves[self.move_count]
        self.animator.queue_move(move[0], move[1])

    def _on_move_complete(self, from_tower, to_tower):
        """Called by the animator after each move animation finishes."""
        self.move_count += 1
        self.move_history.append((from_tower, to_tower))

    def _toggle_pause(self):
        """Toggle pause/resume."""
        if self.is_complete:
            return

        if not self.is_solving:
            # Start auto-solve
            self._start_auto_solve()
        else:
            self.is_paused = not self.is_paused

    def _check_completion(self):
        """Check if the puzzle is solved."""
        if len(self.towers[2].disks) == self.disk_count:
            if not self.is_complete:
                self.is_complete = True
                self.is_solving = False
                self.auto_solve = False

                # Trigger celebration
                self.ui.trigger_completion()
                self.particle_system.emit_celebration(150)
                self.sound_manager.play('success')

    def _handle_drag_start(self, mouse_pos):
        """Start dragging a disk."""
        if self.is_solving or self.is_complete:
            return

        mx, my = mouse_pos
        for tower in self.towers:
            top_disk = tower.peek()
            if top_disk and top_disk.contains_point(mx, my):
                self.dragging_disk = top_disk
                self.drag_source_tower = tower.index
                top_disk.is_dragging = True
                top_disk.glow_time = 0
                self.drag_offset_x = top_disk.x - mx
                self.drag_offset_y = top_disk.y - my
                # Remove from tower temporarily
                tower.pop()
                self.sound_manager.play('pickup')
                self.particle_system.emit_sparkle(top_disk.x, top_disk.y,
                                                  top_disk.base_color, 5)
                break

    def _handle_drag_move(self, mouse_pos):
        """Update dragged disk position."""
        if self.dragging_disk:
            mx, my = mouse_pos
            self.dragging_disk.x = mx + self.drag_offset_x
            self.dragging_disk.y = my + self.drag_offset_y
            # Emit trail
            self.particle_system.emit_trail(
                self.dragging_disk.x, self.dragging_disk.y,
                self.dragging_disk.base_color, 3
            )

    def _handle_drag_end(self, mouse_pos):
        """End dragging and attempt to place the disk."""
        if not self.dragging_disk:
            return

        disk = self.dragging_disk
        disk.is_dragging = False

        # Find the closest tower
        mx = mouse_pos[0]
        closest_tower = None
        min_dist = float('inf')
        for tower in self.towers:
            dist = abs(tower.x - mx)
            if dist < min_dist:
                min_dist = dist
                closest_tower = tower

        # Check if valid placement
        if closest_tower and closest_tower.can_place(disk):
            closest_tower.push(disk)
            self.sound_manager.play('drop')
            self.particle_system.emit_burst(
                disk.x, disk.y, disk.base_color,
                count=8, speed=60, lifetime=0.4, size=2
            )

            # Track as a move if it's a different tower
            if closest_tower.index != self.drag_source_tower:
                self.move_history.append((self.drag_source_tower, closest_tower.index))
                self.move_count += 1
        else:
            # Invalid move — return to source tower
            source = self.towers[self.drag_source_tower]
            source.push(disk)
            disk.start_shake()
            self.sound_manager.play('error')

        self.dragging_disk = None
        self.drag_source_tower = None

    def _map_mouse(self, pos):
        """Map window mouse coordinates to internal surface coordinates."""
        # Calculate the scaled/letterboxed area
        win_w, win_h = self.window_width, self.window_height
        scale = min(win_w / SCREEN_WIDTH, win_h / SCREEN_HEIGHT)
        scaled_w = int(SCREEN_WIDTH * scale)
        scaled_h = int(SCREEN_HEIGHT * scale)
        offset_x = (win_w - scaled_w) // 2
        offset_y = (win_h - scaled_h) // 2

        # Map to internal coordinates
        mx = (pos[0] - offset_x) / scale
        my = (pos[1] - offset_y) / scale
        return (int(mx), int(my))

    def _handle_events(self):
        """Process all input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.VIDEORESIZE:
                self.window_width = event.w
                self.window_height = event.h
                self.window = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )

            elif event.type == pygame.KEYDOWN:
                self._handle_key(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mapped = self._map_mouse(event.pos)
                    self._handle_click(mapped)
                    self._handle_drag_start(mapped)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mapped = self._map_mouse(event.pos)
                    self._handle_drag_end(mapped)

            elif event.type == pygame.MOUSEMOTION:
                mapped = self._map_mouse(event.pos)
                self._handle_drag_move(mapped)

        return True

    def _handle_key(self, key):
        """Handle keyboard shortcuts."""
        if key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        elif key == pygame.K_SPACE:
            self._toggle_pause()
            self.sound_manager.play('click')

        elif key == pygame.K_s:
            if not self.auto_solve:
                self._start_auto_solve()
            else:
                self.is_paused = True
                self.auto_solve = False
                self.is_solving = False
                self.animator.clear_queue()
            self.sound_manager.play('click')

        elif key == pygame.K_n:
            self._step_solve()
            self.sound_manager.play('click')

        elif key == pygame.K_r:
            self._reset_puzzle()
            self.sound_manager.play('click')

        elif key == pygame.K_UP:
            new_count = self.ui.disk_counter.increment()
            if new_count and not self.is_solving:
                self.disk_count = new_count
                self._reset_puzzle()
                self.sound_manager.play('click')

        elif key == pygame.K_DOWN:
            new_count = self.ui.disk_counter.decrement()
            if new_count and not self.is_solving:
                self.disk_count = new_count
                self._reset_puzzle()
                self.sound_manager.play('click')

        elif key == pygame.K_m:
            enabled = self.sound_manager.toggle_sounds()
            self.ui.buttons['sound'].text = f"SOUND: {'ON' if enabled else 'OFF'}"
            self.ui.buttons['sound'].active = enabled

        elif key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
            idx = key - pygame.K_1
            self.ui.speed_slider.set_index(idx)
            self.animator.set_speed(self.ui.speed_slider.value)
            self.sound_manager.play('click')

    def _handle_click(self, mouse_pos):
        """Handle mouse clicks on UI elements."""
        # Check buttons
        if self.ui.buttons['auto_solve'].handle_click(mouse_pos):
            if not self.auto_solve:
                self._start_auto_solve()
            else:
                self.is_paused = True
                self.auto_solve = False
                self.is_solving = False
                self.animator.clear_queue()
            self.sound_manager.play('click')

        elif self.ui.buttons['step'].handle_click(mouse_pos):
            self._step_solve()
            self.sound_manager.play('click')

        elif self.ui.buttons['pause'].handle_click(mouse_pos):
            self._toggle_pause()
            self.sound_manager.play('click')

        elif self.ui.buttons['reset'].handle_click(mouse_pos):
            self._reset_puzzle()
            self.sound_manager.play('click')

        elif self.ui.buttons['sound'].handle_click(mouse_pos):
            enabled = self.sound_manager.toggle_sounds()
            self.ui.buttons['sound'].text = f"SOUND: {'ON' if enabled else 'OFF'}"
            self.ui.buttons['sound'].active = enabled
            self.sound_manager.play('click')

        # Check speed slider
        if self.ui.speed_slider.handle_click(mouse_pos):
            self.animator.set_speed(self.ui.speed_slider.value)
            self.sound_manager.play('click')

        # Check disk counter (only when not solving)
        if not self.is_solving:
            new_count = self.ui.disk_counter.handle_click(mouse_pos)
            if new_count is not None:
                self.disk_count = new_count
                self._reset_puzzle()
                self.sound_manager.play('click')

    def _update(self):
        """Update game logic."""
        dt = self.delta_time

        # Update time
        self.time_elapsed += dt

        # Update particles (always, for visual continuity)
        self.particle_system.update(dt)

        # Update animator only when NOT paused
        if not (self.is_solving and self.is_paused):
            self.animator.update(dt)

        # Update all disks
        for tower in self.towers:
            for disk in tower.disks:
                disk.update(dt)

        # Update dragged disk
        if self.dragging_disk:
            self.dragging_disk.update(dt)

        # Calculate progress
        progress = 0
        if self.disk_count > 0:
            target_count = len(self.towers[2].disks)
            progress = int(target_count / self.disk_count * 100)

        # Update UI
        mouse_pos = self._map_mouse(pygame.mouse.get_pos())
        game_state = {
            'move_count': self.move_count,
            'optimal_moves': self.optimal_moves,
            'disk_count': self.disk_count,
            'progress': progress,
            'is_solving': self.is_solving,
            'is_paused': self.is_paused,
            'is_complete': self.is_complete,
            'is_animating': self.animator.busy,
        }
        self.ui.update(dt, mouse_pos, game_state)

        # Hover highlight on towers (use mapped mouse)
        raw_mouse = pygame.mouse.get_pos()
        mapped_mouse = self._map_mouse(raw_mouse)
        for tower in self.towers:
            dist = abs(tower.x - mapped_mouse[0])
            tower.highlight = max(0, 1.0 - dist / 150) * 0.5

        # Check completion
        self._check_completion()

    def _draw(self):
        """Render the complete frame."""
        # Background gradient
        self._draw_background()

        # Draw ambient particles (behind everything)
        self.particle_system.draw_ambient(self.screen)

        # Draw grid overlay
        self.screen.blit(self._grid_surface, (0, 0))

        # Draw motion trails
        self.particle_system.draw_trails(self.screen)

        # Draw towers and their disks
        for tower in self.towers:
            tower.draw(self.screen, self.time_elapsed)

        # Draw dragged disk on top
        if self.dragging_disk:
            self.dragging_disk.draw(self.screen, self.time_elapsed)

        # Draw active animation disk
        if self.animator.current_animation:
            anim = self.animator.current_animation
            anim.disk.draw(self.screen, self.time_elapsed)

        # Draw particles (on top of everything)
        self.particle_system.draw_particles(self.screen)

        # Calculate progress for UI
        progress = 0
        if self.disk_count > 0:
            target_count = len(self.towers[2].disks)
            progress = int(target_count / self.disk_count * 100)

        # Draw UI
        game_state = {
            'move_count': self.move_count,
            'optimal_moves': self.optimal_moves,
            'disk_count': self.disk_count,
            'progress': progress,
            'is_solving': self.is_solving,
            'is_paused': self.is_paused,
            'is_complete': self.is_complete,
            'is_animating': self.animator.busy,
        }
        self.ui.draw(self.screen, game_state)

        # Draw keyboard shortcuts help (bottom right corner)
        self._draw_help_hint()

        # Scale internal surface to window (preserving aspect ratio)
        win_w, win_h = self.window_width, self.window_height
        scale = min(win_w / SCREEN_WIDTH, win_h / SCREEN_HEIGHT)
        scaled_w = int(SCREEN_WIDTH * scale)
        scaled_h = int(SCREEN_HEIGHT * scale)
        offset_x = (win_w - scaled_w) // 2
        offset_y = (win_h - scaled_h) // 2

        # Clear window to black (for letterbox bars)
        self.window.fill((0, 0, 0))
        # Scale and blit the internal render surface
        scaled_surface = pygame.transform.smoothscale(self.screen, (scaled_w, scaled_h))
        self.window.blit(scaled_surface, (offset_x, offset_y))

        # Update display
        pygame.display.flip()

    def _draw_background(self):
        """Draw the pre-cached gradient background with animated glow."""
        # Blit pre-cached gradient
        self.screen.blit(self._bg_surface, (0, 0))

        # Subtle animated radial glow in center
        glow_pulse = 0.5 + 0.2 * math.sin(self.time_elapsed * 0.5)
        glow_size = int(300 * glow_pulse)
        if glow_size > 10:
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            for radius in range(glow_size, 0, -5):
                alpha = int(3 * (1 - radius / glow_size))
                pygame.draw.circle(glow_surf, (20, 40, 80, alpha),
                                   (glow_size, glow_size), radius)
            self.screen.blit(glow_surf,
                             (SCREEN_WIDTH // 2 - glow_size,
                              SCREEN_HEIGHT // 2 - glow_size - 50))

    def _draw_help_hint(self):
        """Draw a small keyboard shortcuts hint."""
        font = pygame.font.SysFont("Consolas", 10)
        hints = [
            "SPACE: Start/Pause  |  S: Auto-Solve  |  N: Next Step",
            "R: Reset  |  ↑↓: Disks  |  1-4: Speed  |  M: Sound  |  Drag disks!"
        ]
        for i, hint in enumerate(hints):
            surf = font.render(hint, True, (60, 70, 90))
            rect = surf.get_rect(
                right=SCREEN_WIDTH - 20,
                bottom=SCREEN_HEIGHT - 10 + i * 14 - 14
            )
            self.screen.blit(surf, rect)

    def run(self):
        """Main game loop."""
        running = True
        while running:
            # Delta time
            self.delta_time = self.clock.tick(FPS) / 1000.0
            # Cap delta time to avoid physics explosions
            self.delta_time = min(self.delta_time, 0.05)

            # Events
            running = self._handle_events()

            # Update
            self._update()

            # Draw
            self._draw()

        pygame.quit()
        sys.exit()


def main():
    """Entry point."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
