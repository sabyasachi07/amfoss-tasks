-- Keep a log of any SQL queries you execute as you solve the mystery.
select * from crime_scene_reports WHERE day = 28. AND month = 7 AND street LIKE "Chamberlin Street";
select * from interviews where year = 2020 and day = 28 and month = 7 and transcript LIKE "%courthouse%";

SELECT name FROM people JOIN courthouse_security_logs  ON courthouse_security_logs.license_plate = people.license_plate
WHERE year = 2020 and month = 7 and day = 28 AND hour = 10 and minute > 15 and activity LIKE "exit";


select * from atm_transactions WHERE atm_location like "fifer street" and day = 28 and month = 7 and year = 2020;

select passport_number from flights
JOIN airports on flights.origin_airport_id = airports.id
JOIN passengers on passengers.flight_id = flights.id
where flights.month = 7 and flights.year = 2020 and flights.day = 29 and flights.hour < 12 ORDER BY hour;

select distinct(name) from people, phone_calls where duration < 60 and month = 7 and day = 28 and year = 2020
and people.phone_number IN (phone_calls.receiver, phone_calls.caller) and people.passport_number IS NOT NULL;

select * from atm_transactions where year = 2020 and month = 7 and day = 28  and atm_location LIKE "fifer street" and transaction_type LIKE "withdraw";


--The THIEF is:
SELECT name FROM people JOIN courthouse_security_logs  ON courthouse_security_logs.license_plate = people.license_plate
WHERE year = 2020 and month = 7 and day = 28 AND hour = 10 and minute between 15 and 26 and activity LIKE "exit"
intersect
select distinct(name), passport_number from people, phone_calls JOIN bank_accounts ON  bank_accounts.person_id = people.id
where duration < 60 and month = 7 and day = 28 and year = 2020
and people.phone_number IN (phone_calls.receiver, phone_calls.caller) and people.passport_number IN (select passport_number from flights
JOIN airports on flights.origin_airport_id = airports.id
JOIN passengers on passengers.flight_id = flights.id
where flights.month = 7 and flights.year = 2020 and flights.day = 29 and flights.hour < 9 ORDER BY hour) and bank_accounts.account_number IN(
select account_number from atm_transactions where year = 2020 and month = 7 and day = 28  and atm_location LIKE "fifer street" and transaction_type LIKE "withdraw"
);

--The thief ESCAPED TO:
select city from airports
JOIN flights ON flights.destination_airport_id = airports.id
JOIN passengers ON passengers.flight_id = flights.id
where passengers.passport_number = 5773159633;


--The ACCOMPLICE is:
select name from people
JOIN phone_calls on people.phone_number = phone_calls.receiver
where phone_calls.duration < 60 and phone_calls.month = 7 and phone_calls.day = 28 and phone_calls.year = 2020 = (select phone_number from people where name LIKe "Ernest");


