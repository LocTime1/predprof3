from flask import request, session, Blueprint, redirect, url_for
from flask import render_template
from flask_login import login_required, current_user
from db_func import add_field, get_all_clients, add_prize, get_prizes, update_prize, delete_prize, link_client_field,\
    get_all_fields, get_info_about_field, update_field
from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileField
import os


class CreatePrizeForm(FlaskForm):
    name_prize = StringField(validators=[DataRequired()])
    file = FileField("Файл", validators=[FileRequired()])
    desc = TextAreaField('Описание', validators=[DataRequired()])


admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
def admin_func_not_post():
    if current_user.is_admin == None:
        return redirect(url_for('client.client_func'))
    form = CreatePrizeForm()
    return render_template('admin.html', sl=get_all_fields(), sl_with_prizes=get_prizes(), form=form)


@admin.route('/admin', methods=['POST', 'GET'])
@login_required
def admin_func():
    if current_user.is_admin == None:
        return redirect(url_for('client.client_func'))
    if request.form.get('choise_client_btn'):
        num_hits = []
        id_clients = [int(i) for i in request.form.getlist('checkbox')]
        for i in get_all_clients():
            if request.form.get(f'btn {i[0]}'):
                num_hits.append(int(request.form.get(f'btn {i[0]}')))
        print('Размер таблицы -', session['size_pole'])
        print('Клетки с кораблями -', session['list_coords'])
        print('Номера призов в клетках с короблями -', session['name_prizes'])
        print('id пользователей к этой таблице -', id_clients)
        print('кол-во выстрелов у пользователей -', num_hits)
        if session['id_field'] == 0:
            add_field([session['size_pole'], session['name_prizes'], session['list_coords']])
            for el in range(len(id_clients)):
                link_client_field(id_clients[el], num_hits[el])
        else:
            update_field([session['id_field'], session['size_pole'], str(session['name_prizes']),
                          str(session['list_coords']), id_clients, num_hits])

    elif request.form.get('save_new_prize'):
        form = CreatePrizeForm()
        print(111)
        name, desc = form.name_prize.data, form.desc.data
        file = request.files[form.file.name]
        filename = file.filename
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        add_prize([filename, name, desc])
    elif request.form.get('save_prize'):
        print(int(request.form.get('save_prize')))
        name, desc, file = request.form.get('name_prize'), request.form.get('desc_prize'), request.files['file']
        filename = file.filename
        print(filename)
        file.save(os.path.join('static/prizes', filename))
        update_prize([int(request.form.get('save_prize')), filename, name, desc])

    elif request.form.get('delete_prize'):
        delete_prize(int(request.form.get('delete_prize')))
    session['id_field'] = 0
    form = CreatePrizeForm()
    return render_template('admin.html', sl=get_all_fields(), sl_with_prizes=get_prizes(), form=form)


@admin.route('/create_field')
@login_required
def create_field(): # начало создания поля
    if current_user.is_admin == None:
        return redirect(url_for('client.client_func'))
    session.clear()
    session['size_pole'] = 0
    session['list_coords'] = []
    session['name_prizes'] = []
    session['prizes'] = get_prizes()
    session['id_field'] = 0
    return render_template('create_pole.html', n=0, d=[])


@admin.route('/create_field', methods=['POST'])
@login_required
def create_field_post():
    if current_user.is_admin == None:
        return redirect(url_for('client.client_func'))
    if request.form.get('change_pole'): # изменить старое поле
        session['id_field'] = int(request.form.get('change_pole'))
        info_field = get_info_about_field(session['id_field'])
        session['size_pole'] = info_field[0]
        session['list_coords'] = info_field[2]
        session['name_prizes'] = info_field[1]
        session['prizes'] = get_prizes()
    elif request.form.get('size_pole'): # задать размер поля
        if int(request.form.get('size_pole')) == 0:
            return redirect(url_for('admin.create_field'))
        else:
            session['size_pole'] = int(request.form.get('size_pole'))
    elif request.form.get('set_prize'): # установка кораблика
        session['name_prizes'] = session['name_prizes'] + [int(request.form.get('set_prize'))]
    elif request.form.get('delete_ship'):
        req = request.form['delete_ship']
        n_3 = [int(i) for i in req.split()]
        ind = session['list_coords'].index(n_3)
        session['list_coords'] = session['list_coords'][:ind] + session['list_coords'][ind + 1:]
        session['name_prizes'] = session['name_prizes'][:ind] + session['name_prizes'][ind + 1:]
    print(session)
    return render_template('create_pole.html', n=session.get('size_pole'), d=session['list_coords'])


@admin.route('/set_prize', methods=['POST', 'GET'])
@login_required
def set_ship():
    if current_user.is_admin == None:
        return redirect(url_for('client.client_func'))
    if request.form.get('btn'):
        coords = [int(i) for i in request.form.get('btn').split()]
        session['list_coords'] = session['list_coords'] + [coords]
    elif request.form.get('change_prize'):
        req = request.form['change_prize']
        n_3 = [int(i) for i in req.split()]
        ind = session['list_coords'].index(n_3)
        session['name_prizes'] = session['name_prizes'][:ind] + session['name_prizes'][ind + 1:]
    return render_template('set_prize.html', sl=session['prizes'])


@admin.route('/choise_client', methods=['POST', 'GET'])
@login_required
def choice_clients():
    if current_user.is_admin == None:
        return redirect(url_for('client.client_func'))
    return render_template('choise_clients.html', spisok=get_all_clients())


@admin.route('/change_prize', methods=['POST', 'GET'])
@login_required
def change_prize():
    if current_user.is_admin == None:
        return redirect(url_for('client.client_func'))
    if request.method == 'POST':
        req = request.form['btn']
        n_3 = [int(i) for i in req.split()]
        ind = session['list_coords'].index(n_3)
        session['list_coords'] = session['list_coords'][:ind] + session['list_coords'][ind + 1:]
        session['name_prizes'] = session['name_prizes'][:ind] + session['name_prizes'][ind + 1:]
        return render_template('change_prize.html', n=req)


@admin.route('/create_prize')
@login_required
def create_prize():
    form = CreatePrizeForm()
    if current_user.is_admin == None:
        return redirect(url_for('client.client_func'))
    return render_template('create_prize.html', prize=[], idd='aaa', flag=False, form=form)


@admin.route('/create_prize', methods=['POST'])
@login_required
def create_prize_post():
    form = CreatePrizeForm()
    if current_user.is_admin == None:
        return redirect(url_for('client.client_func'))
    num_prize = int(request.form.get('update_prize'))
    print(get_prizes()[num_prize])
    return render_template('create_prize.html', prize=get_prizes()[num_prize], idd=num_prize, flag=True, form=form)


'''    if request.form.get('change_pole'):
        d = request.form.get('change_pole').split(" ! ")
        d[0] = int(d[0])
        d[1] = [int(i) for i in d[1].split(', ')]
        last = []
        for i in d[2].split('], ['):
            last.append([int(j) for j in i.split(', ')])
        del d[2]
        d.append(last)
        print(d)
        session['size_pole'] = d[0]
        session['list_coords'] = d[2]
        session['name_prices'] = d[1]
        session['prices'] = {}
        return render_template('create_pole.html', n=session.get('size_pole'), d=session['list_coords'])'''