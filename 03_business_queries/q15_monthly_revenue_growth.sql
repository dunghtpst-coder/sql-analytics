-- ============================================================================
-- Q15: Doanh thu theo từng tháng và % tăng trưởng so với tháng trước
-- Business question: "Doanh thu theo tháng đang biến động như thế nào, mùa nào cao điểm?"
-- (Minh họa window function LAG() để tính tăng trưởng MoM)
-- ============================================================================
WITH Monthly_Revenue AS (
    SELECT
        strftime('%Y-%m', Payment_Date) AS Month,
        SUM(Amount) AS Revenue
    FROM Payment
    WHERE Payment_Status = 'Success'
    GROUP BY strftime('%Y-%m', Payment_Date)
)
SELECT
    Month,
    Revenue,
    LAG(Revenue) OVER (ORDER BY Month) AS Prev_Month_Revenue,
    ROUND(
        100.0 * (Revenue - LAG(Revenue) OVER (ORDER BY Month))
        / NULLIF(LAG(Revenue) OVER (ORDER BY Month), 0), 1
    ) AS Growth_Percent
FROM Monthly_Revenue
ORDER BY Month;
