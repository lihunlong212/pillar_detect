from dataclasses import dataclass


@dataclass(frozen=True)
class LidarParams:
    """LiDAR derived parameters for pillar detection."""

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
        if pillar_diameter_m <= 0:
            raise ValueError("pillar_diameter_m must be > 0")
        if distance_m <= 0:
            raise ValueError("distance_m must be > 0")

        pillar_angular_width_deg = (pillar_diameter_m / distance_m) * 57.295779513
        estimated_hits = pillar_angular_width_deg / self.angular_resolution_deg
        return max(1, int(round(estimated_hits)))
