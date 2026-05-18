from pathlib import Path

OUTPUT_DIR = Path("data/raw/enterprise_docs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

documents = {
    "01_hr_remote_work_policy.txt": """
Enterprise HR Policy: Remote Work Policy

Department: Human Resources
Document Owner: HR Operations
Effective Date: 2026-01-01
Confidentiality Level: Internal

Purpose:
This policy defines how employees may work remotely while maintaining productivity, security, and compliance.

Policy Details:
Employees are allowed to work from home up to two days per week with direct manager approval. Remote work must be documented in the HR management system before the start of the work week.

Eligibility:
Full-time employees who have completed at least 90 days of employment are eligible for recurring remote work arrangements. Contractors may work remotely only if approved by their vendor manager and internal business owner.

Security Requirements:
Employees must use company-approved devices, VPN access, multi-factor authentication, and encrypted storage. Customer information must not be downloaded to personal devices.

Manager Responsibilities:
Managers must verify that remote employees remain available during business hours, attend required meetings, and complete assigned deliverables.

Exception Process:
Requests for more than two remote days per week require written approval from HR and the department director.
""",

    "02_hr_employee_onboarding.txt": """
Enterprise HR Procedure: Employee Onboarding

Department: Human Resources
Document Owner: Talent Operations
Confidentiality Level: Internal

Purpose:
This document describes the standard onboarding process for new employees.

Process:
Before the start date, HR must create the employee profile, complete background verification, collect tax forms, and issue the offer confirmation. IT must provision a laptop, email account, identity access, VPN profile, and required software.

First Day Requirements:
The employee must complete orientation, security awareness training, benefits enrollment, and company policy acknowledgement.

First Week Requirements:
The manager must provide role expectations, team introductions, project overview, communication channels, and initial assignments.

System Access:
Access to production systems is not granted on day one. Production access requires manager approval, completion of security training, and approval from the system owner.

Audit Notes:
All onboarding tasks must be logged in the HR system for compliance review.
""",

    "03_finance_expense_reimbursement.txt": """
Enterprise Finance Policy: Expense Reimbursement

Department: Finance
Document Owner: Accounts Payable
Confidentiality Level: Internal

Purpose:
This policy defines how employees submit expenses for reimbursement.

Policy Details:
Employees must submit expense reports within 30 days of the purchase date. Receipts are required for all expenses above 25 dollars.

Approved Expenses:
Approved expenses include business travel, lodging, client meals, approved software tools, training fees, and business-related supplies.

Non-Reimbursable Expenses:
Personal meals, entertainment without client purpose, luxury upgrades, fines, penalties, and unapproved subscriptions are not reimbursable.

Approval Workflow:
Expense reports must be approved by the direct manager and reviewed by Finance before payment.

Payment Timeline:
Approved reimbursements are processed within two payroll cycles.

Audit Requirement:
Finance may request additional documentation if an expense appears unusual or incomplete.
""",

    "04_finance_month_end_close.txt": """
Enterprise Finance Procedure: Month-End Close

Department: Finance
Document Owner: Accounting Operations
Confidentiality Level: Internal

Purpose:
This procedure defines the monthly accounting close process.

Close Timeline:
The close process begins on the first business day after month end and must be completed within five business days.

Key Activities:
Finance must reconcile bank accounts, validate revenue postings, review accounts payable accruals, confirm payroll entries, and review deferred revenue schedules.

Data Sources:
Finance uses ERP reports, bank statements, payment processor exports, billing system reports, and data warehouse revenue tables.

Controls:
All manual journal entries require preparer and reviewer approval. Any adjustment above 10,000 dollars requires controller review.

Reporting:
Final financial reports are distributed to leadership after controller approval.
""",

    "05_it_security_password_policy.txt": """
Enterprise IT Security Policy: Password and Authentication Policy

Department: Information Security
Document Owner: Security Engineering
Confidentiality Level: Internal

Purpose:
This policy defines password and authentication requirements.

Password Requirements:
Passwords must be at least 14 characters and must not reuse passwords from previous company accounts. Passwords must not include employee names, company names, or common phrases.

Multi-Factor Authentication:
MFA is required for email, VPN, cloud systems, code repositories, financial systems, and production systems.

Password Rotation:
Password rotation is required immediately after suspected compromise. Routine rotation is only required for privileged accounts.

Privileged Accounts:
Administrator accounts must use stronger controls, including hardware security keys where available.

Violation:
Sharing passwords or storing passwords in plain text is a security violation.
""",

    "06_it_security_data_classification.txt": """
Enterprise IT Security Standard: Data Classification

Department: Information Security
Document Owner: Governance Risk and Compliance
Confidentiality Level: Internal

Purpose:
This standard defines company data classification levels.

Classification Levels:
Public data may be shared externally without restriction. Internal data is limited to employees and approved contractors. Confidential data includes customer records, financial data, contracts, security documents, and employee records. Restricted data includes regulated data, authentication secrets, encryption keys, and sensitive personal information.

Handling Requirements:
Confidential and restricted data must be encrypted during storage and transmission.

Access Control:
Access must be based on business need and approved by the data owner.

Retention:
Data must be retained according to legal, regulatory, and business requirements.

AI Usage:
Restricted data must not be entered into unapproved AI systems.
""",

    "07_it_security_incident_response.txt": """
Enterprise Security Procedure: Incident Response

Department: Information Security
Document Owner: Security Operations Center
Confidentiality Level: Confidential

Purpose:
This document defines the incident response process for cybersecurity events.

Incident Reporting:
Security incidents must be reported to the IT security team within 24 hours. Critical incidents must be reported immediately.

Required Information:
The report must include incident date, system affected, business impact, data involved, suspected root cause, and immediate actions taken.

Severity Levels:
Severity 1 incidents involve active data exfiltration, ransomware, production outage, or confirmed compromise of privileged credentials. Severity 2 incidents involve suspicious access or limited service impact. Severity 3 incidents involve low-risk policy violations.

Response Workflow:
The security team triages the incident, contains the threat, preserves evidence, notifies stakeholders, remediates the issue, and completes a post-incident review.

Post-Incident Review:
All Severity 1 and Severity 2 incidents require a written root cause analysis within five business days.
""",

    "08_it_vpn_access_policy.txt": """
Enterprise IT Policy: VPN Access

Department: IT Infrastructure
Document Owner: Network Operations
Confidentiality Level: Internal

Purpose:
This policy defines requirements for remote access through VPN.

VPN Requirement:
Employees and contractors must use VPN when accessing internal systems from outside the corporate network.

Authentication:
VPN access requires company credentials and multi-factor authentication.

Contractor Access:
Contractor VPN access must have an expiration date and must be reviewed every 90 days.

Prohibited Activity:
Users must not share VPN credentials or connect from unmanaged public devices.

Logging:
VPN activity is logged and reviewed for suspicious access patterns.

Access Removal:
VPN access must be removed when an employee leaves the company or when contractor engagement ends.
""",

    "09_customer_support_refund_policy.txt": """
Enterprise Customer Support Policy: Refund Policy

Department: Customer Support
Document Owner: Support Operations
Confidentiality Level: Internal

Purpose:
This policy defines how customer refund requests are reviewed and processed.

Refund Eligibility:
Customers may request a refund within 30 days of purchase if the product was not used beyond the trial limit or if there was a documented service issue.

Non-Eligible Refunds:
Refunds are not available for policy violations, expired subscription periods, completed professional services, or usage beyond the approved limit.

Approval:
Refunds below 500 dollars may be approved by a support manager. Refunds above 500 dollars require Finance approval.

Documentation:
Support agents must document customer name, account ID, purchase date, refund reason, and approval status.

Processing Time:
Approved refunds are processed within 7 to 10 business days.
""",

    "10_customer_support_escalation_matrix.txt": """
Enterprise Customer Support Procedure: Escalation Matrix

Department: Customer Support
Document Owner: Support Operations
Confidentiality Level: Internal

Purpose:
This document explains how support cases are escalated.

Tier 1:
Tier 1 handles account questions, password reset guidance, basic billing questions, and general product navigation.

Tier 2:
Tier 2 handles technical troubleshooting, integration issues, failed workflows, and repeat customer problems.

Tier 3:
Tier 3 handles engineering defects, production bugs, API failures, data mismatch issues, and platform outages.

Escalation Timing:
A case must be escalated if there is no progress within 24 hours for high priority issues or 72 hours for normal issues.

Required Escalation Notes:
Agents must include customer impact, steps already taken, screenshots if available, logs, error messages, and business urgency.

Executive Escalation:
Cases involving strategic customers or legal risk must be flagged to support leadership.
""",

    "11_sales_discount_approval_policy.txt": """
Enterprise Sales Policy: Discount Approval

Department: Sales
Document Owner: Revenue Operations
Confidentiality Level: Internal

Purpose:
This policy defines discount approval rules for customer contracts.

Standard Discount:
Sales representatives may offer discounts up to 10 percent without additional approval.

Manager Approval:
Discounts between 10 and 20 percent require sales manager approval.

Director Approval:
Discounts between 20 and 30 percent require regional sales director approval.

Executive Approval:
Discounts above 30 percent require executive approval and Finance review.

Documentation:
All discounts must be documented in the CRM opportunity record with business justification.

Compliance:
Discounts must not be offered in exchange for personal benefit, gifts, or improper incentives.
""",

    "12_sales_crm_data_quality.txt": """
Enterprise Sales Procedure: CRM Data Quality

Department: Sales Operations
Document Owner: Revenue Operations
Confidentiality Level: Internal

Purpose:
This procedure defines CRM data quality expectations.

Required Fields:
Every opportunity must include account name, opportunity owner, expected close date, stage, forecast category, estimated contract value, and next step.

Data Hygiene:
Sales representatives must update active opportunities at least once per week.

Close Date Accuracy:
Close dates must reflect realistic customer buying timelines and must not be moved repeatedly without explanation.

Forecasting:
Forecast calls rely on accurate CRM data. Incomplete opportunities may be excluded from forecast review.

Audit:
Revenue Operations reviews CRM data quality weekly and reports missing fields to sales leadership.
""",

    "13_legal_contract_review_process.txt": """
Enterprise Legal Procedure: Contract Review Process

Department: Legal
Document Owner: Commercial Legal
Confidentiality Level: Confidential

Purpose:
This document defines when contracts require legal review.

Review Required:
Legal review is required for customer contracts, vendor agreements, data processing agreements, non-standard liability terms, security addendums, and contracts above 50,000 dollars.

Standard Templates:
Approved company templates may be used without legal review if no changes are made to legal terms.

Turnaround Time:
Standard contract review takes three to five business days. Urgent reviews require business justification.

Redlines:
All redlines must be tracked in the contract management system.

Approval:
Legal approval does not replace Finance, Security, or executive approval when those reviews are required.
""",

    "14_legal_data_privacy_policy.txt": """
Enterprise Legal Policy: Data Privacy

Department: Legal
Document Owner: Privacy Office
Confidentiality Level: Confidential

Purpose:
This policy defines privacy requirements for personal data.

Personal Data:
Personal data includes names, addresses, phone numbers, emails, account IDs, payment information, device IDs, and employment records.

Processing Requirement:
Personal data may only be collected and processed for approved business purposes.

Access:
Access to personal data must follow least privilege principles.

Retention:
Personal data must not be retained longer than required by business, legal, or regulatory needs.

Incident Notification:
Suspected privacy incidents must be reported to Legal and Information Security immediately.

AI Restriction:
Personal data must not be uploaded into unapproved AI tools.
""",

    "15_operations_vendor_management.txt": """
Enterprise Operations Policy: Vendor Management

Department: Operations
Document Owner: Vendor Management Office
Confidentiality Level: Internal

Purpose:
This policy defines vendor onboarding and monitoring requirements.

Vendor Onboarding:
All new vendors must complete business justification, security review, legal review, and Finance approval before services begin.

Risk Tiering:
Vendors are classified as low, medium, or high risk based on data access, system access, business criticality, and regulatory impact.

High-Risk Vendors:
High-risk vendors require annual security review, updated insurance documentation, and executive sponsor approval.

Contractor Requirements:
Contractors must complete security awareness training and must use company-approved accounts.

Offboarding:
Vendor access must be removed within 24 hours after contract termination.
""",

    "16_operations_business_continuity.txt": """
Enterprise Operations Plan: Business Continuity

Department: Operations
Document Owner: Business Continuity Office
Confidentiality Level: Internal

Purpose:
This plan defines how critical business operations continue during disruptions.

Critical Functions:
Critical functions include customer support, production operations, security monitoring, payroll, billing, and executive communications.

Recovery Time Objectives:
Production operations must be restored within four hours. Customer support must resume within eight hours. Finance payment operations must resume within two business days.

Communication:
During a disruption, the incident commander sends updates every two hours to leadership.

Backup Process:
Critical documents and operational runbooks must be stored in approved shared repositories.

Testing:
Business continuity plans must be tested at least once per year.
""",

    "17_data_engineering_bronze_silver_gold.txt": """
Enterprise Data Engineering Standard: Bronze, Silver, and Gold Layers

Department: Data Engineering
Document Owner: Data Platform Team
Confidentiality Level: Internal

Purpose:
This standard defines the data lake architecture used for analytics and AI pipelines.

Bronze Layer:
The Bronze layer stores raw ingested data from source systems. Data is stored with minimal transformation and includes ingestion timestamps, source identifiers, and raw schema.

Silver Layer:
The Silver layer stores cleaned and standardized data. Duplicate records are removed, data types are corrected, and invalid records are quarantined.

Gold Layer:
The Gold layer stores business-ready data for reporting, analytics, machine learning, and RAG enrichment.

Quality Checks:
Data pipelines must check for missing values, duplicate records, schema drift, invalid dates, and unexpected null rates.

Lineage:
Every pipeline must track input source, transformation logic, output table, and execution timestamp.
""",

    "18_data_engineering_pipeline_failure_runbook.txt": """
Enterprise Data Engineering Runbook: Pipeline Failure Handling

Department: Data Engineering
Document Owner: Data Platform Operations
Confidentiality Level: Internal

Purpose:
This runbook explains how to handle failed data pipelines.

Failure Detection:
Pipeline failures are detected through workflow alerts, Databricks job status, orchestration logs, and data quality checks.

Initial Triage:
The engineer must identify failed task, input dataset, error message, execution time, and recent code or schema changes.

Common Causes:
Common failure causes include missing input files, schema changes, permission errors, cluster timeout, memory pressure, and downstream table locks.

Recovery:
If the issue is transient, the job may be retried once. If the issue is data-related, the bad input must be quarantined and the business owner notified.

Documentation:
Every production pipeline failure must be documented with root cause, fix, owner, and prevention step.
""",

    "19_ai_governance_approved_ai_tools.txt": """
Enterprise AI Governance Policy: Approved AI Tools

Department: AI Governance
Document Owner: Responsible AI Committee
Confidentiality Level: Internal

Purpose:
This policy defines approved AI tool usage.

Approved Use:
Employees may use approved AI tools for documentation, summarization, coding assistance, analytics support, and internal knowledge search.

Restricted Use:
Employees must not enter confidential customer data, regulated personal data, passwords, API keys, financial records, or legal documents into unapproved AI tools.

Human Review:
AI-generated outputs must be reviewed by a human before use in customer communication, financial reporting, legal documents, or production deployment.

Model Selection:
Teams must consider cost, latency, accuracy, data sensitivity, and compliance before selecting a model provider.

Audit:
AI usage may be reviewed for compliance with security and privacy requirements.
""",

    "20_ai_governance_rag_quality_standards.txt": """
Enterprise AI Governance Standard: RAG Quality Standards

Department: AI Governance
Document Owner: AI Platform Team
Confidentiality Level: Internal

Purpose:
This standard defines quality expectations for retrieval-augmented generation systems.

Retrieval Quality:
RAG systems must retrieve relevant, current, and authorized documents before generating answers.

Grounding:
Generated answers must be grounded in retrieved context. The model should not invent unsupported facts.

Citations:
When possible, answers should include document source, title, section, or chunk reference.

Evaluation:
RAG pipelines must be evaluated using test questions, expected answers, retrieval precision, answer accuracy, and hallucination checks.

Access Control:
Users must only retrieve documents they are authorized to access.

Monitoring:
Production RAG systems must log query, retrieved document IDs, latency, model used, and user feedback.
""",

    "21_platform_api_design_guidelines.txt": """
Enterprise Platform Guideline: API Design

Department: Platform Engineering
Document Owner: API Standards Team
Confidentiality Level: Internal

Purpose:
This guideline defines API design standards.

Endpoint Naming:
APIs should use clear resource-based paths such as /documents, /users, /search, and /rag/ask.

HTTP Methods:
GET is used for reading data. POST is used for creating or executing operations. PUT or PATCH is used for updates. DELETE is used for removals.

Error Handling:
APIs must return clear error messages with appropriate HTTP status codes.

Documentation:
All APIs must be documented using OpenAPI or Swagger.

Authentication:
Production APIs must require authentication and authorization.

Logging:
APIs must log request ID, timestamp, endpoint, response status, latency, and error details when applicable.
""",

    "22_platform_fastapi_service_standards.txt": """
Enterprise Platform Standard: FastAPI Service Standards

Department: Platform Engineering
Document Owner: Backend Architecture Team
Confidentiality Level: Internal

Purpose:
This standard defines how FastAPI services should be structured.

Project Structure:
FastAPI applications should separate routes, services, configuration, storage, and models.

Configuration:
Environment-specific settings should be loaded from environment variables or secure secret stores.

Health Endpoint:
Every service must expose a /health endpoint for monitoring.

Error Handling:
Service code should catch expected errors and return meaningful HTTP responses.

Swagger:
Swagger documentation should be enabled in development and controlled in production.

Testing:
Endpoints should include unit tests and integration tests before production release.
""",

    "23_product_release_management.txt": """
Enterprise Product Procedure: Release Management

Department: Product Operations
Document Owner: Release Management
Confidentiality Level: Internal

Purpose:
This procedure defines how product releases are planned and executed.

Release Planning:
Every release must include scope, owner, target date, impacted systems, customer impact, rollback plan, and communication plan.

Pre-Release Checklist:
Engineering must complete code review, testing, security review if needed, documentation updates, and deployment approval.

Release Communication:
Customer-facing changes require release notes. Internal teams must be notified before major launches.

Rollback:
Every release must have a rollback plan. Rollback decisions are made by the incident commander or release owner.

Post-Release Review:
Major releases require review of defects, customer impact, support tickets, and success metrics.
""",

    "24_product_customer_feedback_process.txt": """
Enterprise Product Procedure: Customer Feedback Process

Department: Product Management
Document Owner: Product Operations
Confidentiality Level: Internal

Purpose:
This procedure defines how customer feedback is collected and prioritized.

Feedback Sources:
Feedback may come from support tickets, sales calls, customer interviews, surveys, usage analytics, and executive escalations.

Classification:
Feedback is classified as bug, feature request, usability issue, performance issue, integration request, or documentation gap.

Prioritization:
Product managers prioritize feedback based on customer impact, revenue impact, strategic alignment, frequency, and implementation effort.

Tracking:
All accepted feedback items must be tracked in the product backlog.

Communication:
Customer-facing teams must be informed when high-priority feedback is planned, rejected, or released.
""",

    "25_devops_ci_cd_policy.txt": """
Enterprise DevOps Policy: CI/CD Pipeline

Department: DevOps
Document Owner: Engineering Productivity
Confidentiality Level: Internal

Purpose:
This policy defines continuous integration and deployment expectations.

Source Control:
All production code must be stored in an approved Git repository.

Branching:
Feature branches are used for development. Pull requests are required before merging to main.

Build:
The CI pipeline must install dependencies, run tests, check formatting, and scan for known vulnerabilities.

Deployment:
Production deployments require approval and must use automated deployment workflows.

Rollback:
Deployment pipelines must support rollback to the last known stable version.

Audit:
Build logs, deployment logs, approvers, and release versions must be retained.
""",

    "26_devops_environment_management.txt": """
Enterprise DevOps Standard: Environment Management

Department: DevOps
Document Owner: Cloud Platform Team
Confidentiality Level: Internal

Purpose:
This standard defines development, staging, and production environments.

Development:
The development environment is used for local testing and active engineering work.

Staging:
The staging environment mirrors production configuration where possible and is used for final validation.

Production:
Production serves real users and requires strict access control, monitoring, and change management.

Configuration:
Environment variables must be used for environment-specific settings. Secrets must not be committed to Git.

Access:
Production access is limited to approved engineers and must be reviewed quarterly.

Monitoring:
Each environment must have logs, health checks, and error tracking.
""",

    "27_compliance_audit_logging.txt": """
Enterprise Compliance Standard: Audit Logging

Department: Compliance
Document Owner: Internal Audit
Confidentiality Level: Confidential

Purpose:
This standard defines audit logging requirements.

Required Logs:
Systems must log user login events, permission changes, data exports, failed access attempts, administrative actions, and production configuration changes.

Log Contents:
Audit logs must include timestamp, user ID, action, system affected, source IP when available, and result status.

Retention:
Audit logs must be retained for at least one year unless a longer retention period is required.

Protection:
Audit logs must be protected from unauthorized modification or deletion.

Review:
High-risk system logs must be reviewed periodically by system owners or compliance teams.
""",

    "28_compliance_access_review.txt": """
Enterprise Compliance Procedure: Access Review

Department: Compliance
Document Owner: Governance Risk and Compliance
Confidentiality Level: Confidential

Purpose:
This procedure defines periodic user access reviews.

Review Frequency:
Production system access must be reviewed quarterly. Financial system access must be reviewed quarterly. General internal tools may be reviewed semi-annually.

Review Owners:
System owners are responsible for confirming whether each user still requires access.

Removal:
Access that is no longer required must be removed within five business days.

Evidence:
Completed access reviews must include reviewer name, review date, system name, user list, exceptions, and remediation status.

Privileged Access:
Administrator access requires additional justification and stronger review.
""",

    "29_analytics_forecasting_guidelines.txt": """
Enterprise Analytics Guideline: Forecasting Models

Department: Analytics
Document Owner: Business Science Team
Confidentiality Level: Internal

Purpose:
This guideline defines expectations for forecasting analysis.

Use Cases:
Forecasting may be used for revenue planning, support volume prediction, inventory planning, staffing, and customer demand analysis.

Methods:
Approved forecasting methods include moving averages, exponential smoothing, ARIMA, Prophet, regression models, and machine learning models when justified.

Validation:
Forecasts must be validated using historical holdout periods and error metrics such as MAPE, RMSE, or MAE.

Documentation:
Analysts must document input data, assumptions, model method, validation results, and limitations.

Business Review:
Forecasts used for executive planning must be reviewed with business stakeholders.
""",

    "30_analytics_dashboard_standards.txt": """
Enterprise Analytics Standard: Dashboard Design

Department: Analytics
Document Owner: Data Visualization Team
Confidentiality Level: Internal

Purpose:
This standard defines dashboard design expectations.

Dashboard Requirements:
Dashboards must have a clear business owner, defined audience, refresh frequency, data source, and metric definitions.

Metric Definitions:
Every KPI must include calculation logic, filter rules, grain, and data owner.

Design:
Dashboards should prioritize clarity, consistent formatting, readable labels, and actionable insights.

Performance:
Dashboards should avoid unnecessary high-cardinality visuals and should use optimized tables when possible.

Governance:
Executive dashboards must use certified datasets and must be reviewed before publication.
"""
}

for filename, content in documents.items():
    file_path = OUTPUT_DIR / filename
    file_path.write_text(content.strip(), encoding="utf-8")

print(f"Created {len(documents)} enterprise text documents in {OUTPUT_DIR}")