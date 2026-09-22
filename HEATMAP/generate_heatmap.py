#!/usr/bin/env python3
"""
scripts/generate_heatmap.py
===========================
Generates a GitHub-compatible contribution heatmap SVG inspired by GitHub and LeetCode,
based on the exact date metadata embedded in all HackerRank solution files.

Features:
- Pure Python 3 standard library (no external dependencies).
- Scans PYTHON/, CPP/, and '30 DAYS OF CODE/' directories.
- Strictly parses dates from source comments (e.g. #DD/MM/YYYY or //DD/MM/YYYY).
- Never guesses dates or relies on filesystem timestamps.
- Renders an elegant GitHub-Dark themed SVG with green intensity levels.
- Renders an aesthetic fire indicator (🔥) on days with > 5 solved problems.
- Embeds native SVG <title> tooltips for interactive date inspection on GitHub.
- Produces assets/contribution_heatmap.svg ready for README.md.

Usage:
    python scripts/generate_heatmap.py
"""

import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
import xml.sax.saxutils as saxutils

# Reconfigure stdout/stderr for Windows UTF-8 compatibility
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# Base paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
HEATMAP_DIR = SCRIPT_DIR
OUTPUT_SVG = os.path.join(HEATMAP_DIR, "contribution_heatmap.svg")


SOLUTION_DIRS = ["PYTHON", "CPP", "30 DAYS OF CODE"]
VALID_EXTENSIONS = {".py", ".cpp"}

# Color palette (GitHub Dark theme)
COLOR_BG = "#0d1117"
COLOR_BORDER = "#30363d"
COLOR_TEXT_PRIMARY = "#f0f6fc"
COLOR_TEXT_MUTED = "#8b949e"
COLOR_TEXT_DIM = "#484f58"

# Shading levels: 0, 1, 2, 3-4, 5
LEVEL_COLORS = {
    0: ("#161b22", "#21262d"),       # 0 problems (empty cell, border)
    1: ("#0e4429", "#006d32"),       # 1 problem
    2: ("#006d32", "#26a641"),       # 2 problems
    3: ("#26a641", "#39d353"),       # 3-4 problems
    4: ("#39d353", "#56ff77"),       # 5 problems
}

FIRE_BG = "#4a1212"
FIRE_BORDER = "#f85149"


def parse_solution_file(filepath):
    """
    Extracts the solving date string from the top 10 lines of a solution file.
    Matches #DD/MM/YYYY, //DD/MM/YYYY, # DATE: DD/MM/YYYY, etc.
    Returns (parsed_date_iso, raw_date_str) or (None, error_reason).
    """
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = [f.readline() for _ in range(10)]

    found_str = None
    for line in lines:
        raw = line.strip()
        if raw.startswith("//"):
            raw = raw[2:].strip()
        elif raw.startswith("#"):
            raw = raw[1:].strip()
        else:
            continue

        # Check for DATE: or DATE prefix
        if raw.upper().startswith("DATE:"):
            raw = raw[5:].strip()
        elif raw.upper().startswith("DATE"):
            raw = raw[4:].strip()

        m = re.match(r"^(\d{1,4}[-/. ]\d{1,2}[-/. ]\d{2,4})", raw)
        if m:
            found_str = m.group(1).strip()
            break

    if not found_str:
        return None, "No date header found"

    # Attempt parsing with standard formats
    for fmt in ["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%Y/%m/%d"]:
        try:
            dt = datetime.strptime(found_str, fmt).date()
            return dt, found_str
        except ValueError:
            pass

    return None, f"Malformed date string: '{found_str}'"


def collect_repository_data(root_dir):
    """
    Scans all solution files across target directories and compiles metrics.
    """
    date_counts = Counter()
    files_by_date = defaultdict(list)
    missing_date_files = []
    malformed_date_files = []
    total_files = 0

    language_counts = Counter()

    for d in SOLUTION_DIRS:
        target_dir = os.path.join(root_dir, d)
        if not os.path.isdir(target_dir):
            continue

        for fname in sorted(os.listdir(target_dir)):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in VALID_EXTENSIONS:
                continue

            total_files += 1
            fpath = os.path.join(target_dir, fname)
            rel_path = os.path.relpath(fpath, root_dir)

            if ext == ".py":
                language_counts["Python"] += 1
            elif ext == ".cpp":
                language_counts["C++"] += 1

            dt, raw_val = parse_solution_file(fpath)
            if dt is None:
                if "Malformed" in raw_val:
                    malformed_date_files.append((rel_path, raw_val))
                else:
                    missing_date_files.append((rel_path, raw_val))
            else:
                date_counts[dt] += 1
                files_by_date[dt].append(rel_path)

    return {
        "total_files": total_files,
        "date_counts": date_counts,
        "files_by_date": files_by_date,
        "missing_date_files": missing_date_files,
        "malformed_date_files": malformed_date_files,
        "language_counts": language_counts,
    }


def compute_streaks(date_counts):
    """
    Computes current streak, longest streak, and max daily solved.
    """
    if not date_counts:
        return 0, 0, 0

    sorted_dates = sorted(date_counts.keys())
    date_set = set(sorted_dates)

    # Max single-day solve count
    max_in_day = max(date_counts.values())

    # Longest streak
    longest_streak = 0
    curr_streak = 0
    prev_date = None

    for d in sorted_dates:
        if prev_date is None or d == prev_date + timedelta(days=1):
            curr_streak += 1
        else:
            curr_streak = 1
        longest_streak = max(longest_streak, curr_streak)
        prev_date = d

    # Active streak up to latest activity date
    latest_date = sorted_dates[-1]
    streak_tail = 0
    check_date = latest_date
    while check_date in date_set:
        streak_tail += 1
        check_date -= timedelta(days=1)

    return streak_tail, longest_streak, max_in_day


def get_level(count):
    """
    Maps daily solved problem count to a heatmap intensity level (0 to 4),
    or returns 'FIRE' if count > 5.
    """
    if count == 0:
        return 0
    elif count == 1:
        return 1
    elif count == 2:
        return 2
    elif 3 <= count <= 4:
        return 3
    elif count == 5:
        return 4
    else:
        return "FIRE"


def generate_svg(data, output_path):
    """
    Builds the high-resolution, responsive GitHub-compatible SVG heatmap card.
    """
    date_counts = data["date_counts"]
    total_solved = data["total_files"]
    active_days = len(date_counts)

    curr_streak, longest_streak, max_in_day = compute_streaks(date_counts)
    fire_days = [d for d, c in date_counts.items() if c > 5]
    total_fire_days = len(fire_days)

    # Determine calendar grid bounds: July 2026 through July 2027 (57 weeks)
    # The week containing July 1, 2026 starts on Sunday, June 28, 2026.
    cal_start = date(2026, 6, 28)
    num_weeks = 57  # 57 weeks spans from June 28, 2026 through July 31, 2027

    # Grid parameters
    cell_size = 11
    cell_gap = 3
    cell_step = cell_size + cell_gap  # 14px
    corner_radius = 2.5

    grid_x = 52
    grid_y = 92

    width = 880
    height = 260

    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="100%" height="{height}" '
        'style="background-color: transparent; font-family: \'Helvetica\', Arial, sans-serif;">'
    )


    # SVG Definitions & Gradients
    svg.append("  <defs>")
    svg.append(
        '    <linearGradient id="fireGrad" x1="0%" y1="100%" x2="0%" y2="0%">'
        '<stop offset="0%" stop-color="#ff3b30"/>'
        '<stop offset="45%" stop-color="#ff9500"/>'
        '<stop offset="100%" stop-color="#ffd60a"/>'
        "</linearGradient>"
    )
    svg.append(
        '    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">'
        '<feGaussianBlur stdDeviation="1.5" result="blur"/>'
        '<feComposite in="SourceGraphic" in2="blur" operator="over"/>'
        "</filter>"
    )
    svg.append(
        "    <style>"
        "      * { font-family: 'Helvetica', Arial, sans-serif; }"
        "      text { font-family: 'Helvetica', Arial, sans-serif; }"
        "      .cell { cursor: pointer; }"
        "      .cell:hover rect { stroke: #f0f6fc !important; stroke-width: 1.2px !important; }"
        "    </style>"
    )
    svg.append("  </defs>")

    # Background Card
    svg.append(
        f'  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" '
        f'fill="{COLOR_BG}" stroke="{COLOR_BORDER}" stroke-width="1"/>'
    )

    # Header Title
    svg.append(
        '  <text x="32" y="38" fill="#f0f6fc" font-size="16" font-weight="600">'
        "HackerRank Contribution Activity"
        "</text>"
    )
    svg.append(
        f'  <text x="32" y="56" fill="{COLOR_TEXT_MUTED}" font-size="12">'
        "Contributions &amp; Problem Solving Calendar • July 2026 – July 2027"
        "</text>"
    )


    # Stats Badges / Pills on top right
    badges = [
        (f"{total_solved} Solved", "#388bfd", "#1f6feb", "#0d1d30"),
        (f"{active_days} Active Days", "#3fb950", "#238636", "#0c2114"),
        (f"🔥 {total_fire_days} Fire Days", "#ff7b72", "#da3633", "#2c1012"),
        (f"Max {max_in_day}/Day", "#d29922", "#9e6a03", "#221a08"),
    ]

    badge_x = width - 32
    for label, text_color, stroke_color, bg_color in reversed(badges):
        # Approximate width based on character count
        b_width = len(label) * 7.5 + 18
        badge_x -= b_width
        svg.append(
            f'  <g transform="translate({badge_x}, 24)">'
            f'<rect width="{b_width}" height="24" rx="12" fill="{bg_color}" stroke="{stroke_color}" stroke-width="0.8"/>'
            f'<text x="{b_width / 2}" y="16" text-anchor="middle" fill="{text_color}" font-size="11" font-weight="600">{label}</text>'
            "</g>"
        )
        badge_x -= 8

    # Month Labels across top of grid
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    rendered_months = set()

    for col in range(num_weeks):
        week_start = cal_start + timedelta(days=col * 7)
        # Check if 1st of any month falls in this week
        for d_offset in range(7):
            cur_d = week_start + timedelta(days=d_offset)
            m_key = (cur_d.year, cur_d.month)
            if cur_d.day == 1 and m_key not in rendered_months:
                rendered_months.add(m_key)
                m_label = month_names[cur_d.month - 1]
                label_x = grid_x + col * cell_step
                svg.append(
                    f'  <text x="{label_x}" y="{grid_y - 10}" fill="{COLOR_TEXT_MUTED}" '
                    f'font-size="11" font-weight="500">{m_label}</text>'
                )
                break

    # Day-of-week labels (Mon, Wed, Fri) on the left
    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    for row_idx, label in day_labels:
        label_y = grid_y + row_idx * cell_step + 10
        svg.append(
            f'  <text x="{grid_x - 12}" y="{label_y}" text-anchor="end" '
            f'fill="{COLOR_TEXT_DIM}" font-size="10" font-weight="400">{label}</text>'
        )

    # Calendar Cells
    for col in range(num_weeks):
        for row in range(7):
            cell_date = cal_start + timedelta(days=col * 7 + row)
            cnt = date_counts.get(cell_date, 0)
            lvl = get_level(cnt)

            x = grid_x + col * cell_step
            y = grid_y + row * cell_step

            # Tooltip format: "DD/MM/YY : 1 commit" or "DD/MM/YY : X commits", and for 0 commits: "DD/MM/YY"
            short_date = cell_date.strftime("%d/%m/%y")
            if cnt == 0:
                tooltip = short_date
            elif cnt == 1:
                tooltip = f"{short_date} : 1 commit"
            else:
                tooltip = f"{short_date} : {cnt} commits"
            safe_tooltip = saxutils.escape(tooltip)

            if lvl == "FIRE":
                svg.append(f'  <g class="cell" tabindex="0">')
                svg.append(f"    <title>{safe_tooltip}</title>")
                # Background cell with ember red fill
                svg.append(
                    f'    <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="{corner_radius}" '
                    f'fill="{FIRE_BG}" stroke="{FIRE_BORDER}" stroke-width="0.9"/>'
                )
                # Flame vector icon centered in 11x11 cell
                flame_path = (
                    "M6 0.8C5.8 1.4 5.3 2.1 4.7 2.7C3.9 3.5 3.1 4.5 3.1 5.9C3.1 7.7 4.4 8.9 6 8.9"
                    "C7.6 8.9 8.9 7.7 8.9 5.9C8.9 4.3 7.9 3.2 7.3 2.5C7.2 3.4 6.5 4.1 5.7 4.1"
                    "C5.2 4.1 4.9 3.7 5.0 3.1C5.1 2.4 5.7 1.6 6 0.8Z"
                )
                svg.append(
                    f'    <path d="{flame_path}" fill="url(#fireGrad)" '
                    f'transform="translate({x - 0.8:.2f}, {y + 0.4:.2f}) scale(1.05)"/>'
                )
                svg.append("  </g>")

            else:
                fill_col, stroke_col = LEVEL_COLORS[lvl]
                svg.append(f'  <g class="cell" tabindex="0">')
                svg.append(f"    <title>{safe_tooltip}</title>")
                svg.append(
                    f'    <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="{corner_radius}" '
                    f'fill="{fill_col}" stroke="{stroke_col}" stroke-width="0.5"/>'
                )
                svg.append("  </g>")


    # Legend at bottom
    legend_y = grid_y + 7 * cell_step + 18

    # Left legend note: explains fire condition
    svg.append(
        f'  <text x="32" y="{legend_y + 10}" fill="{COLOR_TEXT_MUTED}" font-size="11">'
        f'<tspan fill="#ff7b72" font-weight="600">🔥 Fire Day</tspan>: Days with &gt; 5 problems solved '
        f'(Personal Record: {max_in_day} in one day)'
        "</text>"
    )

    # Right legend: Less [0] [1] [2] [3-4] [5] [🔥] More
    leg_x = width - 265
    svg.append(
        f'  <text x="{leg_x}" y="{legend_y + 10}" fill="{COLOR_TEXT_DIM}" font-size="11" text-anchor="end">Less</text>'
    )
    leg_x += 8

    # Standard levels 0, 1, 2, 3, 4
    for lvl_idx in range(5):
        f_c, s_c = LEVEL_COLORS[lvl_idx]
        svg.append(
            f'  <rect x="{leg_x}" y="{legend_y}" width="11" height="11" rx="2" '
            f'fill="{f_c}" stroke="{s_c}" stroke-width="0.5"/>'
        )
        leg_x += 15

    # Fire level in legend
    svg.append(
        f'  <rect x="{leg_x}" y="{legend_y}" width="11" height="11" rx="2" '
        f'fill="{FIRE_BG}" stroke="{FIRE_BORDER}" stroke-width="0.8"/>'
    )
    svg.append(
        f'  <path d="{flame_path}" fill="url(#fireGrad)" '
        f'transform="translate({leg_x - 0.8:.2f}, {legend_y + 0.4:.2f}) scale(1.05)"/>'
    )
    leg_x += 16


    svg.append(
        f'  <text x="{leg_x}" y="{legend_y + 10}" fill="{COLOR_TEXT_DIM}" font-size="11">More</text>'
    )

    svg.append("</svg>")

    # Ensure output dir exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"[+] Successfully generated heatmap SVG: {os.path.relpath(output_path, REPO_ROOT)}")


def main():
    print("=" * 60)
    print(" HackerRank Solutions Activity Heatmap Generator")
    print("=" * 60)
    print(f"[*] Scanning repository: {REPO_ROOT}")
    print(f"[*] Target directories: {', '.join(SOLUTION_DIRS)}")

    data = collect_repository_data(REPO_ROOT)

    print(f"\n[+] Total Solution Files: {data['total_files']}")
    for lang, count in data["language_counts"].items():
        print(f"    - {lang}: {count} files")

    print(f"[+] Unique Active Solving Days: {len(data['date_counts'])}")

    # Report metadata discrepancies if any
    if data["missing_date_files"]:
        print(f"\n[!] WARNING: {len(data['missing_date_files'])} files missing solving date metadata:")
        for f, reason in data["missing_date_files"]:
            print(f"    - {f}: {reason}")
    else:
        print("[+] 0 missing date files. (100% metadata coverage)")

    if data["malformed_date_files"]:
        print(f"\n[!] WARNING: {len(data['malformed_date_files'])} files with malformed date strings:")
        for f, reason in data["malformed_date_files"]:
            print(f"    - {f}: {reason}")
    else:
        print("[+] 0 malformed date files. (100% parse success)")

    curr_streak, longest_streak, max_in_day = compute_streaks(data["date_counts"])
    fire_days = sorted([d for d, c in data["date_counts"].items() if c > 5])

    print(f"\n[+] Streak Statistics:")
    print(f"    - Current Streak : {curr_streak} days")
    print(f"    - Longest Streak : {longest_streak} days")
    print(f"    - Max in One Day : {max_in_day} problems")

    print(f"\n[+] Fire Days (> 5 solved in a single day): {len(fire_days)}")
    for fd in fire_days:
        cnt = data["date_counts"][fd]
        print(f"    - {fd.strftime('%Y-%m-%d')}: {cnt} problems solved 🔥")

    # Generate the SVG
    generate_svg(data, OUTPUT_SVG)
    print("=" * 60)
    print(" Heatmap generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
