from carford_car_crm.db import get_db

def insert_new_person_in_db(first_name, last_name):
    db = get_db()
    db.execute(
        'INSERT INTO person (first_name, last_name)'
        ' VALUES (?, ?)',
        (first_name, last_name)
    )
    db.commit()


def get_number_of_vehicles_owned_by_person(owner_id):
    db = get_db()
    owned_vehicles = db.execute(
        'SELECT count(*) FROM vehicle WHERE owner_id = {}'.format(
            owner_id
        )
    ).fetchone()[0]

    return owned_vehicles


def set_sale_opportunity_to_false(owner_id):
    db = get_db()
    db.execute(
        'UPDATE person'
        ' SET sale_opportunity = 0'
        ' WHERE id = ?',
        owner_id
    )
    db.commit()


def insert_new_vehicle_in_db(owner_id, color, model):
    db = get_db()
    db.execute(
        'INSERT INTO vehicle (owner_id, color, model)'
        ' VALUES (?, ?, ?)',
        (owner_id, color, model)
    )
    db.commit()


def get_owner_id_options():
    db = get_db()
    owner_id_options = db.execute(
        'SELECT id FROM person'
    ).fetchall()

    owner_id_options = [str(x[0]) for x in owner_id_options]

    return owner_id_options


def validate_add_vehicle_form(form_parameters, owner_id, color, model):
    error = None

    if owner_id not in form_parameters['owner_id_options']:
        error = 'Invalid Owner Id.'
    elif color not in form_parameters['color_options']:
        error = 'Invalid Color.'
    elif model not in form_parameters['model_options']:
        error = 'Invalid Model.'

    return error