# 🔐 CoreLock — Password Manager
### PySide6 + SQLite | OOP Design Pattern

---

## 📦 โครงสร้างโปรเจค

```
CoreLock/
├── main.py       ← Entry point (รันไฟล์นี้)
├── database.py   ← Database layer (SQLite CRUD)
├── models.py     ← OOP Models & Utility classes
├── styles.py     ← Light Theme QSS ทั้งหมด
├── dialogs.py    ← BaseDialog (abstract) + subclasses
└── windows.py    ← LoginPage, VaultPage, MainWindow
```

---

## 🚀 วิธีติดตั้งและรัน

```bash
pip install PySide6
cd CoreLock
python main.py
```

**บัญชีเริ่มต้น:**
- Username: `admin`
- Password: `admin1234`

---

## 🎓 OOP Concepts ที่ใช้

### 1. Inheritance (การสืบทอด)
```
BaseDialog (QDialog + ABC)
    ├── RegisterDialog   ← สืบทอด + override สำหรับหน้าสมัครสมาชิก
    └── EntryDialog      ← สืบทอด + override สำหรับเพิ่ม/แก้ไข password
```

### 2. Abstraction (การซ่อนรายละเอียด)
- `BaseDialog` กำหนด `@abstractmethod` สองตัว:
  - `_build_form()` — subclass ต้องสร้าง UI ของตัวเอง
  - `_on_accept()` — subclass ต้อง validate และรวบรวมข้อมูล
- ผู้ใช้ BaseDialog ไม่ต้องรู้ว่าข้างในทำงานอย่างไร

### 3. Encapsulation (การห่อหุ้มข้อมูล)
- `Database.__conn` → private attribute, เข้าถึงผ่าน method เท่านั้น
- `Database._hash()` → ซ่อน SHA-256 hashing logic
- `PasswordAnalyzer._password, _score, _color` → private, อ่านผ่าน property

### 4. Polymorphism (ความหลากหลาย)
- `_build_form()` ถูก override โดย `RegisterDialog` และ `EntryDialog` ต่างกัน
- `_on_accept()` ถูก override โดย `RegisterDialog` และ `EntryDialog` ต่างกัน

---

## 🧩 Widgets ที่ใช้ (หลากหลาย)

| Widget | ใช้ที่ | จุดประสงค์ |
|--------|--------|------------|
| `QMainWindow` | MainWindow | หน้าต่างหลัก |
| `QStackedWidget` | MainWindow | สลับระหว่าง Login/Vault |
| `QTableWidget` | VaultPage | แสดงรายการ passwords |
| `QLineEdit` | ทุก form | กรอกข้อมูล |
| `QPushButton` | ทุกหน้า | ปุ่มกด action |
| `QComboBox` | EntryDialog, VaultPage | เลือก category, filter |
| `QProgressBar` | EntryDialog, RegisterDialog | แสดงความแข็งแรง |
| `QGroupBox` | EntryDialog | จัดกลุ่ม options |
| `QLabel` | ทุกที่ | แสดงข้อความ |
| `QFrame` | ทุกที่ | จัดกลุ่ม layout |

---

## ✨ Features

- ✅ Login / Logout / สมัครสมาชิก
- ✅ เพิ่ม / แก้ไข / ลบ password entries
- ✅ Password strength meter (0–100 คะแนน)
- ✅ ค้นหา real-time (search bar)
- ✅ Filter by category (Social, Work, Finance…)
- ✅ Show/Hide password ใน table
- ✅ Copy to clipboard (auto-clear 30 วิ)
- ✅ Stats cards (ทั้งหมด / อ่อนแอ / แข็งแรง)
- ✅ Light theme สะอาด ทันสมัย
