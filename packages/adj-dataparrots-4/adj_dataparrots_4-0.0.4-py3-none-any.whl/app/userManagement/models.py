from app import db


class ConnectionUser(db.Model):
    __tablename__ = 'connection_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    conn_id = db.Column(db.Integer)
