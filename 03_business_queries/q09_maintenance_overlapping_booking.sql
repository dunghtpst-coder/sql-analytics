-- ============================================================================
-- Q09: Tìm xe đang trong lịch bảo trì nhưng vẫn có booking trùng khoảng thời gian
-- Business question: "Có xung đột lịch nào giữa bảo trì và đặt xe cần xử lý gấp không?"
-- ============================================================================
SELECT
    V.Vehicle_ID,
    V.Brand,
    V.Model,
    M.Start_Date AS Maintenance_Start,
    M.End_Date   AS Maintenance_End,
    B.Start_Date AS Booking_Start,
    B.End_Date   AS Booking_End,
    B.Booking_Status
FROM Vehicle V
JOIN Vehicle_Maintenance M ON V.Vehicle_ID = M.Vehicle_ID
JOIN Booking_Request B ON V.Vehicle_ID = B.Vehicle_ID
WHERE B.Booking_Status IN ('Confirmed', 'Pending')
  AND M.End_Date IS NOT NULL
  AND date(B.Start_Date) <= date(M.End_Date)
  AND date(B.End_Date) >= date(M.Start_Date);
