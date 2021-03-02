from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from carford_car_crm.auth import login_required
from carford_car_crm.crm_app_constants import (
    VEHICLE_COLOR_OPTIONS, VEHICLE_MODEL_OPTIONS,
    VEHICLE_OWNERSHIP_LIMIT_PER_PERSON
)
from carford_car_crm.crm_app_utils import (
    insert_new_person_in_db, insert_new_vehicle_in_db,
    get_owner_id_options, get_number_of_vehicles_owned_by_person,
    set_sale_opportunity_to_false, validate_add_vehicle_form
)


bp = Blueprint('crm_app', __name__)


@bp.route('/')
def index():
    return render_template('crm_app/index.html')


@bp.route('/add_person', methods=('GET', 'POST'))
@login_required
def add_person():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        error = None

        if not first_name or not last_name:
            error = 'First Name and Last Name are required fields.'

        if error is not None:
            flash(error)
        else:
            insert_new_person_in_db(first_name, last_name)
            return redirect(url_for('crm_app.index'))

    return render_template('crm_app/add_person.html')


@bp.route('/add_vehicle', methods=('GET', 'POST'))
@login_required
def add_vehicle():
    owner_id_options = get_owner_id_options()

    form_parameters = {
        'owner_id_options': owner_id_options,
        'color_options': VEHICLE_COLOR_OPTIONS,
        'model_options': VEHICLE_MODEL_OPTIONS
    }

    if request.method == 'POST':
        owner_id = request.form['owner_id']
        color = request.form['color']
        model = request.form['model']

        error = validate_add_vehicle_form(
            form_parameters, owner_id, color, model
        )

        owned_vehicles = get_number_of_vehicles_owned_by_person(owner_id)

        if owned_vehicles >= VEHICLE_OWNERSHIP_LIMIT_PER_PERSON:
            error = 'This Person already owns the maximum amount of vehicles possible ({}).'.format(
                VEHICLE_OWNERSHIP_LIMIT_PER_PERSON
            )
        if owned_vehicles == VEHICLE_OWNERSHIP_LIMIT_PER_PERSON - 1:
            set_sale_opportunity_to_false(owner_id)

        if error is not None:
            flash(error)
        else:
            insert_new_vehicle_in_db(owner_id, color, model)
            return redirect(url_for('crm_app.index'))

    return render_template('crm_app/add_vehicle.html', data=form_parameters)