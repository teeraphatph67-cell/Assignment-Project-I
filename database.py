"""
ใช้ SQLite + Encapsulation (private __conn)

OOP:
  • Encapsulation — __conn เป็น private
  • Single Responsibility — แค่จัดการ DB เท่านั้น
"""

import sqlite3
import hashlib
from models import VaultEntry, CATEGORIES


class Database:
    """
    จัดการ SQLite ทั้งหมด
    __conn ถูกซ่อน → เข้าถึงผ่าน public method เท่านั้น
    """

    DB_FILE = "corelock.db"

    def __init__(self):
        self.__conn = sqlite3.connect(self.DB_FILE)
        self.__conn.row_factory = sqlite3.Row
        self.__conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()
        self._seed_admin()

    # ── private ─────────────────────────────────────────
    def _create_tables(self):
        self.__conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT    UNIQUE NOT NULL,
                password    TEXT    NOT NULL,
                full_name   TEXT    DEFAULT '',
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS vault (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                website     TEXT    NOT NULL,
                username    TEXT    NOT NULL,
                password    TEXT    NOT NULL,
                category    TEXT    DEFAULT 'Other',
                note        TEXT    DEFAULT '',
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        self.__conn.commit()

    def _seed_admin(self):
        """สร้าง default admin"""
        count = self.__conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count == 0:
            self.create_user("admin", "admin1234", "Administrator")

    @staticmethod
    def _hash(password: str) -> str:
        """SHA-256 hashing (Encapsulation)"""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def _execute(self, sql: str, params: tuple = ()):
        """helper สำหรับ INSERT / UPDATE / DELETE"""
        self.__conn.execute(sql, params)
        self.__conn.commit()

    # ══════════════════════════════════════════════════
    #  USER MANAGEMENT
    # ══════════════════════════════════════════════════
    def create_user(self, username: str, password: str,
                    full_name: str = "") -> bool:
        """สร้าง user ใหม่ คืน True ถ้าสำเร็จ"""
        try:
            self._execute(
                "INSERT INTO users (username, password, full_name) VALUES (?,?,?)",
                (username.strip(), self._hash(password), full_name.strip())
            )
            return True
        except sqlite3.IntegrityError:
            return False   # username ซ้ำ

    def get_user_by_username(self, username: str):
        return self.__conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username.strip(),)
        ).fetchone()

    def verify_login(self, username: str, password: str):
        """คืน user_id ถ้า login ถูกต้อง, None ถ้าผิด"""
        row = self.get_user_by_username(username)
        if row and row["password"] == self._hash(password):
            return row["id"], row["full_name"] or row["username"]
        return None, None

    def username_exists(self, username: str) -> bool:
        return self.get_user_by_username(username) is not None

    def change_password(self, user_id: int,
                        old_pw: str, new_pw: str) -> bool:
        row = self.__conn.execute(
            "SELECT password FROM users WHERE id=?", (user_id,)
        ).fetchone()
        if row and row["password"] == self._hash(old_pw):
            self._execute(
                "UPDATE users SET password=? WHERE id=?",
                (self._hash(new_pw), user_id)
            )
            return True
        return False

    # ══════════════════════════════════════════════════
    #  VAULT CRUD
    # ══════════════════════════════════════════════════
    def get_entries(self, user_id: int,
                    search: str = "",
                    category: str = "All") -> list[VaultEntry]:
        cat_clause = "AND category = ?" if category != "All" else ""
        sql = f"""
            SELECT * FROM vault
            WHERE user_id = ?
              AND (
                  website  LIKE ? OR
                  username LIKE ? OR
                  note     LIKE ?
              )
              {cat_clause}
            ORDER BY website COLLATE NOCASE
        """
        like   = f"%{search}%"
        params = (user_id, like, like, like)
        if category != "All":
            params += (category,)

        rows = self.__conn.execute(sql, params).fetchall()
        return [
            VaultEntry(
                id=r["id"], user_id=r["user_id"],
                website=r["website"], username=r["username"],
                password=r["password"], category=r["category"],
                note=r["note"] or "", created_at=r["created_at"]
            )
            for r in rows
        ]

    def add_entry(self, entry: VaultEntry):
        self._execute(
            "INSERT INTO vault (user_id,website,username,password,category,note)"
            " VALUES (?,?,?,?,?,?)",
            (entry.user_id, entry.website, entry.username,
             entry.password, entry.category, entry.note)
        )

    def update_entry(self, entry: VaultEntry):
        self._execute(
            "UPDATE vault SET website=?,username=?,password=?,"
            "category=?,note=? WHERE id=?",
            (entry.website, entry.username, entry.password,
             entry.category, entry.note, entry.id)
        )

    def delete_entry(self, entry_id: int):
        self._execute("DELETE FROM vault WHERE id=?", (entry_id,))

    def count_entries(self, user_id: int) -> int:
        return self.__conn.execute(
            "SELECT COUNT(*) FROM vault WHERE user_id=?",
            (user_id,)
        ).fetchone()[0]

    # ══════════════════════════════════════════════════
    #  STATS / ANALYTICS
    # ══════════════════════════════════════════════════
    def get_stats(self, user_id: int) -> dict:
        """คำนวณสถิติ vault ของ user"""
        from models import PasswordAnalyzer
        rows = self.__conn.execute(
            "SELECT password, category FROM vault WHERE user_id=?",
            (user_id,)
        ).fetchall()

        total    = len(rows)
        weak     = 0
        cats: dict[str, int] = {}
        scores   = []

        for r in rows:
            ana = PasswordAnalyzer(r["password"])
            scores.append(ana.score)
            if ana.score < 50:
                weak += 1
            c = r["category"]
            cats[c] = cats.get(c, 0) + 1

        avg_score = round(sum(scores) / len(scores)) if scores else 0

        return {
            "total":     total,
            "weak":      weak,
            "strong":    total - weak,
            "avg_score": avg_score,
            "cats":      cats,
        }
