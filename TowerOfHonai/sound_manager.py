"""
Sound manager — generates all sounds programmatically using pygame.
No external audio files needed.
"""

import pygame
import numpy as np
import math


class SoundManager:
    """Manages all sound effects and music, generated procedurally."""

    def __init__(self):
        self.enabled = True
        self.music_enabled = False
        self.sounds = {}
        self.music_playing = False
        self._init_sounds()

    def _init_sounds(self):
        """Generate all sound effects programmatically."""
        sample_rate = 44100

        # Whoosh sound — filtered noise sweep
        self.sounds['whoosh'] = self._make_whoosh(sample_rate)

        # Click sound — short beep
        self.sounds['click'] = self._make_click(sample_rate)

        # Error sound — dissonant buzz
        self.sounds['error'] = self._make_error(sample_rate)

        # Success/completion — rising arpeggio
        self.sounds['success'] = self._make_success(sample_rate)

        # Pickup sound — quick rising tone
        self.sounds['pickup'] = self._make_pickup(sample_rate)

        # Drop sound — thud
        self.sounds['drop'] = self._make_drop(sample_rate)

    def _make_whoosh(self, sr):
        """Create a whoosh sound effect."""
        duration = 0.3
        n = int(sr * duration)
        t = np.linspace(0, duration, n, dtype=np.float32)

        # Noise-like swoosh using multiple detuned sine waves
        signal = np.zeros(n, dtype=np.float32)
        for freq in [200, 350, 500, 700, 900]:
            sweep = freq * (1 + t * 2)
            signal += np.sin(2 * np.pi * sweep * t) * 0.1

        # Envelope: fade in then fade out
        env = np.sin(np.pi * t / duration)
        signal *= env * 0.3

        # Convert to int16
        signal = np.clip(signal, -1, 1)
        samples = (signal * 32767).astype(np.int16)
        # Make stereo
        stereo = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo)

    def _make_click(self, sr):
        """Create a UI click sound."""
        duration = 0.05
        n = int(sr * duration)
        t = np.linspace(0, duration, n, dtype=np.float32)

        signal = np.sin(2 * np.pi * 800 * t) * 0.4
        env = np.exp(-t * 60)
        signal *= env

        signal = np.clip(signal, -1, 1)
        samples = (signal * 32767).astype(np.int16)
        stereo = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo)

    def _make_error(self, sr):
        """Create an error/invalid move sound."""
        duration = 0.25
        n = int(sr * duration)
        t = np.linspace(0, duration, n, dtype=np.float32)

        signal = np.sin(2 * np.pi * 200 * t) * 0.3
        signal += np.sin(2 * np.pi * 250 * t) * 0.2
        env = np.exp(-t * 8)
        signal *= env

        signal = np.clip(signal, -1, 1)
        samples = (signal * 32767).astype(np.int16)
        stereo = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo)

    def _make_success(self, sr):
        """Create a success/celebration sound."""
        duration = 1.0
        n = int(sr * duration)
        t = np.linspace(0, duration, n, dtype=np.float32)

        signal = np.zeros(n, dtype=np.float32)
        # Rising arpeggio: C5, E5, G5, C6
        notes = [523.25, 659.25, 783.99, 1046.5]
        note_dur = duration / len(notes)
        for i, freq in enumerate(notes):
            start = int(i * note_dur * sr)
            end = min(n, int((i + 1) * note_dur * sr))
            seg_len = end - start
            seg_t = np.linspace(0, note_dur, seg_len, dtype=np.float32)
            seg = np.sin(2 * np.pi * freq * seg_t) * 0.3
            seg *= np.exp(-seg_t * 3)
            signal[start:end] += seg

        signal = np.clip(signal, -1, 1)
        samples = (signal * 32767).astype(np.int16)
        stereo = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo)

    def _make_pickup(self, sr):
        """Create a disk pickup sound."""
        duration = 0.12
        n = int(sr * duration)
        t = np.linspace(0, duration, n, dtype=np.float32)

        freq = 400 + t * 800  # Rising pitch
        signal = np.sin(2 * np.pi * freq * t) * 0.3
        env = np.exp(-t * 15)
        signal *= env

        signal = np.clip(signal, -1, 1)
        samples = (signal * 32767).astype(np.int16)
        stereo = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo)

    def _make_drop(self, sr):
        """Create a disk drop/land sound."""
        duration = 0.15
        n = int(sr * duration)
        t = np.linspace(0, duration, n, dtype=np.float32)

        freq = 300 - t * 200  # Falling pitch
        signal = np.sin(2 * np.pi * freq * t) * 0.4
        env = np.exp(-t * 20)
        signal *= env

        signal = np.clip(signal, -1, 1)
        samples = (signal * 32767).astype(np.int16)
        stereo = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo)

    def play(self, name):
        """Play a named sound effect."""
        if self.enabled and name in self.sounds:
            self.sounds[name].play()

    def toggle_sounds(self):
        """Toggle sound effects on/off."""
        self.enabled = not self.enabled
        return self.enabled

    def toggle_music(self):
        """Toggle background music on/off."""
        self.music_enabled = not self.music_enabled
        return self.music_enabled
