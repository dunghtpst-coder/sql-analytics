-- ============================================================================
-- Q13: Tìm các hợp đồng có tổng thanh toán thực nhận nhỏ hơn tiền đặt cọc yêu cầu
-- Business question: "Hợp đồng nào đang bị thiếu tiền cọc, cần đối soát tài chính?"
-- ============================================================================
SELECT
    R.Contract_ID,
    R.Deposit_Amount,
    SUM(P.Amount) AS Total_Paid
FROM Rental_Contract R
JOIN Payment P ON R.Contract_ID = P.Contract_ID
WHERE P.Payment_Status = 'Success'
GROUP BY R.Contract_ID, R.Deposit_Amount
HAVING SUM(P.Amount) < R.Deposit_Amount;
