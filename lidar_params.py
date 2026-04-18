from dataclasses import dataclass
from math import atan, degrees


@dataclass(frozen=True)
class LidarParams:
    """LiDAR derived parameters for Pillar detection.

    Args:
        angular_resolution_deg: Angular resolution in degrees (> 0).
        rotation_speed_rpm: Rotation speed in RPM (> 0).
    """

    angular_resolution_deg: float
    rotation_speed_rpm: float

    def __post_init__(self) -> None:
        if self.angular_resolution_deg <= 0:
            raise ValueError("angular_resolution_deg must be > 0")
        if self.rotation_speed_rpm <= 0:
            raise ValueError("rotation_speed_rpm must be > 0")

    @property
    def points_per_revolution(self) -> int:
        return int(round(360.0 / self.angular_resolution_deg))

    @property
    def scan_frequency_hz(self) -> float:
        return self.rotation_speed_rpm / 60.0

    @property
    def scan_period_s(self) -> float:
        return 1.0 / self.scan_frequency_hz

    def recommend_min_cluster_points(self, pillar_diameter_m: float, distance_m: float) -> int:
        """Estimate minimum points on one pillar in a single scan.

        The method estimates pillar angular width by `2 * atan((diameter / 2) / distance)`
        and
        converts it to point count using the configured angular resolution.
        """
        if pillar_diameter_m <= 0:
            raise ValueError("pillar_diameter_m must be > 0")
        if distance_m <= 0:
            raise ValueError("distance_m must be > 0")

        pillar_angular_width_deg = degrees(2.0 * atan((pillar_diameter_m / 2.0) / distance_m))
        estimated_hits = pillar_angular_width_deg / self.angular_resolution_deg
        return max(1, int(round(estimated_hits)))
