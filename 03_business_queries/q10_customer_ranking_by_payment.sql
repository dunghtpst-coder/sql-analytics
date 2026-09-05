-- ============================================================================
-- Q10: Xếp hạng (RANK) khách hàng theo tổng số tiền đã thanh toán thành công
-- Business question: "Top khách hàng đóng góp doanh thu nhiều nhất là ai?"
-- (Minh họa window function RANK() OVER)
-- ============================================================================
SELECT
    U.Users_ID,
    U.Full_Name,
    SUM(P.Amount) AS Total_Spent,
    RANK() OVER (ORDER BY SUM(P.Amount) DESC) AS Customer_Rank_Position
FROM Users U
JOIN Customer C ON U.Users_ID = C.Users_ID
JOIN Payment P ON U.Users_ID = P.Payer_ID
WHERE P.Payment_Status = 'Success'
GROUP BY U.Users_ID, U.Full_Name
ORDER BY Total_Spent DESC
LIMIT 20;
