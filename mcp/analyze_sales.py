from fetch_sales import fetch_sales


def analyze_sales():
    """
    Analyzes the sales data returned by fetch_sales().
    """

    data = fetch_sales()

    sales = data["sales"]

    total = sum(item["revenue"] for item in sales)

    average = total / len(sales)

    best = max(sales, key=lambda x: x["revenue"])

    worst = min(sales, key=lambda x: x["revenue"])

    return {
        "success": True,
        "analysis": {
            "total_revenue": total,
            "average_revenue": average,
            "best_month": best["month"],
            "best_revenue": best["revenue"],
            "lowest_month": worst["month"],
            "lowest_revenue": worst["revenue"],
            "months_analyzed": len(sales)
        }
    }
