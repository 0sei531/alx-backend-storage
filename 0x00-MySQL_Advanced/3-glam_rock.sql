-- Task 3: Old school band - lists bands with Glam rock as their main style, ranked by longevity

SELECT band_name,
       IF(split = 0 OR split IS NULL, 2020, split) - formed AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', style)
ORDER BY lifespan DESC;
