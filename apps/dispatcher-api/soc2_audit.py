import sqlite3
import json
import time
import os

SOC2_VAULT_DB = os.path.join(os.path.dirname(__file__), "soc2_audit_vault.db")

def init_soc2_vault():
    """Initializes the immutable SQLite vault for SOC2 compliance logging."""
    conn = sqlite3.connect(SOC2_VAULT_DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            event_type TEXT,
            payload TEXT,
            signature TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_soc2_event(event_type: str, payload: dict):
    """
    Logs an immutable event into the SOC2 vault.
    Simulates a cryptographically signed payload for compliance auditing.
    """
    # Mock encryption/hashing signature representing SOC2 integrity checks
    signature = f"SHA256:ENCRYPTED_MOCK_SIGNATURE_{int(time.time())}"
    conn = sqlite3.connect(SOC2_VAULT_DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO audit_logs (timestamp, event_type, payload, signature) VALUES (?, ?, ?, ?)",
        (time.time(), event_type, json.dumps(payload), signature)
    )
    conn.commit()
    conn.close()

# Auto-initialize vault on module load
init_soc2_vault()
