from app import db
from app.app_log import app_log
from app.models import DBConnection
from app.userManagement.models import ConnectionUser
from app.main.apirequest import request_post
import math
from app.common import Result
from flask import request, current_app
from concurrent.futures import ThreadPoolExecutor
import datetime
import asyncio
import requests
from app.workbench.models import OpenAiUsage, RelatedQuestions
from config import Config
from app.access_token import AccessToken
from app.main.dbexec import get_db_schema_imp, get_db_schema_imp_new

executor = ThreadPoolExecutor(3)


def create_db_connection(name, db_type, db_name, username, password, ip_address, port_number, ds_name, db_summary):
    try:
        db_connection = DBConnection(name=name, db_type=db_type, db_name=db_name, username=username, password=password,
                                     ip_address=ip_address, port_number=port_number, ds_name=ds_name,
                                     db_summary=db_summary, is_delete=0, state=1,
                                     create_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                     update_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        db.session.add(db_connection)
        db.session.commit()

        url = '/api/create_connection'
        data = {
            'conn_id': db_connection.id,
            'name': name,
            'db_type': db_type,
            'db_name': db_name
        }
        return request_post(url, data)
    except Exception as error:
        current_app.logger.error(error)
        return {'status': 1, 'error': f'{error}'}


def create_usage(portal_username, conn_id, user_id, user_question, query_type, total_tokens, prompt_tokens,
                 completion_tokens):
    # 保存usage记录
    usage = OpenAiUsage()
    usage.conn_id = conn_id
    usage.user_id = user_id
    usage.portal_username = portal_username
    usage.question_text = user_question
    usage.query_type = query_type
    usage.total_tokens = total_tokens
    usage.prompt_tokens = prompt_tokens
    usage.completion_tokens = completion_tokens
    nowDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    usage.create_time = nowDateTime
    usage.update_time = nowDateTime
    usage.is_delete = 0
    db.session.add(usage)
    db.session.commit()
    # 保存usage到admin端
    url = '/api/create_usage'
    data = {
        'conn_id': conn_id,
        'user_id': user_id,
        'portal_username': portal_username,
        'query_type': query_type,
        'question_text': user_question,
        'total_tokens': total_tokens,
        'prompt_tokens': prompt_tokens,
        'completion_tokens': completion_tokens,
        'is_delete': 0,
        'create_time': nowDateTime,
        'update_time': nowDateTime
    }
    return request_post(url, data)


def get_summary(requestData, conn_id):
    print('Get summary')
    result = get_db_schema_imp_new(requestData)
    db_schema = result['db_schema']
    data = {'database_schema': db_schema}
    api_url = Config.API_ROOT + "/get_db_summary"
    token = AccessToken().get_access_token()
    headers = {'Authorization': "Bearer {}".format(token)}
    response = requests.post(api_url, json=data, headers=headers)
    json = response.json()
    db_summary = json['result']
    try:
        from app import create_app
        app = create_app()
        with app.app_context():
            conn = DBConnection.query.filter_by(id=conn_id).first()
            conn.db_summary = db_summary
            db.session.commit()
    except Exception as error:
        current_app.logger.error(f'Update summary exception: {error}')
    print("Create usage")
    usageJson = json['usage']
    try:
        from app import create_app
        app = create_app()
        with app.app_context():
            create_usage(Config.API_USER_NAME, conn_id, requestData['user_id'], None, 2, usageJson['total_tokens'],
                         usageJson['prompt_tokens'],
                         usageJson['completion_tokens'])
    except Exception as err:
        current_app.logger.error(f'Create usage exception: {err}')


def create_db_connection_new(requestData, databaseFile, name, db_type, db_name, username, password, ip_address,
                             port_number, ds_name, db_summary):
    nowDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        db_connection = DBConnection(name=name, db_type=db_type, db_name=db_name, username=username, password=password,
                                     ip_address=ip_address, port_number=port_number, ds_name=ds_name,
                                     db_summary=db_summary, is_delete=0, state=1,
                                     create_time=nowDateTime,
                                     update_time=nowDateTime,
                                     database_file=databaseFile)
        db.session.add(db_connection)
        db.session.commit()

        if len(db_summary) == 0 or ' ' == db_summary:
            executor.submit(get_summary, requestData, db_connection.id)

        # if len(userIds) != 0:
        #     conn_id = db_connection.id
        #     for userId in userIds:
        #         connUser = ConnectionUser()
        #         connUser.user_id = userId
        #         connUser.conn_id = conn_id
        #         db.session.add(connUser)
        #         db.session.commit()

        url = '/api/create_connection'
        data = {
            'conn_id': db_connection.id,
            'name': name,
            'db_type': db_type,
            'db_name': db_name,
            'state': 1,
            'is_delete': 0,
            'create_time': nowDateTime,
            'update_time': nowDateTime
        }
        return request_post(url, data)
        # return {'status': 0}
    except Exception as error:
        current_app.logger.error(error)
        return {'status': 1, 'error': f'{error}'}


def create_relation_questions_new(userId, conn_id, question):
    nowDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        related_question = RelatedQuestions(user_id=userId, conn_id=conn_id, question=question, is_delete=0,
                                            create_time=nowDateTime,
                                            update_time=nowDateTime)
        db.session.add(related_question)
        db.session.commit()

        url = '/api/create_related_question'
        data = {
            'userId': userId,
            'conn_id': conn_id,
            'question': question,
            'create_time': nowDateTime,
            'update_time': nowDateTime
        }
        return request_post(url, data)
        # return {'status': 0}
    except Exception as error:
        current_app.logger.error(error)
        return {'status': 1, 'error': f'{error}'}


def get_db_connections():
    try:
        db_conns = DBConnection().query.all()
        connectionsJson = []
        for x in db_conns:
            connection = {
                'id': x.id,
                'name': x.name,
                'db_type': x.db_type,
                'username': x.username,
                'password': x.password,
                'ip_address': x.ip_address,
                'port_number': x.port_number,
                'ds_name': x.ds_name,
                'db_name': x.db_name,
                'db_summary': x.db_summary
            }
            connectionsJson.append(connection)

        return {'status': 0, 'result': connectionsJson}
    except Exception as error:
        return {'status': 1, 'error': f'{error}'}


def get_db_connections_new(dbType, page, start, size, state, keyword):
    try:
        # db_conns = DBConnection().query.all()
        if len(state) > 0:
            allCount = DBConnection().query.filter(DBConnection.name.like("%" + keyword + "%"),
                                                   keyword is not None).filter(
                DBConnection.state.in_(state)).filter_by(is_delete=0,
                                                         db_type=dbType).count()
            db_conns = DBConnection().query.filter(DBConnection.name.like("%" + keyword + "%"),
                                                   keyword is not None).filter(DBConnection.state.in_(state)).filter_by(
                is_delete=0,
                db_type=dbType).order_by(
                DBConnection.id.desc()).offset(
                start).limit(size)
        else:
            allCount = DBConnection().query.filter(DBConnection.name.like("%" + keyword + "%"),
                                                   keyword is not None).filter_by(is_delete=0, db_type=dbType).count()
            db_conns = DBConnection().query.filter(DBConnection.name.like("%" + keyword + "%"),
                                                   keyword is not None).filter_by(is_delete=0, db_type=dbType).order_by(
                DBConnection.id.desc()).offset(
                start).limit(size)
        connectionsJson = []
        for x in db_conns:
            connection = {
                'id': x.id,
                'name': x.name,
                'db_type': x.db_type,
                'username': x.username,
                'password': x.password,
                'ip_address': x.ip_address,
                'port_number': x.port_number,
                'ds_name': x.ds_name,
                'db_name': x.db_name,
                'db_summary': x.db_summary,
                'database_file': x.database_file,
                'state': x.state,
                'is_delete': x.is_delete,
                'create_time': x.create_time,
                'update_time': x.update_time
            }
            connectionsJson.append(connection)

        if len(connectionsJson) > 0:
            allPage = math.ceil(allCount / size)
        else:
            allPage = 0

        return Result.successWithPage(connectionsJson, allPage, page, allCount)
        # return Result.success({'totalPage': allPage, 'total': allCount, 'page': page, 'size': size,
        #                        'records': connectionsJson})
    except Exception as error:
        current_app.logger.error(error)
        return Result.common(400, error)


def update_db_connection(conn_id, name, db_type, db_name, username, password, ip_address, port_number, ds_name,
                         db_summary, database_file):
    try:
        db_conn = DBConnection().query.filter_by(id=conn_id).first()
        db_conn.name = name
        db_conn.db_type = db_type
        db_conn.db_name = db_name
        db_conn.username = username
        db_conn.password = password
        db_conn.ip_address = ip_address
        db_conn.port_number = port_number
        db_conn.ds_name = ds_name
        if len(db_summary) != 0 and db_summary != ' ' and db_summary != '':
            db_conn.db_summary = db_summary
        db_conn.database_file = database_file
        db_conn.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()

        url = '/api/update_connection'
        data = {
            'id': conn_id,
            'name': name,
            'db_type': db_type,
            'db_name': db_name
        }
        return request_post(url, data)
    except Exception as error:
        current_app.logger.error(error)
        return {'status': 1, 'error': f'{error}'}


def update_db_connection_state(conn_id, state):
    try:
        url = '/api/update_connection_state'
        data = {
            'id': conn_id,
            'state': state
        }
        return request_post(url, data)
    except Exception as error:
        current_app.logger.error(error)
        return {'status': 1, 'error': f'{error}'}


def delte_db_connection(conn_id):
    try:
        db_conn = DBConnection.query.filter_by(id=conn_id).first()
        db_conn.is_delete = 1
        db_conn.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()

        url = '/api/delete_connection'
        data = {
            'id': conn_id
        }
        return request_post(url, data)
    except Exception as error:
        current_app.logger.error(error)
        return {'status': 1, 'error': f'{error}'}
