class SessionManager:
    def __init__(self):
        self.collection = dict()

    def set(self, session_id: str, new_history):
        self.collection[session_id] = new_history

    def get(self, session_id: str):
        return self.collection.get(session_id)

    def delete(self, session_id: str):
        if self.collection.get(session_id) is not None:
            del self.collection[session_id]

    def append(self, session_id: str, query: str, answer: str):
        history = self.get(session_id)
        new_content = {
                "inputs": {
                    "query": query,
                },
                "outputs": {
                    "answer": answer
                }
            }
        if history is None:
            history = [new_content]
        else:
            history.append(new_content)

        if len(history) > 20:
            history = history[-20:]
        self.set(session_id=session_id, new_history=history)

    def get_nickname(self, doc_dict) -> str:
        nickname0_map = doc_dict.get("nickname0", {})
        return nickname0_map.get("name", "")

    def get_user_information(self, doc) -> str:
        if doc is None:
            return "You don't know this guy yet."
        doc_dict = doc.to_dict()

        return f'''
birthday: {doc_dict.get("birthday", "unknown")}
gender: {doc_dict.get("gender", "unknown")}
name: {doc_dict.get("name", "unknown")}
nickname: {self.get_nickname(doc_dict)}
        '''.strip()
