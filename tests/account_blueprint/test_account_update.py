"""It contains tests for the account updating endpoint."""

from datetime import datetime

from flask import json
from ..util import create_user, create_tokens, get_unique_username


def test_update_account_with_data_well_formatted_returning_200_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(session, user.username)
    endpoint = '/account'
    data = {'username': get_unique_username(), 'password': "x123x"}
    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert int(response.json['data']['id']) == user.id
    assert response.json['data']['username'] == data['username']


def test_update_account_with_an_user_already_excluded_returning_404_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(session, user.username)
    # delete the user
    session.delete(user)
    session.commit()
    # request
    response = client.put('/account',
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    # asserts
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'not Found'


def test_update_account_without_data_returning_400_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(session, user.username)
    endpoint = '/account'
    response = client.put(endpoint,
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_update_account_with_empty_data_returning_400_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(session, user.username)
    endpoint = '/account'
    data = {}
    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {'username': 'must be filled'} in response.json['data']
    assert {'password': 'must be filled'} in response.json['data']


def test_update_account_without_username_returning_400_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(session, user.username)
    endpoint = '/account'
    data = {'password': 'x123x'}
    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {'username': 'must be filled'} in response.json['data']
    assert not {'password': 'must be filled'} in response.json['data']    


def test_update_account_without_password_returning_400_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(session, user.username)
    endpoint = '/account'
    data = {'username': 'user'}
    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert not {'username': 'must be filled'} in response.json['data']
    assert {'password': 'must be filled'} in response.json['data']


def test_update_account_with_a_existent_username_returning_400_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(session, user.username)
    endpoint = '/account'
    data = {'username': 'test', 'password': "123"}
    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {'username': 'is already in use.'} in response.json['data']