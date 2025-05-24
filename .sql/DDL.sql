CREATE TABLE Packaging_Results (
    SupplierName VARCHAR(100),
    GarmentType VARCHAR(50),
    Material VARCHAR(50),
    Weight FLOAT,
    ProposedUnitsPerCarton INT,
    ProposedFoldingMethod VARCHAR(50),
    ProposedLayout VARCHAR(50),
    Size VARCHAR(10),
    Collection VARCHAR(50),
    TotalIncidentsPercent FLOAT,
    AnomaliesDetectedPercent FLOAT,
    BadPackagingRatePercent INT,
    OnTimeDeliveryRatePercent FLOAT,
    AverageCostPerIncidentEUR FLOAT,
    Actual INT,
    Predicted INT,
    Probability FLOAT,
    Correct BOOLEAN,
    CONSTRAINT unique_packaging_combo UNIQUE (
        GarmentType,
        Material,
        ProposedUnitsPerCarton,
        ProposedFoldingMethod,
        ProposedLayout,
        Size,
        Collection
    )
);
