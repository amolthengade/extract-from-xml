import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

def parse_tally_xml(xml_path):
    """Parses Tally XML and extracts 'Receipt' transactions."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    transactions = []

    for voucher in root.findall(".//TALLYMESSAGE/VOUCHER"):
        vch_type = voucher.find("VOUCHERTYPENAME").text if voucher.find("VOUCHERTYPENAME") is not None else ""

        if vch_type == "Receipt":  # Process only "Receipt" transactions
            date = voucher.find("DATE").text if voucher.find("DATE") is not None else ""
            formatted_date = datetime.strptime(date, "%Y%m%d").strftime("%d-%m-%Y") if date else "N/A"
            voucher_number = voucher.find("VOUCHERNUMBER").text if voucher.find("VOUCHERNUMBER") is not None else "N/A"

            for ledger_entry in voucher.findall(".//ALLLEDGERENTRIES.LIST") + voucher.findall(".//LEDGERENTRIES.LIST"):
                ledger_name = ledger_entry.find("LEDGERNAME").text if ledger_entry.find("LEDGERNAME") is not None else "Unknown Ledger"
                amount = ledger_entry.find("AMOUNT").text if ledger_entry.find("AMOUNT") is not None else "0.00"

                transaction = {
                    "Date": formatted_date,
                    "Voucher Number": voucher_number,
                    "Ledger Name": ledger_name,
                    "Amount": amount,
                }
                transactions.append(transaction)

    return transactions

def save_to_excel(transactions, output_file):
    """Saves extracted transactions to an Excel file."""
    df = pd.DataFrame(transactions)
    df.to_excel(output_file, index=False)
    print(f"Receipt transactions saved to {output_file}")
    return output_file
 