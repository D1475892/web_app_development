from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('income', __name__)

@bp.route('/income', methods=['GET', 'POST'])
def income():
    """
    新增收入:
    GET: 渲染 income.html 顯示表單
    POST: 取得表單內容 (amount, category, transaction_date)
          驗證資料是否合法，若非法則 flash 錯誤並回傳表單
          合法則透過 TransactionModel.create('income', ...) 存入資料庫
          寫入成功後重新導向至首頁 (main.index)
    """
    pass
