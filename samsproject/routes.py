from flask import render_template, redirect, url_for, request, Blueprint
from samsproject.models import Server, PerformanceMetrics, Alert
from samsproject import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    servers = Server.query.all()
    return render_template('index.html', servers=servers)

@main.route('/server/<int:server_id>')
def server_detail(server_id):
    server = Server.query.get_or_404(server_id)
    metrics = PerformanceMetrics.query.filter_by(server_id=server.id).all()
    alerts = Alert.query.filter_by(server_id=server.id).all()
    return render_template('servers.html', server=server, metrics=metrics, alerts=alerts)

@main.route('/add_server', methods=['POST'])
def add_server():
    name = request.form.get('name')
    ip_address = request.form.get('ip_address')
    location = request.form.get('location')
    status = request.form.get('status')
    new_server = Server(name=name, ip_address=ip_address, location=location, status=status)
    db.session.add(new_server)
    db.session.commit()
    return redirect(url_for('main.index'))