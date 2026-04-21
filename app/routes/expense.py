from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('expense', __name__)

@bp.route('/expense', methods=['GET', 'POST'])
def expense():
    """
    新增支出:
    GET: 渲染 expense.html 顯示表單
    POST: 取得表單內容 (amount, category, transaction_date)
          驗證資料是否合法，若非法則 flash 錯誤並回傳表單
          合法則透過 TransactionModel.create('expense', ...) 存入資料庫
          寫入成功後重新導向至首頁 (main.index)
    """
    pass
