# Data Repository - User Guide

This folder contains all the information that powers our packaging optimization system. Think of it as a well-organized filing cabinet where we store both the original documents and the cleaned, ready-to-use versions.

## 📂 What's Inside

### 📄 Original Folder
**The Raw Materials** - Contains the original data files exactly as they were received

#### **DensityReports.xlsx**
**What it contains:** Packaging density and quality measurements
- Records of how products were packed in different configurations
- Information about folding methods, layouts, and units per carton
- Quality assessments (Good/Bad) for each packaging attempt
- Supplier details and product specifications
- Think of it as a report card for every packaging experiment we've tried

#### **HistoricalIncidents.xlsx**
**What it contains:** Records of packaging problems and their outcomes
- Details about incidents that occurred during shipping or handling
- Cost impacts of each problem (repair costs, delays, customer complaints)
- Issue descriptions and resolution status
- Timeline of when problems occurred
- Like an insurance claim database for packaging failures

#### **ProductAttributes.xlsx**
**What it contains:** Detailed information about each product
- Product specifications (size, material, weight, collection type)
- Unique product reference codes
- Categories and classifications
- Like a product catalog with all the technical details

#### **SupplierScorecard.xlsx**
**What it contains:** Performance metrics for each supplier
- Monthly performance data for all suppliers
- Key metrics like on-time delivery rates and packaging quality scores
- Number of packages handled and incidents reported
- Average cost per incident
- Like a report card showing how well each supplier is performing

#### **SbS_data_guide.pdf**
**What it contains:** Documentation explaining the data structure
- Detailed descriptions of what each column means
- Data collection methodologies
- Important notes about data quality and limitations
- Like an instruction manual for understanding all the other files

### 🔧 Preprocessed Folder
**The Cleaned and Ready Data** - Contains processed versions optimized for analysis

#### **density_report.xlsx**
**What it contains:** Cleaned version of the density reports
- Fixed naming inconsistencies (standardized supplier names)
- Corrected invalid product reference codes
- Removed or corrected unrealistic values
- Ready for analysis without further data cleaning

#### **historical_incidents.xlsx**
**What it contains:** Cleaned version of the incident records
- Standardized supplier names to match other datasets
- Consistent date formats and data types
- Validated cost impact figures

#### **product_attributes.xlsx**
**What it contains:** Cleaned product information
- Validated product reference codes
- Consistent formatting and categorization
- Ready to be linked with other datasets

#### **supplier_scorecard.xlsx**
**What it contains:** Cleaned and aggregated supplier performance data
- Standardized supplier names across all records
- Calculated summary metrics by supplier and month
- Consistent data formats for analysis

#### **full_join.xlsx**
**What it contains:** The master dataset combining all information
- All cleaned datasets merged into one comprehensive file
- Links products, suppliers, incidents, and performance data
- Includes calculated fields and derived metrics
- The main dataset used for machine learning model training
- Like having all your filing cabinets merged into one super-organized database

#### **model_outputs/**
**What it contains:** Folder for storing model prediction results
- Currently empty but designed to hold outputs from machine learning models
- Will contain prediction files and analysis results as models are run


## 🔄 Data Journey

### Stage 1: Raw Data Collection
- Original files are stored exactly as received from different sources
- No modifications made to preserve data integrity
- Serves as the permanent backup and reference point

### Stage 2: Data Cleaning & Integration
- Raw data is processed to fix errors and inconsistencies
- Multiple sources are standardized to work together
- Invalid or unrealistic values are corrected or removed
- Results in clean, analysis-ready datasets

### Stage 3: Master Dataset Creation
- All cleaned files are combined into one comprehensive dataset
- Relationships between different data sources are established
- Additional calculated fields are created for analysis
- Results in the `full_join.xlsx` file ready for machine learning

## 📊 Data Quality Improvements

### What We Fixed:
- **Naming Consistency**: Standardized supplier names across all files (e.g., "SuplA" → "SupplierA")
- **Product Codes**: Corrected invalid product reference formats
- **Data Types**: Ensured numbers are properly formatted and dates are consistent
- **Missing Values**: Handled gaps in data appropriately
- **Outliers**: Identified and corrected unrealistic values

### Quality Checks Performed:
- Validation of product reference codes against standard format
- Cross-referencing supplier names across different datasets
- Verification of numeric ranges (weights, costs, quantities)
- Date format standardization and timeline validation

## 🎯 How to Use This Data

### For Business Analysis:
- **Start with preprocessed files** for any analysis or reporting
- **Use full_join.xlsx** for comprehensive insights across all data sources
- **Refer to original files** only when you need to verify specific details

### For Machine Learning:
- **full_join.xlsx** is the primary dataset for model training
- Contains all necessary features and target variables
- Pre-processed to ensure model compatibility

### For Data Validation:
- **Compare original vs. preprocessed** to understand what changes were made
- **Use SbS_data_guide.pdf** to understand field definitions
- **Check data lineage** by tracing from original through to master dataset

## 🔍 Key Insights Available

### Supplier Performance:
- Monthly scorecards showing delivery and quality metrics
- Incident rates and cost impacts by supplier
- Trends in performance over time

### Product Analysis:
- Packaging success rates by product type and attributes
- Correlation between product characteristics and packaging outcomes
- Incident patterns by product category

### Packaging Optimization:
- Best-performing packaging configurations
- Risk factors for packaging failures
- Cost-benefit analysis of different packaging approaches

## 📈 Business Value

This organized data repository enables:
- **Data-Driven Decisions**: Base packaging choices on historical evidence
- **Performance Monitoring**: Track supplier and packaging performance over time
- **Predictive Analytics**: Use historical patterns to predict future outcomes
- **Cost Optimization**: Identify the most cost-effective packaging strategies
- **Quality Improvement**: Learn from past incidents to prevent future problems

## 🚨 Important Notes

### Data Freshness:
- Check file timestamps to understand when data was last updated
- Original files should be updated regularly from source systems
- Preprocessed files need to be regenerated when original data changes

### Data Security:
- Contains sensitive business information about suppliers and costs
- Should be handled according to company data privacy policies
- Access should be limited to authorized personnel only

### Data Limitations:
- Historical data may not reflect current business conditions
- Some data cleaning decisions involved assumptions that should be validated
- Missing data for certain time periods or products may affect analysis

---

*This data repository serves as the foundation for all packaging optimization analysis and machine learning models. Quality data leads to quality insights and better business decisions.*
