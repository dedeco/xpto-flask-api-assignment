import json
import jwt
import datetime
import collections
import dateutil.parser
import ast

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from flask import Flask, request, make_response, Response
from functools import wraps
from werkzeug.security import check_password_hash

from .utils import json_response, JSON_MIME_TYPE, validate_fields

from .models import db, User, Channel, Performer, Song, Play
from .app import app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return json_response(json.dumps({'error' : 'Token is missing.'})), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = db.session.query(User).filter_by(public_id=data['public_id']).first()
        except:
            return json_response(json.dumps({'error' : 'Token is not valid.'})), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/ping', methods=['GET','POST'])
#@token_required
def ping():
    return json_response(json.dumps({"ping":"pong"}))

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required."'})

    user = db.session.query(User).filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required."'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return json_response(json.dumps({'token' : token.decode('UTF-8')}))

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required."'})

def _searchChannel(name):
    q = db.session.query(Channel)\
        .filter(Channel.name.ilike(name))
    return q.first()

def _insertChannel(name):
    try:
        c = Channel(name)
        db.session.add(c)
        db.session.commit()
    except IntegrityError: #  if the data already exists on the server, it shouldn't be added again
        pass # wasn't clear (in exercise) to throw an exception, so I passed
    return c

@app.route('/add_channel', methods=['POST'])
def add_channel():

    b, response, data = validate_fields(request,['name'])
    
    if b:
        name = data.get('name') 
        c =_insertChannel(name)
        return json_response(json.dumps(response))
    else:
        return json_response(data=response,status=400)

def _insertPerformer(name):
    try:
        p = Performer(name)
        db.session.add(p)
        db.session.commit()
    except IntegrityError: #  if the data already exists on the server, it shouldn't be added again
        pass 
    return p

def _searchPerfomer(name):
    q = db.session.query(Performer)\
        .filter(Performer.name.ilike('%' + name + '%'))
    return q.first()

@app.route('/add_performer', methods=['POST'])
def add_performer():
    b, response, data = validate_fields(request,['name'])
    
    if b:
        name = data.get('name')
        p =_insertPerformer(name)
        return json_response(json.dumps(response))
    else:
        return json_response(json.dumps(response),400)

def _insertSong(title, perfomer):
    try:
        s = Song(title, perfomer)
        db.session.add(s)
        db.session.commit()
    except IntegrityError: #  if the data already exists on the server, it shouldn't be added again
        pass 
    return s

def _searchSong(title, performer):
    try:
        s = db.session.query(Song)\
            .filter(Song.title.ilike(title))\
            .filter(Song.performer == performer).one()
    except NoResultFound:
        s = db.session.query(Song)\
            .filter(Song.title.ilike(title)).first()
    return s

@app.route('/add_song', methods=['POST'])
def add_song():
    b, response, data = validate_fields(request,['performer','title'])
    
    if b:
        perfomer = data.get('performer')
        
        p = _searchPerfomer(perfomer)
        if not p:
            p =_insertPerformer(perfomer)
        title = data.get('title')

        s =_insertSong(title, p)
        return json_response(json.dumps(response))
    else:
        return json_response(json.dumps(response),400)

@app.route('/add_play', methods=['POST'])
def add_play():
    b, response, data = validate_fields(request,['performer','title','channel','start','end'])

    if b:
        performer = data.get('performer') 
        title = data.get('title') 
        channel = data.get('channel')
        start = data.get('start')
        end = data.get('end')

        p = _searchPerfomer(performer)
        if not p:
            p =_insertPerformer(performer)

        s = _searchSong(title, p)
        if not s:
            s =_insertSong(title, p)

        c = _searchChannel(channel)
        if not c:
            c =_insertChannel(channel)

        try:
            play = Play(s , c , p, start, end)
            db.session.add(play)
            db.session.commit()
        except IntegrityError: #  if the data already exists on the server, it shouldn't be added again
            pass 

        return json_response(json.dumps(response))
    else:
        return json_response(json.dumps(response),400)

def _dict_channel_plays(play):
    x = {
        "performer": play.performer.name,
        "title": play.song.title,
        #"channel": play.channel.name,
        "start": play.start.isoformat(),
        "end": play.end.isoformat()
    }
    return x

@app.route('/get_channel_plays', methods=['GET','POST'])
def get_channel_plays():

    b, response, data = validate_fields(request,['channel','start','end'])

    if b:
        channel = data.get('channel')
        start = data.get('start')
        end = data.get('end')

        c = _searchChannel(channel)
        
        if c:
            try:
                q = db.session.query(Play)\
                    .filter(Play.channel == c)\
                    .filter(Play.start >= dateutil.parser.parse(start))\
                    .filter(Play.end <= dateutil.parser.parse(end))

                plays = [_dict_channel_plays(x) for x in q.all()]

                response = {"result": plays
                            ,"code": 0
                            ,"errors": []
                            }

            except NoResultFound:
                pass

        return json_response(json.dumps(response))
    else:
        return json_response(json.dumps(response),400)

def _dict_song_plays(play):
    x = {
        "channel": play.channel.name,
        #"title": play.song.title,
        "start": play.start.isoformat(),
        "end": play.end.isoformat()
    }
    return x

@app.route('/get_song_plays', methods=['GET','POST'])
def get_song_plays():

    b, response, data = validate_fields(request,['performer','title','start','end'])

    if b:
        performer = data.get('performer')
        title = data.get('title')
        start = data.get('start')
        end = data.get('end')

        p = _searchPerfomer(performer)
        if not p:
            p =_insertPerformer(performer)

        s = _searchSong(title, p)

        if s:
            try:
                q = db.session.query(Play)\
                    .filter(Play.song == s)\
                    .filter(Play.start >= dateutil.parser.parse(start))\
                    .filter(Play.end <= dateutil.parser.parse(end))

                plays = [_dict_song_plays(x) for x in q.all()]

                response = {"result": plays
                            ,"code": 0
                            ,"errors": []
                            }

            except NoResultFound:
                pass

        return json_response(json.dumps(response))
    else:
        return json_response(json.dumps(response),400)

def _get_top(start, plays):
    """
    Calculate top, rank, etc (copied and modified from test.py)
    """
    pc = collections.defaultdict(int)
    previous_pc = collections.defaultdict(int)
    end = start + datetime.timedelta(days=7)
    previous_start = start - datetime.timedelta(days=7)
    for channel in plays.keys():
        for date, (performer, title, length) in plays[channel].items():
            date = datetime.datetime(*date)
            if start <= date < end:
                pc[(performer, title)] += 1
            elif previous_start <= date < start:
                previous_pc[(performer, title)] += 1
    res = []
    previous_pos = sorted(previous_pc.keys(), key=lambda s: -previous_pc[s])
    for song in pc.keys():
        try:
            prev = previous_pos.index(song)
        except ValueError:
            prev = None
        res.append(
            {'performer': song[0], 'title': song[1],
             'plays': pc[song], 'previous_plays': previous_pc[song],
             'previous_rank': prev})
    res = sorted(res, key=lambda x: -x['plays']) 
    for i, r in enumerate(res):
        res[i]['rank'] = i
    return res

def _create_dict_by_list(l):
    d = {}
    for i in l:
        x = {}
        d[i] = x 
    return d

@app.route('/get_top', methods=['GET','POST'])
def get_top():

    b, response, data = validate_fields(request,['channels','start','limit'])

    if b:
        channels = ast.literal_eval(data.get('channels'))
        start = data.get('start')
        limit = data.get('limit')

        q = db.session.query(Channel)\
                        .filter(Channel.name.in_(channels))

        channels_ids = [x.id for x in q.all()]

        start_7 = dateutil.parser.parse(start) - datetime.timedelta(days=7)

        q = db.session.query(Play)\
            .filter(Play.channel_id.in_(channels_ids))\
            .filter(Play.start >= start_7 )\
            .order_by(Play.channel_id,Play.start)

        plays = _create_dict_by_list(channels)

        for reg in q.all():
            key = tuple(
                        list(
                            map(int,
                                reg.start.strftime("%Y,%m,%d,%H,%M,%S")\
                                            .split(','))))
            x = {}
            x[key] =  (reg.song.performer.name
                        ,reg.song.title
                        ,(reg.end - reg.start).total_seconds())

            plays[reg.channel.name].update(x)

        response = {"result": (_get_top(dateutil.parser.parse(start)\
                            , dict(plays)))
                    ,"code": 0
                    ,"errors": []
                    }

        return json_response(json.dumps(response))
    else:
        return json_response(json.dumps(response),400)

