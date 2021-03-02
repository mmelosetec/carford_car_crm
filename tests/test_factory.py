from carford_car_crm import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing