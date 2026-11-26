import csv
import io


def export_csv(rows):
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(("job_id", "outcome"))
    for job_id, outcome in rows:
        writer.writerow((str(job_id), str(outcome)))
    return output.getvalue()
