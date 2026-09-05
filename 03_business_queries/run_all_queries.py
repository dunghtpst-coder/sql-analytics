"""
run_all_queries.py
-------------------
Chạy toàn bộ các file .sql trong thư mục hiện tại (q01.. q15) trên car_rental.db,
in kết quả ra console và lưu thành results/results.md để làm bằng chứng review
(khi HR/interviewer xem repo mà không muốn tự cài DB để chạy thử).

Chạy: python3 run_all_queries.py
"""
import sqlite3
import glob
import os

DB_PATH = "../car_rental.db"
OUT_PATH = "results/results.md"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

query_files = sorted(glob.glob("q*.sql"))
lines = ["# Kết quả chạy thử 15 câu vấn tin (Business Queries)\n",
         "> Sinh tự động bởi `run_all_queries.py` trên dữ liệu mẫu trong `car_rental.db`.\n"]

for qf in query_files:
    sql = open(qf, encoding="utf-8").read()
    title = os.path.basename(qf)
    print(f"\n=== {title} ===")
    lines.append(f"\n## {title}\n")
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        if not rows:
            print("(Không có dòng kết quả)")
            lines.append("_(Không có dòng kết quả phù hợp điều kiện)_\n")
            continue
        cols = rows[0].keys()
        # In console (giới hạn 10 dòng đầu cho gọn)
        for r in rows[:10]:
            print(dict(r))
        print(f"... tổng {len(rows)} dòng" if len(rows) > 10 else f"tổng {len(rows)} dòng")

        # Markdown table (giới hạn 15 dòng để README/kết quả không quá dài)
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("|" + "---|" * len(cols))
        for r in rows[:15]:
            lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
        if len(rows) > 15:
            lines.append(f"\n_... và {len(rows) - 15} dòng khác (tổng {len(rows)} dòng)._\n")
    except Exception as e:
        print(f"LỖI: {e}")
        lines.append(f"**Lỗi khi chạy:** `{e}`\n")

os.makedirs("results", exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\n✅ Đã lưu kết quả vào {OUT_PATH}")
conn.close()
