import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv

# LangGraph & LangChain imports
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Import tools từ file tools.py
from tools import search_flights, search_hotels, calculate_budget

# Load biến môi trường từ file .env
load_dotenv()

# ==========================================
# 1. Đọc System Prompt từ file txt
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
    messages: Annotated[list, add_messages]

# ==========================================
# 3. Khởi tạo LLM và Tools
# ==========================================
tools_list = [search_flights, search_hotels, calculate_budget]
# Temperature = 0 để Agent hoạt động chính xác và ổn định
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) 
llm_with_tools = llm.bind_tools(tools_list)

# ==========================================
# 4. Định nghĩa Agent Node
# ==========================================
def agent_node(state: AgentState):
    messages = state["messages"]
    
    # Chèn System Prompt vào đầu danh sách nếu chưa có
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# ==========================================
# 5. Xây dựng Workflow Graph
# ==========================================
builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools_list))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

# ==========================================
# 6. Chat Loop (Giao diện thực thi)
# ==========================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧳 TRAVELBUDDY - TRỢ LÝ DU LỊCH THÔNG MINH (LAB 4)")
    print("Gõ 'quit', 'exit' hoặc 'q' để thoát chương trình.")
    print("="*60)
    
    while True:
        user_input = input("\n👤 Bạn: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ["quit", "exit", "q"]:
            print("👋 Tạm biệt!")
            break
            
        print("\n🤖 TravelBuddy đang suy nghĩ...")
        
        # Tạo input cho Graph
        current_state = {"messages": [HumanMessage(content=user_input)]}
        final_answer = ""

        # Stream qua các bước của Graph
        for event in graph.stream(current_state, stream_mode="values"):
            if "messages" in event:
                last_msg = event["messages"][-1]
                
                # LOGGING: Hiển thị khi Agent quyết định gọi Tool
                # Điểm này giúp bạn đạt 10% phần Logging rõ ràng trong Rubric
                if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                    for tc in last_msg.tool_calls:
                        print(f"🔍 [LOGGING] Gọi Tool: {tc['name']}")
                        print(f"   ∟ Đối số: {tc['args']}")
                
                # Lưu nội dung phản hồi cuối cùng
                if last_msg.content:
                    final_answer = last_msg.content

        # In câu trả lời cuối cùng sau khi đã chạy xong các bước (bao gồm cả Tool)
        print(f"\n✈️ TravelBuddy: {final_answer}")