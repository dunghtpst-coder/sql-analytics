-- ============================================================================
-- Q05: Tìm các xe chưa từng có hợp đồng hoàn tất nào (xe "ế")
-- Business question: "Xe nào đang không sinh doanh thu, cần xem lại giá/ảnh/mô tả?"
-- ============================================================================
SELECT *
FROM Vehicle
WHERE Vehicle_ID NOT IN
(
    SELECT B.Vehicle_ID
    FROM Booking_Request B
    JOIN Rental_Contract R ON B.Booking_ID = R.Booking_ID
    WHERE R.Contract_Status = 'Completed'
);
