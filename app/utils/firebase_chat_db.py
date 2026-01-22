# app/utils/firebase_chat_db.py
# Firebase functionality has been removed.
# This file remains as a placeholder to prevent import errors during transition.

class FirebaseChatDB:
    def __init__(self):
        pass
    
    def get_chat_history(self, *args, **kwargs):
        return []
        
    def create_message(self, *args, **kwargs):
        return {}
        
    def get_conversations(self, *args, **kwargs):
        return []

    def mark_messages_read(self, *args, **kwargs):
        pass
        
    def delete_conversation(self, *args, **kwargs):
        return True

def get_firebase_chat_db():
    return FirebaseChatDB()
