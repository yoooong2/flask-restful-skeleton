from datetime import datetime

from flask import json
from util import create_user


def test_user_delete_with_all_data_passed_returning_200_status_code(client, session):
    user = create_user(session)
    endpoint = '/users/{}'.format(user.id)
    response = client.delete(endpoint)
    assert response.status_code == 201
    response = client.get(endpoint)
    assert response.status_code == 404