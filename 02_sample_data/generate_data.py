"""
generate_data.py
-----------------
Sinh dữ liệu mẫu (synthetic data) thực tế cho CSDL "Car Rental Service".

- Dữ liệu được sinh có chủ đích ("có câu chuyện") để khi phân tích ra insight
  hợp lý: xe SUV/Cao cấp có giá cao hơn, một số chủ xe/xe "hot" có doanh thu
  vượt trội, mùa cao điểm (Tết, hè, cuối tuần) có lượng đặt xe tăng, khách
  hạng Platinum chi tiêu nhiều hơn hẳn khách Bronze, v.v.
- Kết quả: tạo file SQLite `car_rental.db` và xuất toàn bộ INSERT statements
  ra `seed_data.sql` để ai cũng có thể chạy lại bằng bất kỳ client SQL nào.

Chạy: python3 generate_data.py
"""

import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

random.seed(42)
fake = Faker("vi_VN")
Faker.seed(42)

DB_PATH = "../car_rental.db"
SCHEMA_PATH = "../01_schema/schema.sql"
SEED_SQL_PATH = "seed_data.sql"

TODAY = datetime(2026, 3, 1)  # "hôm nay" giả định để dữ liệu nhất quán


def rand_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=seconds)


def fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def fmt_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


# ----------------------------------------------------------------------------
# Khởi tạo DB từ schema
# ----------------------------------------------------------------------------
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.executescript(open(SCHEMA_PATH, encoding="utf-8").read())
conn.commit()

sql_log = []  # để export ra seed_data.sql


def insert(table: str, columns: list, rows: list):
    placeholders = ",".join(["?"] * len(columns))
    col_str = ",".join(columns)
    cur.executemany(f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})", rows)
    conn.commit()
    for row in rows:
        vals = []
        for v in row:
            if v is None:
                vals.append("NULL")
            elif isinstance(v, (int, float)):
                vals.append(str(v))
            else:
                vals.append("'" + str(v).replace("'", "''") + "'")
        sql_log.append(f"INSERT INTO {table} ({col_str}) VALUES ({','.join(vals)});")


# ----------------------------------------------------------------------------
# I. Role, Bank, Users, Employee
# ----------------------------------------------------------------------------
insert("Role", ["Role_ID", "Role_Name", "Description"], [
    (1, "Customer", "Khách hàng thuê xe"),
    (2, "Vehicle_Owner", "Chủ xe cho thuê"),
    (3, "Employee", "Nhân viên vận hành hệ thống"),
])

banks = [
    (1, "Vietcombank", "VCB"), (2, "Techcombank", "TCB"), (3, "ACB", "ACB"),
    (4, "BIDV", "BIDV"), (5, "MB Bank", "MBB"), (6, "VPBank", "VPB"),
]
insert("Bank", ["Bank_ID", "Bank_Name", "Bank_Code"], banks)

N_EMPLOYEES = 8
N_OWNERS = 22
N_CUSTOMERS = 70
N_USERS = N_EMPLOYEES + N_OWNERS + N_CUSTOMERS

users_rows = []
uid = 1
user_role_map = {}  # uid -> 'employee'/'owner'/'customer'

for i in range(N_EMPLOYEES):
    created = rand_date(datetime(2023, 1, 1), datetime(2023, 6, 1))
    users_rows.append((uid, fake.name(), fake.phone_number()[:15], fake.unique.email(),
                        fake.sha256()[:40], 3, "Active", fmt_date(fake.date_of_birth(minimum_age=24, maximum_age=45)),
                        "Email", fmt(rand_date(created, TODAY)), fmt(created)))
    user_role_map[uid] = "employee"
    uid += 1

for i in range(N_OWNERS):
    created = rand_date(datetime(2023, 1, 1), datetime(2025, 6, 1))
    users_rows.append((uid, fake.name(), fake.phone_number()[:15], fake.unique.email(),
                        fake.sha256()[:40], 2, "Active", fmt_date(fake.date_of_birth(minimum_age=22, maximum_age=55)),
                        random.choice(["Email", "Google", "VNeID"]), fmt(rand_date(created, TODAY)), fmt(created)))
    user_role_map[uid] = "owner"
    uid += 1

for i in range(N_CUSTOMERS):
    created = rand_date(datetime(2023, 1, 1), datetime(2026, 2, 1))
    users_rows.append((uid, fake.name(), fake.phone_number()[:15], fake.unique.email(),
                        fake.sha256()[:40], 1, "Active", fmt_date(fake.date_of_birth(minimum_age=20, maximum_age=50)),
                        random.choice(["Email", "Google", "Facebook", "VNeID"]), fmt(rand_date(created, TODAY)), fmt(created)))
    user_role_map[uid] = "customer"
    uid += 1

insert("Users", ["Users_ID", "Full_Name", "Phone", "Email", "Password_Hash", "Role_ID",
                 "Status", "Date_of_Birth", "Login_With", "Last_Login_At", "Created_At"], users_rows)

employee_ids = [u for u, r in user_role_map.items() if r == "employee"]
owner_user_ids = [u for u, r in user_role_map.items() if r == "owner"]
customer_user_ids = [u for u, r in user_role_map.items() if r == "customer"]

departments = ["Kỹ thuật", "Kinh doanh", "CSKH", "Kiểm duyệt"]
positions = ["Staff", "Staff", "Staff", "Manager"]
emp_rows = []
for idx, u in enumerate(employee_ids, start=1):
    emp_rows.append((idx, u, fake.name(), fake.phone_number()[:15], f"nv{idx}@carrental.vn",
                      random.choice(departments), random.choice(positions),
                      fmt_date(rand_date(datetime(2022, 1, 1), datetime(2024, 1, 1))),
                      "Active", random.choice([9000000, 11000000, 15000000, 20000000]),
                      fmt(datetime(2023, 1, 1))))
insert("Employee", ["Employee_ID", "Users_ID", "Full_Name", "Phone", "Internal_Email",
                    "Department", "Position", "Hire_Date", "Work_Status", "Base_Salary", "Created_At"], emp_rows)

# ----------------------------------------------------------------------------
# II. Vehicle_Type, Vehicle_Category, Vehicle_Owner, Vehicle, ...
# ----------------------------------------------------------------------------
vehicle_types = [(1, "Sedan", "Xe 4 chỗ tiêu chuẩn"), (2, "SUV", "Xe gầm cao 5-7 chỗ"),
                  (3, "Hatchback", "Xe cỡ nhỏ đô thị"), (4, "Bán tải", "Xe bán tải đa dụng"),
                  (5, "MPV", "Xe gia đình 7 chỗ")]
insert("Vehicle_Type", ["Vehicle_Type_ID", "Type_Name", "Description"], vehicle_types)

vehicle_categories = [(1, "Phổ thông", "Phân khúc phổ thông, giá hợp lý"),
                       (2, "Cao cấp", "Phân khúc cao cấp, tiện nghi tốt"),
                       (3, "Hạng sang", "Phân khúc hạng sang, cao cấp nhất")]
insert("Vehicle_Category", ["Vehicle_Category_ID", "Category_Name", "Description"], vehicle_categories)

owner_rows = []
for idx, u in enumerate(owner_user_ids, start=1):
    created = rand_date(datetime(2023, 1, 1), datetime(2025, 6, 1))
    owner_rows.append((idx, u, random.choice([b[0] for b in banks]),
                        random.choice(["Cá nhân", "Cá nhân", "Doanh nghiệp"]),
                        None if random.random() < 0.6 else fake.numerify("#########"),
                        fake.numerify("##########"), "Active",
                        random.choice([15.0, 18.0, 20.0, 22.0]),
                        fmt_date(created), round(random.uniform(3.8, 5.0), 2), fmt(created)))
insert("Vehicle_Owner", ["Owner_ID", "Users_ID", "Bank_ID", "Owner_Type", "Tax_Code",
                         "Account_Number", "Owner_Status", "Commission_Rate", "Contract_Date",
                         "Owner_Rating", "Created_At"], owner_rows)

CAR_CATALOG = [
    # (brand, model, type_id, category_id, base_price/day)
    ("Toyota", "Vios", 1, 1, 550000), ("Toyota", "Camry", 1, 2, 1200000),
    ("Toyota", "Innova", 5, 1, 700000), ("Toyota", "Fortuner", 2, 2, 1300000),
    ("Honda", "City", 1, 1, 580000), ("Honda", "CR-V", 2, 2, 1250000),
    ("Hyundai", "Accent", 1, 1, 520000), ("Hyundai", "SantaFe", 2, 2, 1150000),
    ("Kia", "Seltos", 2, 1, 750000), ("Kia", "Morning", 3, 1, 420000),
    ("Mazda", "CX-5", 2, 2, 1100000), ("Mazda", "3", 1, 1, 650000),
    ("Ford", "Ranger", 4, 2, 1350000), ("Ford", "Everest", 2, 2, 1400000),
    ("VinFast", "VF8", 2, 2, 1600000), ("VinFast", "Fadil", 3, 1, 450000),
    ("Mercedes-Benz", "C200", 1, 3, 2500000), ("BMW", "3 Series", 1, 3, 2600000),
    ("Mitsubishi", "Xpander", 5, 1, 680000), ("Suzuki", "Ertiga", 5, 1, 600000),
]

N_VEHICLES = 55
vehicle_rows = []
pricing_rows = []
image_rows = []
document_rows = []
insurance_rows = []
approval_rows = []

# Một số xe được "ưu tiên" nổi bật hơn (hot) để tạo insight rõ ràng khi phân tích
hot_vehicle_ids = set()

for i in range(1, N_VEHICLES + 1):
    brand, model, type_id, cat_id, base_price = random.choice(CAR_CATALOG)
    owner_id = random.randint(1, N_OWNERS)
    year = random.choice([2020, 2021, 2022, 2023, 2024, 2025])
    seat = 7 if type_id in (2, 5) else (2 if type_id == 4 else 4)
    fuel = random.choices(["Xăng", "Dầu", "Điện", "Hybrid"], weights=[60, 25, 10, 5])[0]
    status = "Available"
    created = rand_date(datetime(2023, 1, 1), datetime(2025, 12, 1))
    vehicle_rows.append((i, owner_id, type_id, cat_id, fake.license_plate(), brand, model, year,
                          seat, fuel, random.choice(["Số tự động", "Số sàn"]),
                          random.choice(["Trắng", "Đen", "Bạc", "Xám", "Đỏ", "Xanh"]),
                          status, f"{brand} {model} đời {year}, nội thất sạch sẽ, bảo dưỡng định kỳ.",
                          fmt(created)))

    # Giá thuê: cao cấp/hạng sang có biến động giá cuối tuần/lễ cao hơn
    weekend_mult = 1.15 if cat_id == 1 else (1.2 if cat_id == 2 else 1.3)
    holiday_mult = 1.35 if cat_id == 1 else (1.5 if cat_id == 2 else 1.7)
    pricing_rows.append((i, i, "Theo ngày", base_price, round(base_price * weekend_mult),
                          round(base_price * holiday_mult), fmt(created), None))

    for k in range(2):
        image_rows.append((len(image_rows) + 1, i, f"https://cdn.carrental.vn/vehicles/{i}/img{k+1}.jpg", fmt(created)))

    for doc_type in ["Đăng ký xe", "Đăng kiểm", "Bảo hiểm TNDS"]:
        document_rows.append((len(document_rows) + 1, i, doc_type,
                               f"https://cdn.carrental.vn/docs/{i}_{doc_type}.pdf", "Approved",
                               random.choice(employee_ids), fmt(rand_date(created, TODAY))))

    insurance_rows.append((i, i, random.choice(["Bảo Việt", "PVI", "Bảo Minh", "PTI"]),
                            fake.numerify("BH-#######"), "Bắt buộc TNDS",
                            fmt_date(created), fmt_date(created + timedelta(days=365))))

    approval_rows.append((i, i, random.choice(employee_ids), "Approved", "Hồ sơ đầy đủ, đạt yêu cầu.",
                           fmt(rand_date(created, created + timedelta(days=3)))))

insert("Vehicle", ["Vehicle_ID", "Owner_ID", "Vehicle_Type_ID", "Vehicle_Category_ID",
                   "License_Plate", "Brand", "Model", "Year", "Seat_Number", "Fuel_Type",
                   "Transmission", "Color", "Vehicle_Status", "Description", "Created_At"], vehicle_rows)
insert("Vehicle_Pricing", ["Pricing_ID", "Vehicle_ID", "Price_Type", "Base_Price", "Weekend_Price",
                           "Holiday_Price", "Effective_From", "Effective_To"], pricing_rows)
insert("Vehicle_Image", ["Image_ID", "Vehicle_ID", "Image_URL", "Uploaded_At"], image_rows)
insert("Vehicle_Document", ["Document_ID", "Vehicle_ID", "Document_Type", "File_URL",
                            "Verify_Status", "Verified_By", "Verified_At"], document_rows)
insert("Insurance_Policy", ["Policy_ID", "Vehicle_ID", "Provider", "Policy_Number",
                            "Coverage_Type", "Start_Date", "End_Date"], insurance_rows)
insert("Vehicle_Approval", ["Approval_ID", "Vehicle_ID", "Employee_ID", "Approval_Status",
                            "Note", "Approved_At"], approval_rows)

# 6 xe "hot" nhất (được đặt nhiều nhất) để insight phân tích rõ nét hơn
hot_vehicle_ids = set(random.sample(range(1, N_VEHICLES + 1), 6))
# 3 xe chưa từng được thuê (để phục vụ vấn tin "xe chưa từng được thuê")
never_rented_ids = set(random.sample([v for v in range(1, N_VEHICLES + 1) if v not in hot_vehicle_ids], 3))

# ----------------------------------------------------------------------------
# III. Vehicle_Availability, Vehicle_Maintenance
# ----------------------------------------------------------------------------
maintenance_rows = []
m_id = 1
for v in range(1, N_VEHICLES + 1):
    n_maint = random.choice([1, 1, 2, 2, 3]) if v not in never_rented_ids else random.choice([0, 1])
    for _ in range(n_maint):
        start = rand_date(datetime(2024, 6, 1), datetime(2026, 2, 15))
        duration_days = random.choice([1, 2, 3, 5, 7]) if random.random() > 0.1 else random.choice([10, 14])
        end = start + timedelta(days=duration_days)
        maintenance_rows.append((m_id, v, random.choice(["Định kỳ", "Sửa chữa", "Khẩn cấp"]),
                                  fmt(start), fmt(end) if end < TODAY else None,
                                  fmt_date(end + timedelta(days=90)), "Completed" if end < TODAY else "In_Progress",
                                  random.choice(employee_ids),
                                  random.choice(["Thay dầu, kiểm tra phanh", "Bảo dưỡng cấp 2",
                                                 "Sửa hệ thống điện", "Thay lốp", "Kiểm tra tổng quát"])))
        m_id += 1
insert("Vehicle_Maintenance", ["Maintenance_ID", "Vehicle_ID", "Maintenance_Type", "Start_Date",
                               "End_Date", "Next_Due_Date", "Status", "Performed_By", "Note"], maintenance_rows)

availability_rows = []
a_id = 1
for v in range(1, N_VEHICLES + 1):
    availability_rows.append((a_id, v, fmt(datetime(2025, 1, 1)), None, "Available"))
    a_id += 1
insert("Vehicle_Availability", ["Availability_ID", "Vehicle_ID", "Start_Date", "End_Date", "Status"], availability_rows)

# ----------------------------------------------------------------------------
# IV. Customer, Location
# ----------------------------------------------------------------------------
customer_rows = []
customer_id_of_user = {}
for idx, u in enumerate(customer_user_ids, start=1):
    customer_id_of_user[u] = idx
    customer_rows.append((idx, u, 0, None, fake.bothify("REF-####") if random.random() < 0.3 else None, "Bronze"))
insert("Customer", ["Customer_ID", "Users_ID", "Total_Rentals", "Last_Rental_Date",
                    "Referral_Code", "Customer_Rank"], customer_rows)

hcm_districts = ["Quận 1", "Quận 3", "Quận 7", "Bình Thạnh", "Thủ Đức", "Gò Vấp",
                 "Phú Nhuận", "Tân Bình", "Quận 10"]
location_rows = []
for i, d in enumerate(hcm_districts, start=1):
    location_rows.append((i, f"Điểm thuê xe {d}", fake.street_address(), d, "TP. Hồ Chí Minh",
                           str(round(random.uniform(10.75, 10.85), 6)),
                           str(round(random.uniform(106.60, 106.75), 6)), f"Văn phòng đại diện tại {d}"))
insert("Location", ["Location_ID", "Location_Name", "Address", "Ward", "City",
                    "Latitude", "Longitude", "Description"], location_rows)

# ----------------------------------------------------------------------------
# V. Booking_Request, Booking_Cancellation, Rental_Contract, Payment*, Invoice,
#    Penalty_Record, Handover/Return_Report, Review
# ----------------------------------------------------------------------------
payment_methods = [(1, "Chuyển khoản ngân hàng", 1, 1), (2, "Thẻ tín dụng/ghi nợ", 1, 1),
                    (3, "Momo", 1, 1), (4, "ZaloPay", 1, 1), (5, "VNPay", 1, 1), (6, "Tiền mặt", 0, 1)]
insert("Payment_Method", ["Method_ID", "Method_Name", "Is_Online", "Is_Active"], payment_methods)

vehicle_base_price = {row[0]: row[6] for row in pricing_rows}  # vehicle_id -> base_price (index 6)
vehicle_base_price = {r[1]: r[3] for r in pricing_rows}  # Pricing rows: (id, vehicle_id, type, base, ...)

N_BOOKINGS = 320
booking_rows = []
cancel_rows = []
contract_rows = []
payment_rows = []
transaction_rows = []
invoice_rows = []
penalty_rows = []
handover_rows = []
return_rows = []
review_rows = []

contract_id_counter = 1
payment_id_counter = 1
transaction_id_counter = 1

# Mùa cao điểm: tháng 6-8 (hè) và tháng 1-2 (Tết) -> tần suất đặt xe cao hơn
def weighted_booking_date():
    month_weights = {1: 1.6, 2: 1.8, 3: 1.0, 4: 1.0, 5: 1.1, 6: 1.5,
                     7: 1.6, 8: 1.5, 9: 1.0, 10: 1.0, 11: 1.0, 12: 1.3}
    months = list(month_weights.keys())
    weights = list(month_weights.values())
    year = random.choices([2025, 2026], weights=[0.75, 0.25])[0]
    month = random.choices(months, weights=weights)[0]
    if year == 2026 and month > 2:
        month = random.choice([1, 2])
    day = random.randint(1, 27)
    return datetime(year, month, day, random.randint(7, 21), random.choice([0, 15, 30, 45]))

customer_rental_count = {c: 0 for c in customer_id_of_user.values()}
vehicle_owner_map = {r[0]: r[1] for r in vehicle_rows}  # vehicle_id -> owner_id

for b in range(1, N_BOOKINGS + 1):
    cust_id = random.randint(1, N_CUSTOMERS)
    # Khách "trung thành" (20% khách) có xu hướng đặt nhiều lần hơn
    if random.random() < 0.35:
        cust_id = random.choice(range(1, 15))

    if random.random() < 0.4:
        veh_id = random.choice(list(hot_vehicle_ids))
    else:
        veh_id = random.choice([v for v in range(1, N_VEHICLES + 1) if v not in never_rented_ids])

    pickup_loc = random.randint(1, len(hcm_districts))
    return_loc = random.choice([pickup_loc, random.randint(1, len(hcm_districts))])

    start_dt = weighted_booking_date()
    n_days = random.choice([1, 2, 2, 3, 3, 4, 5, 7])
    end_dt = start_dt + timedelta(days=n_days)

    base_price = vehicle_base_price.get(veh_id, 600000)
    estimated_total = base_price * n_days

    status_roll = random.random()
    if status_roll < 0.08:
        booking_status = "Rejected"
    elif status_roll < 0.20:
        booking_status = "Cancelled"
    else:
        booking_status = "Confirmed" if end_dt < TODAY else "Confirmed"

    created_at = start_dt - timedelta(days=random.randint(1, 10))
    approved_by = random.choice(employee_ids) if booking_status != "Rejected" else None
    approved_at = created_at + timedelta(hours=random.randint(1, 48)) if approved_by else None

    booking_rows.append((b, cust_id, veh_id, pickup_loc, return_loc, fmt(start_dt), fmt(end_dt),
                          estimated_total, booking_status, approved_by,
                          fmt(approved_at) if approved_at else None, fmt(created_at)))

    if booking_status == "Cancelled":
        cancel_rows.append((len(cancel_rows) + 1, b, cust_id, None,
                             random.choice(["Khách đổi lịch trình", "Tìm được xe khác phù hợp hơn",
                                           "Phát sinh việc đột xuất", "Không còn nhu cầu thuê xe"]),
                             round(estimated_total * random.choice([0, 0.1, 0.15])),
                             fmt(created_at + timedelta(hours=random.randint(2, 72)))))
        continue
    if booking_status == "Rejected":
        continue

    # Confirmed -> tạo hợp đồng
    customer_rental_count[cust_id] += 1
    contract_id = contract_id_counter
    contract_id_counter += 1
    deposit = round(estimated_total * 0.3, -3)
    contract_status = "Completed" if end_dt < TODAY else "Active"
    contract_rows.append((contract_id, b, deposit, estimated_total, contract_status,
                           fmt_date(start_dt), fmt_date(end_dt), fmt(created_at + timedelta(hours=1))))

    payer_uid = customer_user_ids[cust_id - 1]
    method_id = random.choices([1, 2, 3, 4, 5, 6], weights=[25, 20, 20, 15, 15, 5])[0]

    # Thanh toán đặt cọc
    pay_deposit_id = payment_id_counter
    payment_id_counter += 1
    payment_rows.append((pay_deposit_id, contract_id, method_id, payer_uid, deposit, "Deposit",
                          "Success", fmt(created_at + timedelta(hours=2)), fmt(created_at + timedelta(hours=2))))
    if method_id != 6:
        transaction_rows.append((transaction_id_counter, pay_deposit_id, random.choice(["VNPay", "Momo", "OnePay"]),
                                  "Success", "00", fake.bothify("TXN########"), deposit,
                                  fmt(created_at + timedelta(hours=2))))
        transaction_id_counter += 1

    remaining = estimated_total - deposit
    penalty_amt = 0
    late_fee = 0

    if contract_status == "Completed":
        # Thanh toán phần còn lại
        pay_final_id = payment_id_counter
        payment_id_counter += 1
        payment_rows.append((pay_final_id, contract_id, method_id, payer_uid, remaining, "Final_Payment",
                              "Success", fmt(end_dt), fmt(end_dt)))
        if method_id != 6:
            transaction_rows.append((transaction_id_counter, pay_final_id, random.choice(["VNPay", "Momo", "OnePay"]),
                                      "Success", "00", fake.bothify("TXN########"), remaining, fmt(end_dt)))
            transaction_id_counter += 1

        # Bàn giao & trả xe
        handover_rows.append((len(handover_rows) + 1, contract_id, random.choice(employee_ids),
                               "Xe sạch sẽ, đầy đủ nhiên liệu, không trầy xước đáng kể.",
                               f"signature_{contract_id}.png", fmt(start_dt)))

        has_penalty = random.random() < 0.18
        if has_penalty:
            penalty_type = random.choice(["Trả xe trễ", "Vệ sinh xe", "Hư hỏng nhẹ ngoại thất"])
            penalty_amt = random.choice([100000, 200000, 300000, 500000, 800000, 1500000])
            penalty_rows.append((len(penalty_rows) + 1, contract_id, penalty_type, penalty_amt,
                                  "Ghi nhận theo biên bản trả xe.", fmt(end_dt)))
            if penalty_type == "Trả xe trễ":
                late_fee = penalty_amt

        return_rows.append((len(return_rows) + 1, contract_id, random.choice(employee_ids),
                             "Xe được trả trong tình trạng tốt." if not has_penalty else "Phát sinh phí như biên bản.",
                             penalty_amt if has_penalty and "Hư hỏng" in str(penalty_amt) else 0,
                             fmt(end_dt)))

        invoice_rows.append((len(invoice_rows) + 1, contract_id, estimated_total, penalty_amt, late_fee,
                              estimated_total + penalty_amt, fmt(end_dt), "Paid"))

        # Đánh giá (85% khách để lại review sau khi hoàn tất)
        if random.random() < 0.85:
            owner_id = vehicle_owner_map[veh_id]
            rating_base = 4.6 if veh_id in hot_vehicle_ids else 4.1
            rating = max(1, min(5, round(random.gauss(rating_base, 0.7), 1)))
            comments_pos = ["Xe sạch, chủ xe nhiệt tình, sẽ thuê lại!", "Trải nghiệm rất tốt, xe vận hành êm.",
                            "Giao nhận xe đúng giờ, thủ tục nhanh gọn.", "Chủ xe hỗ trợ tận tình, giá hợp lý."]
            comments_neg = ["Xe hơi cũ so với mô tả.", "Giao xe trễ so với hẹn.",
                            "Cần vệ sinh nội thất kỹ hơn.", "Ổn nhưng chưa có gì đặc biệt."]
            comment = random.choice(comments_pos) if rating >= 4 else random.choice(comments_neg)
            review_rows.append((len(review_rows) + 1, contract_id, payer_uid, rating, comment, fmt(end_dt)))
    else:
        # Hợp đồng đang active -> mới bàn giao, chưa trả xe
        handover_rows.append((len(handover_rows) + 1, contract_id, random.choice(employee_ids),
                               "Xe sạch sẽ, đầy đủ nhiên liệu.", f"signature_{contract_id}.png", fmt(start_dt)))

insert("Booking_Request", ["Booking_ID", "Customer_ID", "Vehicle_ID", "Pickup_Location_ID",
                           "Return_Location_ID", "Start_Date", "End_Date", "Estimated_Total",
                           "Booking_Status", "Approved_By", "Approved_At", "Created_At"], booking_rows)
insert("Booking_Cancellation", ["Cancel_ID", "Booking_ID", "Cancelled_By_User_ID",
                                "Cancelled_By_Employee_ID", "Cancel_Reason", "Cancel_Fee", "Cancelled_At"], cancel_rows)
insert("Rental_Contract", ["Contract_ID", "Booking_ID", "Deposit_Amount", "Rent_Price",
                           "Contract_Status", "Start_Date", "End_Date", "Created_At"], contract_rows)
insert("Payment", ["Payment_ID", "Contract_ID", "Method_ID", "Payer_ID", "Amount", "Payment_Type",
                   "Payment_Status", "Payment_Date", "Created_At"], payment_rows)
insert("Payment_Transaction", ["Transaction_ID", "Payment_ID", "Gateway", "Status", "Response_Code",
                               "Transaction_Ref", "Amount", "Created_At"], transaction_rows)
insert("Invoice", ["Invoice_ID", "Contract_ID", "Subtotal", "Penalty_Fee", "Late_Fee",
                   "Total_Amount", "Issued_Date", "Payment_Status"], invoice_rows)
insert("Penalty_Record", ["Penalty_ID", "Contract_ID", "Penalty_Type", "Amount", "Note", "Created_At"], penalty_rows)
insert("Handover_Report", ["Handover_ID", "Contract_ID", "Employee_ID", "Condition_Note",
                           "Customer_Signature", "Created_At"], handover_rows)
insert("Return_Report", ["Return_ID", "Contract_ID", "Employee_ID", "Condition_Note",
                         "Damage_Fee", "Created_At"], return_rows)
insert("Review", ["Review_ID", "Contract_ID", "Reviewer_ID", "Rating", "Comment", "Created_At"], review_rows)

# Cập nhật Total_Rentals / Customer_Rank cho Customer dựa trên số hợp đồng hoàn tất
for cust_id, count in customer_rental_count.items():
    if count >= 6:
        rank = "Platinum"
    elif count >= 4:
        rank = "Gold"
    elif count >= 2:
        rank = "Silver"
    else:
        rank = "Bronze"
    cur.execute("UPDATE Customer SET Total_Rentals = ?, Customer_Rank = ? WHERE Customer_ID = ?",
                (count, rank, cust_id))
    sql_log.append(f"UPDATE Customer SET Total_Rentals = {count}, Customer_Rank = '{rank}' WHERE Customer_ID = {cust_id};")
conn.commit()

# ----------------------------------------------------------------------------
# VI. Notification, Status_History (một lượng vừa phải cho đầy đủ minh hoạ)
# ----------------------------------------------------------------------------
notif_rows = []
for i in range(1, 121):
    uid_n = random.randint(1, N_USERS)
    notif_rows.append((i, uid_n, random.choice(["BookingApproved", "PaymentReminder", "ReviewRequest", "System"]),
                        random.choice(["Yêu cầu đặt xe của bạn đã được duyệt.",
                                      "Vui lòng hoàn tất thanh toán trước 24h.",
                                      "Hãy đánh giá chuyến đi vừa rồi của bạn.",
                                      "Hệ thống bảo trì định kỳ vào 02:00 ngày mai."]),
                        random.choice([0, 1]), fmt(rand_date(datetime(2025, 1, 1), TODAY)), "Booking", random.randint(1, N_BOOKINGS)))
insert("Notification", ["Notification_ID", "Users_ID", "Type", "Message", "Is_Read", "Sent_At",
                        "Related_Entity_Type", "Related_Entity_ID"], notif_rows)

status_hist_rows = []
for i in range(1, 81):
    status_hist_rows.append((i, "Booking_Request", random.randint(1, N_BOOKINGS), "Pending",
                              random.choice(["Confirmed", "Rejected", "Cancelled"]),
                              random.choice(customer_user_ids), None,
                              fmt(rand_date(datetime(2025, 1, 1), TODAY))))
insert("Status_History", ["History_ID", "Entity_Type", "Entity_ID", "Old_Status", "New_Status",
                          "Changed_By_User_ID", "Changed_By_Employee_ID", "Changed_At"], status_hist_rows)

conn.commit()

# ----------------------------------------------------------------------------
# Xuất seed_data.sql
# ----------------------------------------------------------------------------
with open(SEED_SQL_PATH, "w", encoding="utf-8") as f:
    f.write("-- Seed data cho Car Rental Database (sinh tự động bởi generate_data.py)\n")
    f.write("-- Chạy sau schema.sql. Có thể dùng trực tiếp trên SQLite/MySQL/PostgreSQL\n")
    f.write("-- (điều chỉnh nhỏ cú pháp nếu dùng MySQL/PostgreSQL).\n\n")
    f.write("BEGIN TRANSACTION;\n\n")
    f.write("\n".join(sql_log))
    f.write("\n\nCOMMIT;\n")

print("✅ Đã tạo car_rental.db và seed_data.sql")
print(f"   Users: {N_USERS} | Vehicles: {N_VEHICLES} | Bookings: {N_BOOKINGS}")
print(f"   Contracts: {len(contract_rows)} | Payments: {len(payment_rows)} | Reviews: {len(review_rows)}")

conn.close()
