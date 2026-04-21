from flask import Blueprint, request, render_template, redirect, url_for, flash
# from app.models.models import Event, Registration

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    HTTP GET
    撈取所有開放中的活動清單。
    :return: 渲染 index.html (包含活動串列)
    """
    pass

@main_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    """
    HTTP GET
    讀取單一活動的資訊與目前的報名人數，
    用以判斷是否鎖定表單 (已達 capacity_limit)。
    :param event_id: 活動的主鍵 ID
    :return: 渲染 event_detail.html 傳遞活動物件與是否額滿 Boolean
    """
    pass

@main_bp.route('/event/<int:event_id>/register', methods=['POST'])
def register(event_id):
    """
    HTTP POST
    負責接收學生提交的報名表單資料。
    安全機制：必須在寫入前做最後一次的報名總數清點防呆。
    :param event_id: 活動的主鍵 ID
    :return: 成功則重導向 event_success，失敗(額滿/錯誤)重導回原本網頁。
    """
    pass

@main_bp.route('/event/<int:event_id>/success')
def event_success(event_id):
    """
    HTTP GET
    提供報名成功的提示畫面，供學生截圖使用。
    :param event_id: 活動的主鍵 ID
    :return: 渲染 event_success.html
    """
    pass
