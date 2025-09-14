# 🚀 ETL Project - Sales Data Pipeline

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