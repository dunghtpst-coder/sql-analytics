-- ============================================================================
-- CAR RENTAL SERVICE DATABASE — SCHEMA
-- Dự án: Thiết kế CSDL mô hình quản lý dịch vụ cho thuê xe ngắn hạn
-- ============================================================================
PRAGMA foreign_keys = ON;
-- ---------------------------------------------------------------------------
-- I. NHÓM NGƯỜI DÙNG & XÁC THỰC
-- ---------------------------------------------------------------------------

CREATE TABLE Role (
    Role_ID         INTEGER PRIMARY KEY,
    Role_Name       VARCHAR(50) NOT NULL,
    Description     TEXT
);

CREATE TABLE Bank (
    Bank_ID         INTEGER PRIMARY KEY,
    Bank_Name       VARCHAR(100) NOT NULL,
    Bank_Code       VARCHAR(20) NOT NULL
);

CREATE TABLE Users (
    Users_ID        INTEGER PRIMARY KEY,
    Full_Name       VARCHAR(70) NOT NULL,
    Phone           VARCHAR(15) NOT NULL,
    Email           VARCHAR(50) NOT NULL,
    Password_Hash   VARCHAR(255) NOT NULL,
    Role_ID         INTEGER NOT NULL,
    Status          VARCHAR(20) NOT NULL DEFAULT 'Active',
    Date_of_Birth   DATE,
    Login_With      VARCHAR(20) DEFAULT 'Email',
    Last_Login_At   DATETIME,
    Created_At      DATETIME NOT NULL,
    FOREIGN KEY (Role_ID) REFERENCES Role(Role_ID)
);

CREATE TABLE Employee (
    Employee_ID     INTEGER PRIMARY KEY,
    Users_ID        INTEGER NOT NULL,
    Full_Name       VARCHAR(70) NOT NULL,
    Phone           VARCHAR(20) NOT NULL,
    Internal_Email  VARCHAR(100) NOT NULL,
    Department      VARCHAR(50) NOT NULL,
    Position        VARCHAR(50) NOT NULL,
    Hire_Date       DATE NOT NULL,
    Work_Status     VARCHAR(20) NOT NULL DEFAULT 'Active',
    Base_Salary     DECIMAL(12,2) NOT NULL,
    Created_At      DATETIME NOT NULL,
    FOREIGN KEY (Users_ID) REFERENCES Users(Users_ID)
);

CREATE TABLE User_Document (
    Document_ID       INTEGER PRIMARY KEY,
    Users_ID          INTEGER NOT NULL,
    Document_Type     VARCHAR(50) NOT NULL,
    Document_Number   VARCHAR(50) NOT NULL,
    File_URL          VARCHAR(255) NOT NULL,
    Verified_Status   VARCHAR(20) NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (Users_ID) REFERENCES Users(Users_ID)
);

CREATE TABLE OTP_Authentication (
    OTP_ID          INTEGER PRIMARY KEY,
    Users_ID        INTEGER NOT NULL,
    OTP_Code        VARCHAR(10) NOT NULL,
    OTP_Type        VARCHAR(20) NOT NULL,
    Attempt_Count   INTEGER NOT NULL DEFAULT 0,
    Expired_At      DATETIME NOT NULL,
    Verified_Status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    Created_At      DATETIME NOT NULL,
    IP_Address      VARCHAR(100),
    FOREIGN KEY (Users_ID) REFERENCES Users(Users_ID)
);

CREATE TABLE VNeID_Link (
    VNeID_ID        INTEGER PRIMARY KEY,
    Users_ID        INTEGER NOT NULL,
    National_ID     VARCHAR(20) NOT NULL,
    Verified_Status VARCHAR(20) NOT NULL,
    Linked_At       DATETIME NOT NULL,
    Link_Status     VARCHAR(20) NOT NULL,
    FOREIGN KEY (Users_ID) REFERENCES Users(Users_ID)
);

-- ---------------------------------------------------------------------------
-- II. NHÓM CHỦ XE & XE
-- ---------------------------------------------------------------------------

CREATE TABLE Vehicle_Type (
    Vehicle_Type_ID INTEGER PRIMARY KEY,
    Type_Name       VARCHAR(50) NOT NULL,
    Description     TEXT
);

CREATE TABLE Vehicle_Category (
    Vehicle_Category_ID INTEGER PRIMARY KEY,
    Category_Name       VARCHAR(50) NOT NULL,
    Description          TEXT
);

CREATE TABLE Vehicle_Owner (
    Owner_ID          INTEGER PRIMARY KEY,
    Users_ID          INTEGER NOT NULL,
    Bank_ID           INTEGER,
    Owner_Type        VARCHAR(50) NOT NULL,
    Tax_Code          VARCHAR(50),
    Account_Number    VARCHAR(50),
    Owner_Status      VARCHAR(20) NOT NULL DEFAULT 'Active',
    Commission_Rate   DECIMAL(5,2) NOT NULL,
    Contract_Date     DATE NOT NULL,
    Owner_Rating      DECIMAL(3,2),
    Created_At        DATETIME NOT NULL,
    FOREIGN KEY (Users_ID) REFERENCES Users(Users_ID),
    FOREIGN KEY (Bank_ID) REFERENCES Bank(Bank_ID)
);

CREATE TABLE Vehicle (
    Vehicle_ID           INTEGER PRIMARY KEY,
    Owner_ID             INTEGER NOT NULL,
    Vehicle_Type_ID      INTEGER NOT NULL,
    Vehicle_Category_ID  INTEGER NOT NULL,
    License_Plate        VARCHAR(20) NOT NULL,
    Brand                VARCHAR(50) NOT NULL,
    Model                VARCHAR(70) NOT NULL,
    Year                 INTEGER NOT NULL,
    Seat_Number          INTEGER NOT NULL,
    Fuel_Type            VARCHAR(50) NOT NULL,
    Transmission         VARCHAR(50) NOT NULL,
    Color                VARCHAR(50) NOT NULL,
    Vehicle_Status       VARCHAR(20) NOT NULL DEFAULT 'Available',
    Description          TEXT,
    Created_At           DATETIME NOT NULL,
    FOREIGN KEY (Owner_ID) REFERENCES Vehicle_Owner(Owner_ID),
    FOREIGN KEY (Vehicle_Type_ID) REFERENCES Vehicle_Type(Vehicle_Type_ID),
    FOREIGN KEY (Vehicle_Category_ID) REFERENCES Vehicle_Category(Vehicle_Category_ID)
);

CREATE TABLE Vehicle_Image (
    Image_ID        INTEGER PRIMARY KEY,
    Vehicle_ID      INTEGER NOT NULL,
    Image_URL       VARCHAR(255) NOT NULL,
    Uploaded_At     DATETIME NOT NULL,
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID)
);

CREATE TABLE Vehicle_Document (
    Document_ID     INTEGER PRIMARY KEY,
    Vehicle_ID      INTEGER NOT NULL,
    Document_Type   VARCHAR(50) NOT NULL,
    File_URL        VARCHAR(255) NOT NULL,
    Verify_Status   VARCHAR(20) NOT NULL DEFAULT 'Pending',
    Verified_By     INTEGER,
    Verified_At     DATETIME,
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID),
    FOREIGN KEY (Verified_By) REFERENCES Employee(Employee_ID)
);

CREATE TABLE Vehicle_Pricing (
    Pricing_ID      INTEGER PRIMARY KEY,
    Vehicle_ID      INTEGER NOT NULL,
    Price_Type      VARCHAR(50) NOT NULL,
    Base_Price      DECIMAL(12,2) NOT NULL,
    Weekend_Price   DECIMAL(12,2) NOT NULL,
    Holiday_Price   DECIMAL(12,2) NOT NULL,
    Effective_From  DATETIME NOT NULL,
    Effective_To    DATETIME,
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID)
);

CREATE TABLE Insurance_Policy (
    Policy_ID       INTEGER PRIMARY KEY,
    Vehicle_ID      INTEGER NOT NULL,
    Provider        VARCHAR(100) NOT NULL,
    Policy_Number   VARCHAR(50) NOT NULL,
    Coverage_Type   VARCHAR(50) NOT NULL,
    Start_Date      DATE NOT NULL,
    End_Date        DATE NOT NULL,
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID)
);

CREATE TABLE Vehicle_Approval (
    Approval_ID     INTEGER PRIMARY KEY,
    Vehicle_ID      INTEGER NOT NULL,
    Employee_ID     INTEGER NOT NULL,
    Approval_Status VARCHAR(20) NOT NULL,
    Note            TEXT,
    Approved_At     DATETIME,
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID),
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
);

-- ---------------------------------------------------------------------------
-- III. NHÓM VẬN HÀNH XE
-- ---------------------------------------------------------------------------

CREATE TABLE Vehicle_Availability (
    Availability_ID INTEGER PRIMARY KEY,
    Vehicle_ID      INTEGER NOT NULL,
    Start_Date      DATETIME NOT NULL,
    End_Date        DATETIME,
    Status          VARCHAR(20) NOT NULL,
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID)
);

CREATE TABLE Vehicle_Maintenance (
    Maintenance_ID    INTEGER PRIMARY KEY,
    Vehicle_ID        INTEGER NOT NULL,
    Maintenance_Type  VARCHAR(50) NOT NULL,
    Start_Date        DATETIME NOT NULL,
    End_Date          DATETIME,
    Next_Due_Date     DATE,
    Status            VARCHAR(20) NOT NULL DEFAULT 'Completed',
    Performed_By      INTEGER,
    Note              TEXT,
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID),
    FOREIGN KEY (Performed_By) REFERENCES Employee(Employee_ID)
);

-- ---------------------------------------------------------------------------
-- IV. NHÓM KHÁCH HÀNG & ĐẶT XE
-- ---------------------------------------------------------------------------

CREATE TABLE Customer (
    Customer_ID       INTEGER PRIMARY KEY,
    Users_ID          INTEGER NOT NULL,
    Total_Rentals     INTEGER DEFAULT 0,
    Last_Rental_Date  DATE,
    Referral_Code     VARCHAR(50),
    Customer_Rank     VARCHAR(50) NOT NULL DEFAULT 'Bronze',
    FOREIGN KEY (Users_ID) REFERENCES Users(Users_ID)
);

CREATE TABLE Location (
    Location_ID     INTEGER PRIMARY KEY,
    Location_Name   VARCHAR(100) NOT NULL,
    Address         VARCHAR(255) NOT NULL,
    Ward            VARCHAR(50) NOT NULL,
    City            VARCHAR(50) NOT NULL,
    Latitude        VARCHAR(30),
    Longitude       VARCHAR(30),
    Description     TEXT
);

CREATE TABLE Booking_Request (
    Booking_ID          INTEGER PRIMARY KEY,
    Customer_ID         INTEGER NOT NULL,
    Vehicle_ID          INTEGER NOT NULL,
    Pickup_Location_ID  INTEGER NOT NULL,
    Return_Location_ID  INTEGER NOT NULL,
    Start_Date          DATETIME NOT NULL,
    End_Date            DATETIME NOT NULL,
    Estimated_Total     DECIMAL(12,2) NOT NULL,
    Booking_Status      VARCHAR(20) NOT NULL DEFAULT 'Pending',
    Approved_By         INTEGER,
    Approved_At         DATETIME,
    Created_At          DATETIME NOT NULL,
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID),
    FOREIGN KEY (Pickup_Location_ID) REFERENCES Location(Location_ID),
    FOREIGN KEY (Return_Location_ID) REFERENCES Location(Location_ID),
    FOREIGN KEY (Approved_By) REFERENCES Employee(Employee_ID)
);

CREATE TABLE Booking_Cancellation (
    Cancel_ID                  INTEGER PRIMARY KEY,
    Booking_ID                 INTEGER NOT NULL,
    Cancelled_By_User_ID       INTEGER,
    Cancelled_By_Employee_ID   INTEGER,
    Cancel_Reason              TEXT NOT NULL,
    Cancel_Fee                 DECIMAL(12,2) DEFAULT 0,
    Cancelled_At                DATETIME NOT NULL,
    FOREIGN KEY (Booking_ID) REFERENCES Booking_Request(Booking_ID),
    FOREIGN KEY (Cancelled_By_User_ID) REFERENCES Users(Users_ID),
    FOREIGN KEY (Cancelled_By_Employee_ID) REFERENCES Employee(Employee_ID)
);

-- ---------------------------------------------------------------------------
-- V. NHÓM HỢP ĐỒNG & THANH TOÁN
-- ---------------------------------------------------------------------------

CREATE TABLE Rental_Contract (
    Contract_ID       INTEGER PRIMARY KEY,
    Booking_ID        INTEGER NOT NULL,
    Deposit_Amount    DECIMAL(12,2) NOT NULL,
    Rent_Price        DECIMAL(12,2) NOT NULL,
    Contract_Status   VARCHAR(20) NOT NULL DEFAULT 'Active',
    Start_Date        DATE NOT NULL,
    End_Date          DATE NOT NULL,
    Created_At        DATETIME NOT NULL,
    FOREIGN KEY (Booking_ID) REFERENCES Booking_Request(Booking_ID)
);

CREATE TABLE Payment_Method (
    Method_ID     INTEGER PRIMARY KEY,
    Method_Name   VARCHAR(50) NOT NULL,
    Is_Online     INTEGER NOT NULL DEFAULT 1,
    Is_Active     INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE Payment (
    Payment_ID      INTEGER PRIMARY KEY,
    Contract_ID     INTEGER NOT NULL,
    Method_ID       INTEGER NOT NULL,
    Payer_ID        INTEGER NOT NULL,
    Amount          DECIMAL(12,2) NOT NULL,
    Payment_Type    VARCHAR(50) NOT NULL,
    Payment_Status  VARCHAR(20) NOT NULL DEFAULT 'Success',
    Payment_Date    DATETIME NOT NULL,
    Created_At      DATETIME NOT NULL,
    FOREIGN KEY (Contract_ID) REFERENCES Rental_Contract(Contract_ID),
    FOREIGN KEY (Method_ID) REFERENCES Payment_Method(Method_ID),
    FOREIGN KEY (Payer_ID) REFERENCES Users(Users_ID)
);

CREATE TABLE Payment_Transaction (
    Transaction_ID    INTEGER PRIMARY KEY,
    Payment_ID        INTEGER NOT NULL,
    Gateway           VARCHAR(50) NOT NULL,
    Status            VARCHAR(20) NOT NULL,
    Response_Code     VARCHAR(50),
    Transaction_Ref   VARCHAR(100),
    Amount            DECIMAL(12,2) NOT NULL,
    Created_At        DATETIME NOT NULL,
    FOREIGN KEY (Payment_ID) REFERENCES Payment(Payment_ID)
);

CREATE TABLE Invoice (
    Invoice_ID      INTEGER PRIMARY KEY,
    Contract_ID     INTEGER NOT NULL,
    Subtotal        DECIMAL(12,2) NOT NULL,
    Penalty_Fee     DECIMAL(12,2) DEFAULT 0,
    Late_Fee        DECIMAL(12,2) DEFAULT 0,
    Total_Amount    DECIMAL(12,2) NOT NULL,
    Issued_Date     DATETIME NOT NULL,
    Payment_Status  VARCHAR(20) NOT NULL DEFAULT 'Paid',
    FOREIGN KEY (Contract_ID) REFERENCES Rental_Contract(Contract_ID)
);

CREATE TABLE Penalty_Record (
    Penalty_ID    INTEGER PRIMARY KEY,
    Contract_ID   INTEGER NOT NULL,
    Penalty_Type  VARCHAR(100) NOT NULL,
    Amount        DECIMAL(12,2) NOT NULL,
    Note          TEXT,
    Created_At    DATETIME NOT NULL,
    FOREIGN KEY (Contract_ID) REFERENCES Rental_Contract(Contract_ID)
);

-- ---------------------------------------------------------------------------
-- VI. NHÓM BÀN GIAO & HOÀN TẤT
-- ---------------------------------------------------------------------------

CREATE TABLE Handover_Report (
    Handover_ID           INTEGER PRIMARY KEY,
    Contract_ID           INTEGER NOT NULL,
    Employee_ID           INTEGER NOT NULL,
    Condition_Note        TEXT NOT NULL,
    Customer_Signature    VARCHAR(255),
    Created_At            DATETIME NOT NULL,
    FOREIGN KEY (Contract_ID) REFERENCES Rental_Contract(Contract_ID),
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
);

CREATE TABLE Return_Report (
    Return_ID         INTEGER PRIMARY KEY,
    Contract_ID       INTEGER NOT NULL,
    Employee_ID       INTEGER NOT NULL,
    Condition_Note    TEXT NOT NULL,
    Damage_Fee        DECIMAL(12,2) DEFAULT 0,
    Created_At        DATETIME NOT NULL,
    FOREIGN KEY (Contract_ID) REFERENCES Rental_Contract(Contract_ID),
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
);

-- ---------------------------------------------------------------------------
-- VII. NHÓM VẬN HÀNH & GIÁM SÁT HỆ THỐNG
-- ---------------------------------------------------------------------------

CREATE TABLE Review (
    Review_ID     INTEGER PRIMARY KEY,
    Contract_ID   INTEGER NOT NULL,
    Reviewer_ID   INTEGER NOT NULL,
    Rating        DECIMAL(2,1) NOT NULL,
    Comment       TEXT,
    Created_At    DATETIME NOT NULL,
    FOREIGN KEY (Contract_ID) REFERENCES Rental_Contract(Contract_ID),
    FOREIGN KEY (Reviewer_ID) REFERENCES Users(Users_ID)
);

CREATE TABLE Notification (
    Notification_ID       INTEGER PRIMARY KEY,
    Users_ID              INTEGER NOT NULL,
    Type                  VARCHAR(50) NOT NULL,
    Message               TEXT NOT NULL,
    Is_Read               INTEGER NOT NULL DEFAULT 0,
    Sent_At               DATETIME NOT NULL,
    Related_Entity_Type   VARCHAR(50),
    Related_Entity_ID     INTEGER,
    FOREIGN KEY (Users_ID) REFERENCES Users(Users_ID)
);

CREATE TABLE Status_History (
    History_ID                 INTEGER PRIMARY KEY,
    Entity_Type                VARCHAR(50) NOT NULL,
    Entity_ID                  INTEGER NOT NULL,
    Old_Status                 VARCHAR(20),
    New_Status                 VARCHAR(20) NOT NULL,
    Changed_By_User_ID         INTEGER,
    Changed_By_Employee_ID     INTEGER,
    Changed_At                 DATETIME NOT NULL,
    FOREIGN KEY (Changed_By_User_ID) REFERENCES Users(Users_ID),
    FOREIGN KEY (Changed_By_Employee_ID) REFERENCES Employee(Employee_ID)
);

-- ============================================================================
-- INDEXES (tối ưu truy vấn cho các câu vấn tin thường dùng)
-- ============================================================================
CREATE INDEX idx_vehicle_owner ON Vehicle(Owner_ID);
CREATE INDEX idx_booking_customer ON Booking_Request(Customer_ID);
CREATE INDEX idx_booking_vehicle ON Booking_Request(Vehicle_ID);
CREATE INDEX idx_contract_booking ON Rental_Contract(Booking_ID);
CREATE INDEX idx_payment_contract ON Payment(Contract_ID);
CREATE INDEX idx_payment_payer ON Payment(Payer_ID);
CREATE INDEX idx_penalty_contract ON Penalty_Record(Contract_ID);
CREATE INDEX idx_review_contract ON Review(Contract_ID);
