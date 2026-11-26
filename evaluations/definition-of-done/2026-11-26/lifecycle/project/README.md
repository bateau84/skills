# Completed-job CSV export

Call `export_csv(rows)` with job ID and terminal outcome pairs. The export has the header `job_id,outcome`, preserves row order and ends every record with LF (`\n`), including the final record. Empty input returns just the header and its LF.

Values containing commas, quotes or embedded newlines (LF, CRLF or CR) are CSV-escaped in either column: fields are quoted when needed, and embedded quotes are doubled. CSV readers recover the original text, including embedded newlines. Plain values retain their existing text output. Use `newline=""` when opening CSV files for reading or writing so embedded line endings are preserved.

The exporter uses only the Python standard library.

Run `python3 -B -m unittest -v` for local regression verification.
