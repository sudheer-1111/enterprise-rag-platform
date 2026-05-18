from app.services.rag_service import retrieve_relevant_chunks, ask_rag_question


test_cases = [
    {
        "question": "How many days can employees work remotely?",
        "expected_source": "01_hr_remote_work_policy.txt",
    },
    {
        "question": "What expenses are not reimbursable?",
        "expected_source": "03_finance_expense_reimbursement.txt",
    },
    {
        "question": "What is required for password authentication?",
        "expected_source": "05_it_security_password_policy.txt",
    },
    {
        "question": "What must be included in a security incident report?",
        "expected_source": "07_it_security_incident_response.txt",
    },
    {
        "question": "What is the refund approval limit?",
        "expected_source": "09_customer_support_refund_policy.txt",
    },
    {
        "question": "What discounts require executive approval?",
        "expected_source": "11_sales_discount_approval_policy.txt",
    },
    {
        "question": "When is legal review required for contracts?",
        "expected_source": "13_legal_contract_review_process.txt",
    },
    {
        "question": "What are Bronze Silver and Gold layers?",
        "expected_source": "17_data_engineering_bronze_silver_gold.txt",
    },
    {
        "question": "What are approved AI tool use cases?",
        "expected_source": "19_ai_governance_approved_ai_tools.txt",
    },
    {
        "question": "What must be logged for audit compliance?",
        "expected_source": "27_compliance_audit_logging.txt",
    },
]


def run_retrieval_evaluation(top_k: int = 3):
    total = len(test_cases)
    passed = 0
    failed_cases = []

    print("\nStarting RAG retrieval evaluation...\n")

    for index, test in enumerate(test_cases, start=1):
        question = test["question"]
        expected_source = test["expected_source"]

        result = retrieve_relevant_chunks(
            question=question,
            top_k=top_k,
        )

        retrieved_sources = [
            item["source_file"] for item in result.get("results", [])
        ]

        is_pass = expected_source in retrieved_sources

        if is_pass:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"
            failed_cases.append(
                {
                    "question": question,
                    "expected_source": expected_source,
                    "retrieved_sources": retrieved_sources,
                }
            )

        print(f"{index}. {status}")
        print(f"Question: {question}")
        print(f"Expected: {expected_source}")
        print(f"Retrieved: {retrieved_sources}")
        print("-" * 80)

    accuracy = passed / total

    print("\nEvaluation Summary")
    print("=" * 80)
    print(f"Total test cases: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Retrieval accuracy: {accuracy:.2%}")

    if failed_cases:
        print("\nFailed Cases")
        print("=" * 80)

        for case in failed_cases:
            print(f"Question: {case['question']}")
            print(f"Expected: {case['expected_source']}")
            print(f"Retrieved: {case['retrieved_sources']}")
            print("-" * 80)


if __name__ == "__main__":
    run_retrieval_evaluation(top_k=3)