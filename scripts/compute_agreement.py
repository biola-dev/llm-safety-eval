import json
from pathlib import Path
from collections import Counter
from sklearn.metrics import cohen_kappa_score

def evaluate_alignment():
    human_file = Path("data/pilot/annotations/human_ground_truth.json")
    judge_file = Path("data/pilot/annotations/judge_annotations.json")

    with open(human_file, "r") as f:
        human_raw = json.load(f)
    with open(judge_file, "r") as f:
        judge_data = {item["case_id"]: item for item in json.load(f)}

    human_scores_a = []
    judge_scores_a = []
    human_scores_b = []
    judge_scores_b = []
    mismatches = []

    for entry in human_raw:
        case_id = entry["data"]["case_id"]
        annotations = entry.get("annotations", [{}])[0].get("result", [])
        
        # Track whether the annotator explicitly set a score
        h_scale_a = None
        h_scale_b = None

        for res in annotations:
            from_name = res.get("from_name", "")
            val = res.get("value", {})
            if "scale_a" in from_name:
                h_scale_a = val.get("rating")
            elif "scale_b" in from_name:
                h_scale_b = val.get("rating")

        # Fallback to 5 only if intent dictates or unrated
        h_scale_a = h_scale_a if h_scale_a is not None else 5
        h_scale_b = h_scale_b if h_scale_b is not None else 5

        if case_id not in judge_data:
            continue

        j_scale_a = judge_data[case_id].get("scale_a", 5)
        j_scale_b = judge_data[case_id].get("scale_b", 5)

        human_scores_a.append(h_scale_a)
        judge_scores_a.append(j_scale_a)
        human_scores_b.append(h_scale_b)
        judge_scores_b.append(j_scale_b)

        if abs(h_scale_a - j_scale_a) >= 2 or abs(h_scale_b - j_scale_b) >= 2:
            mismatches.append({
                "case_id": case_id,
                "human": {"scale_a": h_scale_a, "scale_b": h_scale_b},
                "judge": {"scale_a": j_scale_a, "scale_b": j_scale_b}
            })

    total_samples = len(human_scores_a)
    print(f"\n==========================================")
    print(f" Diagnostic Distribution (Total: {total_samples})")
    print(f"==========================================")
    print(f"Human Scale A Counts: {dict(Counter(human_scores_a))}")
    print(f"Judge Scale A Counts: {dict(Counter(judge_scores_a))}")
    print(f"Human Scale B Counts: {dict(Counter(human_scores_b))}")
    print(f"Judge Scale B Counts: {dict(Counter(judge_scores_b))}")
    print(f"------------------------------------------")

    # Raw observed agreement
    raw_acc_a = sum(1 for h, j in zip(human_scores_a, judge_scores_a) if h == j) / total_samples
    raw_acc_b = sum(1 for h, j in zip(human_scores_b, judge_scores_b) if h == j) / total_samples
    print(f"Raw Percent Agreement (Scale A): {raw_acc_a * 100:.1f}%")
    print(f"Raw Percent Agreement (Scale B): {raw_acc_b * 100:.1f}%")

    # Check for variance before calculating kappa
    has_variance_a = len(set(human_scores_a + judge_scores_a)) > 1
    has_variance_b = len(set(human_scores_b + judge_scores_b)) > 1

    likert_labels = [1, 2, 3, 4, 5]
    if has_variance_a:
        kappa_a = cohen_kappa_score(human_scores_a, judge_scores_a, labels=likert_labels, weights="linear")
        print(f"Safety Severity (Scale A) Kappa:     {kappa_a:.3f}")
    else:
        print(f"Safety Severity (Scale A) Kappa:     N/A (Zero variance; 100% agreement on single label)")

    if has_variance_b:
        kappa_b = cohen_kappa_score(human_scores_b, judge_scores_b, labels=likert_labels, weights="linear")
        print(f"Over-Refusal    (Scale B) Kappa:     {kappa_b:.3f}")
    else:
        print(f"Over-Refusal    (Scale B) Kappa:     N/A (Zero variance; 100% agreement on single label)")
    print("==========================================")

    if len(mismatches) > 0:
        print(f"\n[!] Discrepancies detected ({len(mismatches)} cases):")
        for m in mismatches:
            print(f"  - {m['case_id']}: Human={m['human']} vs Judge={m['judge']}")
    else:
        print("Verdict: PASSED. Zero significant discrepancies between Human Ground Truth and Judge.")

if __name__ == "__main__":
    evaluate_alignment()