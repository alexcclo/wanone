# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import CHAR, TINYINT, DECIMAL, BIGINT, INTEGER, VARCHAR, TEXT
from sqlalchemy import Index

db = SQLAlchemy()

class Agent(db.Model):
    _tablename_ = 'agent'
    id = db.Column("AGENT_ID", BIGINT, primary_key=True, autoincrement=True)
    uuid = db.Column('UUID', CHAR(32), nullable=True)
    dateCreated = db.Column('DATE_CREATED', BIGINT, nullable=True)
    dateModified = db.Column('DATE_MODIFIED', BIGINT, nullable=True)
    delete = db.Column('DELETE', TINYINT, nullable=True)
    name = db.Column('NAME', VARCHAR(255), nullable=True)
    description = db.Column('DESCRIPTION', TEXT, nullable=True)
    type = db.Column('TYPE', VARCHAR(255), nullable=True)
    persona = db.Column('PERSONA', TEXT, nullable=True)
    settings = db.Column('SETTINGS', TEXT, nullable=True)

class Conversation(db.Model):
    __tablename__ = 'conversation'
    id = db.Column('CONVERSATION_ID', BIGINT, primary_key=True, autoincrement=True)
    uuid = db.Column('UUID', CHAR(32), nullable=True)
    dateCreated = db.Column('DATE_CREATED', BIGINT, nullable=True)
    dateModified = db.Column('DATE_MODIFIED', BIGINT, nullable=True)
    delete = db.Column('DELETE', TINYINT, nullable=True)
    type = db.Column('TYPE', VARCHAR(255), nullable=True)
    status = db.Column('STATUS', VARCHAR(255), nullable=True)
    agent_id = db.Column('AGENT_ID', BIGINT, db.ForeignKey('agent.AGENT_ID'), nullable=True)

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column('MESSAGE_ID', BIGINT, primary_key=True, autoincrement=True)
    uuid = db.Column('UUID', CHAR(32), nullable=True)
    dateCreated = db.Column('DATE_CREATED', BIGINT, nullable=True)
    dateModified = db.Column('DATE_MODIFIED', BIGINT, nullable=True)
    delete = db.Column('DELETE', TINYINT, nullable=True)
    agent_id = db.Column('AGENT_ID', BIGINT, db.ForeignKey('agent.AGENT_ID'), nullable=True)
    conversation_id = db.Column('CONVERSATION_ID', BIGINT, db.ForeignKey('message.MESSAGE_ID'), nullable=True)
    message = db.Column('MESSAGE', TEXT, nullable=True)
    json = db.Column('JSON', TEXT, nullable=True)
    status = db.Column('STATUS', VARCHAR(255), nullable=True)
    sender = db.Column('SENDER', VARCHAR(255), nullable=True)
    completion_tokens = db.Column('COMPLETION_TOKENS', TEXT, nullable=True)
    prompt_tokens = db.Column('PROMPT_TOKENS', TEXT, nullable=True)
    total_tokens = db.Column('TOTAL_TOKENS', INTEGER, nullable=True)
    settings = db.Column('SETTINGS', TEXT, nullable=True)


    

    