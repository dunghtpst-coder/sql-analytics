# Sơ đồ quan hệ thực thể (ERD) — rút gọn các nhóm chính

> Sơ đồ đầy đủ 32 bảng nằm trong báo cáo đồ án gốc (`docs/full_report.pdf`, nếu bạn đính kèm).
> Bên dưới là ERD rút gọn theo 7 nhóm nghiệp vụ, đủ để hiểu luồng dữ liệu chính.
> GitHub sẽ tự render sơ đồ Mermaid này trực tiếp trong trang repo.

```mermaid
erDiagram
    ROLE ||--o{ USERS : "gán vai trò"
    USERS ||--o| VEHICLE_OWNER : "có thể là"
    USERS ||--o| CUSTOMER : "có thể là"
    USERS ||--o| EMPLOYEE : "có thể là"

    VEHICLE_OWNER ||--o{ VEHICLE : "sở hữu"
    VEHICLE_TYPE ||--o{ VEHICLE : "phân loại"
    VEHICLE_CATEGORY ||--o{ VEHICLE : "phân khúc"
    VEHICLE ||--o{ VEHICLE_PRICING : "có bảng giá"
    VEHICLE ||--o{ VEHICLE_MAINTENANCE : "được bảo trì"
    EMPLOYEE ||--o{ VEHICLE_APPROVAL : "kiểm duyệt"
    VEHICLE ||--o{ VEHICLE_APPROVAL : "được duyệt"

    CUSTOMER ||--o{ BOOKING_REQUEST : "tạo yêu cầu"
    VEHICLE ||--o{ BOOKING_REQUEST : "được đặt"
    LOCATION ||--o{ BOOKING_REQUEST : "điểm nhận/trả"
    BOOKING_REQUEST ||--o| BOOKING_CANCELLATION : "có thể bị hủy"
    BOOKING_REQUEST ||--|| RENTAL_CONTRACT : "sinh ra"

    RENTAL_CONTRACT ||--o{ PAYMENT : "phát sinh"
    PAYMENT_METHOD ||--o{ PAYMENT : "sử dụng"
    PAYMENT ||--o{ PAYMENT_TRANSACTION : "ghi log cổng TT"
    RENTAL_CONTRACT ||--o{ INVOICE : "xuất hóa đơn"
    RENTAL_CONTRACT ||--o{ PENALTY_RECORD : "phát sinh phạt"
    RENTAL_CONTRACT ||--o| HANDOVER_REPORT : "bàn giao"
    RENTAL_CONTRACT ||--o| RETURN_REPORT : "trả xe"
    RENTAL_CONTRACT ||--o| REVIEW : "được đánh giá"

    USERS {
        int Users_ID PK
        string Full_Name
        string Email
        int Role_ID FK
    }
    VEHICLE_OWNER {
        int Owner_ID PK
        int Users_ID FK
        decimal Commission_Rate
        decimal Owner_Rating
    }
    CUSTOMER {
        int Customer_ID PK
        int Users_ID FK
        string Customer_Rank
        int Total_Rentals
    }
    VEHICLE {
        int Vehicle_ID PK
        int Owner_ID FK
        int Vehicle_Type_ID FK
        int Vehicle_Category_ID FK
        string Brand
        string Model
        string Vehicle_Status
    }
    BOOKING_REQUEST {
        int Booking_ID PK
        int Customer_ID FK
        int Vehicle_ID FK
        string Booking_Status
        decimal Estimated_Total
    }
    RENTAL_CONTRACT {
        int Contract_ID PK
        int Booking_ID FK
        decimal Deposit_Amount
        decimal Rent_Price
        string Contract_Status
    }
    PAYMENT {
        int Payment_ID PK
        int Contract_ID FK
        int Method_ID FK
        decimal Amount
        string Payment_Status
    }
    REVIEW {
        int Review_ID PK
        int Contract_ID FK
        decimal Rating
    }
```

## Tóm tắt 7 nhóm bảng

| Nhóm | Các bảng chính |
|---|---|
| 1. Người dùng & Xác thực | Role, Users, User_Document, OTP_Authentication, VNeID_Link |
| 2. Chủ xe & Xe | Vehicle_Owner, Vehicle, Vehicle_Type, Vehicle_Category, Vehicle_Image, Vehicle_Document, Vehicle_Pricing, Insurance_Policy, Vehicle_Approval |
| 3. Vận hành xe | Vehicle_Availability, Vehicle_Maintenance |
| 4. Khách hàng & Đặt xe | Customer, Location, Booking_Request, Booking_Cancellation |
| 5. Hợp đồng & Thanh toán | Rental_Contract, Payment, Payment_Transaction, Payment_Method, Invoice, Penalty_Record |
| 6. Bàn giao & Hoàn tất | Handover_Report, Return_Report |
| 7. Vận hành & Giám sát hệ thống | Employee, Review, Notification, Status_History |

Toàn bộ 32 bảng và định nghĩa chi tiết được cài đặt tại [`01_schema/schema.sql`](../01_schema/schema.sql).
