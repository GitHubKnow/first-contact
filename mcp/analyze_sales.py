from .fetch_sales import fetch_sales


def analyze_sales():

    data = fetch_sales()

    sales = data["sales"]

    revenues = [
        item["revenue"]
        for item in sales
    ]

    total = sum(revenues)

    average = total / len(revenues)


    best = max(
        sales,
        key=lambda x: x["revenue"]
    )

    lowest = min(
        sales,
        key=lambda x: x["revenue"]
    )


    return {
        "success": True,
        "analysis": {
            "total_revenue": total,
            "average_revenue": average,
            "best_month": best["month"],
            "best_revenue": best["revenue"],
            "lowest_month": lowest["month"],
            "lowest_revenue": lowest["revenue"],
            "months_analyzed": len(sales)
        }
    }
