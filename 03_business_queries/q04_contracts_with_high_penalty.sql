-- ============================================================================
-- Q04: Tìm các hợp đồng có tổng tiền phạt phát sinh lớn hơn 1 triệu đồng
-- Business question: "Hợp đồng nào cần rà soát vì phát sinh phạt lớn bất thường?"
-- ============================================================================
SELECT
    R.Contract_ID,
    SUM(PR.Amount) AS Total_Penalty
FROM Rental_Contract R
JOIN Penalty_Record PR ON R.Contract_ID = PR.Contract_ID
GROUP BY R.Contract_ID
HAVING SUM(PR.Amount) > 1000000
ORDER BY Total_Penalty DESC;
