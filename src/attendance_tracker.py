from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List


@dataclass
class Student:
    student_id: str
    name: str


@dataclass
class AttendanceRecord:
    student_id: str
    day: date
    present: bool


@dataclass
class AttendanceTracker:
    students: Dict[str, Student] = field(default_factory=dict)
    records: List[AttendanceRecord] = field(default_factory=list)

    def add_student(self, student_id: str, name: str) -> None:
        if student_id in self.students:
            raise ValueError(f"Student with id '{student_id}' already exists")
        self.students[student_id] = Student(student_id=student_id, name=name)

    def mark_attendance(self, student_id: str, day: date, present: bool) -> None:
        if student_id not in self.students:
            raise ValueError(f"Unknown student id '{student_id}'")
        self.records.append(AttendanceRecord(student_id=student_id, day=day, present=present))

    def summary(self, student_id: str) -> dict:
        if student_id not in self.students:
            raise ValueError(f"Unknown student id '{student_id}'")

        student_records = [r for r in self.records if r.student_id == student_id]
        total = len(student_records)
        present_days = sum(1 for r in student_records if r.present)
        absent_days = total - present_days
        percentage = (present_days / total * 100) if total else 0.0

        return {
            "student_id": student_id,
            "student_name": self.students[student_id].name,
            "total_days": total,
            "present_days": present_days,
            "absent_days": absent_days,
            "attendance_percentage": round(percentage, 2),
        }


def demo() -> None:
    tracker = AttendanceTracker()
    tracker.add_student("S001", "Alice")
    tracker.add_student("S002", "Bob")

    today = date.today()
    tracker.mark_attendance("S001", today, True)
    tracker.mark_attendance("S002", today, False)

    print("Attendance Summary")
    print(tracker.summary("S001"))
    print(tracker.summary("S002"))


if __name__ == "__main__":
    demo()
