from flask import Blueprint, request, render_template, redirect, url_for, flash, Response
# from app.models.models import Event, Registration

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def dashboard():
    """
    HTTP GET
    主辦方控制中心首頁，顯示系統中所有的活動與報名狀況簡介。
    :return: 渲染 admin/dashboard.html
    """
    pass

@admin_bp.route('/event/new', methods=['GET', 'POST'])
def create_event():
    """
    HTTP GET / POST
    - GET: 顯示一個空白的新增活動表單頁面。
    - POST: 接收並驗證後端資料，呼叫 Event.create 存檔，然後重導向到 Dashboard。
    :return: GET: 渲染 admin/event_form.html / POST: Redirect
    """
    pass

@admin_bp.route('/event/<int:event_id>/registrations')
def view_registrations(event_id):
    """
    HTTP GET
    列出目標活動所有的報名清單 (學號、姓名等個資明細)。
    :param event_id: 目標活動的主鍵 ID
    :return: 渲染 admin/registrations.html
    """
    pass

@admin_bp.route('/event/<int:event_id>/export')
def export_csv(event_id):
    """
    HTTP GET
    將報名清單轉換成 CSV 字串格式，並將 Response Mimetype 設為屬性下載。
    :param event_id: 目標活動的主鍵 ID
    :return: flask.Response (讓瀏覽器下載檔案)
    """
    pass

@admin_bp.route('/event/<int:event_id>/close', methods=['POST'])
def close_event(event_id):
    """
    HTTP POST
    擴充的防呆功能：若主辦方覺得人數已夠或場地生變，可在此強制把活動可報名人數歸零。
    :param event_id: 目標活動的主鍵 ID
    :return: 重導向回原本的活動或 Dashboard 頁面
    """
    pass
