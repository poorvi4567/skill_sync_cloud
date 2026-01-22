# app/routes/chat.py (DEBUG VERSION - Remove restrictions)
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
from datetime import datetime

router = APIRouter(prefix="/ws", tags=["WebSocket Chat"])

# Store active connections
class ConnectionManager:
    def __init__(self):
        # Format: {username: WebSocket}
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket
        print(f"✅ {username} connected. Total: {len(self.active_connections)}")
    
    def disconnect(self, username: str):
        if username in self.active_connections:
            del self.active_connections[username]
        print(f"❌ {username} disconnected. Total: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: dict, username: str):
        """Send message to a specific user"""
        if username in self.active_connections:
            try:
                await self.active_connections[username].send_json(message)
            except Exception as e:
                print(f"Error sending to {username}: {e}")
                self.disconnect(username)
    
    def is_online(self, username: str) -> bool:
        """Check if user is currently connected"""
        return username in self.active_connections

manager = ConnectionManager()

@router.websocket("/chat/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    print(f"🔌 WebSocket connection attempt from: {username}")
    
    await manager.connect(username, websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            message_type = data.get("type")
            # print(f"📨 Received message type: {message_type} from {username}")
            
            # ===============================
            # 1. GET CHAT HISTORY
            # ===============================
            if message_type == "get_history":
                other_user = data.get("with_user")
                
                # Firebase removed - return empty history
                await websocket.send_json({
                    "type": "history",
                    "with_user": other_user,
                    "messages": [],
                    "count": 0
                })
            
            # ===============================
            # 2. SEND MESSAGE
            # ===============================
            elif message_type == "message":
                from_user = data.get("from_user", username)
                to_user = data.get("to_user")
                text = data.get("text", "")
                
                if not to_user or not text:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Missing required fields: to_user or text"
                    })
                    continue
                
                created_at = datetime.utcnow().isoformat()
                
                # Prepare response message
                response = {
                    "type": "message",
                    "id": f"temp_{datetime.utcnow().timestamp()}",
                    "from_user": from_user,
                    "to_user": to_user,
                    "message": text,
                    "created_at": created_at
                }
                
                # Send to recipient if online
                if manager.is_online(to_user):
                    await manager.send_personal_message(response, to_user)
                    print(f"✅ Message delivered to {to_user}")
                
                # Send confirmation back to sender
                await websocket.send_json({
                    **response,
                    "status": "delivered" if manager.is_online(to_user) else "sent"
                })
            
            # ===============================
            # 3. TYPING INDICATOR
            # ===============================
            elif message_type == "typing":
                to_user = data.get("to_user")
                is_typing = data.get("is_typing", False)
                
                if to_user and manager.is_online(to_user):
                    await manager.send_personal_message({
                        "type": "typing",
                        "from_user": username,
                        "is_typing": is_typing
                    }, to_user)
            
            # ===============================
            # 4. GET ONLINE STATUS
            # ===============================
            elif message_type == "check_online":
                users_to_check = data.get("users", [])
                
                online_status = {
                    user: manager.is_online(user) 
                    for user in users_to_check
                }
                
                await websocket.send_json({
                    "type": "online_status",
                    "users": online_status
                })
            
            # ===============================
            # 5. GET ALL CONVERSATIONS
            # ===============================
            elif message_type == "get_conversations":
                # Firebase removed - return empty conversations
                await websocket.send_json({
                    "type": "conversations",
                    "data": []
                })
            
            # ===============================
            # 6. MARK MESSAGES AS READ
            # ===============================
            elif message_type == "mark_read":
                # No-op without database
                other_user = data.get("from_user")
                await websocket.send_json({
                    "type": "marked_read",
                    "from_user": other_user
                })
            
            # ===============================
            # 7. DELETE CONVERSATION
            # ===============================
            elif message_type == "delete_conversation":
                other_user = data.get("with_user")
                # No-op
                await websocket.send_json({
                    "type": "conversation_deleted",
                    "with_user": other_user
                })
            
            # ===============================
            # 8. PING/PONG (Keep-alive)
            # ===============================
            elif message_type == "ping":
                await websocket.send_json({"type": "pong"})
    
    except WebSocketDisconnect:
        manager.disconnect(username)
        print(f"🔌 {username} disconnected normally")
    except Exception as e:
        print(f"❌ WebSocket error for {username}: {e}")
        import traceback
        traceback.print_exc()
        manager.disconnect(username)

@router.get("/online-users")
async def get_online_users():
    """REST endpoint to check who's online"""
    return {
        "online_users": list(manager.active_connections.keys()),
        "count": len(manager.active_connections)
    }
