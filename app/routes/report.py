from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.transaction import TransactionModel

bp = Blueprint('report', __name__)

@bp.route('/history', methods=['GET'])
def history():
    """
    歷史紀錄
    """
    transactions = TransactionModel.get_all()
    return render_template('history.html', transactions=transactions)

@bp.route('/statistics', methods=['GET'])
def statistics():
    """
    分類統計
    """
    transactions = TransactionModel.get_all()
    
    # 計算各分類支出加總
    category_totals = {}
    for t in transactions:
        if t['type'] == 'expense':
            cat = t['category']
            category_totals[cat] = category_totals.get(cat, 0) + t['amount']
            
    # 準備給圖表的資料
    labels = list(category_totals.keys())
    data = list(category_totals.values())
    
    return render_template('statistics.html', labels=labels, data=data)

@bp.route('/transaction/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    """
    刪除特定紀錄
    """
    try:
        TransactionModel.delete(id)
        flash("紀錄已成功刪除", "success")
    except Exception as e:
        flash(f"刪除失敗: {str(e)}", "danger")
        
    return redirect(url_for('report.history'))
