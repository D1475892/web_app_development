from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('report', __name__)

@bp.route('/history', methods=['GET'])
def history():
    """
    歷史紀錄:
    1. 從 TransactionModel.get_all() 取得所有紀錄依日期降冪排序
    2. 渲染 history.html，傳遞 transactions 陣列供模板迴圈渲染顯示
    """
    pass

@bp.route('/statistics', methods=['GET'])
def statistics():
    """
    分類統計:
    1. 從資料庫撈出所有的支出紀錄 (type_='expense')
    2. 將支出紀錄依據分類 (category) 進行金額加總
    3. 渲染 statistics.html 並將分類統計資料傳入 (可供繪製圖表)
    """
    pass

@bp.route('/transaction/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    """
    刪除特定紀錄:
    1. 接收 POST 請求，呼叫 TransactionModel.delete(id)
    2. 刪除完成後，重新導向回 /history 歷史列表
    """
    pass
