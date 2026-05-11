"""
OOP Models สำหรับ CoreLock

Concepts:
  • Encapsulation  — attribute ส่วนตัว (_private)
  • Abstraction    — ซ่อน logic ภายใน
  • Dataclass      — VaultEntry เป็น plain data object
"""

import re
from dataclasses import dataclass, field
from datetime import datetime

#  เป็น plain data object ที่เก็บข้อมูล 1 รายการ

@dataclass
class VaultEntry:
    """แทน 1 แถวในตาราง vault"""
    id:         int    = 0
    user_id:    int    = 0
    website:    str    = ""
    username:   str    = ""
    password:   str    = ""
    category:   str    = "Other"
    note:       str    = ""
    created_at: str    = field(default_factory=lambda: datetime.now().isoformat(sep=" ", timespec="seconds"))

    def to_dict(self) -> dict:
        return {
            "website": self.website, "username": self.username,
            "password": self.password, "category": self.category,
            "note": self.note,
        }

#  วิเคราะห์ความแข็งแรงของ password (Encapsulation)

class PasswordAnalyzer:
    """
    รับ password แล้วคำนวณ score 0–100
    ซ่อน logic ทั้งหมดไว้ข้างใน (Encapsulation)
    """

    # passwords ที่พบบ่อยและอ่อนแอมาก
    _COMMON = {
        "password", "123456", "qwerty", "abc123", "letmein",
        "monkey", "admin", "welcome", "login", "iloveyou",
        "111111", "123123", "password1", "12345678",
    }

    def __init__(self, password: str):
        self._password = password
        self._score, self._label, self._color, self._tips = self._analyze()

    # ── private ────────────────────────────────────────
    def _analyze(self):
        pw = self._password
        if not pw:
            return 0, "ยังไม่ได้กรอก", "#9CA3AF", []

        score = 0
        tips  = []

        # ── ความยาว (max 35 คะแนน) ─────────────────────
        length = len(pw)
        score += min(length * 3, 35)
        if length < 8:
            tips.append("ควรมีความยาวอย่างน้อย 8 ตัวอักษร")
        elif length < 12:
            tips.append("แนะนำให้ใช้อย่างน้อย 12 ตัวอักษร")

        # ── ความหลากหลายของตัวอักษร (max 40 คะแนน) ────
        has_lower  = bool(re.search(r"[a-z]", pw))
        has_upper  = bool(re.search(r"[A-Z]", pw))
        has_digit  = bool(re.search(r"[0-9]", pw))
        has_symbol = bool(re.search(r"[^a-zA-Z0-9]", pw))

        if has_lower:  score += 10
        if has_upper:  score += 10
        if has_digit:  score += 10
        if has_symbol: score += 10

        if not has_upper:  tips.append("เพิ่มตัวพิมพ์ใหญ่ (A–Z)")
        if not has_digit:  tips.append("เพิ่มตัวเลข (0–9)")
        if not has_symbol: tips.append("เพิ่มอักขระพิเศษ (!@#$)")

        # ── ความไม่ซ้ำกัน (max 15 คะแนน) ──────────────
        unique_ratio = len(set(pw)) / len(pw)
        score += int(unique_ratio * 15)

        # ── pattern ซ้ำๆ (penalty) ─────────────────────
        if re.search(r"(.)\1{2,}", pw):          # aaaa
            score -= 10; tips.append("หลีกเลี่ยงตัวอักษรซ้ำติดกัน")
        if re.search(r"(012|123|234|345|456|567|678|789|890)", pw):
            score -= 8;  tips.append("หลีกเลี่ยงตัวเลขเรียงลำดับ")

        # ── common passwords (penalty) ──────────────────
        if pw.lower() in self._COMMON:
            score = max(score - 50, 2)
            tips.insert(0, "⚠ Password นี้พบบ่อยมาก ไม่ควรใช้!")

        score = max(0, min(score, 100))

        # ── labels ─────────────────────────────────────
        if score < 20:  return score, "อ่อนแอมาก",  "#EF4444", tips
        if score < 40:  return score, "อ่อนแอ",     "#F97316", tips
        if score < 60:  return score, "พอใช้",      "#F59E0B", tips
        if score < 80:  return score, "แข็งแรง",    "#10B981", tips
        return score, "แข็งแรงมาก", "#059669", tips

    # ── public properties ──────────────────────────────
    @property
    def score(self) -> int:   return self._score
    @property
    def label(self) -> str:   return self._label
    @property
    def color(self) -> str:   return self._color
    @property
    def tips(self) -> list:   return self._tips

#  CONSTANTS

CATEGORIES = ["All", "Social", "Work", "Finance",
              "Shopping", "Gaming", "Email", "Other"]

CATEGORY_ICONS = {
    "Social":   "💬",
    "Work":     "💼",
    "Finance":  "💳",
    "Shopping": "🛒",
    "Gaming":   "🎮",
    "Email":    "📧",
    "Other":    "🔑",
    "All":      "📋",
}
