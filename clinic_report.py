#!/usr/bin/env python3

"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """Read usable encounters and return them with the number skipped."""
    encounters = []
    skipped = 0

    with open(data_path, "r") as file:
        rows = file.readlines()

    for row in rows[1:]:
        if row.strip() == "":
            skipped += 1
            print("Skipping a blank row.")
            continue

        fields = row.strip().split(",")

        if len(fields) != 3:
            skipped += 1
            print("Skipped row:", row.rstrip())
            continue

        try:
            systolic = int(fields[2])
        except ValueError:
            skipped += 1
            print("Skipped row:", row.rstrip())
            continue

        if not 60 <= systolic <= 250:
            skipped += 1
            print("Skipped row:", row.rstrip())
            continue

        encounters.append((fields[0], fields[1], systolic))

    return encounters, skipped

  
def main():

    """TODO: write vital summary and follow-up patient list."""
    
    encounters, skipped = read_encounters(DATA_PATH)
    OUTPUT_DIR.mkdir(parents = True, exist_ok = True)

    readings = systolic_readings(encounters)
    print("DEBUG readings =", readings)
    print("DEBUG mean =", mean_systolic(readings))

    #Build the six required reportlines.
    report_lines = [
        f"Usable encounters:{len(encounters)}",
        f"skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {mean_systolic(readings):.1f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]


    report_path = OUTPUT_DIR/"vitals_report.txt" 
    report_path.write_text("\n".join(report_lines)+ "\n")
    
    #Read the saved report and print it. 
    print(report_path.read_text())
    
    #choose the follow-up cut-off.
    cutoff = 140
    patient_at_or_above = patients_at_or_above(encounters, cutoff)

    #Buifollow-up lines
    followup_lines = [
        f"Cutoff: {cutoff}",
        "Reason:Systolic blood pressure at or above cutoff",
    ]

    #Add  one patient ID per line.
    followup_lines.extend(patient_at_or_above)

    followup_path = OUTPUT_DIR / "followup_list.txt"
    followup_path.write_text("\n".join(followup_lines) + "\n")


if __name__ == "__main__":
    main()
