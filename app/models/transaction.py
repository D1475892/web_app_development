import sqlite3
import os

# 設定資料庫連線路徑 (基於應用程式執行位置)
DB_PATH = "instance/database.db"

def get_db_connection():
    """取得資料庫連線並設定 row_factory。若 instance 資料夾不存在會自行建立"""
    # 確保 instance 資料夾存在
    if not os.path.exists('instance'):
        os.makedirs('instance')
        
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 回傳 sqlite3.Row，允許以鍵值提取資料
    return conn

class TransactionModel:
    @staticmethod
    def create(type_, amount, category, transaction_date):
        """新增一筆交易紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO transactions (type, amount, category, transaction_date)
            VALUES (?, ?, ?, ?)
            ''',
            (type_, amount, category, transaction_date)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_all():
        """取得所有交易紀錄，依日期反序排列"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions ORDER BY transaction_date DESC, id DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(transaction_id):
        """根據 ID 取得單筆交易紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(transaction_id, type_, amount, category, transaction_date):
        """更新單筆交易紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE transactions
            SET type = ?, amount = ?, category = ?, transaction_date = ?
            WHERE id = ?
            ''',
            (type_, amount, category, transaction_date, transaction_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(transaction_id):
        """刪除單筆交易紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        conn.commit()
        conn.close()
