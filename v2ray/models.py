import json

from sqlalchemy import Column, Integer, String, BIGINT, Boolean, DATETIME
from datetime import datetime

from init import db


class Customers(db.Model):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    identifier = Column(String(20), nullable=False)
    uuid = Column(String(40), unique=True, nullable=False)
    alterId = Column(Integer, default=4, nullable=False)
    creator = Column(String(20))
    duration = Column(Integer)
    startDate = Column(DATETIME)
    endDate = Column(DATETIME)

    def __init__(self, uuid=None, identifier=None, alterId=None, creator=None, duration=0, startDate=datetime.now(),
                 endDate=datetime.now()):
        self.uuid = uuid
        self.identifier = identifier
        self.alterId = alterId
        self.creator = creator
        self.duration = duration
        self.startDate = startDate
        self.endDate = endDate

    def to_json(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'identifier': self.identifier,
            'alterId': self.alterId,
            'creator': self.creator,
            'duration': self.duration,
            'startDate': self.startDate,
            'endDate': self.endDate
        }

    def to_v2_json(self):
        return {
            'id': self.uuid,
            'alterId': self.alterId,
            'email': self.identifier
        }

    def to_v2_str(self):
        return json.dumps(self.to_v2_json(), indent=2, separators=(',', ': '), sort_keys=True, ensure_ascii=False)


class Inbound(db.Model):
    __tablename__ = 'inbound'
    id = Column(Integer, primary_key=True, autoincrement=True)
    port = Column(Integer, unique=True, nullable=False)
    listen = Column(String(50), default='0.0.0.0')
    protocol = Column(String(50), nullable=False)
    settings = Column(String, nullable=False)
    stream_settings = Column(String, nullable=False)
    tag = Column(String(255), default='', unique=True, nullable=False)
    sniffing = Column(String, default='{"enabled":true,"destOverride":["http","tls"]}')
    remark = Column(String(255), default='', nullable=False)
    up = Column(BIGINT, default=0, nullable=False)
    down = Column(BIGINT, default=0, nullable=False)
    enable = Column(Boolean, default=True, nullable=False)

    def __init__(self, port=None, listen=None, protocol=None,
                 settings=None, stream_settings=None, sniffing=None, remark=None):
        self.port = port
        self.listen = listen
        self.protocol = protocol
        self.settings = settings
        self.stream_settings = stream_settings
        self.tag = 'inbound-%d' % self.port
        self.sniffing = sniffing
        self.remark = remark
        self.up = 0
        self.down = 0
        self.enable = True

    def to_json(self):
        return {
            'id': self.id,
            'port': self.port,
            'listen': self.listen,
            'protocol': self.protocol,
            'settings': json.loads(self.settings, encoding='utf-8'),
            'stream_settings': json.loads(self.stream_settings, encoding='utf-8'),
            'sniffing': json.loads(self.sniffing, encoding='utf-8'),
            'remark': self.remark,
            'up': self.up,
            'down': self.down,
            'enable': self.enable,
        }

    def to_v2_json(self):
        return {
            'port': self.port,
            'listen': self.listen,
            'protocol': self.protocol,
            'settings': json.loads(self.settings, encoding='utf-8'),
            'streamSettings': json.loads(self.stream_settings, encoding='utf-8'),
            'sniffing': json.loads(self.sniffing, encoding='utf-8'),
            'tag': self.tag,
        }

    def to_v2_str(self):
        return json.dumps(self.to_v2_json(), indent=2, separators=(',', ': '), sort_keys=True, ensure_ascii=False)
