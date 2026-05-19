from app.services.rag_service import retrieve_relevant_chunks, retrieve_with_reranking


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


def get_rank(source_list, expected_source):
    """
    Return the rank position of expected_source.
    If not found, return None.
    """

    for index, source in enumerate(source_list, start=1):
        if source == expected_source:
            return index

    return None


def run_rerank_evaluation(initial_k: int = 10, top_n: int = 3):
    total = len(test_cases)

    normal_top_n_pass = 0
    rerank_top_n_pass = 0

    normal_top_1_pass = 0
    rerank_top_1_pass = 0

    improved_cases = []
    worsened_cases = []
    unchanged_cases = []

    print("\nStarting reranking evaluation...\n")

    for index, test in enumerate(test_cases, start=1):
        question = test["question"]
        expected_source = test["expected_source"]

        normal_result = retrieve_relevant_chunks(
            question=question,
            top_k=initial_k,
        )

        normal_sources = [
            item["source_file"]
            for item in normal_result.get("results", [])
        ]

        rerank_result = retrieve_with_reranking(
            question=question,
            initial_k=initial_k,
            top_n=top_n,
        )

        reranked_sources = [
            item["source_file"]
            for item in rerank_result.get("reranked_results", [])
        ]

        normal_rank = get_rank(normal_sources, expected_source)
        rerank_rank = get_rank(reranked_sources, expected_source)

        normal_in_top_n = normal_rank is not None and normal_rank <= top_n
        rerank_in_top_n = rerank_rank is not None and rerank_rank <= top_n

        normal_top_1 = normal_rank == 1
        rerank_top_1 = rerank_rank == 1

        if normal_in_top_n:
            normal_top_n_pass += 1

        if rerank_in_top_n:
            rerank_top_n_pass += 1

        if normal_top_1:
            normal_top_1_pass += 1

        if rerank_top_1:
            rerank_top_1_pass += 1

        if normal_rank is None and rerank_rank is not None:
            improved_cases.append(test)
            change_status = "IMPROVED"
        elif normal_rank is not None and rerank_rank is None:
            worsened_cases.append(test)
            change_status = "WORSENED"
        elif normal_rank is not None and rerank_rank is not None:
            if rerank_rank < normal_rank:
                improved_cases.append(test)
                change_status = "IMPROVED"
            elif rerank_rank > normal_rank:
                worsened_cases.append(test)
                change_status = "WORSENED"
            else:
                unchanged_cases.append(test)
                change_status = "UNCHANGED"
        else:
            unchanged_cases.append(test)
            change_status = "UNCHANGED"

        print(f"{index}. {change_status}")
        print(f"Question: {question}")
        print(f"Expected source: {expected_source}")
        print(f"Normal sources:   {normal_sources[:top_n]}")
        print(f"Reranked sources: {reranked_sources}")
        print(f"Normal rank: {normal_rank}")
        print(f"Reranked rank: {rerank_rank}")
        print("-" * 90)

    normal_top_n_accuracy = normal_top_n_pass / total
    rerank_top_n_accuracy = rerank_top_n_pass / total

    normal_top_1_accuracy = normal_top_1_pass / total
    rerank_top_1_accuracy = rerank_top_1_pass / total

    print("\nReranking Evaluation Summary")
    print("=" * 90)
    print(f"Total test cases: {total}")
    print(f"Initial retrieval k: {initial_k}")
    print(f"Reranked top_n: {top_n}")
    print()
    print(f"Normal top-{top_n} accuracy:   {normal_top_n_accuracy:.2%}")
    print(f"Reranked top-{top_n} accuracy: {rerank_top_n_accuracy:.2%}")
    print()
    print(f"Normal top-1 accuracy:         {normal_top_1_accuracy:.2%}")
    print(f"Reranked top-1 accuracy:       {rerank_top_1_accuracy:.2%}")
    print()
    print(f"Improved cases: {len(improved_cases)}")
    print(f"Worsened cases: {len(worsened_cases)}")
    print(f"Unchanged cases: {len(unchanged_cases)}")


if __name__ == "__main__":
    run_rerank_evaluation(initial_k=10, top_n=3)