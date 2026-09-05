-- ============================================================================
-- Q01: Tìm tất cả booking của khách hàng có tên chứa từ khóa, kèm thông tin xe
-- Business question: "Cho tôi xem lịch sử đặt xe của khách tên Anh để hỗ trợ CSKH"
-- ============================================================================
SELECT
    U.Full_Name,
    B.Booking_ID,
    V.Vehicle_ID,
    V.Brand,
    V.Model,
    B.Start_Date,
    B.End_Date,
    B.Booking_Status
FROM Users U
JOIN Customer C ON U.Users_ID = C.Users_ID
JOIN Booking_Request B ON C.Customer_ID = B.Customer_ID
JOIN Vehicle V ON B.Vehicle_ID = V.Vehicle_ID
WHERE U.Full_Name LIKE '%Anh%'
ORDER BY B.Start_Date DESC;
