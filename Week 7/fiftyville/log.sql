/*
Tables : airports, atm_transactions, bakery_security_logs, bank_accounts,
crime_scene_reports, flights, interviews, passengers, people, phone_calls
*/

-- Read the crime scene description
SELECT description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';
-- Theft took place at 10:15 AM at Humphrey Street bakery

-- Queried the interview transcripts from the date
SELECT * FROM interviews WHERE year = 2023 AND month = 7 AND day = 28;
-- Read the interview transcripts of the three witnesses
SELECT transcript FROM interviews WHERE year = 2023 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';

/*
Relevant info :
Within ten minutes of the theft, thief escaped using a car in the bakery parking lot
Earlier that morning, the thief withdrew money from the ATM on Leggett Street
The thief called someone while leaving the bakery and talked for less than one minute
They planned to take the earliest flight out of Fiftyville the next day and the person on the other end purchased the ticket
*/

-- Review security logs for vehicles exiting the bakery parking lot between 10:15 AM and 10:25 AM
SELECT * FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28
AND hour = 10 AND minute > 15 AND minute < 25;
-- Prepare the initial list of suspects using license plate data
SELECT name FROM people WHERE license_plate in (SELECT license_plate FROM bakery_security_logs
WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25);
-- Vanessa, Barry, Iman, Sofia, Luca, Diana, Kelsey, Bruce

-- Check phone logs for a call which lasted less than one minute during this time frame
SELECT caller, receiver FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60;
-- Get the list of people who made a phone call which is in this list
SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls
WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60);
-- Kenny, Sofia, Benista, Taylor, Diana, Kelsey, Bruce, Carina

-- Suspect List : Sofia, Diana, Kelsey, Bruce

-- Check the list of ATM transactions that occurred that day in the morning at Leggett street
SELECT account_number, amount FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND
atm_location = 'Leggett Street' AND transaction_type = 'withdraw';
-- Get the list of people who hold these bank accounts
SELECT name FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND
atm_location = 'Leggett Street' AND transaction_type = 'withdraw'));
-- Kenny, Iman, Benista, Taylor, Brooke, Luca, Diana, Bruce

-- Suspect List : Diana, Bruce

-- Find the earliest flight on 29th July from Fiftyville's airport
SELECT id, destination_airport_id FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
AND year = 2023 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT 1;
-- Find the the destination airport
SELECT * FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE origin_airport_id =
(SELECT id FROM airports WHERE city = 'Fiftyville') AND year = 2023 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT 1);
-- The destination is LaGuardia Airport, New York City

-- Find the passengers travelling on this flight
SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id =
(SELECT id FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
AND year = 2023 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT 1));
-- Kenny, Sofia, Taylor, Luca, Kelsey, Edward, Bruce, Doris

-- Thief : Bruce

-- Get the thief's phone number and find the accomplice using the phone log earlier
SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE year = 2023
AND month = 7 AND day = 28 AND duration < 60 AND caller = (SELECT phone_number FROM people WHERE name = 'Bruce'));

-- Accomplice : Robin

/*
Hence, the case is closed.
Thief : Bruce
Accomplice : Robin
Destination : New York City
*/
