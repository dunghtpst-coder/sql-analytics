-- ============================================================================
-- Q11: Tìm các xe có doanh thu cao hơn doanh thu trung bình của toàn bộ đội xe
-- Business question: "Xe nào đang hoạt động hiệu quả hơn mặt bằng chung?"
-- (Minh họa CTE - Common Table Expression)
-- ============================================================================
WITH Vehicle_Revenue AS (
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
)
SELECT *
FROM Vehicle_Revenue
WHERE Revenue > (SELECT AVG(Revenue) FROM Vehicle_Revenue)
ORDER BY Revenue DESC;
