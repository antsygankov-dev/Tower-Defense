# tower.py
# Tower class. Finds the nearest monster in range and shoots once per second.

import math
import pygame
from constants import (
    TOWER_RANGE, TOWER_DAMAGE, TOWER_FIRE_COOLDOWN_MS,
    TILE_SIZE, COLORS,
)


class Tower:
    """A tower that attacks monsters within a radius of R."""

    def __init__(self, gx, gy):
        self.gx = gx
        self.gy = gy
        self.x = gx * TILE_SIZE + TILE_SIZE // 2
        self.y = gy * TILE_SIZE + TILE_SIZE // 2
        self.range = TOWER_RANGE
        self.damage = TOWER_DAMAGE
        self.last_shot_time = -TOWER_FIRE_COOLDOWN_MS
        self.powered = False

    # --- Energy grid ---
    def set_powered(self, value):
        self.powered = value

    # --- Logic ---
    def find_target(self, monsters):
        """Returns the nearest monster within radius R, or None."""
        best = None
        best_dist = self.range
        for m in monsters:
            if not m.alive:
                continue
            d = math.hypot(m.x - self.x, m.y - self.y)
            if d < best_dist:
                best_dist = d
                best = m
        return best

    def update(self, monsters, now_ms):
        """Deals damage to the nearest monster once per cooldown."""
        if not self.powered:
            return None
        if now_ms - self.last_shot_time < TOWER_FIRE_COOLDOWN_MS:
            return None
        target = self.find_target(monsters)
        if target is None:
            return None
        self.last_shot_time = now_ms
        target.take_damage(self.damage)
        killed = not target.alive
        return {"target": target, "killed": killed}

    # --- Rendering ---
    def draw(self, surface):
        color = COLORS["tower"] if self.powered else COLORS["tower_off"]
        rect = pygame.Rect(self.gx * TILE_SIZE + 4,
                           self.gy * TILE_SIZE + 4,
                           TILE_SIZE - 8, TILE_SIZE - 8)
        pygame.draw.rect(surface, color, rect, border_radius=6)
        pygame.draw.rect(surface, (20, 20, 20), rect, 2, border_radius=6)
        dot_color = COLORS["good"] if self.powered else COLORS["danger"]
        pygame.draw.circle(surface, dot_color, (self.x, self.y), 4)

    def draw_range(self, surface, force=False):
        """Semi-transparent attack radius circle (for preview)."""
        if not self.powered and not force:
            return
        r = int(self.range)
        surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (60, 160, 220, 40), (r, r), r)
        pygame.draw.circle(surf, (60, 160, 220, 90), (r, r), r, 1)
        surface.blit(surf, (self.x - r, self.y - r))