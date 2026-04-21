from flask import Blueprint, render_template
from app.models.transaction import TransactionModel

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    首頁:
    1. 從 TransactionModel 撈取所有資料
    2. 計算總收入與總支出
    3. 計算總餘額 (總收入 - 總支出)
    4. 渲染 index.html 並將餘額帶入
    """
    transactions = TransactionModel.get_all()
    
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    balance = total_income - total_expense
    
    return render_template('index.html', balance=balance, total_income=total_income, total_expense=total_expense)
