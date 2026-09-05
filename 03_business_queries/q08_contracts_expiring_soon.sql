-- ============================================================================
-- Q08: Liệt kê hợp đồng đang hoạt động sắp hết hạn trong 3 ngày tới
-- Business question: "Hợp đồng nào sắp đến hạn trả xe để CSKH chủ động nhắc khách?"
-- ============================================================================
SELECT *
FROM Rental_Contract
WHERE Contract_Status = 'Active'
AND date(End_Date) BETWEEN date('2026-03-01') AND date('2026-03-01', '+3 days');
-- Lưu ý: '2026-03-01' được dùng làm mốc "hôm nay" giả định khi sinh dữ liệu mẫu.
-- Trên hệ thống thật, thay bằng CURRENT_DATE (SQLite) / GETDATE() (SQL Server) / NOW() (MySQL).
