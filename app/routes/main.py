from flask import Blueprint, render_template

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
    pass
