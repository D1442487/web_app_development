from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models.models import Event, Registration
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    HTTP GET
    撈取所有開放中的活動清單。
    :return: 渲染 index.html (包含活動串列)
    """
    events = Event.get_all()
    # 我們可以初步計算每個活動目前的報名人數，方便在首頁一併呈現給學生看
    event_stats = []
    for evt in events:
        count = Registration.get_registration_count(evt.id)
        event_stats.append({
            'event': evt,
            'current_count': count,
            'is_full': count >= evt.capacity_limit
        })
        
    return render_template('index.html', event_stats=event_stats)

@main_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    """
    HTTP GET
    讀取單一活動的資訊與目前的報名人數，用以判斷是否鎖定表單。
    """
    event = Event.get_by_id(event_id)
    if not event:
        flash("找不到該活動！", "error")
        return redirect(url_for('main.index'))
        
    current_count = Registration.get_registration_count(event_id)
    is_full = current_count >= event.capacity_limit
    
    return render_template('event_detail.html', event=event, current_count=current_count, is_full=is_full)

@main_bp.route('/event/<int:event_id>/register', methods=['POST'])
def register(event_id):
    """
    HTTP POST
    負責接收學生提交的報名表單資料，並進行嚴格防呆。
    """
    event = Event.get_by_id(event_id)
    if not event:
        flash("報名失敗：活動不存在", "error")
        return redirect(url_for('main.index'))

    # 安全機制 1：在寫入前做最後一次的報名總數清點防呆
    current_count = Registration.get_registration_count(event_id)
    if current_count >= event.capacity_limit:
        flash("很遺憾，這場活動剛剛額滿了！", "error")
        return redirect(url_for('main.event_detail', event_id=event_id))

    # 安全機制 2：基本輸入驗證
    student_id = request.form.get('student_id', '').strip()
    student_name = request.form.get('student_name', '').strip()
    department_grade = request.form.get('department_grade', '').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()

    if not all([student_id, student_name, department_grade, phone, email]):
        flash("所有欄位都是必填的喔！請補齊資料。", "error")
        return redirect(url_for('main.event_detail', event_id=event_id))

    # 將資料寫入 DB
    reg_data = {
        'event_id': event_id,
        'student_id': student_id,
        'student_name': student_name,
        'department_grade': department_grade,
        'phone': phone,
        'email': email
    }
    
    new_reg = Registration.create(**reg_data)
    
    if new_reg:
        flash("報名成功！", "success")
        return redirect(url_for('main.event_success', event_id=event_id))
    else:
        flash("系統發生異常，請稍後再試或聯繫主辦方。", "error")
        return redirect(url_for('main.event_detail', event_id=event_id))

@main_bp.route('/event/<int:event_id>/success')
def event_success(event_id):
    """
    HTTP GET
    提供報名成功的提示畫面供學生確認。
    """
    event = Event.get_by_id(event_id)
    if not event:
        return redirect(url_for('main.index'))
        
    return render_template('event_success.html', event=event)
