"""Config file merger — merge multiple config files with conflict resolution."""
from __future__ import annotations
import copy
from dataclasses import dataclass, field

@dataclass
class MergeConflict:
    key: str; source_a: str; source_b: str; value_a: object = None; value_b: object = None; resolution: str = ""

@dataclass
class MergeResult:
    merged: dict = field(default_factory=dict); conflicts: list[MergeConflict] = field(default_factory=list)
    total_keys: int = 0; conflict_count: int = 0; strategy: str = ""
    def to_dict(self) -> dict: return {"total_keys": self.total_keys, "conflicts": self.conflict_count, "strategy": self.strategy}

def deep_merge(base: dict, override: dict, path: str = "", strategy: str = "override") -> tuple[dict, list[MergeConflict]]:
    result, conflicts = copy.deepcopy(base), []
    for key, value in override.items():
        full_key = f"{path}.{key}" if path else key
        if key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                result[key], sc = deep_merge(result[key], value, full_key, strategy)
                conflicts.extend(sc)
            elif isinstance(result[key], list) and isinstance(value, list):
                if strategy == "append": result[key] = result[key] + value
                elif strategy == "unique": result[key] = list(set(result[key] + value))
                else:
                    conflicts.append(MergeConflict(key=full_key, source_a="base", source_b="override", value_a=result[key], value_b=value, resolution="use_b"))
                    result[key] = value
            else:
                if result[key] != value:
                    conflicts.append(MergeConflict(key=full_key, source_a="base", source_b="override", value_a=result[key], value_b=value, resolution="use_b"))
                result[key] = value
        else: result[key] = value
    return result, conflicts

def merge_configs(configs: list[dict], strategy: str = "override") -> MergeResult:
    if not configs: return MergeResult()
    r = MergeResult(strategy=strategy)
    merged, all_conflicts = configs[0], []
    for i in range(1, len(configs)):
        merged, conflicts = deep_merge(merged, configs[i], strategy=strategy)
        all_conflicts.extend(conflicts)
    r.merged, r.conflicts, r.conflict_count, r.total_keys = merged, all_conflicts, len(all_conflicts), count_keys(merged)
    return r

def count_keys(d: dict) -> int:
    count = 0
    for k, v in d.items():
        count += 1
        if isinstance(v, dict): count += count_keys(v)
    return count

def diff_configs(a: dict, b: dict) -> list[str]:
    diffs = []
    for key in sorted(set(a.keys()) | set(b.keys())):
        if key not in a: diffs.append(f"+ {key}: {b[key]}")
        elif key not in b: diffs.append(f"- {key}: {a[key]}")
        elif a[key] != b[key]: diffs.append(f"~ {key}: {a[key]} → {b[key]}")
    return diffs

def format_result_markdown(r: MergeResult) -> str:
    emoji = "✅" if r.conflict_count == 0 else "⚠️"
    lines = [f"## Config Merge {emoji}", f"**Keys:** {r.total_keys} | **Conflicts:** {r.conflict_count} | **Strategy:** {r.strategy}", ""]
    if r.conflicts:
        lines.append("### Conflicts")
        for c in r.conflicts: lines.append(f"- `{c.key}`: {c.value_a} → {c.value_b} (resolved: {c.resolution})")
    else: lines.append("✅ No conflicts!")
    return "\n".join(lines)
