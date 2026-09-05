"""
analysis.py
-----------
Analyze business data from car_rental.db and export visual charts.
This transforms the project from pure database design into a complete
Data Analyst case study: SQL -> pandas -> insight -> chart.

Run: python3 analysis.py
Output: .png files saved in the charts/ directory
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

DB_PATH = "../car_rental.db"
CHART_DIR = "charts"

plt.rcParams["figure.dpi"] = 130
plt.rcParams["font.size"] = 10
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

conn = sqlite3.connect(DB_PATH)

COLOR_PRIMARY = "#2563EB"
COLOR_ACCENT = "#F59E0B"
COLOR_GREEN = "#16A34A"
COLOR_RED = "#DC2626"


def money(x, pos=None):
    return f"{x/1e6:,.0f}M"


# ----------------------------------------------------------------------------
# 1. Monthly Revenue
# ----------------------------------------------------------------------------
df_rev = pd.read_sql_query("""
    SELECT strftime('%Y-%m', Payment_Date) AS month, SUM(Amount) AS revenue
    FROM Payment
    WHERE Payment_Status = 'Success'
    GROUP BY month
    ORDER BY month
""", conn)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_rev["month"], df_rev["revenue"], marker="o", color=COLOR_PRIMARY, linewidth=2)
ax.fill_between(df_rev["month"], df_rev["revenue"], color=COLOR_PRIMARY, alpha=0.08)
ax.set_title("Monthly Revenue (VND)", fontsize=13, fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(money))
plt.xticks(rotation=45, ha="right")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/01_monthly_revenue.png")
plt.close()
print("01_monthly_revenue.png")

# ----------------------------------------------------------------------------
# 2. Top 10 Vehicles by Revenue
# ----------------------------------------------------------------------------
df_top_vehicle = pd.read_sql_query("""
    SELECT V.Brand || ' ' || V.Model || ' (#' || V.Vehicle_ID || ')' AS vehicle,
           SUM(P.Amount) AS revenue
    FROM Vehicle V
    JOIN Booking_Request B ON V.Vehicle_ID = B.Vehicle_ID
    JOIN Rental_Contract R ON B.Booking_ID = R.Booking_ID
    JOIN Payment P ON R.Contract_ID = P.Contract_ID
    WHERE P.Payment_Status = 'Success'
    GROUP BY V.Vehicle_ID
    ORDER BY revenue DESC
    LIMIT 10
""", conn)

fig, ax = plt.subplots(figsize=(9, 6))
bars = ax.barh(df_top_vehicle["vehicle"][::-1], df_top_vehicle["revenue"][::-1], color=COLOR_PRIMARY)
ax.set_title("Top 10 Vehicles by Revenue", fontsize=13, fontweight="bold")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(money))
ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/02_top10_vehicles_revenue.png")
plt.close()
print("02_top10_vehicles_revenue.png")

# ----------------------------------------------------------------------------
# 3. Revenue Share vs. Fleet Share by Vehicle Category
# ----------------------------------------------------------------------------
df_cat = pd.read_sql_query("""
    SELECT VC.Category_Name AS category, SUM(P.Amount) AS revenue, COUNT(DISTINCT V.Vehicle_ID) AS n_vehicles
    FROM Vehicle V
    JOIN Vehicle_Category VC ON V.Vehicle_Category_ID = VC.Vehicle_Category_ID
    JOIN Booking_Request B ON V.Vehicle_ID = B.Vehicle_ID
    JOIN Rental_Contract R ON B.Booking_ID = R.Booking_ID
    JOIN Payment P ON R.Contract_ID = P.Contract_ID
    WHERE P.Payment_Status = 'Success'
    GROUP BY VC.Category_Name
""", conn)
df_cat["revenue_share"] = df_cat["revenue"] / df_cat["revenue"].sum() * 100
df_cat["vehicle_share"] = df_cat["n_vehicles"] / df_cat["n_vehicles"].sum() * 100

fig, ax = plt.subplots(figsize=(8, 5))
x = range(len(df_cat))
width = 0.35
ax.bar([i - width/2 for i in x], df_cat["revenue_share"], width, label="% of Revenue", color=COLOR_PRIMARY)
ax.bar([i + width/2 for i in x], df_cat["vehicle_share"], width, label="% of Fleet", color=COLOR_ACCENT)
ax.set_xticks(list(x))
ax.set_xticklabels(df_cat["category"])
ax.set_ylabel("%")
ax.set_title("Revenue Share vs. Fleet Share by Vehicle Category",
             fontsize=12, fontweight="bold")
ax.legend()
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/03_revenue_vs_fleet_share_by_category.png")
plt.close()
print("03_revenue_vs_fleet_share_by_category.png")

# ----------------------------------------------------------------------------
# 4. Booking Request Status Distribution
# ----------------------------------------------------------------------------
df_status = pd.read_sql_query("""
    SELECT Booking_Status, COUNT(*) AS cnt
    FROM Booking_Request
    GROUP BY Booking_Status
""", conn)

colors_map = {"Confirmed": COLOR_GREEN, "Cancelled": COLOR_RED, "Rejected": "#9CA3AF"}
fig, ax = plt.subplots(figsize=(6, 6))
colors = [colors_map.get(s, COLOR_PRIMARY) for s in df_status["Booking_Status"]]
wedges, texts, autotexts = ax.pie(
    df_status["cnt"], labels=df_status["Booking_Status"], autopct="%1.1f%%",
    colors=colors, startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1.5}
)
ax.set_title("Booking Request Status Distribution", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/04_booking_status_distribution.png")
plt.close()
print("04_booking_status_distribution.png")

# ----------------------------------------------------------------------------
# 5. Customer Distribution by Loyalty Rank
# ----------------------------------------------------------------------------
df_rank = pd.read_sql_query("""
    SELECT Customer_Rank, COUNT(*) AS cnt
    FROM Customer
    GROUP BY Customer_Rank
""", conn)
rank_order = ["Bronze", "Silver", "Gold", "Platinum"]
df_rank["Customer_Rank"] = pd.Categorical(df_rank["Customer_Rank"], categories=rank_order, ordered=True)
df_rank = df_rank.sort_values("Customer_Rank")

fig, ax = plt.subplots(figsize=(7, 5))
rank_colors = ["#CD7F32", "#C0C0C0", "#FFD700", "#7DD3FC"]
ax.bar(df_rank["Customer_Rank"].astype(str), df_rank["cnt"], color=rank_colors)
ax.set_title("Customer Distribution by Loyalty Rank", fontsize=13, fontweight="bold")
ax.set_ylabel("Number of Customers")
for i, v in enumerate(df_rank["cnt"]):
    ax.text(i, v + 0.5, str(v), ha="center", fontweight="bold")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/05_customer_rank_distribution.png")
plt.close()
print("05_customer_rank_distribution.png")

# ----------------------------------------------------------------------------
# 6. Top 10 Vehicle Owners: Revenue vs. Average Rating
# ----------------------------------------------------------------------------
df_owner_perf = pd.read_sql_query("""
    SELECT VO.Owner_ID, U.Full_Name AS owner_name,
           COUNT(DISTINCT V.Vehicle_ID) AS n_vehicles,
           SUM(P.Amount) AS revenue,
           AVG(RV.Rating) AS avg_rating
    FROM Vehicle_Owner VO
    JOIN Users U ON VO.Users_ID = U.Users_ID
    JOIN Vehicle V ON VO.Owner_ID = V.Owner_ID
    LEFT JOIN Booking_Request B ON V.Vehicle_ID = B.Vehicle_ID
    LEFT JOIN Rental_Contract R ON B.Booking_ID = R.Booking_ID
    LEFT JOIN Payment P ON R.Contract_ID = P.Contract_ID AND P.Payment_Status = 'Success'
    LEFT JOIN Review RV ON R.Contract_ID = RV.Contract_ID
    GROUP BY VO.Owner_ID
    HAVING revenue IS NOT NULL
    ORDER BY revenue DESC
    LIMIT 10
""", conn)

fig, ax1 = plt.subplots(figsize=(10, 5.5))
ax2 = ax1.twinx()
x = range(len(df_owner_perf))
ax1.bar(x, df_owner_perf["revenue"], color=COLOR_PRIMARY, alpha=0.85, label="Revenue")
ax2.plot(x, df_owner_perf["avg_rating"], color=COLOR_ACCENT, marker="o", linewidth=2, label="Avg. Rating")
ax1.set_xticks(list(x))
ax1.set_xticklabels(df_owner_perf["owner_name"], rotation=40, ha="right")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(money))
ax1.set_ylabel("Revenue (VND)")
ax2.set_ylabel("Average Rating")
ax2.set_ylim(0, 5.5)
ax1.set_title("Top 10 Vehicle Owners: Revenue vs. Average Rating",
             fontsize=12, fontweight="bold")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/06_top_owners_revenue_vs_rating.png")
plt.close()
print("06_top_owners_revenue_vs_rating.png")

conn.close()

# ----------------------------------------------------------------------------
# Key insights summary to console 
# ----------------------------------------------------------------------------
top_month = df_rev.loc[df_rev["revenue"].idxmax()]
print(f"- Peak revenue month: {top_month['month']} ({top_month['revenue']:,.0f} VND)")
print(f"- #1 Revenue vehicle: {df_top_vehicle.iloc[0]['vehicle']} ({df_top_vehicle.iloc[0]['revenue']:,.0f} VND)")
for _, row in df_cat.iterrows():
    print(f"- Category {row['category']}: accounts for {row['vehicle_share']:.1f}% of vehicles "
          f"but contributes {row['revenue_share']:.1f}% of total revenue")
cancel_rate = df_status.set_index("Booking_Status")["cnt"].get("Cancelled", 0) / df_status["cnt"].sum() * 100
reject_rate = df_status.set_index("Booking_Status")["cnt"].get("Rejected", 0) / df_status["cnt"].sum() * 100
print(f"- Booking cancellation rate: {cancel_rate:.1f}% | rejection rate: {reject_rate:.1f}%")
