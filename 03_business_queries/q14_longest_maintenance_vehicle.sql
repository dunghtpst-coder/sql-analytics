-- ============================================================================
-- Q14: Top 5 xe có thời gian bảo trì (đã hoàn tất) dài nhất
-- Business question: "Xe nào tốn nhiều thời gian bảo trì nhất, ảnh hưởng khả năng khai thác?"
-- ============================================================================
SELECT
    V.Vehicle_ID,
    V.Brand,
    V.Model,
    CAST(julianday(M.End_Date) - julianday(M.Start_Date) AS INTEGER) AS Maintenance_Days
FROM Vehicle V
JOIN Vehicle_Maintenance M ON V.Vehicle_ID = M.Vehicle_ID
WHERE M.Status = 'Completed'
ORDER BY Maintenance_Days DESC
LIMIT 5;
