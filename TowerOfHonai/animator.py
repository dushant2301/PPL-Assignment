"""
Animator — handles the anti-gravity disk movement with multi-phase animations.
Phase 1: Lift (float up with anti-gravity feel)
Phase 2: Glide (horizontal movement with ease-in-out)
Phase 3: Drop (smooth descent with bounce physics)
"""

import math
from constants import *
from easing import (ease_in_out_cubic, ease_out_cubic, ease_in_cubic,
                    ease_out_bounce, smoothstep, lerp)


class MoveAnimation:
    """Represents a single disk move animation with three phases."""

    PHASE_LIFT = 0
    PHASE_GLIDE = 1
    PHASE_DROP = 2
    PHASE_DONE = 3

    def __init__(self, disk, from_tower, to_tower, towers):
        self.disk = disk
        self.from_tower = from_tower
        self.to_tower = to_tower
        self.towers = towers

        # Phase tracking
        self.phase = self.PHASE_LIFT
        self.phase_progress = 0.0

        # Store positions
        self.start_x = disk.x
        self.start_y = disk.y

        # Lift target: go above the tallest tower
        self.lift_y = self.towers[from_tower].top_y - 50

        # Glide target x
        self.target_x = TOWER_POSITIONS[to_tower]

        # Drop target y: where the disk will land on the target tower
        target_tower = self.towers[to_tower]
        n_disks = len(target_tower.disks)
        self.target_y = target_tower.base_y - n_disks * (DISK_HEIGHT + DISK_GAP) - DISK_HEIGHT / 2

        # Phase durations (in seconds, before speed multiplier)
        self.lift_duration = 0.35
        self.glide_duration = 0.4
        self.drop_duration = 0.3

        # Bounce state
        self.bounce_velocity = 0.0
        self.bounce_done = False

        # Mark disk as active
        self.disk.is_active = True
        self.disk.glow_time = 0.0

    def update(self, dt, speed_multiplier=1.0):
        """
        Update the animation. Returns True when the full animation is done.
        """
        adjusted_dt = dt * speed_multiplier

        if self.phase == self.PHASE_LIFT:
            self.phase_progress += adjusted_dt / self.lift_duration
            t = min(1.0, self.phase_progress)
            eased = ease_out_cubic(t)

            self.disk.y = lerp(self.start_y, self.lift_y, eased)
            # Slight horizontal wobble during lift for anti-grav feel
            wobble = math.sin(t * math.pi * 3) * 3 * (1 - t)
            self.disk.x = self.start_x + wobble

            if t >= 1.0:
                self.phase = self.PHASE_GLIDE
                self.phase_progress = 0.0
                self.disk.y = self.lift_y

        elif self.phase == self.PHASE_GLIDE:
            self.phase_progress += adjusted_dt / self.glide_duration
            t = min(1.0, self.phase_progress)
            eased = ease_in_out_cubic(t)

            self.disk.x = lerp(self.start_x, self.target_x, eased)
            # Slight vertical float during glide
            float_offset = math.sin(t * math.pi) * 8
            self.disk.y = self.lift_y - float_offset

            if t >= 1.0:
                self.phase = self.PHASE_DROP
                self.phase_progress = 0.0
                self.disk.x = self.target_x

        elif self.phase == self.PHASE_DROP:
            self.phase_progress += adjusted_dt / self.drop_duration
            t = min(1.0, self.phase_progress)

            # Use bounce easing for satisfying landing
            eased = ease_out_bounce(t)
            self.disk.y = lerp(self.lift_y, self.target_y, eased)

            if t >= 1.0:
                self.phase = self.PHASE_DONE
                self.disk.y = self.target_y
                self.disk.x = self.target_x
                self.disk.is_active = False
                return True

        return False

    def get_trail_position(self):
        """Get current position for trail emission."""
        return (self.disk.x, self.disk.y)

    @property
    def is_lifting(self):
        return self.phase == self.PHASE_LIFT

    @property
    def is_gliding(self):
        return self.phase == self.PHASE_GLIDE

    @property
    def is_dropping(self):
        return self.phase == self.PHASE_DROP

    @property
    def is_done(self):
        return self.phase == self.PHASE_DONE


class Animator:
    """Manages the queue of move animations and coordinates with particle system."""

    def __init__(self, towers, particle_system, sound_manager):
        self.towers = towers
        self.particles = particle_system
        self.sounds = sound_manager
        self.current_animation = None
        self.move_queue = []
        self.speed_multiplier = ANIM_SPEED_NORMAL
        self.is_animating = False
        self.trail_timer = 0.0
        self.trail_interval = 0.02  # Emit trail every 20ms
        self.on_move_complete = None  # Callback: called with (from_tower, to_tower) after each move

    def queue_move(self, from_tower, to_tower):
        """Add a move to the animation queue."""
        self.move_queue.append((from_tower, to_tower))

    def clear_queue(self):
        """Clear all pending animations."""
        self.move_queue.clear()
        if self.current_animation:
            # Snap current animation to end
            anim = self.current_animation
            anim.disk.is_active = False
            anim.disk.x = anim.target_x
            anim.disk.y = anim.target_y
            self.current_animation = None
        self.is_animating = False

    def set_speed(self, speed):
        """Set the animation speed multiplier."""
        self.speed_multiplier = speed

    def start_next(self):
        """Start the next animation in the queue."""
        if not self.move_queue:
            self.is_animating = False
            return False

        from_tower, to_tower = self.move_queue.pop(0)

        # Get the disk from the source tower
        source = self.towers[from_tower]
        disk = source.pop()
        if disk is None:
            return self.start_next()

        # Create the animation
        self.current_animation = MoveAnimation(disk, from_tower, to_tower, self.towers)
        self.is_animating = True

        # Play pickup sound
        self.sounds.play('pickup')

        # Emit pickup particles
        self.particles.emit_sparkle(disk.x, disk.y, disk.base_color, count=8)

        return True

    def update(self, dt):
        """Update the current animation and manage the queue."""
        if self.current_animation is None:
            if self.move_queue:
                self.start_next()
            return

        anim = self.current_animation

        # Update animation
        done = anim.update(dt, self.speed_multiplier)

        # Emit trail particles while moving
        self.trail_timer += dt
        if self.trail_timer >= self.trail_interval:
            self.trail_timer = 0
            tx, ty = anim.get_trail_position()
            self.particles.emit_trail(tx, ty, anim.disk.base_color, size=3)

        # Phase transition effects
        if anim.is_gliding:
            # Occasional sparkles during glide
            if self.trail_timer < 0.01:
                self.particles.emit_sparkle(anim.disk.x, anim.disk.y,
                                            anim.disk.base_color, count=2)

        if done:
            # Place disk on target tower
            target = self.towers[anim.to_tower]
            target.push(anim.disk)

            # Play drop sound
            self.sounds.play('drop')

            # Emit landing particles
            self.particles.emit_burst(
                anim.disk.x, anim.disk.y,
                anim.disk.base_color,
                count=10, speed=80, lifetime=0.5, size=2
            )

            # Notify callback before clearing animation
            from_t = anim.from_tower
            to_t = anim.to_tower

            self.current_animation = None

            # Fire callback
            if self.on_move_complete:
                self.on_move_complete(from_t, to_t)

            # Start next animation if queued
            if self.move_queue:
                self.start_next()
            else:
                self.is_animating = False

    @property
    def busy(self):
        """Check if the animator is currently busy."""
        return self.current_animation is not None or len(self.move_queue) > 0
