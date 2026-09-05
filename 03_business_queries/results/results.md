# Kết quả chạy thử 15 câu vấn tin (Business Queries)

> Sinh tự động bởi `run_all_queries.py` trên dữ liệu mẫu trong `car_rental.db`.


## q01_bookings_by_customer_name.sql

| Full_Name | Booking_ID | Vehicle_ID | Brand | Model | Start_Date | End_Date | Booking_Status |
|---|---|---|---|---|---|---|---|
| Anh Quang Đặng | 265 | 41 | Toyota | Camry | 2026-02-08 10:00:00 | 2026-02-09 10:00:00 | Confirmed |
| Anh Đức Đặng | 145 | 44 | Ford | Ranger | 2025-11-18 21:30:00 | 2025-11-25 21:30:00 | Confirmed |
| Anh Quang Đặng | 89 | 22 | Toyota | Camry | 2025-08-20 08:00:00 | 2025-08-22 08:00:00 | Confirmed |
| Anh Đức Đặng | 93 | 44 | Ford | Ranger | 2025-07-27 11:15:00 | 2025-07-30 11:15:00 | Confirmed |
| Anh Quang Đặng | 20 | 28 | Mitsubishi | Xpander | 2025-06-27 08:30:00 | 2025-07-02 08:30:00 | Confirmed |

## q02_vehicles_rented_over_5_times.sql

| Vehicle_ID | Brand | Model | Total_Rentals |
|---|---|---|---|
| 50 | Mazda | CX-5 | 31 |
| 44 | Ford | Ranger | 20 |
| 52 | Toyota | Innova | 20 |
| 28 | Mitsubishi | Xpander | 19 |
| 40 | Kia | Morning | 18 |
| 36 | Kia | Seltos | 16 |
| 41 | Toyota | Camry | 8 |
| 22 | Toyota | Camry | 6 |
| 55 | Toyota | Camry | 6 |

## q03_customers_above_average_spending.sql

| Customer_ID | Full_Name | Total_Spent |
|---|---|---|
| 1 | Phương Hải Dương | 53880000 |
| 3 | Quang Quang Nguyễn | 49720000 |
| 2 | Bảo Mai Lê | 37490000 |
| 7 | Chi Đặng | 31880000 |
| 12 | Chị Khoa Vũ | 31610000 |
| 4 | Phúc Đức Lê | 30920000 |
| 14 | Hưng Phạm | 29300000 |
| 9 | Quang Mai Vũ | 27570000 |
| 11 | Ông Nam Hoàng | 26380000 |
| 29 | Phúc Vũ | 26100000 |
| 8 | Quý cô Dương Dương | 22450000 |
| 54 | Quang Mai Hoàng | 20770000 |
| 40 | Quý cô Ánh Mai | 20650000 |
| 13 | Nhiên Hoàng | 20620000 |
| 39 | Thành Bảo Nguyễn | 18140000 |

_... và 11 dòng khác (tổng 26 dòng)._


## q04_contracts_with_high_penalty.sql

| Contract_ID | Total_Penalty |
|---|---|
| 102 | 1500000 |
| 117 | 1500000 |
| 188 | 1500000 |
| 231 | 1500000 |
| 254 | 1500000 |

## q05_vehicles_never_rented.sql

| Vehicle_ID | Owner_ID | Vehicle_Type_ID | Vehicle_Category_ID | License_Plate | Brand | Model | Year | Seat_Number | Fuel_Type | Transmission | Color | Vehicle_Status | Description | Created_At |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 22 | 2 | 2 | 63V-37524 | Ford | Everest | 2023 | 7 | Dầu | Số sàn | Xám | Available | Ford Everest đời 2023, nội thất sạch sẽ, bảo dưỡng định kỳ. | 2023-09-28 08:12:34 |
| 38 | 5 | 2 | 2 | 90S-50723 | Ford | Everest | 2021 | 7 | Xăng | Số tự động | Đen | Available | Ford Everest đời 2021, nội thất sạch sẽ, bảo dưỡng định kỳ. | 2025-05-29 03:19:38 |
| 43 | 9 | 2 | 2 | 60Đ-42232 | Honda | CR-V | 2023 | 7 | Hybrid | Số sàn | Trắng | Available | Honda CR-V đời 2023, nội thất sạch sẽ, bảo dưỡng định kỳ. | 2024-04-03 11:40:14 |
| 46 | 18 | 2 | 2 | 00L-17012 | Hyundai | SantaFe | 2021 | 7 | Xăng | Số sàn | Đỏ | Available | Hyundai SantaFe đời 2021, nội thất sạch sẽ, bảo dưỡng định kỳ. | 2024-07-30 08:18:42 |

## q06_customers_frequent_cancellations.sql

| Users_ID | Full_Name | Total_Cancel |
|---|---|---|
| 9 | Quang Nguyễn | 3 |
| 13 | Bảo Phạm | 3 |
| 2 | Lâm Mai Hoàng | 2 |
| 7 | Kim Bùi | 2 |
| 12 | Hải Bùi | 2 |

## q07_top_revenue_vehicle.sql

| Vehicle_ID | Brand | Model | Revenue |
|---|---|---|---|
| 50 | Mazda | CX-5 | 129800000 |
| 44 | Ford | Ranger | 83700000 |
| 36 | Kia | Seltos | 45750000 |
| 28 | Mitsubishi | Xpander | 44880000 |
| 52 | Toyota | Innova | 43400000 |
| 6 | VinFast | VF8 | 28800000 |
| 22 | Toyota | Camry | 27600000 |
| 41 | Toyota | Camry | 25200000 |
| 55 | Toyota | Camry | 25200000 |
| 40 | Kia | Morning | 24360000 |

## q08_contracts_expiring_soon.sql

_(Không có dòng kết quả phù hợp điều kiện)_


## q09_maintenance_overlapping_booking.sql

| Vehicle_ID | Brand | Model | Maintenance_Start | Maintenance_End | Booking_Start | Booking_End | Booking_Status |
|---|---|---|---|---|---|---|---|
| 44 | Ford | Ranger | 2025-10-12 22:03:33 | 2025-10-26 22:03:33 | 2025-10-24 14:30:00 | 2025-10-27 14:30:00 | Confirmed |
| 44 | Ford | Ranger | 2025-10-12 22:03:33 | 2025-10-26 22:03:33 | 2025-10-10 20:00:00 | 2025-10-13 20:00:00 | Confirmed |
| 48 | Hyundai | Accent | 2025-09-24 02:22:34 | 2025-09-29 02:22:34 | 2025-09-27 12:45:00 | 2025-09-30 12:45:00 | Confirmed |
| 52 | Toyota | Innova | 2025-02-10 07:50:45 | 2025-02-13 07:50:45 | 2025-02-07 10:30:00 | 2025-02-10 10:30:00 | Confirmed |

## q10_customer_ranking_by_payment.sql

| Users_ID | Full_Name | Total_Spent | Customer_Rank_Position |
|---|---|---|---|
| 31 | Phương Hải Dương | 53880000 | 1 |
| 33 | Quang Quang Nguyễn | 49720000 | 2 |
| 32 | Bảo Mai Lê | 37490000 | 3 |
| 37 | Chi Đặng | 31880000 | 4 |
| 42 | Chị Khoa Vũ | 31610000 | 5 |
| 34 | Phúc Đức Lê | 30920000 | 6 |
| 44 | Hưng Phạm | 29300000 | 7 |
| 39 | Quang Mai Vũ | 27570000 | 8 |
| 41 | Ông Nam Hoàng | 26380000 | 9 |
| 59 | Phúc Vũ | 26100000 | 10 |
| 38 | Quý cô Dương Dương | 22450000 | 11 |
| 84 | Quang Mai Hoàng | 20770000 | 12 |
| 70 | Quý cô Ánh Mai | 20650000 | 13 |
| 43 | Nhiên Hoàng | 20620000 | 14 |
| 69 | Thành Bảo Nguyễn | 18140000 | 15 |

_... và 5 dòng khác (tổng 20 dòng)._


## q11_vehicles_above_average_revenue.sql

| Vehicle_ID | Brand | Model | Revenue |
|---|---|---|---|
| 50 | Mazda | CX-5 | 129800000 |
| 44 | Ford | Ranger | 83700000 |
| 36 | Kia | Seltos | 45750000 |
| 28 | Mitsubishi | Xpander | 44880000 |
| 52 | Toyota | Innova | 43400000 |
| 6 | VinFast | VF8 | 28800000 |
| 22 | Toyota | Camry | 27600000 |
| 41 | Toyota | Camry | 25200000 |
| 55 | Toyota | Camry | 25200000 |
| 40 | Kia | Morning | 24360000 |
| 47 | VinFast | VF8 | 24000000 |
| 33 | Mercedes-Benz | C200 | 22500000 |
| 19 | VinFast | VF8 | 22400000 |
| 12 | Toyota | Camry | 21600000 |
| 20 | Toyota | Fortuner | 20800000 |

_... và 1 dòng khác (tổng 16 dòng)._


## q12_customers_never_rented_suv.sql

| Customer_ID | Full_Name | Customer_Rank |
|---|---|---|
| 6 | Trọng Mai | Silver |
| 16 | Nam Trần | Silver |
| 32 | Nhật Hoàng | Silver |
| 34 | Hoàng Văn Vũ | Silver |
| 37 | Thành Thế Dương | Silver |
| 45 | An Tấn Lê | Silver |
| 50 | Anh Quang Đặng | Silver |
| 52 | Hải Bùi | Silver |
| 61 | Trung Nguyễn | Silver |
| 62 | Anh Đức Đặng | Silver |
| 58 | Ông Tú Dương | Gold |
| 26 | Nam Dương | Bronze |
| 30 | Nhật Đặng | Bronze |
| 31 | Cô An Vũ | Bronze |
| 44 | Phương Hải Mai | Bronze |

_... và 6 dòng khác (tổng 21 dòng)._


## q13_contracts_underpaid_vs_deposit.sql

_(Không có dòng kết quả phù hợp điều kiện)_


## q14_longest_maintenance_vehicle.sql

| Vehicle_ID | Brand | Model | Maintenance_Days |
|---|---|---|---|
| 9 | Ford | Ranger | 14 |
| 11 | Mazda | CX-5 | 14 |
| 16 | Hyundai | SantaFe | 14 |
| 25 | Hyundai | SantaFe | 14 |
| 29 | Ford | Ranger | 14 |

## q15_monthly_revenue_growth.sql

| Month | Revenue | Prev_Month_Revenue | Growth_Percent |
|---|---|---|---|
| 2024-12 | 4353000 | None | None |
| 2025-01 | 81932000 | 4353000 | 1782.2 |
| 2025-02 | 69445000 | 81932000 | -15.2 |
| 2025-03 | 45792000 | 69445000 | -34.1 |
| 2025-04 | 34058000 | 45792000 | -25.6 |
| 2025-05 | 61448000 | 34058000 | 80.4 |
| 2025-06 | 76132000 | 61448000 | 23.9 |
| 2025-07 | 64980000 | 76132000 | -14.6 |
| 2025-08 | 40760000 | 64980000 | -37.3 |
| 2025-09 | 35591000 | 40760000 | -12.7 |
| 2025-10 | 61581000 | 35591000 | 73.0 |
| 2025-11 | 50252000 | 61581000 | -18.4 |
| 2025-12 | 35840000 | 50252000 | -28.7 |
| 2026-01 | 105042000 | 35840000 | 193.1 |
| 2026-02 | 90414000 | 105042000 | -13.9 |