-- ============================================================================
-- Q03: Tìm khách hàng có tổng chi tiêu lớn hơn mức trung bình toàn hệ thống
-- Business question: "Ai là khách hàng VIP nên được ưu tiên chăm sóc/ưu đãi?"
-- ============================================================================
SELECT
    C.Customer_ID,
    U.Full_Name,
    SUM(P.Amount) AS Total_Spent
FROM Customer C
JOIN Users U ON C.Users_ID = U.Users_ID
JOIN Payment P ON U.Users_ID = P.Payer_ID
WHERE P.Payment_Status = 'Success'
GROUP BY C.Customer_ID, U.Full_Name
HAVING SUM(P.Amount) >
(
    SELECT AVG(Total_Amount)
    FROM
    (
        SELECT SUM(Amount) AS Total_Amount
        FROM Payment
        WHERE Payment_Status = 'Success'
        GROUP BY Payer_ID
    ) X
)
ORDER BY Total_Spent DESC;
