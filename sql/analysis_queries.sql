-- Query to rank doctors, based on how many visits they had
SELECT
    f.doctor_id, -- this is doctor id from facts to make connection
    d.doctor,  -- this is the doctor's name
    COUNT(f.visit_id) AS visit_count -- showing how many vists a doctor has had, (aggregating)
FROM fact_visits f -- use fact table, and alias it as f
JOIN dim_doctors d -- Join with the dim_doctors table, alias it as 'd'
	ON f.doctor_id = d.doctor_id -- Join condition: match doctor_id in fact_visits with doctor_id in dim_doctors
GROUP BY f.doctor_id, d.doctor -- Group results by doctor ID and doctor name (required when using COUNT)
ORDER BY visit_count DESC; -- Sort the results by visit count in descending order (most visits first)

