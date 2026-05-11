# ── Accent / Brand colors ──────────────────────────
PRIMARY      = "#4F46E5"   # Indigo
PRIMARY_DARK = "#3730A3"
PRIMARY_LITE = "#EEF2FF"
DANGER       = "#EF4444"
DANGER_LITE  = "#FEF2F2"
SUCCESS      = "#10B981"
WARNING      = "#F59E0B"

# ── Neutrals ───────────────────────────────────────
BG_APP       = "#F8F9FB"
BG_CARD      = "#FFFFFF"
BG_SIDEBAR   = "#FFFFFF"
BORDER       = "#E5E7EB"
BORDER_FOCUS = "#4F46E5"
TEXT_PRIMARY = "#111827"
TEXT_SECOND  = "#6B7280"
TEXT_MUTED   = "#9CA3AF"
TEXT_WHITE   = "#FFFFFF"


def global_qss() -> str:
    return f"""
/* ── Base ─────────────────────────────── */
* {{
    font-family: 'Segoe UI', 'SF Pro Text', 'Inter', sans-serif;
    font-size: 13px;
}}
QMainWindow, QWidget {{
    background-color: {BG_APP};
    color: {TEXT_PRIMARY};
}}
QDialog {{
    background-color: {BG_CARD};
    color: {TEXT_PRIMARY};
    border-radius: 16px;
}}

/* ── QMessageBox ──────────────────────── */
QMessageBox {{
    background-color: {BG_CARD};
}}
QMessageBox QLabel {{
    color: {TEXT_PRIMARY};
    background: transparent;
    font-size: 13px;
}}
QMessageBox QPushButton {{
    background: {PRIMARY};
    color: {TEXT_WHITE};
    border: none;
    border-radius: 8px;
    padding: 7px 22px;
    font-weight: 600;
    min-width: 80px;
}}
QMessageBox QPushButton:hover {{
    background: {PRIMARY_DARK};
}}

/* ── QToolTip ─────────────────────────── */
QToolTip {{
    background: {TEXT_PRIMARY};
    color: {TEXT_WHITE};
    border: none;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 12px;
}}

/* ── QScrollBar ───────────────────────── */
QScrollBar:vertical {{
    background: {BG_APP};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: #D1D5DB;
    border-radius: 4px;
    min-height: 28px;
}}
QScrollBar::handle:vertical:hover {{
    background: {PRIMARY};
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{ height: 0; }}

QScrollBar:horizontal {{
    background: {BG_APP};
    height: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: #D1D5DB;
    border-radius: 4px;
    min-width: 28px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {PRIMARY};
}}
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{ width: 0; }}

/* ── QTabWidget ───────────────────────── */
QTabWidget::pane {{
    border: 1.5px solid {BORDER};
    border-radius: 10px;
    background: {BG_CARD};
    top: -1px;
}}
QTabBar::tab {{
    background: transparent;
    color: {TEXT_MUTED};
    border: none;
    border-bottom: 2px solid transparent;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: 600;
}}
QTabBar::tab:selected {{
    color: {PRIMARY};
    border-bottom: 2px solid {PRIMARY};
}}
QTabBar::tab:hover:!selected {{
    color: {TEXT_SECOND};
}}

/* ── QComboBox ────────────────────────── */
QComboBox {{
    background: {BG_CARD};
    border: 1.5px solid {BORDER};
    border-radius: 10px;
    color: {TEXT_PRIMARY};
    font-size: 13px;
    padding: 0 14px;
    min-height: 42px;
    selection-background-color: {PRIMARY_LITE};
}}
QComboBox:focus {{
    border-color: {BORDER_FOCUS};
}}
QComboBox::drop-down {{
    border: none;
    width: 32px;
}}
QComboBox::down-arrow {{
    image: none;
    width: 0;
}}
QComboBox QAbstractItemView {{
    background: {BG_CARD};
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    color: {TEXT_PRIMARY};
    selection-background-color: {PRIMARY_LITE};
    selection-color: {PRIMARY};
    outline: 0;
    padding: 4px;
}}

/* ── QProgressBar ─────────────────────── */
QProgressBar {{
    background: #F3F4F6;
    border: none;
    border-radius: 6px;
    height: 10px;
    text-align: center;
    color: transparent;
}}
QProgressBar::chunk {{
    border-radius: 6px;
    background: {PRIMARY};
}}

/* ── QGroupBox ────────────────────────── */
QGroupBox {{
    border: 1.5px solid {BORDER};
    border-radius: 12px;
    margin-top: 16px;
    padding: 12px 8px 8px 8px;
    font-size: 10px;
    font-weight: 700;
    color: {TEXT_MUTED};
    letter-spacing: 1px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 0 6px;
    background: {BG_CARD};
    color: {TEXT_MUTED};
    font-size: 9px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}}

/* ── QLineEdit (global fallback) ──────── */
QLineEdit {{
    background: {BG_CARD};
    border: 1.5px solid {BORDER};
    border-radius: 10px;
    color: {TEXT_PRIMARY};
    font-size: 14px;
    padding: 0 14px;
    min-height: 44px;
    selection-background-color: {PRIMARY_LITE};
}}
QLineEdit:focus {{
    border-color: {BORDER_FOCUS};
    background: {BG_CARD};
}}
QLineEdit:read-only {{
    background: {BG_APP};
    color: {TEXT_SECOND};
}}

/* ── QTableWidget ─────────────────────── */
QTableWidget {{
    background: transparent;
    border: none;
    color: {TEXT_PRIMARY};
    font-size: 13px;
    gridline-color: transparent;
    outline: 0;
}}
QTableWidget::item {{
    padding: 10px 16px;
    border-bottom: 1px solid {BG_APP};
    background: {BG_CARD};
}}
QTableWidget::item:selected {{
    background: {PRIMARY_LITE};
    color: {PRIMARY};
}}
QTableWidget::item:hover:!selected {{
    background: #F9FAFB;
}}
QHeaderView::section {{
    background: {BG_APP};
    color: {TEXT_MUTED};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    padding: 12px 16px;
    border: none;
    border-bottom: 1.5px solid {BORDER};
    border-right: none;
    text-transform: uppercase;
}}
QHeaderView {{
    background: {BG_APP};
}}
"""

# ── Reusable widget stylesheets ────────────────────
def input_style() -> str:
    return f"""
    QLineEdit {{
        background: {BG_CARD};
        border: 1.5px solid {BORDER};
        border-radius: 10px;
        color: {TEXT_PRIMARY};
        font-size: 14px;
        padding: 0 16px;
        min-height: 48px;
        selection-background-color: {PRIMARY_LITE};
    }}
    QLineEdit:focus {{
        border-color: {BORDER_FOCUS};
    }}
    QLineEdit::placeholder {{
        color: {TEXT_MUTED};
    }}
    """

def btn_primary() -> str:
    return f"""
    QPushButton {{
        background: {PRIMARY};
        color: {TEXT_WHITE};
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.5px;
        border: none;
        border-radius: 10px;
        padding: 0 20px;
    }}
    QPushButton:hover {{
        background: {PRIMARY_DARK};
    }}
    QPushButton:pressed {{
        background: #312E81;
    }}
    QPushButton:disabled {{
        background: #E5E7EB;
        color: {TEXT_MUTED};
    }}
    """

def btn_secondary() -> str:
    return f"""
    QPushButton {{
        background: {BG_CARD};
        color: {TEXT_SECOND};
        font-size: 13px;
        font-weight: 600;
        border: 1.5px solid {BORDER};
        border-radius: 10px;
        padding: 0 20px;
    }}
    QPushButton:hover {{
        background: {BG_APP};
        color: {TEXT_PRIMARY};
        border-color: #9CA3AF;
    }}
    QPushButton:pressed {{
        background: #F3F4F6;
    }}
    """

def btn_danger() -> str:
    return f"""
    QPushButton {{
        background: {DANGER_LITE};
        color: {DANGER};
        font-size: 13px;
        font-weight: 600;
        border: 1.5px solid #FECACA;
        border-radius: 10px;
        padding: 0 20px;
    }}
    QPushButton:hover {{
        background: #FEE2E2;
        border-color: {DANGER};
    }}
    QPushButton:pressed {{
        background: #FECACA;
    }}
    """

def btn_ghost() -> str:
    return f"""
    QPushButton {{
        background: transparent;
        color: {TEXT_MUTED};
        font-size: 13px;
        font-weight: 600;
        border: 1.5px solid {BORDER};
        border-radius: 10px;
        padding: 0 16px;
    }}
    QPushButton:hover {{
        background: {BG_APP};
        color: {TEXT_PRIMARY};
    }}
    """

def sidebar_style() -> str:
    return f"""
    QFrame#sidebar {{
        background: {BG_CARD};
        border-right: 1.5px solid {BORDER};
    }}
    """

def card_style(accent: str = PRIMARY) -> str:
    return f"""
    QFrame {{
        background: {BG_CARD};
        border: 1.5px solid {BORDER};
        border-top: 3px solid {accent};
        border-radius: 12px;
    }}
    """