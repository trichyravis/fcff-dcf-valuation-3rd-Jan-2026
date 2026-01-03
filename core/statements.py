
def build_income_statement(xbrl, extract):
    return {
        "Revenue": extract(xbrl, ["Revenues"], "Revenue"),
        "EBIT": extract(xbrl, ["OperatingIncomeLoss"], "EBIT"),
        "Net Income": extract(xbrl, ["NetIncomeLoss"], "NetIncome")
    }

def build_cashflow_statement(xbrl, extract):
    return {
        "Depreciation": extract(
            xbrl, ["DepreciationAndAmortization"], "Dep"
        ),
        "CapEx": extract(
            xbrl, ["PaymentsToAcquirePropertyPlantAndEquipment"], "CapEx"
        )
    }

def build_balance_sheet(xbrl, extract):
    return {
        "Current Assets": extract(
            xbrl, ["AssetsCurrent"], "CA"
        ),
        "Current Liabilities": extract(
            xbrl, ["LiabilitiesCurrent"], "CL"
        ),
        "Cash": extract(
            xbrl,
            ["CashAndCashEquivalentsAtCarryingValue"],
            "Cash"
        )
    }
