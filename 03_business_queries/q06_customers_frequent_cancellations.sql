-- ============================================================================
-- Q06: Tìm khách hàng có số lần hủy booking nhiều (>= 2 lần)
-- Business question: "Khách nào hay đặt rồi hủy, ảnh hưởng đến vận hành đội xe?"
-- ============================================================================
SELECT
    U.Users_ID,
    U.Full_Name,
    COUNT(BC.Cancel_ID) AS Total_Cancel
FROM Booking_Cancellation BC
JOIN Users U ON BC.Cancelled_By_User_ID = U.Users_ID
GROUP BY U.Users_ID, U.Full_Name
HAVING COUNT(BC.Cancel_ID) >= 2
ORDER BY Total_Cancel DESC;
