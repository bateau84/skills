# Completed-job CSV export

Call `export_csv(rows)` with job ID and terminal outcome pairs. The export has the header `job_id,outcome`, preserves row order and ends each record with a newline. The current implementation joins values with commas. Special-character escaping is not implemented yet.

Run `python3 -B -m unittest -v` for local regression verification.
