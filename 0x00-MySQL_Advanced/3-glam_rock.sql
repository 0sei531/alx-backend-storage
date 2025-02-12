 -- Task 3: Old school bandlists - all bands with Glam as their main style
-- ranked by their longevity
SELECT band_name,
       IFNULL(split, 2020) - formed AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', style)
ORDER BY lifespan DESC;
