import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv

# LangGraph & LangChain imports
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Import tools từ file tools.py
from tools import search_flights, search_hotels, calculate_budget

# Load biến môi trường từ file .env
load_dotenv()

# ==========================================
# 1. Đọc System Prompt
# ==========================================
try:
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    SYSTEM_PROMPT = "Bạn là trợ lý du lịch hữu ích."
    print("⚠️ Cảnh báo: Không tìm thấy file system_prompt.txt!")

# ==========================================
# 2. Khai báo State
# ==========================================
class AgentState(TypedDict):
    # add_messages giúp cộng dồn tin nhắn thay vì ghi đè
    messages: Annotated[list, add_messages]

# ==========================================
# 3. Khởi tạo LLM và Tools
# ==========================================
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) 
llm_with_tools = llm.bind_tools(tools_list)

# ==========================================
# 4. Định nghĩa Agent Node
# ==========================================
def agent_node(state: AgentState):
    messages = state["messages"]
    
    # Kiểm tra nếu chưa có SystemMessage trong lịch sử thì chèn vào đầu
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# ==========================================
# 5. Xây dựng Workflow Graph (Giữ nguyên cấu trúc)
# ==========================================
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools_list))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

# ==========================================
# 6. Chat Loop (ĐÃ NÂNG CẤP TRÍ NHỚ)
# ==========================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧳 TRAVELBUDDY - PHIÊN BẢN CÓ TRÍ NHỚ (LAB 4)")
    print("Gõ 'quit', 'exit' hoặc 'q' để thoát.")
    print("="*60)
    
    # BIẾN QUAN TRỌNG: Lưu trữ toàn bộ lịch sử hội thoại của phiên làm việc
    chat_history = []

    while True:
        user_input = input("\n👤 Bạn: ").strip()
        
        if not user_input or user_input.lower() in ["quit", "exit", "q"]:
            print("👋 Tạm biệt!")
            break
            
        print("\n🤖 TravelBuddy đang suy nghĩ...")
        
        # 1. Thêm tin nhắn của người dùng vào lịch sử
        chat_history.append(HumanMessage(content=user_input))
        
        # 2. Gửi TOÀN BỘ lịch sử tin nhắn vào Graph
        final_response_text = ""
        last_ai_message = None

        # Sử dụng stream_mode="values" để lấy trạng thái danh sách tin nhắn sau mỗi bước
        for event in graph.stream({"messages": chat_history}, stream_mode="values"):
            if "messages" in event:
                msg = event["messages"][-1]
                
                # LOGGING gọi Tool (giữ nguyên để lấy điểm Rubric)
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        print(f"🔍 [LOGGING] Gọi Tool: {tc['name']}")
                        print(f"   ∟ Đối số: {tc['args']}")
                
                # Lưu tin nhắn cuối cùng của AI để cập nhật vào lịch sử sau khi loop kết thúc
                if isinstance(msg, AIMessage):
                    last_ai_message = msg
                    if msg.content:
                        final_response_text = msg.content

        # 3. Cập nhật câu trả lời của AI vào lịch sử hội thoại
        if last_ai_message:
            chat_history.append(last_ai_message)

        # In câu trả lời cuối cùng
        print(f"\n✈️ TravelBuddy: {final_response_text}")
