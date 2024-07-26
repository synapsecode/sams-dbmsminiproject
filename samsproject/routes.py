from flask import render_template, redirect, url_for, request, Blueprint
from samsproject.models import Server, PerformanceMetrics, Alert
from samsproject import db
import json
from sqlalchemy.sql import text

main = Blueprint('main', __name__)

@main.route('/')
def index():
    servers = Server.query.all()
    return render_template('index.html', servers=servers,results=[])

@main.route('/server/<server_id>')
def server_detail(server_id):
    server = Server.query.get_or_404(server_id)
    metrics = PerformanceMetrics.query.filter_by(server_id=server.id).all()
    alerts = Alert.query.filter_by(server_id=server.id).all()
    return render_template('servers.html', server=server, metrics=metrics, alerts=alerts)

@main.route('/register_server', methods=['POST'])
def register_server():
    data = json.loads(request.get_json())
    if(data == None):
        return "NO PAYLOAD", 400

    name = data['server_name']
    sid = data['sid']
    ip_address = data['ip']
    location = data['location']
    status = 'active'

    if(Server.query.filter_by(id=sid).first() != None):
        return "SERVER EXISTS", 400

    new_server = Server(id=sid, name=name, ip_address=ip_address, location=location, status=status)
    db.session.add(new_server)
    db.session.commit()
    
    return "SUCCESS", 200

@main.route('/create_alert', methods=['POST'])
def create_alert():
    data = json.loads(request.get_json())
    if(data == None):
        return "NO PAYLOAD", 400

    desc = data['desc']
    timestamp = data['timestamp']
    sid = data['sid']
    typ = data['type']

    if(Server.query.filter_by(id=sid).first() == None):
        return "SERVER DOES NOT EXIST", 400

    new_alert = Alert(description=desc, server_id=sid, alert_type=typ, timestamp=timestamp, resolved=False)
    db.session.add(new_alert)
    db.session.commit()
    
    return "ALERT CREATED!", 200


"""
    network_traffic = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

"""

@main.route('/save_performance', methods=['POST'])
def save_performance():
    data = json.loads(request.get_json())
    if(data == None):
        return "NO PAYLOAD", 400

    sid = data['sid']
    cpu = data['cpu']
    ram = data['ram']
    dsk = data['disk']
    traffic = sum(data['network'])/2
    timestamp = data['timestamp']

    if(Server.query.filter_by(id=sid).first() == None):
        return "SERVER DOES NOT EXIST", 400

    metric = PerformanceMetrics(server_id=sid, cpu_usage=cpu, memory_usage=ram, disk_usage=dsk, network_traffic=traffic, timestamp=timestamp)
    db.session.add(metric)
    db.session.commit()
    
    return "ALERT CREATED!", 200

@main.route('/execute_query', methods=['POST'])
def execute_query():
    data = request.get_json()
    if(data == None):
        return "NO PAYLOAD", 400
    
    query = data['query'].strip()
    res = db.session.execute(text(query))

    columns = [str(k) for k in res.keys()]
    rows = [row for row in res.all()]
    
    data = [rows, columns]

    servers = Server.query.all()
    return render_template('index.html', servers=servers, results=data)