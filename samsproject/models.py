from samsproject import db

class Server(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)

class PerformanceMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.String, db.ForeignKey('server.id'), nullable=False)
    cpu_usage = db.Column(db.Float, nullable=False)
    memory_usage = db.Column(db.Float, nullable=False)
    disk_usage = db.Column(db.Float, nullable=False)
    network_traffic = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.String, db.ForeignKey('server.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    resolved = db.Column(db.Boolean, default=False)