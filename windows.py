from PySide6.QtWidgets import (
    QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView,
    QComboBox, QApplication, QMessageBox,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor

from database import Database
from models import VaultEntry, CATEGORIES, CATEGORY_ICONS
from dialogs import EntryDialog, RegisterDialog
import styles

#  STAT CARD  (reusable widget)

class StatCard(QFrame):
    def __init__(self, icon, label, value, accent, parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setFixedHeight(84)
        self._accent = accent
        self._set_style(False)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 8, 14, 8)
        lay.setSpacing(2)

        top = QLabel(f"{icon}  {label}")
        top.setStyleSheet(
                    f"color: {styles.TEXT_MUTED}; "
                    "font-size: 9px; "
                    "font-weight: 700; "
                    "letter-spacing: 1px; "
                    "background: transparent; "
                    "border: none;"
                )

        self._val = QLabel(value)
        self._val.setStyleSheet(
                    f"color: {accent}; "
                    "font-size: 22px; "
                    "font-weight: 800; "
                    "background: transparent; "
                    "border: none;"
                )

        lay.addWidget(top)
        lay.addWidget(self._val)

    def _set_style(self, _=False):
        self.setStyleSheet(f"""
            QFrame#statCard {{
                background: {styles.BG_CARD};
                border: 1px solid {styles.BORDER};
                border-left: 3px solid {self._accent};
                border-radius: 10px;
            }}
        """)

    def set_value(self, v: str):
        self._val.setText(v)

#  LOGIN PAGE

class LoginPage(QWidget):
    def __init__(self, on_login_success, on_goto_register):
        super().__init__()
        self._on_success  = on_login_success
        self._on_register = on_goto_register
        self._build_ui()

    def _build_ui(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        left = QFrame()
        left.setObjectName("loginLeft")
        left.setFixedWidth(400)
        left.setStyleSheet("""
            QFrame#loginLeft {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4F46E5, stop:0.55 #7C3AED, stop:1 #9333EA
                );
                border: none;
                border-radius: 0;
            }
        """)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(44, 0, 44, 44)
        ll.setSpacing(0)
        ll.addStretch(2)

        for txt, sty in [
            ("🔐",    "font-size:68px;background:transparent;border:none;"),
            ("CoreLock", (
                f"color:white;font-size:36px;font-weight:800;"
                "letter-spacing:3px;background:transparent;border:none;")),
            ("จัดการ Password อย่างปลอดภัย", (
                "color:rgba(255,255,255,0.65);font-size:12px;"
                "background:transparent;border:none;")),
        ]:
            lbl = QLabel(txt)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(sty)
            ll.addWidget(lbl)
            ll.addSpacing(8 if txt == "🔐" else 6)

        ll.addStretch(3)
        outer.addWidget(left)

        right = QWidget()          
        right.setStyleSheet(f"background:{styles.BG_APP};")
        rl = QVBoxLayout(right)
        rl.setContentsMargins(60, 0, 60, 0)
        rl.setSpacing(0)
        rl.addStretch(2)

        # หัว
        wlc = QLabel("ยินดีต้อนรับกลับ 👋")
        wlc.setStyleSheet(
            f"color:{styles.TEXT_PRIMARY};font-size:22px;font-weight:700;")
        rl.addWidget(wlc)
        rl.addSpacing(4)
        sub = QLabel("เข้าสู่ระบบเพื่อจัดการรหัสผ่านของคุณ")
        sub.setStyleSheet(f"color:{styles.TEXT_MUTED};font-size:13px;")
        rl.addWidget(sub)
        rl.addSpacing(32)

        # Fields
        def lbl(text):
            l = QLabel(text)
            l.setStyleSheet(
                f"color:{styles.TEXT_MUTED};font-size:10px;"
                "font-weight:700;letter-spacing:1.5px;")
            rl.addWidget(l)
            rl.addSpacing(5)

        def inp(ph, pw=False):
            i = QLineEdit()
            i.setPlaceholderText(ph)
            i.setFixedHeight(50)
            i.setStyleSheet(styles.input_style())
            if pw: i.setEchoMode(QLineEdit.Password)
            rl.addWidget(i)
            rl.addSpacing(16)
            return i

        lbl("USERNAME")
        self.f_user = inp("กรอก username")
        lbl("MASTER PASSWORD")
        self.f_pw = inp("กรอก password", pw=True)
        self.f_pw.returnPressed.connect(self._do_login)

        self._err = QLabel("")
        self._err.setStyleSheet(
            f"color:{styles.DANGER};font-size:12px;min-height:20px;")
        rl.addWidget(self._err)
        rl.addSpacing(8)

        btn = QPushButton("เข้าสู่ระบบ")
        btn.setFixedHeight(50)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(styles.btn_primary())
        btn.clicked.connect(self._do_login)
        rl.addWidget(btn)
        rl.addSpacing(18)

        # Register link
        rrow = QHBoxLayout()
        rrow.addStretch()
        rl.addSpacing(0)
        no_acc = QLabel("ยังไม่มีบัญชี?")
        no_acc.setStyleSheet(f"color:{styles.TEXT_MUTED};font-size:12px;")
        reg_btn = QPushButton("สมัครสมาชิก")
        reg_btn.setFlat(True)
        reg_btn.setCursor(Qt.PointingHandCursor)
        reg_btn.setStyleSheet(f"""
            QPushButton{{color:{styles.PRIMARY};font-size:12px;
                font-weight:600;background:transparent;border:none;}}
            QPushButton:hover{{color:{styles.PRIMARY_DARK};}}
        """)
        reg_btn.clicked.connect(self._on_register)
        rrow.addWidget(no_acc); rrow.addWidget(reg_btn); rrow.addStretch()
        rl.addLayout(rrow)
        rl.addStretch(3)

        outer.addWidget(right, 1)

    def _do_login(self):
        self._err.clear()
        u = self.f_user.text().strip()
        p = self.f_pw.text()
        if not u or not p:
            self._err.setText("⚠  กรุณากรอก username และ password"); return
        
        self._on_success(u, p)

    def set_error(self, msg): self._err.setText(msg)
    def clear(self):
        self.f_user.clear(); self.f_pw.clear(); self._err.clear()

#  VAULT PAGE

class VaultPage(QWidget):
    def __init__(self, db: Database, on_logout):
        super().__init__()
        self.db         = db
        self._on_logout = on_logout
        self.uid        = 0
        self.uname      = ""
        self._show_rows: dict[int, bool] = {}
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._make_sidebar())
        root.addWidget(self._make_content(), 1)

    # ── Sidebar ────────────────────────────────────────
    def _make_sidebar(self) -> QWidget:
        side = QWidget()
        side.setFixedWidth(248)
        side.setObjectName("vaultSide")
        side.setStyleSheet(f"""
            QWidget#vaultSide {{
                background: {styles.BG_CARD};
                border-right: 1px solid {styles.BORDER};
            }}
        """)
        sl = QVBoxLayout(side)
        sl.setContentsMargins(14, 18, 14, 14)
        sl.setSpacing(6)

        # Logo
        logo = QLabel("🔐  CoreLock")
        logo.setAlignment(Qt.AlignCenter)

        logo.setStyleSheet(f"""
            QLabel {{
                color: {styles.PRIMARY};
                font-size: 15px;
                font-weight: 800;
                letter-spacing: 2px;

                background-color: transparent;
                border: none;
                padding: 0;
                margin: 0;
            }}
        """)

        sl.addWidget(logo)

        self._user_lbl = QLabel("👤  —")
        self._user_lbl.setAlignment(Qt.AlignCenter)

        self._user_lbl.setStyleSheet(f"""
                    QLabel {{
                        color: {styles.TEXT_MUTED};
                        font-size: 11px;
                        background-color: transparent;
                        border: none;
                        padding: 0;
                        margin: 0;
                    }}
                """)
        sl.addWidget(self._user_lbl)

        sl.addWidget(self._div())

        # Stat cards
        self.c_total  = StatCard("📋", "รายการทั้งหมด",   "0", styles.PRIMARY)
        self.c_weak   = StatCard("⚠",  "PASSWORD อ่อนแอ", "0", styles.DANGER)
        self.c_strong = StatCard("✅", "PASSWORD แข็งแรง", "0", styles.SUCCESS)
        for c in [self.c_total, self.c_weak, self.c_strong]:
            sl.addWidget(c)

        sl.addWidget(self._div())

        # Category filter label
        cl = QLabel("FILTER BY CATEGORY")
        cl.setStyleSheet(
            f"color:{styles.TEXT_MUTED};font-size:9px;font-weight:700;"
            "letter-spacing:1.5px;background-color: transparent;")
        sl.addWidget(cl)

        self.cat_combo = QComboBox()
        self.cat_combo.addItems(CATEGORIES)
        self.cat_combo.currentTextChanged.connect(self._refresh)
        sl.addWidget(self.cat_combo)

        sl.addWidget(self._div())

        # Action buttons
        def sbtn(icon, text, style_fn, danger=False):
            b = QPushButton(f"  {icon}  {text}")
            b.setFixedHeight(42)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet(
                style_fn() +
                "QPushButton{text-align:left;border-radius:10px;padding:0 14px;}")
            return b

        self.btn_add  = sbtn("➕", "เพิ่ม Password",    styles.btn_primary)
        self.btn_edit = sbtn("✏️", "แก้ไขที่เลือก",    styles.btn_secondary)
        self.btn_del  = sbtn("🗑️", "ลบที่เลือก",       styles.btn_danger)
        self.btn_copy = sbtn("📋", "คัดลอก Password",  styles.btn_secondary)

        self.btn_add.clicked.connect(self._on_add)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_del.clicked.connect(self._on_delete)
        self.btn_copy.clicked.connect(self._on_copy)

        for b in [self.btn_add, self.btn_edit, self.btn_del, self.btn_copy]:
            sl.addWidget(b)

        sl.addStretch()
        sl.addWidget(self._div())

        lock_btn = QPushButton("🔒 Logout")
        lock_btn.setFixedHeight(38)
        lock_btn.setCursor(Qt.PointingHandCursor)
        lock_btn.setStyleSheet(styles.btn_ghost())
        lock_btn.clicked.connect(self._on_logout)
        sl.addWidget(lock_btn)

        return side

    # ── Main content ───────────────────────────────────
    def _make_content(self) -> QWidget:
        content = QWidget()
        content.setObjectName("vaultContent")
        content.setStyleSheet(
            f"QWidget#vaultContent{{background:{styles.BG_APP};}}")
        cl = QVBoxLayout(content)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        # Topbar
        topbar = QWidget()
        topbar.setObjectName("topbar")
        topbar.setFixedHeight(62)
        topbar.setStyleSheet(f"""
            QWidget#topbar {{
                background: {styles.BG_CARD};
                border-bottom: 1px solid {styles.BORDER};
            }}
        """)
        tb = QHBoxLayout(topbar)
        tb.setContentsMargins(24, 0, 24, 0)
        tb.setSpacing(12)

        title = QLabel("My Accounts")
        title.setObjectName("pageTitle")

        title.setStyleSheet(f"""
            QLabel#pageTitle {{
                color: {styles.TEXT_PRIMARY};
                font-size: 18px;
                font-weight: 700;
                background-color: transparent;
                padding: 0;
                margin: 0;
                border: none;
            }}
        """)
        tb.addWidget(title)
        tb.addStretch()

        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍  ค้นหา website, username…")
        self.search.setFixedHeight(50)
        self.search.setFixedWidth(340)
        self.search.setStyleSheet(f"""
            QLineEdit {{
                background: {styles.BG_APP};
                border: 1.5px solid {styles.BORDER};
                border-radius: 19px;
                color: {styles.TEXT_PRIMARY};
                font-size: 13px;
                padding: 0 16px;
            }}
            QLineEdit:focus {{ border-color: {styles.PRIMARY}; }}
        """)
        self.search.textChanged.connect(self._refresh)
        tb.addWidget(self.search)

        cl.addWidget(topbar)

        # Table area
        tw = QWidget()
        tw.setStyleSheet(f"background:{styles.BG_APP};")
        tl = QVBoxLayout(tw)
        tl.setContentsMargins(20, 14, 20, 14)
        tl.setSpacing(0)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "WEBSITE / APP", "USERNAME", "PASSWORD",
            "CATEGORY", "หมายเหตุ", "SHOW"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.Stretch)
        hh.setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.setColumnWidth(3, 110)
        hh.setSectionResizeMode(4, QHeaderView.Stretch)
        hh.setSectionResizeMode(5, QHeaderView.Fixed)
        self.table.setColumnWidth(5, 60)

        self.table.setStyleSheet(f"""
            QTableWidget {{
                background: {styles.BG_CARD};
                border: 1px solid {styles.BORDER};
                border-radius: 10px;
                color: {styles.TEXT_PRIMARY};
                font-size: 13px;
                gridline-color: transparent;
                outline: 0;
            }}
            QTableWidget::item {{
                padding: 0 14px;
                border: none;
                background: {styles.BG_CARD};
            }}
            QTableWidget::item:alternate {{
                background: {styles.BG_APP};
            }}
            QTableWidget::item:selected {{
                background: {styles.PRIMARY_LITE};
                color: {styles.PRIMARY};
            }}
            QTableWidget::item:hover:!selected {{
                background: #F0F4FF;
            }}
            QHeaderView::section {{
                background: {styles.BG_APP};
                color: {styles.TEXT_MUTED};
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1.5px;
                padding: 10px 14px;
                border: none;
                border-bottom: 1px solid {styles.BORDER};
            }}
            QHeaderView {{
                background: {styles.BG_APP};
                border-radius: 10px 10px 0 0;
            }}
        """)

        tl.addWidget(self.table)
        cl.addWidget(tw, 1)

        return content

    # ── Helpers ────────────────────────────────────────
    def _div(self) -> QFrame:
        d = QFrame()
        d.setObjectName("divider")
        d.setFixedHeight(1)
        d.setStyleSheet(f"QFrame#divider{{background:{styles.BORDER};}}")
        return d

    # ── Data ───────────────────────────────────────────
    def load_user(self, uid: int, uname: str):
        self.uid   = uid
        self.uname = uname
        self._user_lbl.setText(f"👤  {uname}")
        self._refresh()

    def _refresh(self):
        if not self.uid:
            return
        search  = self.search.text().strip()
        cat     = self.cat_combo.currentText()
        entries = self.db.get_entries(self.uid, search, cat)
        self._show_rows.clear()

        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(entries))

        for i, e in enumerate(entries):
            self.table.setRowHeight(i, 50)

            wi = QTableWidgetItem(e.website)
            wi.setData(Qt.UserRole, e.id)
            self.table.setItem(i, 0, wi)

            self.table.setItem(i, 1, QTableWidgetItem(e.username))

            pi = QTableWidgetItem("••••••••")
            pi.setData(Qt.UserRole, e.password)
            pi.setForeground(QColor(styles.PRIMARY))
            self.table.setItem(i, 2, pi)

            icon = CATEGORY_ICONS.get(e.category, "🔑")
            ci = QTableWidgetItem(f"{icon}  {e.category}")
            ci.setForeground(QColor(styles.TEXT_SECOND))
            self.table.setItem(i, 3, ci)

            ni = QTableWidgetItem(e.note or "—")
            ni.setForeground(QColor(styles.TEXT_MUTED))
            self.table.setItem(i, 4, ni)

            eye = QPushButton("👁")
            eye.setCursor(Qt.PointingHandCursor)
            eye.setStyleSheet(f"""
                QPushButton{{background:transparent;color:{styles.TEXT_MUTED};
                    font-size:16px;border:none;}}
                QPushButton:hover{{color:{styles.PRIMARY};}}
            """)
            eye.clicked.connect(lambda _, r=i: self._toggle_show(r))
            self.table.setCellWidget(i, 5, eye)

        self.table.setSortingEnabled(True)

        s = self.db.get_stats(self.uid)
        self.c_total.set_value(str(s["total"]))
        self.c_weak.set_value(str(s["weak"]))
        self.c_strong.set_value(str(s["strong"]))

    def _toggle_show(self, row: int):
        self._show_rows[row] = not self._show_rows.get(row, False)
        item = self.table.item(row, 2)
        if not item: return
        item.setText(
            item.data(Qt.UserRole) if self._show_rows[row] else "••••••••")
        btn = self.table.cellWidget(row, 5)
        if btn: btn.setText("🙈" if self._show_rows[row] else "👁")

    # ── Actions ────────────────────────────────────────
    def _on_add(self):
        dlg = EntryDialog(self, "เพิ่ม Password", VaultEntry(user_id=self.uid))
        if dlg.exec() and dlg.result_data:
            self.db.add_entry(dlg.result_data)
            self._refresh()

    def _on_edit(self):
        row = self.table.currentRow()
        if row < 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("CoreLock")
            msg.setText("กรุณาเลือกรายการที่ต้องการแก้ไข")
            msg.setStyleSheet("QPushButton { color: black; background-color: #f0f0f0; border: 1px solid #adadad; padding: 5px 15px; }")
            msg.exec()
            return
        eid     = self.table.item(row, 0).data(Qt.UserRole)
        entries = self.db.get_entries(self.uid)
        entry   = next((e for e in entries if e.id == eid), None)
        if not entry: return
        dlg = EntryDialog(self, "แก้ไข Password", entry)
        if dlg.exec() and dlg.result_data:
            self.db.update_entry(dlg.result_data)
            self._refresh()

    def _on_delete(self):
        row = self.table.currentRow()
        if row < 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("CoreLock")
            msg.setText("กรุณาเลือกรายการที่ต้องการลบ")
            
            msg.setStyleSheet("""
                QPushButton {
                    color: black; 
                    background-color: #f0f0f0; 
                    border: 1px solid #adadad;
                    padding: 5px 20px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #e1e1e1;
                }
            """)
            msg.exec_()
            return

        eid  = self.table.item(row, 0).data(Qt.UserRole)
        site = self.table.item(row, 0).text()
        
        confirm = QMessageBox(self)
        confirm.setIcon(QMessageBox.Question)
        confirm.setWindowTitle("ยืนยันการลบ")
        confirm.setText(f"ต้องการลบรายการ <b>{site}</b>?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setStyleSheet("QPushButton { color: black; border: 1px solid #adadad; padding: 5px; }")
        
        if confirm.exec_() == QMessageBox.Yes:
            self.db.delete_entry(eid)
            self._refresh()

    def _on_copy(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "CoreLock", "กรุณาเลือกรายการก่อนคัดลอก")
            return
        pw = self.table.item(row, 2).data(Qt.UserRole)
        QApplication.clipboard().setText(pw)
        QTimer.singleShot(30_000, QApplication.clipboard().clear)

    def reset(self):
        self.uid = 0; self.uname = ""
        self.table.setRowCount(0)
        self._show_rows.clear()
        self.search.clear()
        for c in [self.c_total, self.c_weak, self.c_strong]:
            c.set_value("0")

#  MAIN WINDOW

class MainWindow(QMainWindow):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.setWindowTitle("CoreLock — Password Manager")
        self.setMinimumSize(1100, 680)
        self._build_ui()

    def _build_ui(self):
        cw = QWidget()
        cw.setStyleSheet(f"background:{styles.BG_APP};")
        self.setCentralWidget(cw)
        lay = QVBoxLayout(cw)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        self.stack = QStackedWidget()
        lay.addWidget(self.stack)

        self._lp = LoginPage(self._handle_login, self._handle_register)
        self._vp = VaultPage(self.db, self._handle_logout)
        self.stack.addWidget(self._lp)
        self.stack.addWidget(self._vp)
        self.stack.setCurrentIndex(0)


    def _handle_login(self, username, password):
        uid, uname = self.db.verify_login(username, password)
        if uid:
            self._vp.load_user(uid, uname)
            self._lp.clear()
            self.stack.setCurrentIndex(1)
        else:
            self._lp.set_error("⚠  Username หรือ Password ไม่ถูกต้อง")

    def _handle_register(self):
        dlg = RegisterDialog(self)
        if dlg.exec() and dlg.result_data:
            d = dlg.result_data
            if self.db.username_exists(d["username"]):
                QMessageBox.warning(self, "CoreLock", "Username นี้ถูกใช้งานแล้ว")
                return
            if self.db.create_user(d["username"], d["password"], d["full_name"]):
                QMessageBox.information(
                    self, "CoreLock",
                    f"✅  สมัครสำเร็จ!\nเข้าสู่ระบบด้วย username: {d['username']}")
            else:
                QMessageBox.warning(self, "CoreLock", "เกิดข้อผิดพลาด กรุณาลองใหม่")

    def _handle_logout(self):
        self._vp.reset()
        self.stack.setCurrentIndex(0)