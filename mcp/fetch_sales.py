def fetch_sales():
    """
    Returns sample monthly sales data.
    """

    return {
        "success": True,
        "sales": [
            {
                "month": "January",
                "revenue": 12000
            },
            {
                "month": "February",
                "revenue": 18500
            },
            {
                "month": "March",
                "revenue": 16300
            }
        ]
    }
