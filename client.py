from flask import request, session, Blueprint, redirect, url_for
from flask import render_template
from flask_login import current_user
from db_func import get_client_fields, get_info_about_field, update_hits_client, get_cnt_hits,\
    add_prize_to_client, get_prizes_to_client

client = Blueprint('client', __name__)


@client.route('/client')
def client_func():
    session['id_field'] = 0
    session['hits'] = []
    return render_template('client.html', sl=get_client_fields(current_user.id),
                           lst_with_prizes=get_prizes_to_client(current_user.id))


@client.route('/client', methods=['POST'])
def client_func_post():
    if request.form.get('win'):
        a = [int(i) for i in request.form.get('win').split()]
        info_field = get_info_about_field(session['id_field'])
        ind = info_field[2].index(a)
        prize = info_field[1][ind]
        add_prize_to_client(current_user.id, prize)
        session['hits'] = session['hits'] + [a]
        update_hits_client(session['id_field'], current_user.id, session['hits'])
    session['id_field'] = 0
    session['hits'] = []
    return render_template('client.html', sl=get_client_fields(current_user.id),
                           lst_with_prizes=get_prizes_to_client(current_user.id))


@client.route('/open_field', methods=['POST'])
def open_field():
    print(request.form.get('win'))
    if session['id_field'] == 0:
        session['id_field'] = int(request.form.get('open_field'))
        lst = get_info_about_field(session['id_field'])
        session['hits'] = lst[3]
    if request.form.get('lose'):
        a = [int(i) for i in request.form.get('lose').split()]
        session['hits'] = session['hits'] + [a]
        update_hits_client(session['id_field'], current_user.id, session['hits'])
    if request.form.get('win'):
        a = [int(i) for i in request.form.get('win').split()]
        info_field = get_info_about_field(session['id_field'])
        ind = info_field[2].index(a)
        prize = info_field[1][ind]
        add_prize_to_client(current_user.id, prize)
        session['hits'] = session['hits'] + [a]
        update_hits_client(session['id_field'], current_user.id, session['hits'])
    lst = get_info_about_field(session['id_field'])
    cnt_hit = get_cnt_hits(current_user.id, session['id_field'])
    print(lst)
    return render_template('open_field.html', n=lst[0], d=lst[2], hits=session['hits'], cnt_hit=cnt_hit, lst_info=lst)
