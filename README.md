# 🛠️ Retail ETL Pipeline (AWS → Snowflake → Dashboard)

## 📌 Overview

This project implements an end-to-end ETL pipeline for retail sales data, automating the complete workflow from raw data ingestion to interactive analytics dashboards.

**Pipeline Flow:**
```
Raw Data Ingestion → AWS S3 (/raw/) → Data Cleaning → AWS Lambda (Python) → 
Storage → S3 (/cleaned/) → Load → Snowflake (via COPY INTO) → 
Analytics & Dashboard → Snowflake Snowsight
```

**✅ Goal:** Automate raw → cleaned → loaded → visualized in a single workflow.

---

## 📊 Architecture Diagram

![ETL Pipeline Architecture](diagrams/etl_pipeline.png)

**Architecture Flow:**
```
[S3 Raw] → [Lambda Cleaning] → [S3 Cleaned] → [Snowflake Stage] → [Snowflake Table] → [Snowsight Dashboard]
```

---

## 📂 Project Phases

### **Phase 1–3: Infrastructure Setup**

**Completed Tasks:**
- ✅ Created S3 buckets:
  - `etl-retail-data-rounit/raw/` → raw files
  - `etl-retail-data-rounit/cleaned/` → cleaned files
- ✅ Configured IAM role & policies
- ✅ Setup AWS Lambda trigger for S3 → clean data

**📸 Screenshots:**

![S3 Bucket Structure](screenshots/s3_structure.png)
*S3 bucket structure showing raw/ and cleaned/ folders*

---

### **Phase 4–6: ETL Processing**

**Completed Tasks:**
- ✅ Lambda function processes new CSV uploads → cleans & outputs to `/cleaned/`
- ✅ Snowflake COPY INTO loads cleaned data into `sales_cleaned` table
- ✅ Data successfully queried inside Snowflake

**📸 Screenshots:**

![AWS Lambda Function](screenshots/lambda_code.png)
*AWS Lambda function code editor showing ETL cleaning logic*

![Snowflake COPY INTO Command](screenshots/snowflake_copy_into.png)
*Snowflake worksheet showing COPY INTO command execution*

![Snowflake Query Results](screenshots/snowflake_query.png)
*Query results showing cleaned data: SELECT * FROM sales_cleaned LIMIT 10*

---

### **Phase 7: Analytics & Dashboard**

**Completed Tasks:**
- ✅ Built interactive **Retail ETL Dashboard** in Snowsight with 5 analytical tiles:
  1. **Total Sales by Region** (Bar Chart)
  2. **Monthly Sales Trend** (Line Chart)
  3. **Top 5 Products** (Bar Chart)
  4. **Category Sales Distribution** (Bar Chart)
  5. **Average Order Value Trend** (Line Chart)

**📸 Screenshots:**

![Retail ETL Dashboard](screenshots/dashboard.png)
*Complete Retail ETL Dashboard in Snowsight showing all 5 analytical charts*

---

### **Phase 8: Documentation & Polish**

**Completed Tasks:**
- ✅ Finalized README.md (this file)
- ✅ Added architecture diagram
- ✅ Collected screenshots under `screenshots/` directory
- ✅ Created comprehensive documentation

---

### **Phase 9: Final Showcase**

**End-to-End Workflow:**
1. Upload dirty CSV → `/raw/`
2. Lambda auto-triggers → cleans data → saves to `/cleaned/`
3. Snowflake loads → `sales_cleaned` table
4. Dashboard refreshes → updated charts

**📸 Screenshots:**

![Before and After Processing](screenshots/before_after_s3.png)
*Before → After: Raw data vs Cleaned data in S3*

![Updated Dashboard](screenshots/dashboard_updated.png)
*Dashboard with refreshed data after new file processing*

---

## 🚀 How to Run

### **Step 1: Upload Raw Data**
```bash
# Upload raw CSV to S3 bucket
aws s3 cp your_raw_file.csv s3://etl-retail-data-rounit/raw/
```

### **Step 2: Lambda Auto-Processing**
- Lambda automatically triggers on S3 upload
- Cleans and processes data
- Saves cleaned file to `/cleaned/` folder

### **Step 3: Load into Snowflake**
```sql
-- In Snowflake worksheet:
USE WAREHOUSE etl_wh;
USE DATABASE etl_db;
USE SCHEMA etl_schema;

COPY INTO sales_cleaned
FROM @cleaned_stage
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1)
ON_ERROR = 'CONTINUE';
```

### **Step 4: View Dashboard**
- Navigate to Snowsight
- Open **Retail ETL Dashboard**
- View updated analytics and insights

---

## ✅ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Storage** | AWS S3 | Raw and cleaned data storage |
| **Processing** | AWS Lambda (Python) | ETL cleaning function |
| **Data Warehouse** | Snowflake | Data storage and querying |
| **Analytics** | Snowsight | Interactive dashboards |
| **Orchestration** | S3 Event Triggers | Automated pipeline execution |

---

## 📁 Project Structure

```
etl-project/
├── data/
│   ├── sample_sales.csv
│   └── sample_sales_dirty.csv
├── diagrams/
│   └── etl_pipeline.png
├── scripts/
│   ├── lambda/
│   │   └── lambda_function.py
│   ├── automation_plan.md
│   ├── etl_spec.md
│   ├── snowflake_readme.md
│   └── snowflake_setup.sql
├── screenshots/
│   ├── s3_structure.png
│   ├── lambda_code.png
│   ├── snowflake_copy_into.png
│   ├── snowflake_query.png
│   ├── dashboard.png
│   ├── before_after_s3.png
│   └── dashboard_updated.png
└── README.md
```

---

## 📸 Screenshots Index

| Screenshot | Description | Location |
|------------|-------------|----------|
| **S3 Structure** | Raw & Cleaned folders in S3 | `screenshots/s3_structure.png` |
| **Lambda Code** | Lambda function code editor | `screenshots/lambda_code.png` |
| **Snowflake COPY INTO** | COPY INTO command execution | `screenshots/snowflake_copy_into.png` |
| **Snowflake Query** | Cleaned data query results | `screenshots/snowflake_query.png` |
| **Dashboard** | Complete Retail ETL Dashboard | `screenshots/dashboard.png` |
| **Before/After S3** | Raw vs Cleaned data comparison | `screenshots/before_after_s3.png` |
| **Updated Dashboard** | Dashboard with new data | `screenshots/dashboard_updated.png` |
| **Architecture Diagram** | ETL pipeline architecture | `diagrams/etl_pipeline.png` |

---

## 🔧 Setup Instructions

### **Prerequisites**
- AWS Account with S3 and Lambda access
- Snowflake account
- Python 3.9+ for Lambda development

### **AWS Setup**
1. Create S3 bucket: `etl-retail-data-rounit`
2. Create folders: `/raw/` and `/cleaned/`
3. Deploy Lambda function from `scripts/lambda/lambda_function.py`
4. Configure S3 trigger for Lambda
5. Set up IAM roles and policies

### **Snowflake Setup**
1. Create warehouse: `etl_wh`
2. Create database: `etl_db`
3. Create schema: `etl_schema`
4. Create external stage pointing to S3 `/cleaned/`
5. Create table: `sales_cleaned`

### **Dashboard Setup**
1. Open Snowsight
2. Create new dashboard: "Retail ETL Dashboard"
3. Add 5 charts as specified in Phase 7
4. Configure auto-refresh settings

---

## 🎯 Key Features

- **🔄 Automated Pipeline**: End-to-end automation from upload to visualization
- **🧹 Data Cleaning**: Comprehensive ETL processing with Python Lambda
- **📊 Real-time Analytics**: Interactive dashboards with multiple chart types
- **☁️ Cloud-Native**: Fully serverless architecture using AWS and Snowflake
- **📈 Scalable**: Handles varying data volumes efficiently
- **🔍 Monitoring**: Built-in logging and error handling

---

## 📈 Business Impact

- **Reduced Processing Time**: From hours to minutes
- **Improved Data Quality**: Automated cleaning and validation
- **Real-time Insights**: Instant dashboard updates
- **Cost Efficiency**: Serverless, pay-per-use architecture
- **Scalability**: Handles growing data volumes seamlessly

---

## 🚀 Future Enhancements

- [ ] Add data quality monitoring alerts
- [ ] Implement incremental loading strategies
- [ ] Add more advanced analytics (ML predictions)
- [ ] Create mobile-responsive dashboard views
- [ ] Add automated testing for Lambda functions

---

**🎉 Project Status: ✅ COMPLETED**

*This ETL pipeline successfully demonstrates modern cloud-based data engineering practices with full automation, real-time processing, and interactive analytics.*

A comprehensive ETL (Extract, Transform, Load) pipeline for processing sales data from various sources into a centralized data warehouse using AWS and Snowflake.

## 📋 Project Overview

This project demonstrates a complete data engineering workflow that:
- **Extracts** sales data from multiple sources
- **Transforms** data using Python and SQL
- **Loads** processed data into Snowflake data warehouse
- **Orchestrates** the entire pipeline using modern data tools

## 🏗️ Architecture

```
[Data Sources] → [AWS S3] → [Python ETL] → [Snowflake] → [Analytics/BI]
```

*Architecture diagram will be added in Phase 1*

## 📁 Project Structure

```
etl-project/
├── data/                   # Sample datasets and raw data
│   └── sample_sales.csv   # Generated sample sales data (150+ records)
├── scripts/               # ETL scripts and utilities
│   └── generate_data.py   # Sample data generator
├── notebooks/             # Jupyter notebooks for analysis
├── diagrams/              # Architecture and workflow diagrams
├── screenshots/           # Project documentation images
├── .env.template         # Environment variables template
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🛠️ Technology Stack

- **Cloud Platform**: AWS (S3, Lambda, EC2)
- **Data Warehouse**: Snowflake
- **Programming**: Python 3.9+
- **Data Processing**: Pandas, SQL
- **Orchestration**: Apache Airflow (planned)
- **Version Control**: Git/GitHub
- **Region**: Asia-Pacific (Singapore) - `ap-southeast-1`

## 📊 Sample Data

The project includes a realistic sales dataset with:
- **150+ records** of e-commerce transactions
- **Multiple product categories**: Apparel, Electronics, Home, Outdoors, etc.
- **Regional coverage**: Singapore, Malaysia, Thailand, Vietnam, Philippines, Indonesia
- **Time range**: Last 90 days of sales data
- **Realistic pricing** and quantity variations

### Data Schema
```
order_id     | product      | category   | quantity | price  | order_date | region
1001         | Blue T-Shirt | Apparel    | 2        | 30.00  | 2025-09-01 | Singapore
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- AWS CLI (optional)
- Snowflake account

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RounitR/etl-project.git
   cd etl-project
   ```

2. **Set up environment**
   ```bash
   # Copy environment template
   cp .env.template .env
   
   # Edit .env with your credentials
   # (Never commit .env to version control)
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Generate Sample Data

```bash
cd scripts
python generate_data.py
```

This creates fresh sample data in `data/sample_sales.csv` with 150 realistic sales records.

## 📈 Project Phases

### ✅ Phase 0: Project Setup (Completed)
- [x] GitHub repository setup
- [x] Project folder structure
- [x] Sample data generation
- [x] Environment configuration
- [x] Documentation foundation

### 🔄 Phase 1: Data Extraction (In Progress)
- [ ] AWS S3 bucket setup
- [ ] Data ingestion scripts
- [ ] API data sources integration
- [ ] Data validation framework

### 📋 Phase 2: Data Transformation (Planned)
- [ ] Data cleaning and preprocessing
- [ ] Business logic implementation
- [ ] Data quality checks
- [ ] Performance optimization

### 🏢 Phase 3: Data Loading (Planned)
- [ ] Snowflake warehouse setup
- [ ] Table schema design
- [ ] Bulk loading processes
- [ ] Incremental updates

### 🔄 Phase 4: Orchestration (Planned)
- [ ] Airflow DAG development
- [ ] Scheduling and monitoring
- [ ] Error handling and alerts
- [ ] Performance monitoring

## 🔧 Configuration

### Environment Variables
Copy `.env.template` to `.env` and configure:

```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-southeast-1

# Snowflake Configuration
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=ROUNITDTU
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ROLE=your_role
SNOWFLAKE_WAREHOUSE=your_warehouse
```

## 📸 Screenshots

*Screenshots will be added as the project progresses through each phase*

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Project Maintainer**: RounitR  
**GitHub**: [https://github.com/RounitR/etl-project](https://github.com/RounitR/etl-project)  
**Region**: Asia-Pacific (Singapore)

---

*Last Updated: January 2025*  
*Project Status: Phase 0 Complete ✅*