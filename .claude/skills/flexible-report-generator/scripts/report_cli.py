#!/usr/bin/env python3
"""
Flexible Report Generator CLI

Usage:
  python report_cli.py data.json --title "Report Title" [options]

Examples:
  python report_cli.py data.json --title "Q4 Report" --purpose executive --style witty
  python report_cli.py data.json --title "Analysis" --format pdf --output report.pdf
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from report_generator import ReportGenerator


def load_data(file_path: str) -> dict:
    """Load data from JSON or CSV file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    if path.suffix == ".json":
        with open(path) as f:
            return json.load(f)
    elif path.suffix == ".csv":
        # Basic CSV to dict conversion
        import csv
        with open(path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if rows:
                return {
                    "table": {
                        "columns": list(rows[0].keys()),
                        "rows": [list(row.values()) for row in rows]
                    }
                }
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")

    return {}


def save_output(content: str | bytes, output_path: str, fmt: str) -> None:
    """Save output to file."""
    mode = "wb" if fmt == "pdf" else "w"
    with open(output_path, mode) as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(
        description="Flexible Report Generator - Create analyst-quality reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s data.json --title "Q4 Performance"
  %(prog)s data.json --title "Analysis" --purpose analyst --style formal
  %(prog)s data.json --title "Dashboard" --purpose dashboard --output report.html
  %(prog)s data.json --title "Report" --format pdf --output report.pdf
        """
    )

    parser.add_argument(
        "data",
        help="Data file (JSON or CSV format)"
    )
    parser.add_argument(
        "--title", "-t",
        required=True,
        help="Report title"
    )
    parser.add_argument(
        "--purpose", "-p",
        default="executive",
        choices=["executive", "analyst", "dashboard", "storytelling", "comparison"],
        help="Report purpose (default: executive)"
    )
    parser.add_argument(
        "--style", "-s",
        default="witty",
        choices=["witty", "formal", "storyteller", "minimalist"],
        help="Writing style (default: witty)"
    )
    parser.add_argument(
        "--output", "-o",
        default="report.html",
        help="Output file path (default: report.html)"
    )
    parser.add_argument(
        "--format", "-f",
        default="html",
        choices=["html", "pdf"],
        help="Output format (default: html)"
    )

    args = parser.parse_args()

    try:
        # Load data
        print(f"Loading data from: {args.data}")
        data = load_data(args.data)

        # Generate report
        print(f"Generating {args.format.upper()} report...")
        print(f"  Purpose: {args.purpose}")
        print(f"  Style: {args.style}")

        generator = ReportGenerator()
        output = generator.generate(
            data=data,
            title=args.title,
            purpose=args.purpose,
            style=args.style,
            output_format=args.format
        )

        # Save output
        save_output(output, args.output, args.format)
        print(f"Report saved to: {args.output}")

        # Print stats
        if args.format == "html":
            print(f"  Size: {len(output):,} bytes")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error generating report: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
