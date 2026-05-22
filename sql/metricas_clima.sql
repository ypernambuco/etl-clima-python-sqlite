SELECT
    cidade,
    estado,
    COUNT(*) AS dias_analisados,
    ROUND(AVG(temperatura_media_c), 2) AS temperatura_media_c,
    ROUND(MAX(temperatura_maxima_c), 2) AS maior_temperatura_c,
    ROUND(MIN(temperatura_minima_c), 2) AS menor_temperatura_c,
    ROUND(SUM(precipitacao_mm), 2) AS precipitacao_total_mm,
    SUM(CASE WHEN precipitacao_mm > 0 THEN 1 ELSE 0 END) AS dias_com_chuva
FROM clima_diario
GROUP BY cidade, estado
ORDER BY temperatura_media_c DESC;
