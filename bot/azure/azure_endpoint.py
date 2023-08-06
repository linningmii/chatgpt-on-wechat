from config import conf, load_config
import requests
import json
from string import Template
from bot.azure.session_manager import SessionManager
from common.log import logger
from database.firestore import Firestore


class AzureEndpoint:
    def __init__(self):
        super().__init__()
        self.endpoint_url = conf().get("azure_endpoint_url")
        self.endpoint_key = conf().get("azure_endpoint_key")
        self.session_manager = SessionManager()
        self.db = Firestore()

    def update_history(self, session_id: str, query: str, answer: str):
        self.session_manager.append(session_id=session_id, query=query, answer=answer)

    def load_history(self, session_id: str):
        history = self.session_manager.get(session_id)
        if not isinstance(history, list):
            return []
        return history

    def chat(self, raw_session_id: str, query: str) -> str:
        user = self.db.query_by_associated_id(raw_session_id)
        session_id = raw_session_id
        if user is not None:
            session_id = user.id
        logger.info(session_id + "说：" + query)

        if query == "$记忆清除":
            self.session_manager.delete(session_id)
            return "记忆已清除！"

        url = self.endpoint_url
        auth_template = Template('Bearer $key')

        payload = json.dumps({
            "chat_history": self.load_history(session_id),
            "query": query,
            "user_information": self.session_manager.get_user_information(doc=user)
        })
        headers = {
            'Authorization': auth_template.substitute(key=self.endpoint_key),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.ok:
            json_dict = json.loads(response.text)
            answer = json_dict["answer"]
            logger.info("回复" + session_id + "：" + answer)
            self.update_history(session_id, query, answer)
            return answer
        else:
            print(response.status_code, response.text)
            message = "{}正在摸鱼中".format(conf().get("bot_name"))
            logger.error(message)
            return message
