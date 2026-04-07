from langchain_core.tools import tool

# ==========================================
# MOCK DATA - Dữ liệu giả lập
# ==========================================
FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1450000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2800000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1100000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780000, "class": "economy"},
    ]
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1800000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250000, "area": "Hải Châu", "rating": 4.6},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3500000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200000, "area": "Dương Đông", "rating": 4.5},
    ]
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm kiếm các chuyến bay giữa hai thành phố. Tham số: origin, destination."""
    try:
        # Kiểm tra xuôi và ngược (Hà Nội -> Đà Nẵng hoặc ngược lại)
        flights = FLIGHTS_DB.get((origin, destination)) or FLIGHTS_DB.get((destination, origin))
        
        if not flights:
            return f"Hiện tại không tìm thấy chuyến bay trực tiếp giữa {origin} và {destination}."
        
        res = f"Danh sách chuyến bay {origin} <-> {destination}:\n"
        for f in flights:
            res += f"- {f['airline']} ({f['class']}): {f['departure']} -> {f['arrival']}, Giá: {f['price']:,}đ\n"
        return res
    except Exception as e:
        return f"Lỗi hệ thống khi tra cứu chuyến bay: {str(e)}"

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """Tìm kiếm khách sạn tại một thành phố, có lọc theo giá tối đa mỗi đêm."""
    try:
        hotels = HOTELS_DB.get(city, [])
        # Lọc theo giá và sắp xếp theo rating giảm dần
        filtered = [h for h in hotels if h['price_per_night'] <= max_price_per_night]
        filtered.sort(key=lambda x: x['rating'], reverse=True)

        if not filtered:
            return f"Không tìm thấy khách sạn nào tại {city} có giá dưới {max_price_per_night:,}đ/đêm."
        
        res = f"Gợi ý khách sạn tại {city} (Ưu tiên đánh giá cao):\n"
        for h in filtered:
            res += f"- {h['name']} ({h['stars']} sao): {h['price_per_night']:,}đ/đêm - Khu vực: {h['area']} (Rating: {h['rating']})\n"
        return res
    except Exception as e:
        return f"Lỗi hệ thống khi tra cứu khách sạn: {str(e)}"

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại. 
    Tham số: 
    - total_budget: tổng tiền (int)
    - expenses: chuỗi định dạng 'tên_mục:số_tiền,tên_mục:số_tiền'
    """
    try:
        items = expenses.split(",")
        total_spent = 0
        detail_lines = []
        
        for item in items:
            if ":" not in item: continue
            name, amount = item.split(":")
            amt = int(amount.strip())
            total_spent += amt
            detail_lines.append(f"  + {name.strip()}: {amt:,}đ")
            
        remaining = total_budget - total_spent
        
        report = "--- BẢNG CHI PHÍ DỰ KIẾN ---\n"
        report += "\n".join(detail_lines)
        report += f"\n---------------------------\n"
        report += f"Tổng chi: {total_spent:,}đ\n"
        report += f"Ngân sách ban đầu: {total_budget:,}đ\n"
        
        if remaining < 0:
            report += f"⚠️ CẢNH BÁO: Bạn đang vượt ngân sách {abs(remaining):,}đ! Cần điều chỉnh lại kế hoạch."
        else:
            report += f"✅ Số dư còn lại: {remaining:,}đ. Bạn có thể chi tiêu thêm!"
            
        return report
    except Exception:
        return "Lỗi xử lý dữ liệu. Vui lòng đảm bảo tham số expenses đúng định dạng 'tên:số_tiền'."