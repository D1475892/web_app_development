from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.transaction import TransactionModel

bp = Blueprint('expense', __name__)

@bp.route('/expense', methods=['GET', 'POST'])
def expense():
    """
    新增支出:
    """
    if request.method == 'POST':
        amount_str = request.form.get('amount')
        category = request.form.get('category')
        transaction_date = request.form.get('transaction_date')
        
        # 簡易驗證
        if not amount_str or not category or not transaction_date:
            flash("所有欄位皆為必填！", "danger")
            return render_template('expense.html')
            
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("金額必須大於 0")
        except ValueError:
            flash("請輸入有效的金額數字（需大於 0）！", "danger")
            return render_template('expense.html')
            
        # 寫入資料庫
        try:
            TransactionModel.create('expense', amount, category, transaction_date)
            flash("支出新增成功！", "success")
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f"新增失敗: {str(e)}", "danger")
    
    return render_template('expense.html')
