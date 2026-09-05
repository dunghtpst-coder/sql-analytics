-- ============================================================================
-- Q07: Top 10 xe có doanh thu cao nhất từ trước đến nay
-- Business question: "Xe nào đang mang lại doanh thu tốt nhất cho nền tảng?"
-- ============================================================================
SELECT
    V.Vehicle_ID,
    V.Brand,
    V.Model,
    SUM(P.Amount) AS Revenue
FROM Vehicle V
JOIN Booking_Request B ON V.Vehicle_ID = B.Vehicle_ID
JOIN Rental_Contract R ON B.Booking_ID = R.Booking_ID
JOIN Payment P ON R.Contract_ID = P.Contract_ID
WHERE P.Payment_Status = 'Success'
GROUP BY V.Vehicle_ID, V.Brand, V.Model
ORDER BY Revenue DESC
LIMIT 10;
