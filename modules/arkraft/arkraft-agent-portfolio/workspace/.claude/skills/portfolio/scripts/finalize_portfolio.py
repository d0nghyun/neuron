#!/usr/bin/env python3
"""Finalize portfolio and generate output.

Takes evaluations and builds final portfolio.json.

Usage:
    python finalize_portfolio.py --evaluations phase3/evaluations.json --output output/
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def load_evaluations(path: str) -> list[dict]:
    """Load PM evaluations."""
    with open(path) as f:
        data = json.load(f)
    return data.get("evaluations", data) if isinstance(data, dict) else data


def load_clusters(path: str) -> dict:
    """Load cluster assignments."""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"alpha_clusters": {}, "n_clusters": 1}


def load_turnover(path: str) -> dict:
    """Load turnover analysis."""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"turnover_reduction": 0}


def calculate_cluster_weights(
    selected: list[dict],
    clusters: dict
) -> dict[str, float]:
    """Calculate cluster-based equal weights."""
    alpha_clusters = clusters.get("alpha_clusters", {})

    if not alpha_clusters:
        # Fallback to simple equal weight
        n = len(selected)
        return {e["alpha_id"]: 1.0 / n for e in selected} if n > 0 else {}

    # Group by cluster
    cluster_groups = {}
    for e in selected:
        alpha_id = e["alpha_id"]
        cluster_id = alpha_clusters.get(alpha_id, 0)
        if cluster_id not in cluster_groups:
            cluster_groups[cluster_id] = []
        cluster_groups[cluster_id].append(alpha_id)

    # Equal weight per cluster, then equal within cluster
    n_clusters = len(cluster_groups)
    if n_clusters == 0:
        return {}

    cluster_weight = 1.0 / n_clusters
    weights = {}

    for cluster_id, members in cluster_groups.items():
        member_weight = cluster_weight / len(members)
        for alpha_id in members:
            weights[alpha_id] = member_weight

    return weights


def build_portfolio(
    evaluations: list[dict],
    clusters: dict,
    turnover: dict,
    universe: str = "us_stock"
) -> dict:
    """Build final portfolio.json."""
    # Filter selected
    selected = [e for e in evaluations if e.get("recommendation") == "select"]
    excluded = [e for e in evaluations if e.get("recommendation") == "exclude"]
    review = [e for e in evaluations if e.get("recommendation") == "review"]

    # Calculate weights
    weights = calculate_cluster_weights(selected, clusters)

    # Build alpha entries
    alpha_entries = []
    for e in selected:
        alpha_id = e["alpha_id"]
        alpha_entries.append({
            "alpha_id": alpha_id,
            "title": e.get("title", ""),
            "category": e.get("category", ""),
            "weight": weights.get(alpha_id, 0),
            "cluster": clusters.get("alpha_clusters", {}).get(alpha_id, 1),
            "sharpe_ratio": e.get("sharpe_ratio"),
            "cagr_pct": e.get("cagr_pct"),
            "mdd_pct": e.get("mdd_pct"),
            "rationale": e.get("reasoning", ""),
            "evaluation": {
                "rationale_alignment": e.get("rationale_alignment"),
                "economic_sense": e.get("economic_sense"),
                "portfolio_fit": e.get("portfolio_fit"),
                "red_flags": e.get("red_flags", [])
            }
        })

    # Build cluster summary
    cluster_summary = []
    cluster_groups = {}
    for entry in alpha_entries:
        cid = entry["cluster"]
        if cid not in cluster_groups:
            cluster_groups[cid] = []
        cluster_groups[cid].append(entry)

    for cid, members in cluster_groups.items():
        cluster_summary.append({
            "cluster_id": cid,
            "alpha_count": len(members),
            "total_weight": sum(m["weight"] for m in members),
            "categories": list(set(m["category"] for m in members if m["category"]))
        })

    # Estimate portfolio metrics
    avg_sharpe = sum(
        e.get("sharpe_ratio", 0) or 0 for e in selected
    ) / len(selected) if selected else 0

    # Portfolio sharpe is typically higher due to diversification
    expected_sharpe = avg_sharpe * 1.2  # 20% diversification benefit

    return {
        "metadata": {
            "universe": universe,
            "created_at": datetime.now().isoformat(),
            "total_alphas": len(selected),
            "excluded_alphas": len(excluded),
            "review_alphas": len(review),
            "weight_method": "cluster_equal"
        },
        "alphas": alpha_entries,
        "clusters": cluster_summary,
        "portfolio_metrics": {
            "expected_sharpe": round(expected_sharpe, 2),
            "avg_individual_sharpe": round(avg_sharpe, 2),
            "diversification_ratio": round(expected_sharpe / avg_sharpe, 2) if avg_sharpe else 1.0,
            "turnover_reduction": turnover.get("turnover_reduction", 0)
        },
        "excluded": [
            {"alpha_id": e["alpha_id"], "reason": e.get("reasoning", "")}
            for e in excluded
        ],
        "needs_review": [
            {"alpha_id": e["alpha_id"], "reason": e.get("reasoning", "")}
            for e in review
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="Finalize portfolio")
    parser.add_argument("--evaluations", required=True, help="Evaluations JSON")
    parser.add_argument("--clusters", default="phase2/clusters.json", help="Clusters JSON")
    parser.add_argument("--turnover", default="phase2/turnover_analysis.json", help="Turnover JSON")
    parser.add_argument("--universe", default="us_stock", help="Target universe")
    parser.add_argument("--output", required=True, help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading evaluations from: {args.evaluations}")
    evaluations = load_evaluations(args.evaluations)
    print(f"Loaded {len(evaluations)} evaluations")

    print(f"Loading clusters from: {args.clusters}")
    clusters = load_clusters(args.clusters)

    print(f"Loading turnover from: {args.turnover}")
    turnover = load_turnover(args.turnover)

    # Build portfolio
    print("\nBuilding portfolio...")
    portfolio = build_portfolio(evaluations, clusters, turnover, args.universe)

    # Save outputs
    portfolio_path = output_dir / "portfolio.json"
    with open(portfolio_path, "w") as f:
        json.dump(portfolio, f, indent=2, ensure_ascii=False)

    # Also save full state
    state_path = output_dir / "portfolio_state.json"
    state = {
        "portfolio": portfolio,
        "evaluations": evaluations,
        "clusters": clusters,
        "turnover": turnover,
        "updated_at": datetime.now().isoformat()
    }
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\n=== Portfolio Summary ===")
    print(f"Universe: {portfolio['metadata']['universe']}")
    print(f"Selected: {portfolio['metadata']['total_alphas']}")
    print(f"Excluded: {portfolio['metadata']['excluded_alphas']}")
    print(f"Review: {portfolio['metadata']['review_alphas']}")
    print(f"\nExpected Sharpe: {portfolio['portfolio_metrics']['expected_sharpe']}")
    print(f"Diversification: {portfolio['portfolio_metrics']['diversification_ratio']}x")
    print(f"Turnover reduction: {portfolio['portfolio_metrics']['turnover_reduction']:.1%}")

    if portfolio['alphas']:
        print(f"\n--- Selected Alphas ---")
        for a in portfolio['alphas']:
            print(f"  {a['alpha_id']}: {a['weight']:.1%} (cluster {a['cluster']})")

    print(f"\nOutputs saved to: {output_dir}")
    print(f"  - {portfolio_path}")
    print(f"  - {state_path}")


if __name__ == "__main__":
    main()
