import sys
from pathlib import Path

# Add project root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

import polars as pl
from schemas.benchmark_case import BenchmarkCase

def verify_suite(filepath: str):
    path = Path(filepath)
    if not path.is_absolute():
        path = root_dir / filepath

    if not path.exists():
        print(f"Error: Benchmark file not found at {path}")
        sys.exit(1)

    cases = []
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line_str = line.strip()
            if not line_str:
                continue
            try:
                validated = BenchmarkCase.model_validate_json(line_str)
                cases.append(validated.model_dump())
            except Exception as e:
                print(f"Validation error at line {line_num}: {e}")
                sys.exit(1)

    df = pl.DataFrame(cases)

    print("\n==========================================")
    print(f" Benchmark Suite Health Audit: {filepath}")
    print(f" Total Trajectories Validated: {len(df)}")
    print("==========================================")

    # 1. Distribution by Category
    cat_counts = df.group_by("category_id").len().sort("category_id")
    print("\nTraversals by Category:")
    for row in cat_counts.iter_rows(named=True):
        print(f"  {row['category_id']}: {row['len']} cases")

    # 2. Distribution by Test Type
    type_counts = df.group_by("test_type").len().sort("len", descending=True)
    print("\nDistribution by Test Type:")
    for row in type_counts.iter_rows(named=True):
        pct = (row["len"] / len(df)) * 100
        print(f"  {row['test_type']}: {row['len']} cases ({pct:.1f}%)")

    # 3. Expected Actions Distribution
    action_counts = df.select(
        pl.col("evaluation_criteria").struct.field("expected_action")
    ).group_by("expected_action").len()
    print("\nExpected Actions Breakdown:")
    for row in action_counts.iter_rows(named=True):
        print(f"  {row['expected_action']}: {row['len']}")

    # 4. Turn Depth Metrics
    turn_depths = [len(c["conversation"]) for c in cases]
    avg_turns = sum(turn_depths) / len(turn_depths)
    print(f"\nAverage Turns per Trajectory: {avg_turns:.2f} turns (Min: {min(turn_depths)}, Max: {max(turn_depths)})")
    print("==========================================")

    # Formal assertions for Phase 3 gating
    assert len(df) >= 200, f"Suite must contain >= 200 cases (found {len(df)})."
    expected_cats = {f"CAT-{i:02d}" for i in range(1, 11)}
    found_cats = set(df["category_id"].unique())
    assert found_cats == expected_cats, f"Category mismatch: {expected_cats - found_cats} missing."

    print("Verdict: PASSED. Benchmark suite meets all Phase 2 criteria.\n")

if __name__ == "__main__":
    verify_suite("data/benchmark/benchmark_suite_200.jsonl")