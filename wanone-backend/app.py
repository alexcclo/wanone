from flask import Flask, abort, request, Response
from flask_restx import Resource, Api, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from dotenv import load_dotenv
from flask_cors import CORS
from agent_service import AgentService

BASE_URL = "/gen/api"

app = Flask(__name__)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app, version='1.0', 
    title='WanOne AI API',
    description='A finetuned AI Tool created with Hugging Face Transformers and based on Google GEMMA-2B',
    prefix=BASE_URL,
    doc=BASE_URL + '/docs/'
)
load_dotenv()

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@host/database_name"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)
engine = create_engine(SQLALCHEMY_DATABASE_URI)

agent_namespace = api.namespace("agent", description='Agent API')
agent_model = api.model('agent', {
    'conversation_uuid': fields.String(required=True, description='conversation_uuid'),
    'message': fields.String(required=True, description='message'),
    'agent': fields.String(required=True, description='agent')
})
intent_model = api.model('intent', {
    'message': fields.String(required=True, description='message'),
})
@agent_namespace.route('/AI/Reply')
class AIReply(Resource):
    @api.expect(agent_model)
    def post(self):
        data = request.get_json()
        agent = AgentService()
        conversation_uuid = data['conversation_uuid']
        message = data['message']
        agent_name = data['agent']
        reply = agent.getReply(conversation_uuid, message, agent_name)
        return reply

if __name__ == '__main__':
    app.run(debug=True, port=8087, host="0.0.0.0")