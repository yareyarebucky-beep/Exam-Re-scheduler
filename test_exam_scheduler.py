"""
============================================================
  TEST FILE — Exam Re-Scheduler
  CC103 - Computer Programming 2
============================================================
  Run with:  pytest test_exam_scheduler.py -v
============================================================
"""

import pytest
from datetime import date, timedelta, datetime

# ── Import only the backend classes (no tkinter needed) ──
import sys, types

# Stub out tkinter so the import works without a display
tk_stub = types.ModuleType("tkinter")
tk_stub.Tk         = object
tk_stub.Frame      = object
tk_stub.Label      = object
tk_stub.Button     = object
tk_stub.Entry      = object
tk_stub.Toplevel   = object
tk_stub.StringVar  = object
tk_stub.BooleanVar = object
tk_stub.messagebox = types.ModuleType("tkinter.messagebox")
tk_stub.ttk        = types.ModuleType("tkinter.ttk")
sys.modules["tkinter"]            = tk_stub
sys.modules["tkinter.messagebox"] = tk_stub.messagebox
sys.modules["tkinter.ttk"]        = tk_stub.ttk

# Now safely import the backend classes
sys.path.insert(0, ".")
from exam_scheduler import (
    ValidationResult,
    InputValidator,
    Subject,
    PriorityRanker,
    CountdownDisplay,
    SessionManager,
    ExamScheduler,
)

# ── Shared future dates ───────────────────────────────────
TOMORROW   = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
IN_3_DAYS  = (date.today() + timedelta(days=3)).strftime("%Y-%m-%d")
IN_5_DAYS  = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")
IN_10_DAYS = (date.today() + timedelta(days=10)).strftime("%Y-%m-%d")
IN_14_DAYS = (date.today() + timedelta(days=14)).strftime("%Y-%m-%d")
YESTERDAY  = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
TODAY      = date.today().strftime("%Y-%m-%d")


# ════════════════════════════════════════════════════════
#  FEATURE 4 — INPUT VALIDATION
# ════════════════════════════════════════════════════════
class TestValidationResult:

    def test_passed_true(self):
        result = ValidationResult(True, "OK")
        assert result.passed() is True

    def test_passed_false(self):
        result = ValidationResult(False, "Error")
        assert result.passed() is False

    def test_get_message(self):
        result = ValidationResult(False, "Subject name cannot be empty.")
        assert result.get_message() == "Subject name cannot be empty."

    def test_empty_message_default(self):
        result = ValidationResult(True)
        assert result.get_message() == ""


class TestInputValidator:

    # ── is_empty ──────────────────────────────────────────
    def test_is_empty_blank_string(self):
        assert InputValidator.is_empty("") is True

    def test_is_empty_spaces_only(self):
        assert InputValidator.is_empty("   ") is True

    def test_is_empty_valid_string(self):
        assert InputValidator.is_empty("Mathematics") is False

    # ── validate_subject ──────────────────────────────────
    def test_validate_subject_valid(self):
        result = InputValidator.validate_subject("Mathematics")
        assert result.passed() is True

    def test_validate_subject_empty(self):
        result = InputValidator.validate_subject("")
        assert result.passed() is False
        assert "empty" in result.get_message().lower()

    def test_validate_subject_spaces_only(self):
        result = InputValidator.validate_subject("   ")
        assert result.passed() is False

    def test_validate_subject_with_spaces_trimmed(self):
        result = InputValidator.validate_subject("  Physics  ")
        assert result.passed() is True

    # ── validate_date ─────────────────────────────────────
    def test_validate_date_valid_future(self):
        result = InputValidator.validate_date(IN_5_DAYS)
        assert result.passed() is True

    def test_validate_date_empty(self):
        result = InputValidator.validate_date("")
        assert result.passed() is False
        assert "empty" in result.get_message().lower()

    def test_validate_date_wrong_format_slashes(self):
        result = InputValidator.validate_date("06/20/2026")
        assert result.passed() is False
        assert "format" in result.get_message().lower()

    def test_validate_date_wrong_format_text(self):
        result = InputValidator.validate_date("June 20 2026")
        assert result.passed() is False

    def test_validate_date_past_date(self):
        result = InputValidator.validate_date(YESTERDAY)
        assert result.passed() is False
        assert "future" in result.get_message().lower()

    def test_validate_date_today_is_invalid(self):
        result = InputValidator.validate_date(TODAY)
        assert result.passed() is False

    def test_validate_date_invalid_day(self):
        result = InputValidator.validate_date("2026-13-45")
        assert result.passed() is False

    # ── is_future_date ────────────────────────────────────
    def test_is_future_date_true(self):
        assert InputValidator.is_future_date(IN_10_DAYS) is True

    def test_is_future_date_past(self):
        assert InputValidator.is_future_date(YESTERDAY) is False

    def test_is_future_date_bad_format(self):
        assert InputValidator.is_future_date("not-a-date") is False

    # ── get_error ─────────────────────────────────────────
    def test_get_error_subject(self):
        msg = InputValidator.get_error("subject")
        assert "empty" in msg.lower()

    def test_get_error_date(self):
        msg = InputValidator.get_error("date")
        assert "date" in msg.lower()

    def test_get_error_unknown_field(self):
        msg = InputValidator.get_error("unknown")
        assert msg == "Invalid input."


# ════════════════════════════════════════════════════════
#  FEATURE 1 — SUBJECT MODEL
# ════════════════════════════════════════════════════════
class TestSubject:

    def test_get_name(self):
        s = Subject("Mathematics", IN_5_DAYS)
        assert s.get_name() == "Mathematics"

    def test_get_name_strips_whitespace(self):
        s = Subject("  Physics  ", IN_5_DAYS)
        assert s.get_name() == "Physics"

    def test_get_exam_date_str(self):
        s = Subject("English", IN_5_DAYS)
        assert s.get_exam_date_str() == IN_5_DAYS

    def test_get_days_left_future(self):
        s = Subject("Biology", IN_10_DAYS)
        assert s.get_days_left() == 10

    def test_get_days_left_tomorrow(self):
        s = Subject("Chemistry", TOMORROW)
        assert s.get_days_left() == 1

    def test_get_hours_left_positive(self):
        s = Subject("History", IN_3_DAYS)
        assert s.get_hours_left() > 0

    def test_is_past_future_subject(self):
        s = Subject("Math", IN_5_DAYS)
        assert s.is_past() is False

    def test_is_past_past_subject(self):
        s = Subject("Old Exam", YESTERDAY)
        assert s.is_past() is True

    def test_priority_score_equals_days_left(self):
        s = Subject("Science", IN_10_DAYS)
        assert s.priority_score() == s.get_days_left()

    def test_is_valid_future_subject(self):
        s = Subject("English", IN_5_DAYS)
        assert s.is_valid() is True

    def test_is_valid_past_subject(self):
        s = Subject("Old", YESTERDAY)
        assert s.is_valid() is False

    def test_update_date(self):
        s = Subject("Math", IN_3_DAYS)
        s.update_date(IN_14_DAYS)
        assert s.get_days_left() == 14

    def test_get_exam_date_returns_date_object(self):
        s = Subject("Physics", IN_5_DAYS)
        assert isinstance(s.get_exam_date(), date)


# ════════════════════════════════════════════════════════
#  FEATURE 2 — AUTOMATIC SUBJECT PRIORITIZATION
# ════════════════════════════════════════════════════════
class TestPriorityRanker:

    def setup_method(self):
        self.s1 = Subject("Math",    IN_10_DAYS)
        self.s2 = Subject("Science", IN_3_DAYS)
        self.s3 = Subject("English", IN_5_DAYS)
        self.subjects = [self.s1, self.s2, self.s3]
        self.ranker   = PriorityRanker(self.subjects)

    def test_sort_by_urgency_order(self):
        sorted_list = self.ranker.sort_by_urgency()
        names = [s.get_name() for s in sorted_list]
        assert names == ["Science", "English", "Math"]

    def test_sort_by_urgency_fewest_days_first(self):
        sorted_list = self.ranker.sort_by_urgency()
        days = [s.get_days_left() for s in sorted_list]
        assert days == sorted(days)

    def test_assign_ranks_count(self):
        ranked = self.ranker.assign_ranks()
        assert len(ranked) == 3

    def test_assign_ranks_first_is_rank_one(self):
        ranked = self.ranker.assign_ranks()
        rank, subject = ranked[0]
        assert rank == 1
        assert subject.get_name() == "Science"

    def test_assign_ranks_last_rank(self):
        ranked = self.ranker.assign_ranks()
        rank, subject = ranked[-1]
        assert rank == 3
        assert subject.get_name() == "Math"

    def test_get_top_returns_most_urgent(self):
        top = self.ranker.get_top()
        assert top.get_name() == "Science"

    def test_get_top_empty_list(self):
        ranker = PriorityRanker([])
        assert ranker.get_top() is None

    def test_single_subject_rank_is_one(self):
        ranker  = PriorityRanker([self.s1])
        ranked  = ranker.assign_ranks()
        rank, _ = ranked[0]
        assert rank == 1

    def test_display_ranked_same_as_assign_ranks(self):
        assert self.ranker.display_ranked() == self.ranker.assign_ranks()

    def test_four_subjects_all_ranked(self):
        s4 = Subject("History", TOMORROW)
        ranker = PriorityRanker([self.s1, self.s2, self.s3, s4])
        ranked = ranker.assign_ranks()
        assert len(ranked) == 4
        assert ranked[0][1].get_name() == "History"


# ════════════════════════════════════════════════════════
#  FEATURE 3 — EXAM COUNTDOWN DISPLAY
# ════════════════════════════════════════════════════════
class TestCountdownDisplay:

    def setup_method(self):
        self.upcoming  = Subject("Math",    IN_5_DAYS)
        self.urgent    = Subject("Science", TOMORROW)
        self.past      = Subject("Old",     YESTERDAY)
        self.subjects  = [self.upcoming, self.urgent, self.past]
        self.cd        = CountdownDisplay(self.subjects)

    def test_calc_days_upcoming(self):
        assert self.cd.calc_days(self.upcoming) == 5

    def test_calc_days_urgent(self):
        assert self.cd.calc_days(self.urgent) == 1

    def test_calc_hours_positive(self):
        assert self.cd.calc_hours(self.upcoming) > 0

    def test_is_expired_past(self):
        assert self.cd.is_expired(self.past) is True

    def test_is_expired_future(self):
        assert self.cd.is_expired(self.upcoming) is False

    def test_format_display_upcoming_status(self):
        item = self.cd.format_display(self.upcoming)
        assert item["status"] == "upcoming"

    def test_format_display_upcoming_name(self):
        item = self.cd.format_display(self.upcoming)
        assert item["name"] == "Math"

    def test_format_display_upcoming_days(self):
        item = self.cd.format_display(self.upcoming)
        assert item["days"] == 5

    def test_format_display_upcoming_message_contains_days(self):
        item = self.cd.format_display(self.upcoming)
        assert "5" in item["message"]

    def test_format_display_expired_status(self):
        item = self.cd.format_display(self.past)
        assert item["status"] == "expired"

    def test_format_display_expired_days_zero(self):
        item = self.cd.format_display(self.past)
        assert item["days"] == 0

    def test_format_display_expired_message(self):
        item = self.cd.format_display(self.past)
        assert "passed" in item["message"].lower()

    def test_sort_by_urgency_upcoming_before_past(self):
        sorted_list = self.cd.sort_by_urgency()
        statuses = ["past" if s.is_past() else "upcoming" for s in sorted_list]
        # all upcoming first, then past
        seen_past = False
        for status in statuses:
            if status == "past":
                seen_past = True
            if seen_past:
                assert status == "past"

    def test_sort_by_urgency_all_subjects_included(self):
        sorted_list = self.cd.sort_by_urgency()
        assert len(sorted_list) == 3

    def test_sort_by_urgency_urgent_is_first(self):
        sorted_list = self.cd.sort_by_urgency()
        assert sorted_list[0].get_name() == "Science"

    def test_empty_subjects_sort(self):
        cd = CountdownDisplay([])
        assert cd.sort_by_urgency() == []


# ════════════════════════════════════════════════════════
#  FEATURE 5 — RETAKE / CLEAR ALL
# ════════════════════════════════════════════════════════
class TestSessionManager:

    def setup_method(self):
        self.subjects = [
            Subject("Math",    IN_5_DAYS),
            Subject("Science", IN_10_DAYS),
        ]
        self.sm = SessionManager(self.subjects)

    def test_is_empty_false_when_has_subjects(self):
        assert self.sm.is_empty() is False

    def test_is_empty_true_when_no_subjects(self):
        sm = SessionManager([])
        assert sm.is_empty() is True

    def test_clear_all_returns_count(self):
        count = self.sm.clear_all()
        assert count == 2

    def test_clear_all_empties_list(self):
        self.sm.clear_all()
        assert self.sm.is_empty() is True

    def test_confirm_clear_before_clear(self):
        assert self.sm.confirm_clear() is False

    def test_confirm_clear_after_clear(self):
        self.sm.clear_all()
        assert self.sm.confirm_clear() is True

    def test_show_summary_before_clear(self):
        summary = self.sm.show_summary()
        assert "2" in summary

    def test_show_summary_after_clear(self):
        self.sm.clear_all()
        summary = self.sm.show_summary()
        assert "0" in summary

    def test_restart_session_clears_list(self):
        self.sm.restart_session()
        assert self.sm.is_empty() is True

    def test_restart_session_resets_cleared_flag(self):
        self.sm.clear_all()
        self.sm.restart_session()
        assert self.sm.confirm_clear() is False

    def test_clear_all_single_subject(self):
        sm = SessionManager([Subject("Math", IN_5_DAYS)])
        count = sm.clear_all()
        assert count == 1
        assert sm.is_empty() is True

    def test_clear_already_empty(self):
        sm = SessionManager([])
        count = sm.clear_all()
        assert count == 0


# ════════════════════════════════════════════════════════
#  EXAM SCHEDULER — MAIN CONTROLLER
# ════════════════════════════════════════════════════════
class TestExamScheduler:

    def setup_method(self):
        self.scheduler = ExamScheduler()

    # ── add_subject ───────────────────────────────────────
    def test_add_subject_success(self):
        result = self.scheduler.add_subject("Math", IN_5_DAYS)
        assert result.passed() is True

    def test_add_subject_adds_to_list(self):
        self.scheduler.add_subject("Math", IN_5_DAYS)
        assert len(self.scheduler.get_subjects()) == 1

    def test_add_subject_empty_name_fails(self):
        result = self.scheduler.add_subject("", IN_5_DAYS)
        assert result.passed() is False

    def test_add_subject_empty_date_fails(self):
        result = self.scheduler.add_subject("Math", "")
        assert result.passed() is False

    def test_add_subject_past_date_fails(self):
        result = self.scheduler.add_subject("Math", YESTERDAY)
        assert result.passed() is False

    def test_add_subject_wrong_format_fails(self):
        result = self.scheduler.add_subject("Math", "20-06-2026")
        assert result.passed() is False

    def test_add_multiple_subjects(self):
        self.scheduler.add_subject("Math",    IN_3_DAYS)
        self.scheduler.add_subject("Science", IN_5_DAYS)
        self.scheduler.add_subject("English", IN_10_DAYS)
        assert len(self.scheduler.get_subjects()) == 3

    def test_add_subject_success_message(self):
        result = self.scheduler.add_subject("Physics", IN_5_DAYS)
        assert "Physics" in result.get_message()

    # ── edit_subject ──────────────────────────────────────
    def test_edit_subject_success(self):
        self.scheduler.add_subject("Math", IN_5_DAYS)
        result = self.scheduler.edit_subject(0, "Advanced Math", IN_10_DAYS)
        assert result.passed() is True

    def test_edit_subject_updates_name(self):
        self.scheduler.add_subject("Math", IN_5_DAYS)
        self.scheduler.edit_subject(0, "Advanced Math", IN_10_DAYS)
        assert self.scheduler.get_subjects()[0].get_name() == "Advanced Math"

    def test_edit_subject_updates_date(self):
        self.scheduler.add_subject("Math", IN_5_DAYS)
        self.scheduler.edit_subject(0, "Math", IN_14_DAYS)
        assert self.scheduler.get_subjects()[0].get_days_left() == 14

    def test_edit_subject_empty_name_fails(self):
        self.scheduler.add_subject("Math", IN_5_DAYS)
        result = self.scheduler.edit_subject(0, "", IN_10_DAYS)
        assert result.passed() is False

    def test_edit_subject_past_date_fails(self):
        self.scheduler.add_subject("Math", IN_5_DAYS)
        result = self.scheduler.edit_subject(0, "Math", YESTERDAY)
        assert result.passed() is False

    # ── delete_subject ────────────────────────────────────
    def test_delete_subject_removes_from_list(self):
        self.scheduler.add_subject("Math",    IN_5_DAYS)
        self.scheduler.add_subject("Science", IN_10_DAYS)
        self.scheduler.delete_subject(0)
        assert len(self.scheduler.get_subjects()) == 1

    def test_delete_subject_correct_one_removed(self):
        self.scheduler.add_subject("Math",    IN_5_DAYS)
        self.scheduler.add_subject("Science", IN_10_DAYS)
        self.scheduler.delete_subject(0)
        assert self.scheduler.get_subjects()[0].get_name() == "Science"

    def test_delete_invalid_index_no_crash(self):
        self.scheduler.add_subject("Math", IN_5_DAYS)
        self.scheduler.delete_subject(99)
        assert len(self.scheduler.get_subjects()) == 1

    # ── get_ranked ────────────────────────────────────────
    def test_get_ranked_returns_all(self):
        self.scheduler.add_subject("Math",    IN_10_DAYS)
        self.scheduler.add_subject("Science", IN_3_DAYS)
        ranked = self.scheduler.get_ranked()
        assert len(ranked) == 2

    def test_get_ranked_most_urgent_first(self):
        self.scheduler.add_subject("Math",    IN_10_DAYS)
        self.scheduler.add_subject("Science", IN_3_DAYS)
        ranked = self.scheduler.get_ranked()
        rank, subject = ranked[0]
        assert subject.get_name() == "Science"
        assert rank == 1

    def test_get_ranked_empty_list(self):
        assert self.scheduler.get_ranked() == []

    # ── get_countdown ─────────────────────────────────────
    def test_get_countdown_returns_all_subjects(self):
        self.scheduler.add_subject("Math",    IN_5_DAYS)
        self.scheduler.add_subject("Science", IN_3_DAYS)
        self.scheduler.add_subject("English", IN_10_DAYS)
        self.scheduler.add_subject("History", TOMORROW)
        countdowns = self.scheduler.get_countdown()
        assert len(countdowns) == 4

    def test_get_countdown_has_correct_keys(self):
        self.scheduler.add_subject("Math", IN_5_DAYS)
        item = self.scheduler.get_countdown()[0]
        for key in ["name", "status", "message", "days", "hours", "exam_date_str"]:
            assert key in item

    def test_get_countdown_status_upcoming(self):
        self.scheduler.add_subject("Math", IN_5_DAYS)
        item = self.scheduler.get_countdown()[0]
        assert item["status"] == "upcoming"

    def test_get_countdown_sorted_by_urgency(self):
        self.scheduler.add_subject("Math",    IN_10_DAYS)
        self.scheduler.add_subject("Science", IN_3_DAYS)
        countdowns = self.scheduler.get_countdown()
        assert countdowns[0]["name"] == "Science"
        assert countdowns[1]["name"] == "Math"

    def test_get_countdown_empty_list(self):
        assert self.scheduler.get_countdown() == []

    # ── has_subjects ──────────────────────────────────────
    def test_has_subjects_false_when_empty(self):
        assert self.scheduler.has_subjects() is False

    def test_has_subjects_true_after_add(self):
        self.scheduler.add_subject("Math", IN_5_DAYS)
        assert self.scheduler.has_subjects() is True

    # ── clear_all ─────────────────────────────────────────
    def test_clear_all_removes_all_subjects(self):
        self.scheduler.add_subject("Math",    IN_5_DAYS)
        self.scheduler.add_subject("Science", IN_10_DAYS)
        self.scheduler.clear_all()
        assert len(self.scheduler.get_subjects()) == 0

    def test_clear_all_returns_correct_count(self):
        self.scheduler.add_subject("Math",    IN_5_DAYS)
        self.scheduler.add_subject("Science", IN_10_DAYS)
        self.scheduler.add_subject("English", IN_14_DAYS)
        count = self.scheduler.clear_all()
        assert count == 3

    def test_clear_all_then_add_again(self):
        self.scheduler.add_subject("Math", IN_5_DAYS)
        self.scheduler.clear_all()
        result = self.scheduler.add_subject("Science", IN_10_DAYS)
        assert result.passed() is True
        assert len(self.scheduler.get_subjects()) == 1
