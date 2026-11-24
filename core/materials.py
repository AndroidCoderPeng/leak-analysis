"""管材声速表：从 JSON 加载，按材料与管径匹配声速。"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VelocityEntry:
    material: str
    low: int  # 管径下限 (mm)；-1 表示上限不设限
    high: int  # 管径上限 (mm)；-1 表示上限不设限
    velocity: float


def load_velocity_table(path: str | Path) -> list[VelocityEntry]:
    """从 JSON 文件加载声速表（MaterialName / LowDiameter / HighDiameter / Velocity）。"""
    with open(path, "r", encoding="utf-8-sig") as file:
        raw = json.load(file)
    if not isinstance(raw, list):
        raise ValueError("声速表文件根节点必须为 JSON 数组")

    entries = []
    for item in raw:
        try:
            entries.append(VelocityEntry(
                material=str(item["MaterialName"]).strip(),
                low=int(item["LowDiameter"]),
                high=int(item["HighDiameter"]),
                velocity=float(item["Velocity"]),
            ))
        except (KeyError, TypeError, ValueError):
            continue
    return entries


def match_velocity(entries: list[VelocityEntry], material: str,
                   diameter: int) -> float | None:
    """按材料与管径匹配声速；找不到时返回 None。"""
    for entry in entries:
        if entry.material != material:
            continue
        if diameter >= entry.low and (entry.high < 0 or diameter <= entry.high):
            return entry.velocity
    return None


def materials(entries: list[VelocityEntry]) -> list[str]:
    """声速表中出现过的材料名（按首次出现顺序去重）。"""
    seen: list[str] = []
    for entry in entries:
        if entry.material not in seen:
            seen.append(entry.material)
    return seen
