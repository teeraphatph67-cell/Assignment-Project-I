import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor

from database import Database
from windows import MainWindow
import styles


def apply_light_palette(app: QApplication):
    app.setStyle("Fusion")
    pal = QPalette()

    mapping = {
        QPalette.Window:          styles.BG_APP,
        QPalette.WindowText:      styles.TEXT_PRIMARY,
        QPalette.Base:            styles.BG_CARD,
        QPalette.AlternateBase:   styles.BG_APP,
        QPalette.Text:            styles.TEXT_PRIMARY,
        QPalette.BrightText:      "#000000",
        QPalette.Button:          styles.BG_CARD,
        QPalette.ButtonText:      styles.TEXT_PRIMARY,
        QPalette.Highlight:       styles.PRIMARY,
        QPalette.HighlightedText: "#FFFFFF",
        QPalette.ToolTipBase:     "#1F2937",
        QPalette.ToolTipText:     "#FFFFFF",
        QPalette.PlaceholderText: styles.TEXT_MUTED,
        QPalette.Mid:             styles.BORDER,
        QPalette.Dark:            "#D1D5DB",
        QPalette.Shadow:          "#9CA3AF",
        QPalette.Link:            styles.PRIMARY,
        QPalette.LinkVisited:     "#7C3AED",
    }

    for role, hex_color in mapping.items():
        c = QColor(hex_color)
        pal.setColor(role, c)
        pal.setColor(QPalette.Disabled, role, c.lighter(115))

    app.setPalette(pal)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("CoreLock")
    app.setOrganizationName("OOP Project")
    app.setApplicationVersion("2.0")

    apply_light_palette(app)
    app.setStyleSheet(styles.global_qss())

    db = Database()

    win = MainWindow(db)
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
