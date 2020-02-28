import typing as typ
import enum


class DiffKind(enum.Enum):
    DEL = 0
    ADD = 1


GradeEntry = typ.Dict[str, str]
GradeTable = typ.List[GradeEntry]
GradeDiff = typ.List[typ.Tuple[DiffKind, GradeEntry]]


def diff(grades_previous: GradeTable, grades_current: GradeTable) -> GradeDiff:
    grade_diff = []
    for entry1 in grades_previous:
        for entry2 in grades_current:
            if entry1 == entry2:
                # Found match
                break
        else:
            # Entry from previous table could not be found in new table
            grade_diff.append((DiffKind.DEL, entry1))
    for entry1 in grades_current:
        for entry2 in grades_previous:
            if entry1 == entry2:
                # Found match
                break
        else:
            # Entry from new table could not be found in previous table
            grade_diff.append((DiffKind.ADD, entry1))
    return grade_diff
