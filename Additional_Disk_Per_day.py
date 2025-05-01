# Recursively output the files and their sizes to a txt file (So we can work on this independently)

# find /datadrive/nextcloud/__groupfolders -type f -printf "%TY-%Tm-%Td %TH:%TM %s %p\n" > files_listing.txt

# TODO: Replicate without template

from datetime import datetime, timedelta
from collections import defaultdict

# Settings
days_to_consider = 30
filename = "files_listing.txt"

# Prep
cutoff = datetime.now() - timedelta(days=days_to_consider)
daily_totals = defaultdict(int)

with open(filename) as f:
    for line in f:
        try:
            date_str, time_str, size_str, *_ = line.strip().split(' ', 3)
            timestamp = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            size_bytes = int(size_str)

            if timestamp >= cutoff:
                day_key = timestamp.date()
                daily_totals[day_key] += size_bytes
        except Exception as e:
            print(f"Skipping line: {line.strip()} (error: {e})")

# Compute average
total_days = len(daily_totals)
total_mb = sum(size for size in daily_totals.values()) / (1024 * 1024)

if total_days:
    avg_per_day_mb = total_mb / total_days
    print(f"Average MB added per day over the last {days_to_consider} days: {avg_per_day_mb:.2f} MB/day")
else:
    print("No files found in the last 30 days.")
