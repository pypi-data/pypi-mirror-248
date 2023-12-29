import math
from dataclasses import dataclass

DRAG_COEFFICIENT = 0.47
AIR_DENSITY = 1.206  # at 20 degrees Celsius kg/m^3
GRAVITY = 9.8101  # meters / second^2 in Katowice


@dataclass
class Displacement:
    """Displacement of the ball"""

    north: float = 0
    east: float = 0


@dataclass
class WindSpeed:
    """Wind speed in 3 axes expressed in m/s."""

    north: float = 0
    east: float = 0
    down: float = 0


class CalculateBallDisplacement:
    def __init__(self, ball_mass_kg: float, ball_radius_m: float) -> None:
        self._ball_mass_kg = ball_mass_kg
        self._ball_radius_m = ball_radius_m
        self._ball_cross_area = (ball_radius_m**2) * math.pi

    def calculate_displacement(
        self, altitude_agl_m: float, wind_speed: WindSpeed
    ) -> Displacement:
        """Calculate the displacement of the ball caused by the wind
        after dropping from a given altitude.

        Args:
            altitude_agl_m: drop altitude, re   lative to ground level.
            wind_speed: components of wind speed.
        """
        ball_drop_time = math.sqrt((altitude_agl_m * 2) / GRAVITY)

        wind_force_east = (
            0.5
            * AIR_DENSITY
            * (wind_speed.east**2)
            * DRAG_COEFFICIENT
            * self._ball_cross_area
        )
        wind_force_north = (
            0.5
            * AIR_DENSITY
            * (wind_speed.north**2)
            * DRAG_COEFFICIENT
            * self._ball_cross_area
        )

        displacement = Displacement()
        displacement.east = -(
            (wind_force_east / self._ball_mass_kg) * (ball_drop_time**2) / 2
        )
        displacement.north = -(
            (wind_force_north / self._ball_mass_kg) * (ball_drop_time**2) / 2
        )

        return displacement


if __name__ == "__main__":
    ball = CalculateBallDisplacement(ball_mass_kg=0.056, ball_radius_m=0.067)
    wind = WindSpeed(north=1, east=3, down=0)

    displacement = ball.calculate_displacement(altitude_agl_m=2, wind_speed=wind)
    print(
        f"North displacement: {(displacement.north * 100.0):.2f} cm, east displacement: {(displacement.east * 100.0):.2f} cm"
    )
