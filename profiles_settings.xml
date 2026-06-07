"""
============================================================
  EXAM RE-SCHEDULER: Smart Study Planning Application
  CC103 - Computer Programming 2
  Desktop Application using Tkinter
============================================================
  Features:
    1. Subject and Exam Date Input
    2. Automatic Subject Prioritization
    3. Exam Countdown Display
    4. Input Validation
    5. Retake / Clear All
============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date


# ══════════════════════════════════════════════════════════
#  COLORS & THEME
# ══════════════════════════════════════════════════════════
BG          = "#F4F1FB"       # soft lavender-white background
SIDEBAR_BG  = "#6C5CE7"       # purple sidebar
SIDEBAR_SEL = "#5A4BD1"       # darker purple for selected item
CARD_BG     = "#FFFFFF"       # white card
ACCENT      = "#6C5CE7"       # purple accent
ACCENT2     = "#00B894"       # teal accent
DANGER      = "#E17055"       # orange-red for urgent
WARNING     = "#FDCB6E"       # yellow-orange for moderate
SUCCESS     = "#00B894"       # green for safe
TEXT_DARK   = "#2D3436"       # dark text
TEXT_MED    = "#636E72"       # medium text
TEXT_LIGHT  = "#B2BEC3"       # light/placeholder text
WHITE       = "#FFFFFF"
BORDER      = "#DFE6E9"

FONT_TITLE  = ("Segoe UI", 22, "bold")
FONT_HEAD   = ("Segoe UI", 14, "bold")
FONT_SUB    = ("Segoe UI", 11, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_MONO   = ("Courier New", 10)


# ══════════════════════════════════════════════════════════
#  FEATURE 4 — INPUT VALIDATION
#  InputValidator: validates subject name and exam date
# ══════════════════════════════════════════════════════════
class ValidationResult:
    """Carries pass/fail status and an error message."""
    def __init__(self, passed: bool, message: str = ""):
        self._passed  = passed
        self._message = message

    def passed(self) -> bool:
        return self._passed

    def get_message(self) -> str:
        return self._message


class InputValidator:
    """Validates all user inputs. No stored state."""

    @staticmethod
    def is_empty(value: str) -> bool:
        return not value.strip()

    @staticmethod
    def validate_subject(name: str) -> ValidationResult:
        if InputValidator.is_empty(name):
            return ValidationResult(False, "Subject name cannot be empty.")
        return ValidationResult(True)

    @staticmethod
    def validate_date(date_str: str) -> ValidationResult:
        if InputValidator.is_empty(date_str):
            return ValidationResult(False, "Exam date cannot be empty.")
        try:
            exam_date = datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
        except ValueError:
            return ValidationResult(
                False,
                "Invalid date format. Please use YYYY-MM-DD (e.g. 2026-07-15)."
            )
        if exam_date <= date.today():
            return ValidationResult(False, "Exam date must be a future date.")
        return ValidationResult(True)

    @staticmethod
    def is_future_date(date_str: str) -> bool:
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d").date() > date.today()
        except ValueError:
            return False

    @staticmethod
    def get_error(field: str) -> str:
        errors = {
            "subject": "Subject name cannot be empty.",
            "date":    "Please enter a valid future date in YYYY-MM-DD format.",
        }
        return errors.get(field, "Invalid input.")


# ══════════════════════════════════════════════════════════
#  FEATURE 1 — SUBJECT MODEL
#  Subject: stores name, exam date, and computed fields
# ══════════════════════════════════════════════════════════
class Subject:
    """Stores one subject's name and exam date."""

    def __init__(self, name: str, exam_date_str: str):
        self._name      = name.strip()
        self._exam_date = datetime.strptime(exam_date_str.strip(), "%Y-%m-%d").date()

    def get_name(self) -> str:
        return self._name

    def get_exam_date(self) -> date:
        return self._exam_date

    def get_exam_date_str(self) -> str:
        return self._exam_date.strftime("%Y-%m-%d")

    def get_days_left(self) -> int:
        return (self._exam_date - date.today()).days

    def get_hours_left(self) -> int:
        now  = datetime.now()
        exam = datetime.combine(self._exam_date, datetime.min.time())
        diff = exam - now
        return max(0, int(diff.total_seconds() // 3600))

    def is_past(self) -> bool:
        return self._exam_date < date.today()

    def update_date(self, new_date_str: str):
        self._exam_date = datetime.strptime(new_date_str.strip(), "%Y-%m-%d").date()

    def priority_score(self) -> int:
        return self.get_days_left()

    def is_valid(self) -> bool:
        return bool(self._name) and not self.is_past()


# ══════════════════════════════════════════════════════════
#  FEATURE 2 — AUTOMATIC SUBJECT PRIORITIZATION
#  PriorityRanker: sorts subjects by nearest exam date
# ══════════════════════════════════════════════════════════
class PriorityRanker:
    """Sorts and ranks subjects by urgency (fewest days first)."""

    def __init__(self, subjects: list):
        self._subjects = subjects

    def sort_by_urgency(self) -> list:
        return sorted(self._subjects, key=lambda s: s.priority_score())

    def assign_ranks(self) -> list:
        """Return list of (rank, subject) tuples."""
        return [(i + 1, s) for i, s in enumerate(self.sort_by_urgency())]

    def get_top(self):
        ranked = self.sort_by_urgency()
        return ranked[0] if ranked else None

    def display_ranked(self) -> list:
        return self.assign_ranks()


# ══════════════════════════════════════════════════════════
#  FEATURE 3 — EXAM COUNTDOWN DISPLAY
#  CountdownDisplay: calculates days & hours to each exam
# ══════════════════════════════════════════════════════════
class CountdownDisplay:
    """Handles countdown calculations and display strings."""

    def __init__(self, subjects: list):
        self._subjects = subjects

    def calc_days(self, subject: Subject) -> int:
        return subject.get_days_left()

    def calc_hours(self, subject: Subject) -> int:
        return subject.get_hours_left()

    def is_expired(self, subject: Subject) -> bool:
        return subject.is_past()

    def format_display(self, subject: Subject) -> dict:
        if self.is_expired(subject):
            return {
                "name":    subject.get_name(),
                "status":  "expired",
                "message": "Exam has already passed.",
                "days":    0,
                "hours":   0,
            }
        days  = self.calc_days(subject)
        hours = self.calc_hours(subject) % 24
        return {
            "name":    subject.get_name(),
            "status":  "upcoming",
            "message": f"{days} day(s) and {hours} hour(s) remaining",
            "days":    days,
            "hours":   hours,
        }

    def sort_by_urgency(self) -> list:
        upcoming = [s for s in self._subjects if not s.is_past()]
        past     = [s for s in self._subjects if s.is_past()]
        return sorted(upcoming, key=lambda s: s.priority_score()) + past


# ══════════════════════════════════════════════════════════
#  FEATURE 5 — RETAKE / CLEAR ALL
#  SessionManager: safely resets the session
# ══════════════════════════════════════════════════════════
class SessionManager:
    """Manages session reset and clear-all operations."""

    def __init__(self, subjects: list):
        self._subjects   = subjects
        self._is_cleared = False

    def is_empty(self) -> bool:
        return len(self._subjects) == 0

    def clear_all(self) -> int:
        count = len(self._subjects)
        self._subjects.clear()
        self._is_cleared = True
        return count

    def restart_session(self):
        self._subjects.clear()
        self._is_cleared = False

    def show_summary(self) -> str:
        return f"{len(self._subjects)} subject(s) currently in the session."

    def confirm_clear(self) -> bool:
        return self._is_cleared


# ══════════════════════════════════════════════════════════
#  EXAM SCHEDULER — MAIN CONTROLLER
# ══════════════════════════════════════════════════════════
class ExamScheduler:
    """Central controller coordinating all features."""

    def __init__(self):
        self._subjects:  list[Subject] = []
        self._validator  = InputValidator()

    def get_subjects(self) -> list:
        return self._subjects

    def add_subject(self, name: str, date_str: str) -> ValidationResult:
        name_result = self._validator.validate_subject(name)
        if not name_result.passed():
            return name_result
        date_result = self._validator.validate_date(date_str)
        if not date_result.passed():
            return date_result
        self._subjects.append(Subject(name, date_str))
        return ValidationResult(True, f"'{name}' added successfully.")

    def edit_subject(self, index: int, new_name: str, new_date_str: str) -> ValidationResult:
        name_result = self._validator.validate_subject(new_name)
        if not name_result.passed():
            return name_result
        date_result = self._validator.validate_date(new_date_str)
        if not date_result.passed():
            return date_result
        self._subjects[index]._name = new_name.strip()
        self._subjects[index].update_date(new_date_str)
        return ValidationResult(True, f"'{new_name}' updated successfully.")

    def delete_subject(self, index: int):
        if 0 <= index < len(self._subjects):
            self._subjects.pop(index)

    def get_ranked(self) -> list:
        ranker = PriorityRanker(self._subjects)
        return ranker.assign_ranks()

    def get_countdown(self) -> list:
        cd = CountdownDisplay(self._subjects)
        all_subjects = cd.sort_by_urgency()
        result = []
        for s in all_subjects:
            item = cd.format_display(s)
            item["exam_date_str"] = s.get_exam_date_str()
            result.append(item)
        return result

    def clear_all(self) -> int:
        sm = SessionManager(self._subjects)
        return sm.clear_all()

    def has_subjects(self) -> bool:
        return len(self._subjects) > 0


# ══════════════════════════════════════════════════════════
#  REUSABLE UI HELPERS
# ══════════════════════════════════════════════════════════
def make_card(parent, pady=(0, 16), padx=0):
    card = tk.Frame(parent, bg=CARD_BG, bd=0, highlightthickness=1,
                    highlightbackground=BORDER)
    card.pack(fill="x", pady=pady, padx=padx)
    return card


def urgency_color(days: int) -> str:
    if days <= 2:  return DANGER
    if days <= 7:  return WARNING
    return SUCCESS


def urgency_label(days: int) -> str:
    if days <= 2:  return "🔴  URGENT"
    if days <= 7:  return "🟡  HIGH"
    return "🟢  LOW"


# ══════════════════════════════════════════════════════════
#  MODAL DIALOGS
# ══════════════════════════════════════════════════════════
class AddSubjectDialog(tk.Toplevel):
    """Modal dialog to add or edit a subject."""

    def __init__(self, parent, scheduler: ExamScheduler,
                 edit_index: int = None, edit_subject: Subject = None,
                 on_success=None):
        super().__init__(parent)
        self._scheduler  = scheduler
        self._edit_index = edit_index
        self._on_success = on_success
        is_edit = edit_index is not None

        self.title("Edit Subject" if is_edit else "Add Subject")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()

        w, h = 500, 420
        sw   = self.winfo_screenwidth()
        sh   = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        # ── Title ────────────────────────────────────────
        tk.Label(self, text="✏️  Edit Subject" if is_edit else "➕  Add Subject",
                 font=FONT_HEAD, bg=BG, fg=TEXT_DARK).pack(pady=(24, 4))
        tk.Label(self, text="Fill in the subject details below.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_MED).pack()

        form = tk.Frame(self, bg=BG)
        form.pack(fill="x", padx=32, pady=16)

        # Subject name
        tk.Label(form, text="Subject Name", font=FONT_SUB,
                 bg=BG, fg=TEXT_DARK, anchor="w").grid(row=0, column=0, sticky="w", pady=(0,4))
        self._name_var = tk.StringVar(value=edit_subject.get_name() if is_edit else "")
        name_entry = tk.Entry(form, textvariable=self._name_var, font=FONT_BODY,
                              relief="flat", bd=0, bg=WHITE, fg=TEXT_DARK,
                              highlightthickness=1, highlightbackground=BORDER,
                              highlightcolor=ACCENT)
        name_entry.grid(row=1, column=0, sticky="ew", ipady=8, pady=(0,14))
        name_entry.focus()

        # Exam date
        tk.Label(form, text="Exam Date  (YYYY-MM-DD)", font=FONT_SUB,
                 bg=BG, fg=TEXT_DARK, anchor="w").grid(row=2, column=0, sticky="w", pady=(0,4))
        self._date_var = tk.StringVar(
            value=edit_subject.get_exam_date_str() if is_edit else "")
        date_entry = tk.Entry(form, textvariable=self._date_var, font=FONT_BODY,
                              relief="flat", bd=0, bg=WHITE, fg=TEXT_DARK,
                              highlightthickness=1, highlightbackground=BORDER,
                              highlightcolor=ACCENT)
        date_entry.grid(row=3, column=0, sticky="ew", ipady=8, pady=(0,4))
        form.columnconfigure(0, weight=1)

        # Error label
        self._err_var = tk.StringVar()
        tk.Label(form, textvariable=self._err_var, font=FONT_SMALL,
                 bg=BG, fg=DANGER, wraplength=340, justify="left"
                 ).grid(row=4, column=0, sticky="w")

        # Buttons
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(fill="x", padx=32, pady=(16, 32))

        tk.Button(btn_row, text="Cancel", font=("Segoe UI", 12, "bold"),
                  bg=BORDER, fg=TEXT_DARK, relief="flat", bd=0,
                  width=14, height=2, cursor="hand2",
                  command=self.destroy).pack(side="left")

        lbl = "Save Changes" if is_edit else "Add Subject"
        tk.Button(btn_row, text=lbl, font=("Segoe UI", 12, "bold"),
                  bg=ACCENT, fg=WHITE, relief="flat", bd=0,
                  width=16, height=2, cursor="hand2",
                  command=self._submit).pack(side="right")

    def _submit(self):
        name     = self._name_var.get()
        date_str = self._date_var.get()
        if self._edit_index is not None:
            result = self._scheduler.edit_subject(self._edit_index, name, date_str)
        else:
            result = self._scheduler.add_subject(name, date_str)

        if result.passed():
            if self._on_success:
                self._on_success()
            self.destroy()
        else:
            self._err_var.set("⚠  " + result.get_message())


class ConfirmClearDialog(tk.Toplevel):
    """Safety confirmation before clearing all subjects."""

    def __init__(self, parent, scheduler: ExamScheduler, on_confirmed=None):
        super().__init__(parent)
        self._scheduler    = scheduler
        self._on_confirmed = on_confirmed

        self.title("Confirm Clear All")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()

        w, h = 400, 260
        sw   = self.winfo_screenwidth()
        sh   = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        tk.Label(self, text="🗑️  Clear All Subjects?",
                 font=FONT_HEAD, bg=BG, fg=TEXT_DARK).pack(pady=(28, 8))

        count = len(scheduler.get_subjects())
        msg   = (f"You are about to remove all {count} subject(s) from your schedule.\n"
                 "This action cannot be undone.")
        tk.Label(self, text=msg, font=FONT_BODY, bg=BG, fg=TEXT_MED,
                 wraplength=340, justify="center").pack(pady=(0, 24))

        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(fill="x", padx=40)

        tk.Button(btn_row, text="Cancel", font=FONT_BODY,
                  bg=BORDER, fg=TEXT_DARK, relief="flat", bd=0,
                  padx=20, pady=8, cursor="hand2",
                  command=self.destroy).pack(side="left")

        tk.Button(btn_row, text="Yes, Clear All", font=FONT_SUB,
                  bg=DANGER, fg=WHITE, relief="flat", bd=0,
                  padx=20, pady=8, cursor="hand2",
                  command=self._confirm).pack(side="right")

    def _confirm(self):
        removed = self._scheduler.clear_all()
        if self._on_confirmed:
            self._on_confirmed(removed)
        self.destroy()


# ══════════════════════════════════════════════════════════
#  PAGE: ADD / MANAGE SUBJECTS  (Feature 1 + 4)
# ══════════════════════════════════════════════════════════
class SubjectInputPage(tk.Frame):

    def __init__(self, parent, scheduler: ExamScheduler, on_change=None):
        super().__init__(parent, bg=BG)
        self._scheduler  = scheduler
        self._on_change  = on_change
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", pady=(0, 16))
        tk.Label(hdr, text="Subject and Exam Date Input",
                 font=FONT_TITLE, bg=BG, fg=TEXT_DARK).pack(side="left")
        tk.Button(hdr, text="➕  Add Subject", font=FONT_SUB,
                  bg=ACCENT, fg=WHITE, relief="flat", bd=0,
                  padx=16, pady=8, cursor="hand2",
                  command=self._open_add).pack(side="right")

        tk.Label(self,
                 text="Enter your subjects and exam dates. The app will validate each entry.",
                 font=FONT_BODY, bg=BG, fg=TEXT_MED).pack(anchor="w", pady=(0, 16))

        # Scrollable subject list
        self._list_frame = tk.Frame(self, bg=BG)
        self._list_frame.pack(fill="both", expand=True)
        self._refresh()

    def _refresh(self):
        for w in self._list_frame.winfo_children():
            w.destroy()

        subjects = self._scheduler.get_subjects()
        if not subjects:
            empty = tk.Frame(self._list_frame, bg=CARD_BG,
                             highlightthickness=1, highlightbackground=BORDER)
            empty.pack(fill="x", pady=8)
            tk.Label(empty,
                     text="📭  No subjects added yet.\nClick '➕ Add Subject' to get started.",
                     font=FONT_BODY, bg=CARD_BG, fg=TEXT_LIGHT,
                     pady=40, justify="center").pack()
            return

        for i, subj in enumerate(subjects):
            self._make_subject_row(i, subj)

    def _make_subject_row(self, index: int, subj: Subject):
        days  = subj.get_days_left()
        color = urgency_color(days)
        badge = urgency_label(days)

        card = tk.Frame(self._list_frame, bg=CARD_BG,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(fill="x", pady=4)

        # Color accent bar (left strip)
        strip = tk.Frame(card, bg=color, width=6)
        strip.pack(side="left", fill="y")

        body = tk.Frame(card, bg=CARD_BG, padx=16, pady=12)
        body.pack(side="left", fill="both", expand=True)

        # Subject name + badge
        top = tk.Frame(body, bg=CARD_BG)
        top.pack(fill="x")
        tk.Label(top, text=subj.get_name(), font=FONT_SUB,
                 bg=CARD_BG, fg=TEXT_DARK).pack(side="left")
        tk.Label(top, text=badge, font=FONT_SMALL,
                 bg=color, fg=WHITE, padx=8, pady=2).pack(side="left", padx=8)

        # Exam date + days left
        tk.Label(body,
                 text=f"📅  {subj.get_exam_date_str()}   |   "
                      f"{'⏳  ' + str(days) + ' day(s) left' if days >= 0 else '❌  Exam passed'}",
                 font=FONT_SMALL, bg=CARD_BG, fg=TEXT_MED).pack(anchor="w", pady=(2, 0))

        # Buttons
        btn_area = tk.Frame(card, bg=CARD_BG, padx=12)
        btn_area.pack(side="right", fill="y")
        tk.Button(btn_area, text="✏️", font=FONT_BODY,
                  bg=CARD_BG, fg=ACCENT, relief="flat", bd=0,
                  cursor="hand2",
                  command=lambda i=index, s=subj: self._open_edit(i, s)
                  ).pack(side="left", padx=4)
        tk.Button(btn_area, text="🗑️", font=FONT_BODY,
                  bg=CARD_BG, fg=DANGER, relief="flat", bd=0,
                  cursor="hand2",
                  command=lambda i=index: self._delete(i)
                  ).pack(side="left")

    def _open_add(self):
        AddSubjectDialog(self, self._scheduler,
                         on_success=self._after_change)

    def _open_edit(self, index: int, subj: Subject):
        AddSubjectDialog(self, self._scheduler,
                         edit_index=index, edit_subject=subj,
                         on_success=self._after_change)

    def _delete(self, index: int):
        name = self._scheduler.get_subjects()[index].get_name()
        if messagebox.askyesno("Delete Subject",
                               f"Remove '{name}' from your schedule?"):
            self._scheduler.delete_subject(index)
            self._after_change()

    def _after_change(self):
        self._refresh()
        if self._on_change:
            self._on_change()


# ══════════════════════════════════════════════════════════
#  PAGE: PRIORITY RANKING  (Feature 2)
# ══════════════════════════════════════════════════════════
class PriorityPage(tk.Frame):

    def __init__(self, parent, scheduler: ExamScheduler):
        super().__init__(parent, bg=BG)
        self._scheduler = scheduler
        self._build()

    def _build(self):
        tk.Label(self, text="Automatic Subject Prioritization",
                 font=FONT_TITLE, bg=BG, fg=TEXT_DARK
                 ).pack(anchor="w", pady=(0, 4))
        tk.Label(self,
                 text="Subjects are automatically sorted by nearest exam date — "
                      "most urgent first.",
                 font=FONT_BODY, bg=BG, fg=TEXT_MED
                 ).pack(anchor="w", pady=(0, 20))

        self._body = tk.Frame(self, bg=BG)
        self._body.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self):
        for w in self._body.winfo_children():
            w.destroy()

        if not self._scheduler.has_subjects():
            card = make_card(self._body)
            tk.Label(card,
                     text="📭  No subjects to rank yet.\nAdd subjects in the Input tab first.",
                     font=FONT_BODY, bg=CARD_BG, fg=TEXT_LIGHT,
                     pady=40, justify="center").pack()
            return

        ranked = self._scheduler.get_ranked()

        # Header row
        hdr = tk.Frame(self._body, bg=ACCENT)
        hdr.pack(fill="x", pady=(0, 2))
        for col, width in [("Rank", 6), ("Subject", 30), ("Exam Date", 14),
                           ("Days Left", 12), ("Urgency", 12)]:
            tk.Label(hdr, text=col, font=FONT_SUB, bg=ACCENT, fg=WHITE,
                     width=width, anchor="w", padx=8, pady=8
                     ).pack(side="left")

        for rank, subj in ranked:
            days  = subj.get_days_left()
            color = urgency_color(days)
            badge = urgency_label(days)

            row = tk.Frame(self._body, bg=CARD_BG,
                           highlightthickness=1, highlightbackground=BORDER)
            row.pack(fill="x", pady=2)

            # Rank badge
            rank_frame = tk.Frame(row, bg=color, width=50)
            rank_frame.pack(side="left", fill="y")
            tk.Label(rank_frame, text=f"#{rank}", font=FONT_SUB,
                     bg=color, fg=WHITE, padx=8).pack(expand=True)

            # Subject name
            tk.Label(row, text=subj.get_name(), font=FONT_BODY,
                     bg=CARD_BG, fg=TEXT_DARK, width=28, anchor="w",
                     padx=8, pady=10).pack(side="left")

            # Exam date
            tk.Label(row, text=subj.get_exam_date_str(), font=FONT_BODY,
                     bg=CARD_BG, fg=TEXT_MED, width=14, anchor="w"
                     ).pack(side="left")

            # Days left
            day_text = f"{days} day(s)" if days >= 0 else "Passed"
            tk.Label(row, text=day_text, font=FONT_BODY,
                     bg=CARD_BG, fg=color, width=12, anchor="w"
                     ).pack(side="left")

            # Urgency
            tk.Label(row, text=badge, font=FONT_SMALL,
                     bg=CARD_BG, fg=color, width=12, anchor="w"
                     ).pack(side="left")


# ══════════════════════════════════════════════════════════
#  PAGE: COUNTDOWN DISPLAY  (Feature 3)
# ══════════════════════════════════════════════════════════
class CountdownPage(tk.Frame):

    def __init__(self, parent, scheduler: ExamScheduler):
        super().__init__(parent, bg=BG)
        self._scheduler = scheduler
        self._build()

    def _build(self):
        tk.Label(self, text="Exam Countdown Display",
                 font=FONT_TITLE, bg=BG, fg=TEXT_DARK
                 ).pack(anchor="w", pady=(0, 4))
        tk.Label(self,
                 text="Live countdown to each exam sort by urgency — updated every time you visit this page.",
                 font=FONT_BODY, bg=BG, fg=TEXT_MED
                 ).pack(anchor="w", pady=(0, 20))

        self._body = tk.Frame(self, bg=BG)
        self._body.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self):
        for w in self._body.winfo_children():
            w.destroy()

        if not self._scheduler.has_subjects():
            card = make_card(self._body)
            tk.Label(card,
                     text="📭  No subjects found.\nAdd subjects in the Input tab first.",
                     font=FONT_BODY, bg=CARD_BG, fg=TEXT_LIGHT,
                     pady=40, justify="center").pack()
            return

        countdowns = self._scheduler.get_countdown()

        for item in countdowns:
            days   = item["days"]
            status = item["status"]
            color  = DANGER if status == "expired" else urgency_color(days)

            card = tk.Frame(self._body, bg=CARD_BG,
                            highlightthickness=1, highlightbackground=BORDER)
            card.pack(fill="x", pady=5)

            strip = tk.Frame(card, bg=color, width=8)
            strip.pack(side="left", fill="y")

            body = tk.Frame(card, bg=CARD_BG, padx=20, pady=16)
            body.pack(side="left", fill="both", expand=True)

            # Subject name
            tk.Label(body, text=item["name"], font=FONT_HEAD,
                     bg=CARD_BG, fg=TEXT_DARK).pack(anchor="w")

            if status == "expired":
                tk.Label(body, text="❌  Exam has already passed.",
                         font=FONT_BODY, bg=CARD_BG, fg=DANGER).pack(anchor="w")
            else:
                hours_rem = item["hours"] % 24
                # Big countdown numbers
                ctr = tk.Frame(body, bg=CARD_BG)
                ctr.pack(anchor="w", pady=(6, 0))

                for val, lbl in [(str(days), "DAYS"), (str(hours_rem), "HOURS")]:
                    box = tk.Frame(ctr, bg=color, padx=16, pady=8)
                    box.pack(side="left", padx=(0, 8))
                    tk.Label(box, text=val, font=("Segoe UI", 20, "bold"),
                             bg=color, fg=WHITE).pack()
                    tk.Label(box, text=lbl, font=FONT_SMALL,
                             bg=color, fg=WHITE).pack()

                tk.Label(body,
                         text=f"📅  {item['message']}",
                         font=FONT_SMALL, bg=CARD_BG, fg=TEXT_MED
                         ).pack(anchor="w", pady=(6, 0))


# ══════════════════════════════════════════════════════════
#  PAGE: CLEAR ALL  (Feature 5)
# ══════════════════════════════════════════════════════════
class ClearAllPage(tk.Frame):

    def __init__(self, parent, scheduler: ExamScheduler, on_cleared=None):
        super().__init__(parent, bg=BG)
        self._scheduler = scheduler
        self._on_cleared = on_cleared
        self._build()

    def _build(self):
        tk.Label(self, text="Retake / Clear All",
                 font=FONT_TITLE, bg=BG, fg=TEXT_DARK
                 ).pack(anchor="w", pady=(0, 4))
        tk.Label(self,
                 text="Reset your session and start fresh. This will remove all subjects.",
                 font=FONT_BODY, bg=BG, fg=TEXT_MED
                 ).pack(anchor="w", pady=(0, 24))

        self._body = tk.Frame(self, bg=BG)
        self._body.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self):
        for w in self._body.winfo_children():
            w.destroy()

        subjects = self._scheduler.get_subjects()

        # Summary card
        card = make_card(self._body)
        inner = tk.Frame(card, bg=CARD_BG, padx=24, pady=20)
        inner.pack(fill="x")

        if not subjects:
            tk.Label(inner,
                     text="✅  Your schedule is already empty.\n"
                          "Head to the Input tab to add subjects.",
                     font=FONT_BODY, bg=CARD_BG, fg=SUCCESS,
                     justify="center", pady=20).pack()
            return

        tk.Label(inner, text="📋  Current Session Summary",
                 font=FONT_HEAD, bg=CARD_BG, fg=TEXT_DARK).pack(anchor="w", pady=(0, 12))

        for i, subj in enumerate(subjects, 1):
            days = subj.get_days_left()
            row  = tk.Frame(inner, bg=CARD_BG)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"  {i}.", font=FONT_BODY,
                     bg=CARD_BG, fg=TEXT_MED, width=4).pack(side="left")
            tk.Label(row, text=subj.get_name(), font=FONT_SUB,
                     bg=CARD_BG, fg=TEXT_DARK).pack(side="left")
            day_str = f"{days} day(s) left" if days >= 0 else "Passed"
            tk.Label(row, text=f"  —  {subj.get_exam_date_str()}  ({day_str})",
                     font=FONT_BODY, bg=CARD_BG,
                     fg=urgency_color(days)).pack(side="left")

        # Warning
        warn = tk.Frame(self._body, bg="#FFF3F0",
                        highlightthickness=1, highlightbackground=DANGER)
        warn.pack(fill="x", pady=12)
        tk.Label(warn,
                 text=f"⚠️  Clearing will permanently remove all "
                      f"{len(subjects)} subject(s) from this session.",
                 font=FONT_BODY, bg="#FFF3F0", fg=DANGER,
                 padx=16, pady=12).pack(anchor="w")

        # Button
        tk.Button(self._body, text="🗑️  Clear All Subjects",
                  font=FONT_SUB, bg=DANGER, fg=WHITE,
                  relief="flat", bd=0, padx=24, pady=12,
                  cursor="hand2",
                  command=self._open_confirm).pack(anchor="w", pady=(4, 0))

    def _open_confirm(self):
        ConfirmClearDialog(self, self._scheduler,
                           on_confirmed=self._after_clear)

    def _after_clear(self, removed: int):
        messagebox.showinfo("Session Cleared",
                            f"✅  {removed} subject(s) removed.\n"
                            "Your session has been reset successfully.")
        self.refresh()
        if self._on_cleared:
            self._on_cleared()


# ══════════════════════════════════════════════════════════
#  MAIN APPLICATION WINDOW
# ══════════════════════════════════════════════════════════
class ExamSchedulerApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Exam Re-Scheduler — Smart Study Planning")
        self.configure(bg=BG)
        self.minsize(900, 600)

        # Center window
        w, h = 1100, 680
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self._scheduler    = ExamScheduler()
        self._current_page = None
        self._nav_buttons  = {}

        self._build_layout()
        self._show_page("input")

    # ── Layout ───────────────────────────────────────────
    def _build_layout(self):
        # Sidebar
        self._sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=220)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        # App logo / title
        logo = tk.Frame(self._sidebar, bg=SIDEBAR_BG, pady=24)
        logo.pack(fill="x")
        tk.Label(logo, text="📚", font=("Segoe UI", 28),
                 bg=SIDEBAR_BG, fg=WHITE).pack()
        tk.Label(logo, text="Exam Re-Scheduler",
                 font=("Segoe UI", 12, "bold"),
                 bg=SIDEBAR_BG, fg=WHITE).pack()
        tk.Label(logo, text="Smart Study Planning",
                 font=FONT_SMALL, bg=SIDEBAR_BG, fg="#A29BFE").pack()

        # Divider
        tk.Frame(self._sidebar, bg="#5A4BD1", height=1).pack(fill="x", padx=16, pady=8)

        # Nav items
        nav_items = [
            ("input",     "📝", "Subject Input"),
            ("priority",  "🏆", "Priority Ranking"),
            ("countdown", "⏱️", "Countdown"),
            ("clear",     "🗑️", "Clear All"),
        ]
        for key, icon, label in nav_items:
            self._make_nav_btn(key, icon, label)

        # Spacer + version
        tk.Frame(self._sidebar, bg=SIDEBAR_BG).pack(expand=True, fill="y")
        tk.Label(self._sidebar,
                 text="CC103 — Computer Programming 2\nv1.0",
                 font=FONT_SMALL, bg=SIDEBAR_BG, fg="#A29BFE",
                 pady=16, justify="center").pack(fill="x")

        # Main content area
        self._content = tk.Frame(self, bg=BG)
        self._content.pack(side="left", fill="both", expand=True, padx=32, pady=24)

    def _make_nav_btn(self, key: str, icon: str, label: str):
        btn = tk.Button(
            self._sidebar,
            text=f"  {icon}  {label}",
            font=FONT_BODY,
            bg=SIDEBAR_BG, fg=WHITE,
            relief="flat", bd=0,
            anchor="w", padx=16, pady=12,
            cursor="hand2",
            activebackground=SIDEBAR_SEL,
            activeforeground=WHITE,
            command=lambda k=key: self._show_page(k)
        )
        btn.pack(fill="x", padx=8, pady=2)
        self._nav_buttons[key] = btn

    # ── Page Switching ────────────────────────────────────
    def _show_page(self, key: str):
        # Clear content
        for w in self._content.winfo_children():
            w.destroy()

        # Highlight active nav
        for k, btn in self._nav_buttons.items():
            btn.configure(bg=SIDEBAR_SEL if k == key else SIDEBAR_BG)

        self._current_page = key

        if key == "input":
            SubjectInputPage(self._content, self._scheduler,
                             on_change=self._on_data_change
                             ).pack(fill="both", expand=True)

        elif key == "priority":
            page = PriorityPage(self._content, self._scheduler)
            page.pack(fill="both", expand=True)

        elif key == "countdown":
            page = CountdownPage(self._content, self._scheduler)
            page.pack(fill="both", expand=True)

        elif key == "clear":
            ClearAllPage(self._content, self._scheduler,
                         on_cleared=self._on_data_change
                         ).pack(fill="both", expand=True)

    def _on_data_change(self):
        """Called whenever subjects are added/edited/deleted/cleared."""
        if self._current_page == "priority":
            for w in self._content.winfo_children():
                if isinstance(w, PriorityPage):
                    w.refresh()
        elif self._current_page == "countdown":
            for w in self._content.winfo_children():
                if isinstance(w, CountdownPage):
                    w.refresh()
        elif self._current_page == "clear":
            for w in self._content.winfo_children():
                if isinstance(w, ClearAllPage):
                    w.refresh()


# ══════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = ExamSchedulerApp()
    app.mainloop()
