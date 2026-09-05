-- ============================================================================
-- Q02: Liệt kê các xe có tổng số lần thuê (hợp đồng) lớn hơn 5 lần
-- Business question: "Xe nào đang được khách ưa chuộng nhất để ưu tiên marketing?"
-- ============================================================================
SELECT
    V.Vehicle_ID,
    V.Brand,
    V.Model,
    COUNT(R.Contract_ID) AS Total_Rentals
FROM Vehicle V
JOIN Booking_Request B ON V.Vehicle_ID = B.Vehicle_ID
JOIN Rental_Contract R ON B.Booking_ID = R.Booking_ID
GROUP BY V.Vehicle_ID, V.Brand, V.Model
HAVING COUNT(R.Contract_ID) > 5
ORDER BY Total_Rentals DESC;
