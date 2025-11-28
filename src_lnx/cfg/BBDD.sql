-- Creación de la BBDD de Estados financieros de la CNBV

/*
CREATE TABLE P_CNBV_EEFF_FILECURL (
    Periodo         VARCHAR2(10),
    ClavePizarra    VARCHAR2(40),
    Iden            NUMBER,
    FEnvio          DATE,
    Taxonomia       VARCHAR2(50),
    FileXbrl        VARCHAR2(100),
    TipoFile        NUMBER,
    CURL            VARCHAR2(600)
);

CREATE TABLE P_CNBV_EEFF_TOTALES1 (
    Periodo         VARCHAR2(10),
    Iden            NUMBER,
    Hoja            VARCHAR2(10),
    ColumnaA        NUMBER,
    ColumnaB        NUMBER,
    ColumnaC        NUMBER,
    FileX           VARCHAR2(100)
);

CREATE TABLE P_CNBV_EEFF_TOTALES2(
    Periodo             VARCHAR2(10),
    ClavePizarra        VARCHAR2(40),
    Iden                NUMBER,
    FEnvio              DATE,           
    Taxonomia           VARCHAR2(50),
    TActivos            NUMBER,
    TActivosCirculantes NUMBER, 
    TCapitalContable    NUMBER,
    TPasivosCirculantes NUMBER,    
    TPasivos            NUMBER,
    UtilPerdOperacion   NUMBER,
    UtilPerdNeta        NUMBER
);


CREATE INDEX idx_CNBV_EEFF_FILECURL_1 ON P_CNBV_EEFF_FILECURL (Periodo);
CREATE INDEX idx_CNBV_EEFF_FILECURL_2 ON P_CNBV_EEFF_FILECURL(ClavePizarra);
CREATE UNIQUE INDEX idx_CNBV_EEFF_FILECURL_3 ON P_CNBV_EEFF_FILECURL(Periodo, ClavePizarra);

CREATE INDEX idx_CNBV_EEFF_TOTALES1_1 ON P_CNBV_EEFF_TOTALES1(Periodo);
CREATE INDEX idx_CNBV_EEFF_TOTALES1_2 ON P_CNBV_EEFF_TOTALES1(Iden);
CREATE UNIQUE INDEX idx_CNBV_EEFF_TOTALES1_3 ON P_CNBV_EEFF_TOTALES1(Periodo, Iden);

CREATE INDEX idx_CNBV_EEFF_TOTALES2_1 ON P_CNBV_EEFF_TOTALES2(Periodo);
CREATE INDEX idx_CNBV_EEFF_TOTALES2_2 ON P_CNBV_EEFF_TOTALES2(ClavePizarra);
CREATE UNIQUE INDEX idx_CNBV_EEFF_TOTALES2_3 ON P_CNBV_EEFF_TOTALES2(Periodo, ClavePizarra);


*/

-- Seleccionar la Tabla Producción
SELECT * FROM P_CNBV_EEFF_FILECURL;
SELECT COUNT(iden) as TOTAL FROM P_CNBV_EEFF_FILECURL;

-- Seleccionar la carga Copia Seguridad
SELECT * FROM P_BOLSAS_EVENTOS_RELEVANTES_20250602;
SELECT COUNT(N) as TOTAL FROM P_BOLSAS_EVENTOS_RELEVANTES_20250602;

-- Seleccionar la carga Histórica
SELECT * FROM P_CNBV_EEFF_FILECURL WHERE Periodo = '2025 - 1';
SELECT COUNT(Periodo) as TOTAL FROM P_CNBV_EEFF_FILECURL WHERE Periodo = '2025 - 1';





-- Seleccionar un carga Diaria
SELECT * FROM P_BOLSAS_EVENTOS_RELEVANTES WHERE NOTA = 'CARGA_DIARIA' AND TRUNC(FPROCESO) = TO_DATE('2025-06-10', 'YYYY-MM-DD');

-- Borrar una carga Diaria
-- DELETE FROM P_BOLSAS_EVENTOS_RELEVANTES WHERE NOTA = 'CARGA_DIARIA' AND TRUNC(FPROCESO) = TO_DATE('2025-06-10', 'YYYY-MM-DD');
-- COMMIT;