from app import db


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(120))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    is_delete = db.Column(db.Integer, default=0)


class GroupUser(db.Model):
    __tablename__ = 'group_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)


class GroupConn(db.Model):
    __tablename__ = 'group_conn'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer)
    conn_id = db.Column(db.Integer)
