import pytest

from carford_car_crm.db import get_db


def test_index_view_logged_out(client):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data


def test_index_view_logged_in(client, auth):
    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'Add Vehicle' in response.data
    assert b'Add Person' in response.data


def test_get_add_person_logged_out(client):
    response = client.get('/add_person')
    expected_redirect_text = b'You should be redirected automatically to target URL: <a href="/auth/login">/auth/login</a>'
    assert expected_redirect_text in response.data


def test_get_add_person_logged_in(client, auth):
    auth.login()
    response = client.get('/add_person')
    assert b'First Name' in response.data
    assert b'Last Name' in response.data
    assert b'Submit' in response.data


def test_post_add_person_logged_out(client, app):
    form_data = {
        'first_name': 'Luke',
        'last_name': 'Skytester'
    }
    client.post('/add_person', data=form_data)

    with app.app_context():
        assert get_db().execute(
            "select * from person where last_name = 'Skytester'",
        ).fetchone() is None


def test_post_add_person_logged_in(client, auth, app):
    auth.login()
    form_data = {
        'first_name': 'Luke',
        'last_name': 'Skytester'
    }
    client.post('/add_person', data=form_data)

    with app.app_context():
        assert get_db().execute(
            "select * from person where last_name = 'Skytester'",
        ).fetchone() is not None


def test_get_add_vehicle_logged_out(client):
    response = client.get('/add_vehicle')
    expected_redirect_text = b'You should be redirected automatically to target URL: <a href="/auth/login">/auth/login</a>'
    assert expected_redirect_text in response.data


def test_get_add_vehicle_logged_in(client, auth):
    auth.login()
    response = client.get('/add_vehicle')
    assert b'Owner ID' in response.data
    assert b'Color' in response.data
    assert b'Model' in response.data
    assert b'Submit' in response.data


def test_post_add_vehicle_logged_out_with_good_form_data(client, app):
    form_data = {
        'owner_id': 1,
        'color': 'yellow',
        'model': 'convertible'
    }
    client.post('/add_vehicle', data=form_data)

    with app.app_context():
        assert get_db().execute(
            "select * from vehicle where owner_id = '1' and color = 'blue' and model = 'convertible'",
        ).fetchone() is None


def test_post_add_vehicle_logged_in_with_good_form_data(client, auth, app):
    auth.login()
    form_data = {
        'owner_id': 1,
        'color': 'yellow',
        'model': 'convertible'
    }
    client.post('/add_vehicle', data=form_data)

    with app.app_context():
        assert get_db().execute(
            "select * from vehicle where owner_id = '1' and color = 'yellow' and model = 'convertible'",
        ).fetchone() is not None


def test_post_add_vehicle_logged_in_with_bad_form_owner_id_data(client, auth, app):
    auth.login()
    form_data = {
        'owner_id': 0,
        'color': 'yellow',
        'model': 'convertible'
    }
    response = client.post('/add_vehicle', data=form_data)

    assert b'Invalid Owner Id.' in response.data

    with app.app_context():
        assert get_db().execute(
            "select * from vehicle where owner_id = '0' and color = 'yellow' and model = 'convertible'",
        ).fetchone() is None


def test_post_add_vehicle_logged_in_with_bad_form_color_data(client, auth, app):
    auth.login()
    form_data = {
        'owner_id': 1,
        'color': 'red',
        'model': 'convertible'
    }
    response = client.post('/add_vehicle', data=form_data)

    assert b'Invalid Color.' in response.data

    with app.app_context():
        assert get_db().execute(
            "select * from vehicle where owner_id = '1' and color = 'red' and model = 'convertible'",
        ).fetchone() is None


def test_post_add_vehicle_logged_in_with_bad_form_model_data(client, auth, app):
    auth.login()
    form_data = {
        'owner_id': 1,
        'color': 'yellow',
        'model': 'truck'
    }
    response = client.post('/add_vehicle', data=form_data)

    assert b'Invalid Model.' in response.data

    with app.app_context():
        assert get_db().execute(
            "select * from vehicle where owner_id = '1' and color = 'yellow' and model = 'truck'",
        ).fetchone() is None


def test_add_3_vehicles_for_a_person_changes_sale_opportunity_flag(client, auth, app):
    with app.app_context():
        previous_sale_opportunity = get_db().execute(
            "select * from person where id = '2'",
        ).fetchone()
        assert previous_sale_opportunity['sale_opportunity'] == 1

    auth.login()
    form_data = {
        'owner_id': 2,
        'color': 'yellow',
        'model': 'convertible'
    }
    client.post('/add_vehicle', data=form_data)
    client.post('/add_vehicle', data=form_data)
    client.post('/add_vehicle', data=form_data)

    with app.app_context():
        new_sale_opportunity = get_db().execute(
            "select sale_opportunity from person where id = '2'",
        ).fetchone()
        assert new_sale_opportunity['sale_opportunity'] == 0


def test_add_more_than_3_vehicles_for_a_person(client, auth, app):
    auth.login()
    form_data = {
        'owner_id': 3,
        'color': 'gray',
        'model': 'sedan'
    }
    client.post('/add_vehicle', data=form_data)
    client.post('/add_vehicle', data=form_data)
    client.post('/add_vehicle', data=form_data)

    response = client.post('/add_vehicle', data=form_data)

    assert b'This Person already owns the maximum amount of vehicles possible' in response.data

    with app.app_context():
        count_vehicles = get_db().execute(
            "select count(*) from vehicle where owner_id = '3'",
        ).fetchone()
        assert count_vehicles['count(*)'] == 3
