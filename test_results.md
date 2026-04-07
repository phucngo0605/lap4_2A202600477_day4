# TravelBuddy Test Cases

## TestCase1: Initial Greeting

**👤 Bạn:** Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

**🤖 TravelBuddy đang suy nghĩ...**

**✈️ TravelBuddy:** Chào bạn! Có rất nhiều điểm đến thú vị để bạn khám phá. Bạn có thể cho tôi biết thêm về sở thích của bạn không? Bạn thích biển, núi, thành phố lớn hay những nơi yên tĩnh? Ngoài ra, bạn có thời gian đi du lịch trong bao lâu và ngân sách dự kiến là bao nhiêu?

---

## TestCase2: Flight Search

**👤 Bạn:** Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

**🤖 TravelBuddy đang suy nghĩ...**

**🔍 [LOGGING]** Gọi Tool: `search_flights`
- Đối số: `{'origin': 'Hà Nội', 'destination': 'Đà Nẵng'}`

**✈️ TravelBuddy:** Dưới đây là danh sách các chuyến bay từ Hà Nội đi Đà Nẵng:

1. **Vietnam Airlines (economy)**
   - Giờ bay: 06:00 → 07:20
   - Giá: 1,450,000đ

2. **Vietnam Airlines (business)**
   - Giờ bay: 14:00 → 15:20
   - Giá: 2,800,000đ

3. **VietJet Air (economy)**
   - Giờ bay: 08:30 → 09:50
   - Giá: 890,000đ

Bạn có muốn biết thêm thông tin nào khác không?

---

## TestCase3: Complete Trip Planning

**👤 Bạn:** Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

**🤖 TravelBuddy đang suy nghĩ...**

**🔍 [LOGGING]** Gọi Tool: `search_flights`
- Đối số: `{'origin': 'Hà Nội', 'destination': 'Phú Quốc'}`

**🔍 [LOGGING]** Gọi Tool: `search_hotels`
- Đối số: `{'city': 'Phú Quốc', 'max_price_per_night': 2500000}`

**✈️ TravelBuddy:** Dưới đây là thông tin về chuyến bay và khách sạn cho chuyến đi của bạn từ Hà Nội đến Phú Quốc trong 2 đêm:

### Chuyến bay từ Hà Nội đến Phú Quốc

1. **Vietnam Airlines (economy)**
   - Giờ bay: 07:00 → 09:15
   - Giá: 2,100,000đ

2. **VietJet Air (economy)**
   - Giờ bay: 16:00 → 18:15
   - Giá: 1,100,000đ

### Khách sạn tại Phú Quốc (giá tối đa 2,500,000đ/đêm)

1. **9Station Hostel (2 sao)**
   - Giá: 200,000đ/đêm
   - Khu vực: Dương Đông
   - Đánh giá: 4.5

2. **Lahana Resort (3 sao)**
   - Giá: 800,000đ/đêm
   - Khu vực: Dương Đông
   - Đánh giá: 4.0

### Tính toán ngân sách

| Chi phí | Số tiền |
|---------|---------|
| Chuyến bay (VietJet Air) | 1,100,000đ |
| Khách sạn (9Station Hostel) 2 đêm | 400,000đ |
| **Tổng chi phí** | **1,500,000đ** |
| **Ngân sách còn lại** | **3,500,000đ** |

Bạn có thể chọn chuyến bay và khách sạn phù hợp với ngân sách của mình. Nếu cần thêm thông tin hoặc hỗ trợ, hãy cho tôi biết!

---

## TestCase4: Incomplete Hotel Booking Request

**👤 Bạn:** Tôi muốn đặt khách sạn

**🤖 TravelBuddy đang suy nghĩ...**

**✈️ TravelBuddy:** Bạn muốn đặt khách sạn ở thành phố nào và có ngân sách tối đa mỗi đêm là bao nhiêu?

---

## TestCase5: Out of Scope Request

**👤 Bạn:** Giải giúp tôi bài tập lập trình Python về linked list

**🤖 TravelBuddy đang suy nghĩ...**

**✈️ TravelBuddy:** Xin lỗi, mình là trợ lý du lịch của TravelBuddy nên chỉ có thể giúp bạn tìm vé máy bay, phòng khách sạn và lên kế hoạch chi tiêu du lịch thôi nè!
