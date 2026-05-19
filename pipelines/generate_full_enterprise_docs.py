from pathlib import Path
import time
import ollama

OUTPUT_DIR = Path("data/raw/enterprise_docs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "qwen2.5:3b"

DOCUMENT_TOPICS = {
    "hr": [
        "Remote Work Policy",
        "Employee Onboarding Procedure",
        "Employee Offboarding Checklist",
        "Performance Improvement Plan Procedure",
        "Annual Performance Review Policy",
        "Leave of Absence Procedure",
        "Workplace Conduct Policy",
        "Contractor Engagement Policy",
        "Training Completion Policy",
        "Employee Data Change Request Procedure",
    ],
    "finance": [
        "Expense Reimbursement Policy",
        "Purchase Order Approval Policy",
        "Vendor Payment Procedure",
        "Invoice Dispute Handling Procedure",
        "Month-End Close Procedure",
        "Revenue Recognition Review Policy",
        "Budget Forecasting Guideline",
        "Corporate Card Usage Policy",
        "Payroll Reconciliation Procedure",
        "Capital Expenditure Approval Policy",
    ],
    "it_security": [
        "Password and MFA Policy",
        "Privileged Access Management Procedure",
        "Security Incident Response Runbook",
        "VPN Access Policy",
        "Endpoint Security Standard",
        "Data Classification Standard",
        "Cloud Security Baseline",
        "Phishing Investigation Procedure",
        "Secrets Management Policy",
        "Security Exception Request Process",
    ],
    "data_engineering": [
        "Bronze Silver Gold Data Lake Standard",
        "Databricks Job Failure Runbook",
        "Schema Drift Handling Procedure",
        "Large File Ingestion Standard",
        "Data Quality Validation Standard",
        "ETL Job Scheduling Procedure",
        "Data Lineage Documentation Standard",
        "PII Masking Procedure",
        "Delta Table Optimization Guideline",
        "Backfill and Replay Procedure",
    ],
    "ai_governance": [
        "Approved AI Tools Policy",
        "RAG Quality Standard",
        "Prompt Review Guideline",
        "Model Selection Standard",
        "AI Output Human Review Policy",
        "Sensitive Data AI Restriction",
        "Hallucination Monitoring Procedure",
        "AI Usage Audit Logging Standard",
        "Embedding Data Retention Policy",
        "AI Risk Assessment Procedure",
    ],
    "customer_support": [
        "Refund Policy",
        "Support Escalation Matrix",
        "High Priority Case Handling Procedure",
        "Customer Complaint Handling Procedure",
        "SLA Response Guideline",
        "Support Ticket Classification Standard",
        "Customer Communication Standard",
        "Knowledge Base Update Process",
        "Account Access Support Procedure",
        "Production Outage Customer Response Plan",
    ],
    "legal": [
        "Contract Review Process",
        "Data Privacy Policy",
        "NDA Handling Procedure",
        "Vendor Agreement Review Procedure",
        "Customer Terms Exception Process",
        "Legal Hold Policy",
        "Regulatory Request Handling Procedure",
        "Data Processing Agreement Review",
        "Intellectual Property Review Policy",
        "Contract Renewal Risk Review",
    ],
    "devops": [
        "CI CD Pipeline Policy",
        "Production Deployment Approval Procedure",
        "Rollback Runbook",
        "Environment Management Standard",
        "Secrets Rotation Procedure",
        "Infrastructure Change Management Process",
        "Release Branching Standard",
        "Production Monitoring Guideline",
        "Incident Commander Runbook",
        "Service Health Check Standard",
    ],
    "compliance": [
        "Audit Logging Standard",
        "Quarterly Access Review Procedure",
        "Evidence Collection Process",
        "Control Testing Guideline",
        "Policy Exception Handling Procedure",
        "Regulatory Reporting Procedure",
        "Data Retention Policy",
        "Vendor Compliance Review",
        "Internal Audit Response Procedure",
        "Compliance Review Calendar",
    ],
    "analytics": [
        "Forecasting Model Guideline",
        "Dashboard Design Standard",
        "KPI Definition Process",
        "Executive Reporting Standard",
        "Metric Certification Process",
        "Analytics Request Intake Procedure",
        "Report Refresh Procedure",
        "Data Visualization Guideline",
        "Self Service Analytics Policy",
        "Forecast Accuracy Review Procedure",
    ],
}


DEPARTMENT_CONTEXT = {
    "hr": "employee lifecycle, manager approvals, HRIS records, policy acknowledgements, employee relations, contractors, onboarding and offboarding controls",
    "finance": "purchase controls, invoice processing, accounting close, approvals, reconciliation, payment timing, audit evidence, revenue and budget controls",
    "it_security": "access control, MFA, privileged access, security incidents, data protection, encryption, cloud security, audit trails, phishing and risk exceptions",
    "data_engineering": "Databricks, PySpark, data pipelines, bronze silver gold layers, schema drift, data quality checks, Delta tables, job orchestration and backfills",
    "ai_governance": "RAG systems, model selection, prompt review, AI risk, sensitive data, human review, hallucination monitoring, embedding storage and audit logs",
    "customer_support": "support tickets, SLA, refund review, customer impact, priority levels, escalation, communication templates, outage handling and knowledge base updates",
    "legal": "contract review, privacy, NDAs, legal holds, regulatory requests, customer terms, vendor terms, risk review and approval evidence",
    "devops": "CI/CD, production deployment, rollback, release branches, monitoring, secrets rotation, infrastructure changes and incident management",
    "compliance": "audit logging, access review, evidence collection, control testing, exceptions, regulatory reporting and retention requirements",
    "analytics": "dashboards, KPIs, forecasting, metric definitions, executive reporting, certified datasets, refresh schedules and analytics governance",
}


def slugify(text: str) -> str:
    return (
        text.lower()
        .replace("&", "and")
        .replace("/", " ")
        .replace("-", " ")
        .replace("  ", " ")
        .replace(" ", "_")
    )


def build_prompt(doc_id: int, department: str, title: str) -> str:
    department_name = department.replace("_", " ").title()
    context = DEPARTMENT_CONTEXT[department]

    return f"""
Write a complete enterprise internal policy/procedure document.

Document ID: DOC-{doc_id:03d}
Department: {department_name}
Title: {title}
Business Context: {context}

Important instructions:
- Write realistic company content, not generic filler.
- Make the document specific to the title.
- Include concrete rules, timelines, thresholds, examples, required fields, approvals, exception handling, and audit evidence.
- Use plain text only.
- Do not mention that this is AI-generated.
- Do not use markdown tables.
- Length should be around 900 to 1300 words.
- Use clear section headers.

Required sections:
1. Document Header
2. Purpose
3. Scope
4. Definitions
5. Policy or Procedure Details
6. Roles and Responsibilities
7. Step-by-Step Workflow
8. Required Documentation
9. Approval Rules
10. Exception Handling
11. Audit Evidence
12. Common Failure Scenarios
13. Example Scenario
14. Frequently Asked Questions
15. Summary

Make the document detailed enough for a RAG system to answer specific questions from it.
"""


def generate_document(doc_id: int, department: str, title: str) -> str:
    prompt = build_prompt(doc_id, department, title)

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior enterprise documentation specialist. "
                    "You write detailed internal company policies, SOPs, runbooks, and standards."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        options={
            "temperature": 0.4,
        },
    )

    return response["message"]["content"].strip()


def main():
    doc_id = 1
    total_created = 0

    for department, titles in DOCUMENT_TOPICS.items():
        for title in titles:
            filename = f"{doc_id:03d}_{department}_{slugify(title)}.txt"
            file_path = OUTPUT_DIR / filename

            print(f"Generating {filename} ...")

            content = generate_document(
                doc_id=doc_id,
                department=department,
                title=title,
            )

            file_path.write_text(content, encoding="utf-8")

            total_created += 1
            doc_id += 1

            # Small pause so Ollama does not get overloaded
            time.sleep(1)

    print(f"\nCreated {total_created} full-content enterprise documents.")
    print(f"Output folder: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()