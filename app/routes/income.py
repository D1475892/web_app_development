from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.transaction import TransactionModel

bp = Blueprint('income', __name__)

@bp.route('/income', methods=['GET', 'POST'])
def income():
    """
    新增收入:
    """
    if request.method == 'POST':
        amount_str = request.form.get('amount')
        category = request.form.get('category')
        transaction_date = request.form.get('transaction_date')
        
        # 簡易驗證
        if not amount_str or not category or not transaction_date:
            flash("所有欄位皆為必填！", "danger")
            return render_template('income.html')
            
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("金額必須大於 0")
        except ValueError:
            flash("請輸入有效的金額數字（需大於 0）！", "danger")
            return render_template('income.html')
            
        # 寫入資料庫
        try:
            TransactionModel.create('income', amount, category, transaction_date)
            flash("收入新增成功！", "success")
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f"新增失敗: {str(e)}", "danger")
    
    return render_template('income.html')
