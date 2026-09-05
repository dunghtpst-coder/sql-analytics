-- ============================================================================
-- Q12: Tìm khách hàng đã thuê xe hoàn tất nhưng CHƯA từng thuê loại xe SUV
-- Business question: "Nhóm khách nào phù hợp để nhắm quảng cáo dòng xe SUV mới?"
-- (Minh họa NOT EXISTS - phép chia quan hệ)
-- ============================================================================
SELECT DISTINCT
    C.Customer_ID,
    U.Full_Name,
    C.Customer_Rank
FROM Customer C
JOIN Users U ON C.Users_ID = U.Users_ID
WHERE C.Total_Rentals > 0
AND NOT EXISTS
(
    SELECT 1
    FROM Booking_Request B
    JOIN Rental_Contract R ON B.Booking_ID = R.Booking_ID
    JOIN Vehicle V ON B.Vehicle_ID = V.Vehicle_ID
    JOIN Vehicle_Type T ON V.Vehicle_Type_ID = T.Vehicle_Type_ID
    WHERE B.Customer_ID = C.Customer_ID
      AND T.Type_Name = 'SUV'
      AND R.Contract_Status = 'Completed'
)
ORDER BY C.Customer_Rank DESC;
