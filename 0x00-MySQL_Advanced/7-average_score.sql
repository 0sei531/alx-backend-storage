DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);  -- Adjust precision as needed

    -- Compute average score
    SELECT AVG(score) INTO avg_score 
    FROM corrections 
    WHERE user_id = user_id;

    -- Handle cases where there are no corrections
    IF avg_score IS NULL THEN
        SET avg_score = 0;  -- or NULL as per your application logic
    END IF;

    -- Update users table with the computed average score
    UPDATE users SET average_score = avg_score WHERE id = user_id;

    COMMIT;  -- Commit transaction
END $$
DELIMITER ;
