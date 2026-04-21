from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# 初始化 db，會在 app.py 中註冊給 Flask App 使用
db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    capacity_limit = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # cascade 確保當活動刪除時，底下所有的報名紀錄自動刪除
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Event {self.id}: {self.name}>'
        
    @classmethod
    def create(cls, **kwargs):
        """新增活動一筆記錄"""
        try:
            event = cls(**kwargs)
            db.session.add(event)
            db.session.commit()
            return event
        except Exception as e:
            db.session.rollback()
            print(f"[Model Error] Failed to create Event: {e}")
            return None

    @classmethod
    def get_by_id(cls, event_id):
        """取得單筆記錄"""
        try:
            return cls.query.get(event_id)
        except Exception as e:
            print(f"[Model Error] Failed to get Event {event_id}: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有記錄"""
        try:
            return cls.query.order_by(cls.event_date.desc()).all()
        except Exception as e:
            print(f"[Model Error] Failed to get all Events: {e}")
            return []

    def update(self, **kwargs):
        """更新該筆記錄"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"[Model Error] Failed to update Event {self.id}: {e}")
            return False

    @classmethod
    def delete(cls, event_id):
        """根據 ID 刪除記錄"""
        try:
            event = cls.query.get(event_id)
            if event:
                db.session.delete(event)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"[Model Error] Failed to delete Event {event_id}: {e}")
            return False


class Registration(db.Model):
    __tablename__ = 'registration'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete="CASCADE"), nullable=False)
    student_id = db.Column(db.String(50), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    department_grade = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Registration {self.student_name} for Event {self.event_id}>'
        
    @classmethod
    def create(cls, **kwargs):
        """新增一筆學生的報名記錄"""
        try:
            reg = cls(**kwargs)
            db.session.add(reg)
            db.session.commit()
            return reg
        except Exception as e:
            db.session.rollback()
            print(f"[Model Error] Failed to create Registration: {e}")
            return None

    @classmethod
    def get_by_event(cls, event_id):
        """取得目標活動的所有報名記錄，並以報名時間排序"""
        try:
            return cls.query.filter_by(event_id=event_id).order_by(cls.created_at.asc()).all()
        except Exception as e:
            print(f"[Model Error] Failed to get Registrations for event {event_id}: {e}")
            return []

    @classmethod
    def get_registration_count(cls, event_id):
        """單獨統計目前該活動已報名人數 (防呆用)"""
        try:
            return cls.query.filter_by(event_id=event_id).count()
        except Exception as e:
            print(f"[Model Error] Failed to get Registration count for event {event_id}: {e}")
            return 0

    @classmethod
    def delete(cls, reg_id):
        """根據 ID 取消某個學生的報名紀錄"""
        try:
            reg = cls.query.get(reg_id)
            if reg:
                db.session.delete(reg)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"[Model Error] Failed to delete Registration {reg_id}: {e}")
            return False
