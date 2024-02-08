from models import db, Fields, Clients, Prizes, FieldsAndClients, ClientAndPrizes


def add_client(lst):
    new_client = Clients(email=lst[0], name=lst[1], password=lst[2])
    db.session.add(new_client)
    db.session.commit()


def add_field(lst):
    field = Fields(size=lst[0], name_prize=str(lst[1]), location_ship=str(lst[2]), hits_client='')
    db.session.add(field)
    db.session.commit()


def add_prize(lst):
    prize = Prizes(file=lst[0], name=lst[1], description=lst[2])
    db.session.add(prize)
    db.session.commit()


def get_all_clients():
    clients = Clients.query.all()
    return [[i.id, i.email] for i in clients if i.is_admin != 'True']


def get_prizes():
    prizes = Prizes.query.all()
    sl = {}
    for i in prizes:
        sl[i.id] = [i.file, i.name, i.description]
    return sl


def update_prize(lst):
    prize = Prizes.query.filter_by(id=lst[0]).first()
    prize.file = lst[1]
    prize.name = lst[2]
    prize.description = lst[3]
    db.session.commit()


def delete_prize(idd):
    prize = Prizes.query.filter_by(id=idd).first()
    db.session.delete(prize)
    db.session.commit()


def get_last_id_field():
    fields = Fields.query.all()
    return fields[-1].id


def link_client_field(id_client, num_hit, id_field=''):
    if id_field == '':
        id_field = get_last_id_field()
    new_entry = FieldsAndClients(id_client=id_client, id_field=id_field, numbers_hits=num_hit)
    db.session.add(new_entry)
    db.session.commit()


def get_all_fields():
    fields = Fields.query.all()
    sl = {}
    for i in fields:
        print(i.name_prize)
        if i.name_prize != '[]':
            name_prize = [int(j) for j in i.name_prize[1:-1].split(', ')]
        else:
            name_prize = []
        if i.location_ship != '[]':
            location_ship = [[int(q) for q in j.split(', ')] for j in i.location_ship[2:-2].split('], [')]
        else:
            location_ship = []
        if i.hits_client == '':
            hits_client = ''
            sl[i.id] = [i.size, name_prize, location_ship, hits_client]
    return sl


def get_info_about_field(id_field):
    i = Fields.query.filter_by(id=id_field).first()
    if i.name_prize != '[]':
        name_prize = [int(j) for j in i.name_prize[1:-1].split(', ')]
    else:
        name_prize = []
    if i.location_ship != '[]':
        location_ship = [[int(q) for q in j.split(', ')] for j in i.location_ship[2:-2].split('], [')]
    else:
        location_ship = []
    if i.hits_client != '':
        hits_client = [[int(q) for q in j.split(', ')] for j in i.hits_client[2:-2].split('], [')]
    else:
        hits_client = []
    return [i.size, name_prize, location_ship, hits_client]


def update_field(lst):
    field = Fields.query.filter_by(id=lst[0]).first()
    field.size = lst[1]
    field.name_prize = lst[2]
    field.location_ship = lst[3]
    field_and_client = FieldsAndClients.query.filter_by(id_field=lst[0]).all()
    for i in field_and_client:
        db.session.delete(i)
    for i in range(len(lst[4])):
        link_client_field(lst[4][i], lst[5][i], lst[0])
    db.session.commit()


def update_hits_client(id_field, id_client, lst_hits):
    field = Fields.query.filter_by(id=id_field).first()
    field.hits_client = str(lst_hits)
    field_and_client = FieldsAndClients.query.filter_by(id_client=id_client).all()
    for i in field_and_client:
        if i.id_field == id_field:
            i.numbers_hits = i.numbers_hits - 1
            db.session.commit()
            break


def get_client_fields(id_client):
    fields = FieldsAndClients.query.filter_by(id_client=id_client).all()
    sl = {}
    for i in fields:
        sl[i.id_field] = get_info_about_field(i.id_field)
    print(sl)
    return sl


def get_cnt_hits(id_client, id_field):
    fields = FieldsAndClients.query.filter_by(id_client=id_client).all()
    for i in fields:
        if i.id_field == id_field:
            return i.numbers_hits


def add_prize_to_client(id_client, id_prize):
    last = ClientAndPrizes.query.filter_by(id_client=id_client).first()
    if last:
        d = [int(i) for i in last.prizes[1:-1].split(', ')]
        print(d)
        d.append(id_prize)
        print(d)
        last.prizes = str(d)
        db.session.commit()
    else:
        client_and_prize = ClientAndPrizes(id_client=id_client, prizes=str([id_prize]))
        db.session.add(client_and_prize)
        db.session.commit()


def get_info_about_prize(id_prize):
    prize = Prizes.query.filter_by(id=id_prize).first()
    return [prize.file, prize.name, prize.description]


def get_prizes_to_client(id_client):
    prizes = ClientAndPrizes.query.filter_by(id_client=id_client).first()
    if prizes:
        d, d_2 = [], []
        for i in prizes.prizes[1:-1].split(', '):
            d_2.append(get_info_about_prize(int(i)))
            print(d_2)
        return d_2
    return []
