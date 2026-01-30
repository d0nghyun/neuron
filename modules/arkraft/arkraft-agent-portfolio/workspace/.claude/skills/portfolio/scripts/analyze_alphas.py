#!/usr/bin/env python3
"""Analyze alphas for portfolio construction.

Computes correlations, turnover analysis, and clustering.

Usage:
    python analyze_alphas.py --input phase1/context.json --output phase2/
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def load_context(path: str) -> list[dict]:
    """Load alpha context from JSON."""
    with open(path) as f:
        data = json.load(f)

    # Handle both list and dict with 'alphas' key
    if isinstance(data, list):
        return data
    return data.get("alphas", [])


def compute_mock_correlation(alphas: list[dict]) -> dict:
    """Compute mock correlation matrix (placeholder).

    In production, this would use actual return data.
    """
    n = len(alphas)
    alpha_ids = [a.get("alpha_id", a.get("id", f"alpha_{i}")) for i, a in enumerate(alphas)]

    # Mock correlation: same category = high corr, different = low
    matrix = {}
    for i, id1 in enumerate(alpha_ids):
        matrix[id1] = {}
        cat1 = alphas[i].get("category", "")
        for j, id2 in enumerate(alpha_ids):
            if i == j:
                matrix[id1][id2] = 1.0
            else:
                cat2 = alphas[j].get("category", "")
                # Same category: 0.5-0.8, different: 0.1-0.4
                if cat1 == cat2 and cat1:
                    matrix[id1][id2] = 0.6
                else:
                    matrix[id1][id2] = 0.2

    return {
        "alpha_ids": alpha_ids,
        "matrix": matrix
    }


def compute_turnover_analysis(alphas: list[dict]) -> dict:
    """Analyze turnover reduction from combining alphas."""
    # Extract turnover values (mock if not available)
    turnovers = []
    for a in alphas:
        metrics = a.get("metrics", {})
        turnover = metrics.get("turnover", 500)  # Default mock value
        turnovers.append(turnover)

    individual_sum = sum(turnovers)
    # Combined turnover is typically 40-70% of sum due to position offsetting
    combined = individual_sum * 0.5  # Mock: 50% reduction
    reduction = 1 - (combined / individual_sum) if individual_sum > 0 else 0

    return {
        "individual_turnovers": {
            alphas[i].get("alpha_id", f"alpha_{i}"): t
            for i, t in enumerate(turnovers)
        },
        "individual_sum": individual_sum,
        "combined_estimate": combined,
        "turnover_reduction": reduction,
        "interpretation": (
            "strong" if reduction > 0.3 else
            "moderate" if reduction > 0.1 else
            "weak"
        )
    }


def compute_clusters(alphas: list[dict], correlation: dict) -> dict:
    """Assign alphas to clusters based on correlation."""
    alpha_ids = correlation["alpha_ids"]
    matrix = correlation["matrix"]

    # Simple greedy clustering (threshold = 0.5)
    threshold = 0.5
    clusters = {}
    cluster_id = 0
    assigned = set()

    for id1 in alpha_ids:
        if id1 in assigned:
            continue

        # Start new cluster
        cluster_id += 1
        cluster_members = [id1]
        assigned.add(id1)

        # Find similar alphas
        for id2 in alpha_ids:
            if id2 in assigned:
                continue
            if matrix.get(id1, {}).get(id2, 0) >= threshold:
                cluster_members.append(id2)
                assigned.add(id2)

        clusters[cluster_id] = cluster_members

    # Build alpha -> cluster mapping
    alpha_clusters = {}
    for cid, members in clusters.items():
        for alpha_id in members:
            alpha_clusters[alpha_id] = cid

    return {
        "clusters": clusters,
        "alpha_clusters": alpha_clusters,
        "n_clusters": len(clusters),
        "threshold": threshold
    }


def generate_analysis_summary(
    alphas: list[dict],
    correlation: dict,
    turnover: dict,
    clusters: dict
) -> dict:
    """Generate summary analysis."""
    return {
        "timestamp": datetime.now().isoformat(),
        "n_alphas": len(alphas),
        "n_clusters": clusters["n_clusters"],
        "avg_correlation": 0.4,  # Mock
        "turnover_reduction": turnover["turnover_reduction"],
        "turnover_interpretation": turnover["interpretation"],
        "categories": list(set(a.get("category", "") for a in alphas if a.get("category"))),
        "recommendations": [
            "Use cluster-based weighting for factor diversity",
            f"Turnover reduction is {turnover['interpretation']} - "
            f"{'high-turnover alphas add value' if turnover['interpretation'] == 'strong' else 'consider turnover in evaluation'}"
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze alphas for portfolio")
    parser.add_argument("--input", required=True, help="Input context JSON")
    parser.add_argument("--output", required=True, help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading context from: {args.input}")
    alphas = load_context(args.input)
    print(f"Loaded {len(alphas)} alphas")

    if not alphas:
        print("No alphas to analyze!")
        return

    # Compute analyses
    print("\nComputing correlation matrix...")
    correlation = compute_mock_correlation(alphas)

    print("Computing turnover analysis...")
    turnover = compute_turnover_analysis(alphas)

    print("Computing clusters...")
    clusters = compute_clusters(alphas, correlation)

    print("Generating summary...")
    summary = generate_analysis_summary(alphas, correlation, turnover, clusters)

    # Save outputs
    with open(output_dir / "correlation.json", "w") as f:
        json.dump(correlation, f, indent=2)

    with open(output_dir / "turnover_analysis.json", "w") as f:
        json.dump(turnover, f, indent=2)

    with open(output_dir / "clusters.json", "w") as f:
        json.dump(clusters, f, indent=2)

    with open(output_dir / "analysis.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n=== Analysis Summary ===")
    print(f"Alphas: {summary['n_alphas']}")
    print(f"Clusters: {summary['n_clusters']}")
    print(f"Turnover reduction: {summary['turnover_reduction']:.1%} ({summary['turnover_interpretation']})")
    print(f"\nOutputs saved to: {output_dir}")


if __name__ == "__main__":
    main()
