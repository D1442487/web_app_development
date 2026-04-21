from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# 初始化 db，稍後會在 app.__init__.py 註冊給 Flask App 使用
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

    # 設置 Relationship，方便透過 Event.registrations 取得所有報名者
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Event {self.id}: {self.name}>'
        
    @classmethod
    def create(cls, **kwargs):
        """新增活動"""
        event = cls(**kwargs)
        db.session.add(event)
        db.session.commit()
        return event

    @classmethod
    def get_by_id(cls, event_id):
        """根據 ID 取得活動"""
        return cls.query.get(event_id)

    @classmethod
    def get_all(cls):
        """取得所有活動，以日期排序"""
        return cls.query.order_by(cls.event_date.desc()).all()


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
        """新增報名紀錄並寫入資料庫"""
        reg = cls(**kwargs)
        db.session.add(reg)
        db.session.commit()
        return reg

    @classmethod
    def get_by_event(cls, event_id):
        """取得單一活動的所有報名名單"""
        return cls.query.filter_by(event_id=event_id).all()

    @classmethod
    def get_registration_count(cls, event_id):
        """統計目前此活動的報名人數，用於防呆"""
        return cls.query.filter_by(event_id=event_id).count()
