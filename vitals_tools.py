"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """TODO: describe what this pulls out of the encounter records."""
    # TODO: collect the systolic value of every encounter into one list.
    
    return [encounter[2] for encounter in encounters]
    pass


def mean_systolic(readings):
    """Return the mean of the readings, or None if the list is empty."""
    if len(readings) == 0:
        return None

    return sum(readings) / len(readings)


def count_patients(encounters):
    """TODO: describe what this counts."""
    # TODO: collect the patient IDs and keep only the distinct ones.
    return len({encounter[0] for encounter in encounters})
    pass


def patients_at_or_above(encounters, cutoff):
    """TODO: describe which patient IDs come back."""
    # TODO: keep each patient whose systolic reading is at or above cutoff.
    return [
        encounter[0]
        for encounter in encounters 
        if encounter[2] >= cutoff
        ]
    pass
