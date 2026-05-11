"""
OOP Concepts:
  • Inheritance   — EntryDialog, RegisterDialog ต่างสืบทอดจาก BaseDialog
  • Abstraction   — BaseDialog กำหนด interface ผ่าน @abstractmethod
  • Polymorphism  — _build_form() และ _on_accept() override คนละแบบ
"""

from abc import abstractmethod, ABCMeta

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QTabWidget, QWidget, QComboBox,
    QProgressBar, QCheckBox, QSpinBox, QSlider, QGroupBox,
    QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from models import PasswordAnalyzer, VaultEntry, CATEGORIES
import styles


# ══════════════════════════════════════════════════════
#  แก้ metaclass conflict ระหว่าง Qt (Shiboken) + ABCMeta
# ══════════════════════════════════════════════════════
class _DialogMeta(type(QDialog), ABCMeta):
    """Combined metaclass — แก้ TypeError: metaclass conflict"""
    pass

# ═════════════════════════════════════════════════════
#  BASE DIALOG  (Abstract — Abstraction + Inheritance)
# ══════════════════════════════════════════════════════
class BaseDialog(QDialog, metaclass=_DialogMeta):
    def __init__(self, parent=None, title="", subtitle="",
                 width=500, height=560):
        super().__init__(parent)
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setFixedSize(width, height)
        self.result_data = None

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(10, 10, 10, 10)

        self.window_frame = QFrame()
        self.window_frame.setObjectName("WindowFrame")
        self.window_frame.setStyleSheet(f"""
            #WindowFrame {{
                background: {styles.BG_CARD};
                border-radius: 20px;   /* ความมนของขอบหน้าต่าง */
                border: 1px solid {styles.BORDER};
            }}
        """)
        outer_layout.addWidget(self.window_frame)

        root = QVBoxLayout(self.window_frame)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header strip ───────────────────────
        self._header = QFrame()
        self._header.setFixedHeight(80)
        self._header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(
                    x1:0,y1:0,x2:1,y2:0,
                    stop:0 {styles.PRIMARY},
                    stop:1 #7C3AED
                );
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }}
        """)
        hl = QVBoxLayout(self._header)
        hl.setContentsMargins(28, 14, 28, 14)
        hl.setSpacing(2)

        htitle = QLabel(title)
        htitle.setStyleSheet("color:white; font-size:18px; font-weight:700; background:transparent; border:none;")
        hsub = QLabel(subtitle)
        hsub.setStyleSheet("color:rgba(255,255,255,0.7); font-size:12px; background:transparent; border:none;")
        hl.addWidget(htitle)
        if subtitle: hl.addWidget(hsub)

        root.addWidget(self._header)

        # ── Body ──────────────────────────────
        self._body = QWidget()
        self._body_layout = QVBoxLayout(self._body)
        self._body_layout.setContentsMargins(28, 20, 28, 10)
        self._body_layout.setSpacing(10)
        root.addWidget(self._body, 1)

        # ── Footer ─────────────────────────────
        footer = QFrame()
        footer.setFixedHeight(68)
        footer.setStyleSheet(f"""
            QFrame {{
                background: {styles.BG_APP};
                border-top: 1px solid {styles.BORDER};
                border-bottom-left-radius: 20px;
                border-bottom-right-radius: 20px;
            }}
        """)
        fl = QHBoxLayout(footer)
        fl.setContentsMargins(28, 0, 28, 0)
        fl.setSpacing(10)

        self._err_lbl = QLabel("")
        self._err_lbl.setStyleSheet(f"color:{styles.DANGER}; font-size:12px; font-weight:500;")
        
        self._btn_cancel = QPushButton("ยกเลิก")
        self._btn_cancel.setFixedSize(100, 40)
        self._btn_cancel.setStyleSheet(styles.btn_secondary())
        self._btn_cancel.clicked.connect(self.reject)

        self._btn_ok = QPushButton("บันทึก")
        self._btn_ok.setFixedSize(120, 40)
        self._btn_ok.setStyleSheet(styles.btn_primary())
        self._btn_ok.clicked.connect(self._on_accept)

        fl.addWidget(self._err_lbl, 1)
        fl.addWidget(self._btn_cancel)
        fl.addWidget(self._btn_ok)
        root.addWidget(footer)

        self._build_form()

    # ── Shared helpers ──────────────────────────────────
    def _field_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(
            f"color:{styles.TEXT_MUTED};font-size:10px;"
            "font-weight:700;letter-spacing:1.5px;")
        return lbl

    def _make_input(self, placeholder="",
                    is_password=False) -> QLineEdit:
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setFixedHeight(48)
        if is_password:
            inp.setEchoMode(QLineEdit.Password)
        return inp

    def _set_error(self, msg: str):
        self._err_lbl.setText(msg)

    # ── Abstract ────────────────────────────────────────
    @abstractmethod
    def _build_form(self):
        """Subclass สร้าง widgets ใส่ self._body_layout"""

    @abstractmethod
    def _on_accept(self):
        """Subclass validate แล้ว set self.result_data"""

class RegisterDialog(BaseDialog):


    def __init__(self, parent=None):
        super().__init__(
            parent,
            title    = "สมัครสมาชิก",
            subtitle = "สร้างบัญชีใหม่สำหรับ CoreLock",
            width    = 460,
            height   = 560,
        )
        self._btn_ok.setText("สร้างบัญชี")

    def _build_form(self):    
        lay = self._body_layout

        # Full name
        lay.addWidget(self._field_label("ชื่อ-นามสกุล"))
        self.f_name = self._make_input("กรอกชื่อจริง (ไม่บังคับ)")
        lay.addWidget(self.f_name)

        # Username
        lay.addWidget(self._field_label("USERNAME"))
        self.f_user = self._make_input("เลือก username")
        lay.addWidget(self.f_user)

        # Password
        lay.addWidget(self._field_label("MASTER PASSWORD"))
        pw_row = QHBoxLayout(); pw_row.setSpacing(6)
        self.f_pw1 = self._make_input("ตั้ง master password", is_password=True)
        self.f_pw1.textChanged.connect(self._update_strength)
        eye1 = self._eye_button()
        eye1.toggled.connect(
            lambda on: self.f_pw1.setEchoMode(
                QLineEdit.Normal if on else QLineEdit.Password))
        pw_row.addWidget(self.f_pw1, 1)
        pw_row.addWidget(eye1)
        lay.addLayout(pw_row)

        # Strength bar
        str_row = QHBoxLayout(); str_row.setSpacing(8)
        self.s_bar = QProgressBar()
        self.s_bar.setRange(0, 100); self.s_bar.setValue(0)
        self.s_bar.setFixedHeight(6)
        self.s_lbl = QLabel("—")
        self.s_lbl.setFixedWidth(80)
        self.s_lbl.setStyleSheet(f"font-size:11px;color:{styles.TEXT_MUTED};font-weight:600;")
        str_row.addWidget(self.s_bar, 1)
        str_row.addWidget(self.s_lbl)
        lay.addLayout(str_row)

        # Confirm password
        lay.addWidget(self._field_label("ยืนยัน PASSWORD"))
        self.f_pw2 = self._make_input("พิมพ์ password อีกครั้ง", is_password=True)
        lay.addWidget(self.f_pw2)

        lay.addStretch()

    def _eye_button(self) -> QPushButton:
        btn = QPushButton("👁")
        btn.setFixedSize(48, 48)
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background:{styles.BG_APP};border:1.5px solid {styles.BORDER};
                border-radius:10px;font-size:16px;
            }}
            QPushButton:checked {{ border-color:{styles.PRIMARY}; }}
        """)
        return btn

    def _update_strength(self, text: str):
        a = PasswordAnalyzer(text)
        self.s_bar.setValue(a.score)
        self.s_bar.setStyleSheet(
            f"QProgressBar::chunk{{background:{a.color};border-radius:3px;}}")
        self.s_lbl.setText(a.label)
        self.s_lbl.setStyleSheet(
            f"font-size:11px;color:{a.color};font-weight:600;")

    def _on_accept(self):    
        user  = self.f_user.text().strip()
        pw    = self.f_pw1.text()
        pw2   = self.f_pw2.text()
        name  = self.f_name.text().strip()

        if not user:
            self._set_error("⚠  กรุณากรอก username"); return
        if len(user) < 3:
            self._set_error("⚠  Username ต้องมีอย่างน้อย 3 ตัวอักษร"); return
        if len(pw) < 6:
            self._set_error("⚠  Password ต้องมีอย่างน้อย 6 ตัวอักษร"); return
        if pw != pw2:
            self._set_error("⚠  Password ไม่ตรงกัน"); return

        self.result_data = {"username": user, "password": pw, "full_name": name}
        self.accept()

class EntryDialog(BaseDialog):

    def __init__(self, parent=None, title="เพิ่ม Password",
                 entry: VaultEntry = None):
        self._entry = entry or VaultEntry()
        is_edit = bool(entry and entry.id)
        super().__init__(
            parent,
            title    = title,
            subtitle = "แก้ไขข้อมูลด้านล่าง" if is_edit else "กรอกข้อมูลบัญชีใหม่",
            width    = 540,
            height   = 640,
        )
        self._btn_ok.setText("บันทึก")
        self._body_layout.setContentsMargins(0, 0, 0, 0)

    def _build_form(self):     # ← Polymorphism
        tabs = QTabWidget()
        self._body_layout.addWidget(tabs)

        # ══ Tab 1: รายละเอียด ═════════════════
        tab1 = QWidget()
        t1   = QVBoxLayout(tab1)
        t1.setContentsMargins(24, 16, 24, 8)
        t1.setSpacing(8)

        # Website
        t1.addWidget(self._field_label("WEBSITE / APPLICATION"))
        self.f_site = self._make_input("เช่น google.com, LINE")
        self.f_site.setText(self._entry.website)
        t1.addWidget(self.f_site)

        # Username
        t1.addWidget(self._field_label("USERNAME / EMAIL"))
        self.f_user = self._make_input("เช่น user@gmail.com")
        self.f_user.setText(self._entry.username)
        t1.addWidget(self.f_user)

        # Password row
        t1.addWidget(self._field_label("PASSWORD"))
        pw_row = QHBoxLayout(); pw_row.setSpacing(6)
        self.f_pw = self._make_input("กรอก password", is_password=True)
        self.f_pw.setText(self._entry.password)
        self.f_pw.textChanged.connect(self._update_strength)
        self._eye = QPushButton("👁")
        self._eye.setFixedSize(48, 48)
        self._eye.setCheckable(True)
        self._eye.setCursor(Qt.PointingHandCursor)
        self._eye.setStyleSheet(f"""
            QPushButton{{background:{styles.BG_APP};
                border:1.5px solid {styles.BORDER};border-radius:10px;
                font-size:16px;}}
            QPushButton:checked{{border-color:{styles.PRIMARY};
                background:{styles.PRIMARY_LITE};}}
        """)
        self._eye.toggled.connect(
            lambda on: self.f_pw.setEchoMode(
                QLineEdit.Normal if on else QLineEdit.Password))
        pw_row.addWidget(self.f_pw, 1)
        pw_row.addWidget(self._eye)
        t1.addLayout(pw_row)

        # Strength indicator
        s_row = QHBoxLayout(); s_row.setSpacing(8)
        self._str_bar = QProgressBar()
        self._str_bar.setRange(0, 100)
        self._str_bar.setValue(0)
        self._str_bar.setFixedHeight(7)
        self._str_lbl = QLabel("—")
        self._str_lbl.setFixedWidth(75)
        self._str_lbl.setStyleSheet(
            f"font-size:11px;color:{styles.TEXT_MUTED};font-weight:600;")
        s_row.addWidget(self._str_bar, 1)
        s_row.addWidget(self._str_lbl)
        t1.addLayout(s_row)

        # Category (QComboBox)
        t1.addWidget(self._field_label("CATEGORY"))
        self.f_cat = QComboBox()
        self.f_cat.addItems([c for c in CATEGORIES if c != "All"])
        idx = self.f_cat.findText(self._entry.category)
        if idx >= 0: self.f_cat.setCurrentIndex(idx)
        t1.addWidget(self.f_cat)

        # Note
        t1.addWidget(self._field_label("หมายเหตุ (ไม่บังคับ)"))
        self.f_note = QLineEdit()
        self.f_note.setPlaceholderText("บันทึกสั้นๆ เกี่ยวกับบัญชีนี้")
        self.f_note.setFixedHeight(44)
        self.f_note.setText(self._entry.note)
        t1.addWidget(self.f_note)
        t1.addStretch()

        tabs.addTab(tab1, "  รายละเอียด  ")

    # ── Slot methods ────────────────────────────────────
    def _update_strength(self, text: str):
        a = PasswordAnalyzer(text)
        self._str_bar.setValue(a.score)
        self._str_bar.setStyleSheet(
            f"QProgressBar::chunk{{background:{a.color};border-radius:3px;}}")
        self._str_lbl.setText(a.label)
        self._str_lbl.setStyleSheet(
            f"font-size:11px;color:{a.color};font-weight:600;")

    def _on_accept(self):     # ← Polymorphism
        w = self.f_site.text().strip()
        u = self.f_user.text().strip()
        p = self.f_pw.text().strip()

        if not w: self._set_error("⚠  กรุณากรอก Website / App"); return
        if not u: self._set_error("⚠  กรุณากรอก Username"); return
        if not p: self._set_error("⚠  กรุณากรอก Password"); return

        self._entry.website  = w
        self._entry.username = u
        self._entry.password = p
        self._entry.category = self.f_cat.currentText()
        self._entry.note     = self.f_note.text().strip()
        self.result_data     = self._entry
        self.accept()
