# pillar_detect
激光雷达寻找柱子以及定位。

## 基于雷达精度与转速的参数计算
新增 `lidar_params.py`，可根据：
- `angular_resolution_deg`（角分辨率/精度）
- `rotation_speed_rpm`（转速）

自动计算：
- 每圈点数 `points_per_revolution`
- 扫描频率 `scan_frequency_hz`
- 扫描周期 `scan_period_s`
- 柱体最小聚类点数建议 `recommend_min_cluster_points(...)`

示例：

```python
from lidar_params import LidarParams

params = LidarParams(angular_resolution_deg=0.5, rotation_speed_rpm=600)
print(params.points_per_revolution)  # 720
print(params.scan_frequency_hz)      # 10.0
print(params.scan_period_s)          # 0.1
```
