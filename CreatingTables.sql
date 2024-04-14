
CREATE TABLE Trainer (
    TrainerID SERIAL PRIMARY KEY,
    Password VARCHAR(100),
    Email VARCHAR(255) UNIQUE,
    Schedule VARCHAR(255),
    Name VARCHAR(255)
);

CREATE TABLE Members (
    RegisterationID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Phone CHAR(10) CHECK (LENGTH(Phone) = 10),
    Password VARCHAR(100),
    Weight FLOAT CHECK (Weight >= 0),
    Time FLOAT CHECK (Time >= 0),
    BoneDensity FLOAT CHECK (BoneDensity >= 0),
    FatPercentage FLOAT CHECK (FatPercentage >= 0),
    ExerciseRoutines VARCHAR(1000),
    HealthStatistics INT,
    FitnessAccomplishments VARCHAR(1000),
    Schedule VARCHAR(255)
);

CREATE TABLE FitnessClasses (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Date DATE,
    Time TIMESTAMP,
    TrainerID INT REFERENCES Trainer (TrainerID)
);

CREATE TABLE Room (
    RoomNumber SERIAL PRIMARY KEY,
    Capacity INT CHECK (Capacity >= 0),
    AvailabilityStatus VARCHAR(50),
    ID INT REFERENCES FitnessClasses (ID), -- Corrected foreign key reference
    Time TIMESTAMP
);

CREATE TABLE AdministrativeStaff (
    AdminID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255),
    Duty VARCHAR(255)
);

CREATE TABLE Trains (
    RegisterationID INT REFERENCES Members (RegisterationID),
    TrainerID INT REFERENCES Trainer (TrainerID),
    Date DATE,
    Time TIMESTAMP,
    Duration INT
);

CREATE TABLE Joins (
    ID SERIAL PRIMARY KEY,
    RegisterationID INT REFERENCES Members (RegisterationID)
);


CREATE TABLE Equipment (
    EquipmentID SERIAL PRIMARY KEY,
    EquipmentName VARCHAR(100) NOT NULL,
    EquipmentType VARCHAR(50) NOT NULL,
    LastMaintenanceDate DATE,
    MaintenanceDue BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE payment (
    billingID SERIAL PRIMARY KEY,
    registerationid INT REFERENCES members (registerationid),
    amount DECIMAL(10,2) DEFAULT 100.00,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Corrected DEFAULT value
    service VARCHAR(255),
    status VARCHAR(255) DEFAULT 'payment in process'
);

-- Insert data into Trainer table
INSERT INTO Trainer (Password, Email, Schedule, Name)
VALUES 
    ('saleh12', 'yousefSalah@gmail.com', '2024-04-10,08:00:00-12:00:00,2024-04-08,13:00:00-21:00:00', 'Yousef'),
    ('password2', 'gabewestin@gmail.com', '2024-04-06,09:00:00-12:00:00', 'Gabe'),
    ('5622', 'kaleklein@gmail.com', '2024-04-06,15:00:00-20:00:00', 'Kale');

-- Insert data into Members table
INSERT INTO Members (Name, Email, Phone, Password, Weight, Time, BoneDensity, FatPercentage, ExerciseRoutines, HealthStatistics, FitnessAccomplishments, Schedule)
VALUES 
    ('Reem', 'reemzelzle@gmail.com', '1234567890', 'reem123', 70.5, 2.5, 0.9, 20.0, 'Cardio, Weightlifting', 80, 'Ran a marathon', 'Monday, Wednesday, Friday'),
    ('Nicholas Tahiani', 'nicholasT@gmail.com', '9876543210', 'nick321', 65.2, 1.8, 0.95, 18.5, 'Yoga, Swimming', 85, 'Completed a triathlon', 'Tuesday, Thursday, Saturday');
	
-- Insert data into FitnessClasses table
INSERT INTO FitnessClasses (Name, Date, Time, TrainerID)
VALUES 
    ('Yoga Class', '2024-04-02', '2024-04-02 10:00:00', 1),
    ('Zumba Class', '2024-04-03', '2024-04-03 15:00:00', 2);

INSERT INTO room (roomnumber, availabilitystatus, capacity, id, time)
VALUES (205, 'Available', 50, NULL, '2024-04-06 18:00:00');

INSERT INTO room (roomnumber, availabilitystatus, capacity, id, time)
VALUES (106, 'Available', 30, NULL, '2024-04-11 09:00:00');

-- Insert data into AdministrativeStaff table
INSERT INTO AdministrativeStaff (Name, Email, Duty)
VALUES 
    ('abass', 'abasszelzle@gmail.com', 'Front Desk'),
    ('nour', 'nourzelzle@gmail.com', 'Finance');

-- Insert data into Trains table
INSERT INTO Trains (RegisterationID, TrainerID, Date, Time, Duration)
VALUES 
    (1, 1, '2024-04-04', '2024-04-04 08:00:00'::TIMESTAMP, 60),
    (2, 2, '2024-04-05', '2024-04-05 09:00:00'::TIMESTAMP, 45);



INSERT INTO payment (registerationid, amount, service)
VALUES (1, 100.00, 'Gym Membership');

INSERT INTO Equipment (EquipmentName, EquipmentType, LastMaintenanceDate, MaintenanceDue)
VALUES
    ('Treadmill', 'Cardio', '2023-03-15', TRUE),
    ('Barbell', 'Strength', '2023-02-20', FALSE),
    ('Stationary Bike', 'Cardio', '2023-04-10', TRUE),
    ('Dumbbells', 'Strength', '2023-03-30', FALSE);
