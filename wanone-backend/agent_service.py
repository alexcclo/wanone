import json
import re
import uuid
from datetime import datetime
from transformers import AutoTokenizer
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM
from models import db, Message, Agent, Conversation

class AgentService:
    def __init__(self):
        config = PeftConfig.from_pretrained("alexcclo/wanone-2024-10-12-02")
        base_model = AutoModelForCausalLM.from_pretrained("google/gemma-2b")
        self.model = PeftModel.from_pretrained(base_model, "alexcclo/wanone-2024-10-12-02")
        self.tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b")
        self.model_version = "custom-wanone-2024-10-12-02"

    def getReply(self, conversation_uuid, message, agent):
        agent_id = self.getAgentID(agent)
        conversation_id = self.getConversationID(conversation_uuid, agent_id)
        if conversation_id:
            return self.returnMessage(message, conversation_id, agent_id)
        else:
            return {"status": "Failed"}

    def getAgentID(self, agent_name):
        agent = db.session.query(Agent).filter(Agent.name == agent_name).first()
        return agent.id if agent else None

    def getPersonaByAgent(self, agent_name):
        agent = db.session.query(Agent).filter(Agent.name == agent_name).first()
        return agent.persona if agent else None

    def getPersonaByConversation(self, conversation_id):
        conversation = db.session.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            agent = db.session.query(Agent).filter(Agent.id == conversation.agent_id).first()
            return agent.persona if agent else None
        return None

    def getConversationID(self, conservation_uuid, agent_id):
        if agent_id:
            conversation = db.session.query(Conversation).filter(Conversation.uuid == conservation_uuid).first()
            if conversation:
                return conversation.id
            else:
                new_conversation = Conversation(
                    uuid=conservation_uuid,
                    dateCreated=int(datetime.now().timestamp() * 1000),
                    dateModified=int(datetime.now().timestamp() * 1000),
                    type="chat",
                    status="active",
                    agent_id=agent_id,
                    delete=0
                )
                db.session.add(new_conversation)
                db.session.commit()
                return new_conversation.id
        return None

    def buildMessageByID(self, conversation_id):
        records = db.session.query(Message).filter(Message.conversation_id == conversation_id).all()
        persona = self.getPersonaByConversation(conversation_id)
        messages = [{"role": "system", "content": persona}]
        for record in records:
            role = "user" if record.sender == 'user' else "assistant"
            messages.append({"role": role, "content": record.message})
        return messages

    def extract_json_from_response(self, response_content):
        json_match = re.search(r'```(?:json)?(.*?)```', response_content, re.DOTALL)
        json_str = json_match.group(1).strip() if json_match else response_content.strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            print("Failed to decode JSON")
            return None

    def getIntent(self, message):
        persona = self.getPersonaByAgent("INTENT_AGENT")
        input_text = f"{persona}\n\nUser: {message}\nAssistant:"
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
        output = self.model.generate(input_ids, max_length=200)
        ai_response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        json_data = self.extract_json_from_response(ai_response)
        return json_data

    def returnMessage(self, message, conversation_id, agent_id):
        messages = self.buildMessageByID(conversation_id)
        messages.append({"role": "user", "content": message})
        
        input_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in messages])
        input_text += "\nAssistant:"
        
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
        output = self.model.generate(input_ids, max_length=500)
        ai_response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        
        json_data = self.extract_json_from_response(ai_response)
        
        user_message_record = Message(
            uuid=str(uuid.uuid4()).replace('-', ''),
            conversation_id=conversation_id,
            agent_id=agent_id,
            message=message,
            sender='user',
            status='complete',
            dateCreated=int(datetime.now().timestamp() * 1000),
            dateModified=int(datetime.now().timestamp() * 1000),
            delete=0
        )
        db.session.add(user_message_record)
        
        assistant_message_record = Message(
            uuid=str(uuid.uuid4()).replace('-', ''),
            conversation_id=conversation_id,
            agent_id=agent_id,
            message=ai_response,
            json=json_data,
            sender='assistant',
            status='complete',
            dateCreated=int(datetime.now().timestamp() * 1000),
            dateModified=int(datetime.now().timestamp() * 1000),
            delete=0
        )
        db.session.add(assistant_message_record)
        
        db.session.commit()

        response_data = {
            "status": "success",
            "model": self.model_version,
            "conversation_id": conversation_id,
            "message": ai_response,
            "json_data": json_data,
            "usage": {
                "completion_tokens": len(self.tokenizer.encode(ai_response)),
                "prompt_tokens": len(input_ids[0]),
                "total_tokens": len(self.tokenizer.encode(ai_response)) + len(input_ids[0])
            }
        }
        return response_data