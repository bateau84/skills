def export_csv(rows):
    lines = ["job_id,outcome"]
    for job_id, outcome in rows:
        lines.append(f"{job_id},{outcome}")
    return "\n".join(lines) + "\n"
