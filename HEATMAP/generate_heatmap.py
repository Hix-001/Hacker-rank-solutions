#!/usr/bin/env python3
"""Generate an SVG contribution heatmap from dated HackerRank solution files."""

import os
import re
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from xml.sax.saxutils import escape

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_SVG = os.path.join(SCRIPT_DIR, "contribution_heatmap.svg")
SOLUTION_DIRS = ("PYTHON", "CPP", "30 DAYS OF CODE")
VALID_EXTENSIONS = {".py", ".cpp"}

CALENDAR_START = date(2026, 6, 28)  # Sunday before July 2026
CALENDAR_WEEKS = 57

PALETTE = {
    0: ("#171d27", "#242d3a"),
    1: ("#123b2b", "#1b5138"),
    2: ("#12643a", "#1b7946"),
    3: ("#20a34a", "#2dbd59"),
    4: ("#39d353", "#69ed7d"),
}
FUTURE_FILL = "#101722"
FUTURE_STROKE = "#1b2431"


def parse_solution_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="replace") as source:
        lines = [source.readline() for _ in range(10)]

    date_pattern = re.compile(r"^(\d{1,4}[-/. ]\d{1,2}[-/. ]\d{2,4})")
    formats = ("%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%Y-%m-%d", "%Y/%m/%d")

    for line in lines:
        raw = line.strip()
        if raw.startswith("//"):
            raw = raw[2:].strip()
        elif raw.startswith("#"):
            raw = raw[1:].strip()
        else:
            continue

        raw = re.sub(r"^DATE\s*:?\s*", "", raw, flags=re.IGNORECASE)
        match = date_pattern.match(raw)
        if not match:
            continue

        value = match.group(1).strip()
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt).date(), None
            except ValueError:
                continue
        return None, f"Malformed date: {value}"

    return None, "No date header found in first 10 lines"


def collect_repository_data(root_dir):
    date_counts = Counter()
    language_counts = Counter()
    missing_dates = []
    malformed_dates = []
    total_files = 0

    for directory in SOLUTION_DIRS:
        folder = os.path.join(root_dir, directory)
        if not os.path.isdir(folder):
            continue

        for filename in sorted(os.listdir(folder)):
            extension = os.path.splitext(filename)[1].lower()
            if extension not in VALID_EXTENSIONS:
                continue

            total_files += 1
            relative_path = os.path.relpath(os.path.join(folder, filename), root_dir)
            language_counts["Python" if extension == ".py" else "C++"] += 1
            solved_date, error = parse_solution_file(os.path.join(folder, filename))

            if solved_date is None:
                record = (relative_path, error)
                (malformed_dates if error.startswith("Malformed") else missing_dates).append(record)
            else:
                date_counts[solved_date] += 1

    return {
        "total_files": total_files,
        "date_counts": date_counts,
        "language_counts": language_counts,
        "missing_dates": missing_dates,
        "malformed_dates": malformed_dates,
    }


def compute_streaks(date_counts, today=None):
    if not date_counts:
        return 0, 0, 0

    today = today or date.today()
    active_dates = set(date_counts)
    latest_date = max(active_dates)
    max_daily = max(date_counts.values())

    longest = run = 0
    previous = None
    for solved_date in sorted(active_dates):
        run = run + 1 if previous and solved_date == previous + timedelta(days=1) else 1
        longest = max(longest, run)
        previous = solved_date

    current = 0
    check_date = today if today in active_dates else today - timedelta(days=1)
    if latest_date <= today and check_date in active_dates:
        while check_date in active_dates:
            current += 1
            check_date -= timedelta(days=1)

    return current, longest, max_daily


def get_level(count):
    if count <= 0:
        return 0
    if count == 1:
        return 1
    if count == 2:
        return 2
    if count <= 4:
        return 3
    return 4


def generate_svg(data, output_path, quiet=False):
    counts = data["date_counts"]
    total_solved = data["total_files"]
    active_days = len(counts)
    current_streak, longest_streak, max_daily = compute_streaks(counts)
    today = date.today()

    cell_size = 11
    gap = 3
    step = cell_size + gap
    grid_x = 52
    grid_y = 91
    width = 880
    height = 260
    radius = 3
    month_names = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" role="img" aria-labelledby="title description">',
        '<title id="title">HackerRank contribution activity</title>',
        '<desc id="description">Daily HackerRank solutions from July 2026 through July 2027. Brighter green cells indicate more solutions.</desc>',
        '<defs>',
        '<linearGradient id="card" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0%" stop-color="#111722"/><stop offset="100%" stop-color="#0b111a"/>',
        '</linearGradient>',
        '<linearGradient id="topSheen" x1="0" y1="0" x2="0" y2="1">',
        '<stop offset="0%" stop-color="#ffffff" stop-opacity=".045"/><stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>',
        '</linearGradient>',
        '<filter id="shadow" x="-10%" y="-10%" width="120%" height="125%">',
        '<feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#000000" flood-opacity=".28"/>',
        '</filter>',
        '<style>',
        'text{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}',
        '.cell{outline:none}.cell rect{transition:stroke .12s ease,filter .12s ease}',
        '.cell:hover rect,.cell:focus rect{stroke:#f8fafc;stroke-width:1.2;filter:drop-shadow(0 0 2px #ffffff66)}',
        '</style>',
        '</defs>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="20" fill="url(#card)" stroke="#293343" stroke-width="1.2" filter="url(#shadow)"/>',
        f'<rect x="2" y="2" width="{width-4}" height="85" rx="19" fill="url(#topSheen)"/>',
        '<text x="32" y="37" fill="#f8fafc" font-size="18" font-weight="700" letter-spacing="-.25">HackerRank Contribution Activity</text>',
        '<text x="32" y="56" fill="#9aa8ba" font-size="12.5">Contributions &amp; Problem Solving Calendar · July 2026 – July 2027</text>',
    ]

    badges = [
        (f"{total_solved} Solved", "#60a5fa", "#17263b"),
        (f"{active_days} Active Days", "#34d399", "#132b25"),
        (f"{current_streak} Day Streak", "#c084fc", "#282036"),
        (f"Max {max_daily}/Day", "#fbbf24", "#302719"),
    ]
    badge_widths = [max(84, len(label) * 6.5 + 22) for label, _, _ in badges]
    badge_gap = 7
    badge_x = width - 31 - sum(badge_widths) - badge_gap * (len(badges) - 1)
    for (label, color, background), badge_width in zip(badges, badge_widths):
        svg.extend([
            f'<g transform="translate({badge_x:.1f},23)">',
            f'<rect width="{badge_width:.1f}" height="25" rx="12.5" fill="{background}" stroke="{color}" stroke-opacity=".48" stroke-width=".8"/>',
            f'<text x="{badge_width/2:.1f}" y="16.5" text-anchor="middle" fill="{color}" font-size="11.5" font-weight="650">{escape(label)}</text>',
            '</g>',
        ])
        badge_x += badge_width + badge_gap

    rendered_months = set()
    for col in range(CALENDAR_WEEKS):
        week_start = CALENDAR_START + timedelta(days=col * 7)
        for offset in range(7):
            current_date = week_start + timedelta(days=offset)
            key = (current_date.year, current_date.month)
            if current_date.day == 1 and key not in rendered_months:
                rendered_months.add(key)
                x = grid_x + col * step
                svg.append(f'<text x="{x}" y="{grid_y-11}" fill="#9aa8ba" font-size="11.5">{month_names[current_date.month-1]}</text>')
                break

    for row, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = grid_y + row * step + 9
        svg.append(f'<text x="{grid_x-12}" y="{y}" fill="#748398" font-size="10.5" text-anchor="end">{label}</text>')

    for col in range(CALENDAR_WEEKS):
        for row in range(7):
            cell_date = CALENDAR_START + timedelta(days=col * 7 + row)
            count = counts.get(cell_date, 0)
            x = grid_x + col * step
            y = grid_y + row * step
            if cell_date > today:
                fill, stroke = FUTURE_FILL, FUTURE_STROKE
                tooltip = f"{cell_date:%d/%m/%y} · Future date"
            else:
                fill, stroke = PALETTE[get_level(count)]
                if count == 0:
                    tooltip = f"{cell_date:%d/%m/%y} · No solutions recorded"
                else:
                    unit = "solution" if count == 1 else "solutions"
                    tooltip = f"{cell_date:%d/%m/%y} · {count} {unit}"
            svg.extend([
                f'<g class="cell" tabindex="0" role="img" aria-label="{escape(tooltip)}">',
                f'<title>{escape(tooltip)}</title>',
                f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width=".65"/>',
                '</g>',
            ])

    legend_y = grid_y + 7 * step + 17
    svg.append(f'<text x="32" y="{legend_y+10}" fill="#9aa8ba" font-size="11.5">Daily problem-solving activity · July 2026 – July 2027</text>')
    legend_x = width - 229
    svg.append(f'<text x="{legend_x}" y="{legend_y+10}" fill="#748398" font-size="11.5" text-anchor="end">Less</text>')
    legend_x += 10
    for level in range(5):
        fill, stroke = PALETTE[level]
        svg.append(f'<rect x="{legend_x}" y="{legend_y}" width="11" height="11" rx="2.5" fill="{fill}" stroke="{stroke}" stroke-width=".65"/>')
        legend_x += 15
    svg.append(f'<text x="{legend_x+1}" y="{legend_y+10}" fill="#748398" font-size="11.5">More</text>')
    svg.append('</svg>')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as output:
        output.write("\n".join(svg))

    if not quiet:
        print(f"Generated heatmap: {os.path.relpath(output_path, REPO_ROOT)}")


def main():
    quiet = "-q" in sys.argv or "--quiet" in sys.argv
    data = collect_repository_data(REPO_ROOT)
    current, longest, max_daily = compute_streaks(data["date_counts"])

    if not quiet:
        print(f"Scanning repository: {REPO_ROOT}")
        print(f"Solution files: {data['total_files']}")
        for language, count in sorted(data["language_counts"].items()):
            print(f"  {language}: {count}")
        print(f"Dated active days: {len(data['date_counts'])}")
        print(f"Current streak: {current} days | Longest streak: {longest} days | Max/day: {max_daily}")
        for heading, entries in (("Missing date metadata", data["missing_dates"]), ("Malformed dates", data["malformed_dates"])):
            if entries:
                print(f"\n{heading} ({len(entries)}):")
                for path, reason in entries:
                    print(f"  - {path}: {reason}")

    generate_svg(data, OUTPUT_SVG, quiet=quiet)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    main()
