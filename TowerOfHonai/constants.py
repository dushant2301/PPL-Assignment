"""
Constants and configuration for Tower of Hanoi Visual Simulator.
"""

# =============================================================================
# WINDOW SETTINGS
# =============================================================================
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 850
FPS = 60
TITLE = "Tower of Hanoi — Dushant Sewatkar CS25D006"

# =============================================================================
# COLOR PALETTE — Futuristic Neon Theme
# =============================================================================
# Base Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BG = (8, 10, 22)
DARK_BG_2 = (12, 15, 30)
PANEL_BG = (15, 18, 35, 180)

# Neon Colors
NEON_CYAN = (0, 255, 255)
NEON_PINK = (255, 0, 200)
NEON_PURPLE = (160, 50, 255)
NEON_GREEN = (0, 255, 128)
NEON_BLUE = (50, 130, 255)
NEON_ORANGE = (255, 160, 30)
NEON_YELLOW = (255, 255, 50)
NEON_RED = (255, 50, 80)

# Disk gradient palette (from smallest to largest)
DISK_COLORS = [
    (0, 255, 255),      # Cyan
    (0, 200, 255),      # Sky Blue
    (80, 120, 255),     # Royal Blue
    (160, 50, 255),     # Purple
    (255, 0, 200),      # Pink
    (255, 50, 80),      # Red
    (255, 120, 30),     # Orange
    (255, 200, 0),      # Gold
    (0, 255, 128),      # Green
    (100, 255, 50),     # Lime
    (255, 255, 50),     # Yellow
    (50, 255, 200),     # Teal
]

# UI Colors
UI_TEXT = (200, 210, 230)
UI_TEXT_DIM = (100, 110, 130)
UI_ACCENT = (0, 200, 255)
UI_BORDER = (40, 50, 80)
UI_HIGHLIGHT = (60, 70, 110)

# =============================================================================
# TOWER LAYOUT
# =============================================================================
TOWER_POSITIONS = [
    SCREEN_WIDTH // 4,           # Left tower
    SCREEN_WIDTH // 2,           # Center tower
    3 * SCREEN_WIDTH // 4,       # Right tower
]
TOWER_BASE_Y = 620
TOWER_HEIGHT = 340
TOWER_WIDTH = 8
TOWER_BASE_WIDTH = 250
TOWER_BASE_HEIGHT = 10

# =============================================================================
# DISK SETTINGS
# =============================================================================
MIN_DISK_WIDTH = 50
MAX_DISK_WIDTH = 210
DISK_HEIGHT = 32
DISK_CORNER_RADIUS = 10
DISK_GAP = 4
DEFAULT_DISK_COUNT = 5
MIN_DISKS = 1
MAX_DISKS = 10

# =============================================================================
# ANIMATION SETTINGS
# =============================================================================
LIFT_HEIGHT = 100          # How high disks lift before moving
ANIM_SPEED_SLOW = 0.3
ANIM_SPEED_NORMAL = 1.0
ANIM_SPEED_FAST = 2.5
ANIM_SPEED_ULTRA = 6.0

# Particle settings
PARTICLE_COUNT = 15
PARTICLE_LIFETIME = 0.8
PARTICLE_SPEED = 120

# Trail settings
TRAIL_LENGTH = 12
TRAIL_FADE_RATE = 0.85

# Glow settings
GLOW_RADIUS = 15
GLOW_INTENSITY = 80
GLOW_PULSE_SPEED = 4.0

# Bounce physics
BOUNCE_DAMPING = 0.4
BOUNCE_THRESHOLD = 2.0

# =============================================================================
# UI LAYOUT
# =============================================================================
BUTTON_WIDTH = 130
BUTTON_HEIGHT = 42
BUTTON_RADIUS = 10
BUTTON_GAP = 12

# Top panel
TOP_PANEL_HEIGHT = 75
TOP_PANEL_MARGIN = 15

# Bottom controls
BOTTOM_PANEL_Y = 700
BOTTOM_PANEL_HEIGHT = 130

# Speed labels
SPEED_LABELS = ["Slow", "Normal", "Fast", "Ultra"]
SPEED_VALUES = [ANIM_SPEED_SLOW, ANIM_SPEED_NORMAL, ANIM_SPEED_FAST, ANIM_SPEED_ULTRA]

# =============================================================================
# KEYBOARD SHORTCUTS
# =============================================================================
# Defined in event handler, documented here for reference:
# SPACE   - Start / Pause / Resume
# R       - Reset
# N       - Next move (step mode)
# S       - Toggle auto-solve
# 1-4     - Speed settings
# UP/DOWN - Adjust disk count
# M       - Toggle music
# ESC     - Quit
