import argparse
import csv
import math
from pathlib import Path


REQUIRED_COLUMNS = {
    "transaction_id",
    "sales_amount",
    "discount_percentage",
    "customer_category",
    "is_anomaly",
}


def load_transactions(csv_path):
    with csv_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing_columns:
            columns = ", ".join(sorted(missing_columns))
            raise ValueError(f"Kolom CSV tidak ditemukan: {columns}")

        transactions = []
        for line_number, row in enumerate(reader, start=2):
            try:
                sales_amount = float(row["sales_amount"])
                discount = float(row["discount_percentage"])
                actual_label = int(row["is_anomaly"])
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Nilai angka tidak valid pada baris {line_number}."
                ) from error

            if not math.isfinite(sales_amount) or not math.isfinite(discount):
                raise ValueError(f"Nilai angka tidak valid pada baris {line_number}.")
            if actual_label not in (0, 1):
                raise ValueError(f"Label is_anomaly harus 0 atau 1 pada baris {line_number}.")

            transactions.append({
                "transaction_id": row["transaction_id"],
                "sales_amount": sales_amount,
                "discount": discount,
                "customer_category": (row["customer_category"] or "").strip(),
                "actual_label": actual_label,
            })

    if not transactions:
        raise ValueError("CSV tidak berisi data transaksi.")
    return transactions


def inspect_transaction(transaction):
    reasons = []
    if transaction["discount"] > 50:
        reasons.append("diskon lebih dari 50%")
    if transaction["sales_amount"] <= 0:
        reasons.append("nilai penjualan nol atau negatif")
    if not transaction["customer_category"]:
        reasons.append("kategori pelanggan kosong")
    return reasons


def main():
    parser = argparse.ArgumentParser(
        description="Deteksi anomali diskon pada transaksi penjualan."
    )
    default_csv = Path(__file__).with_name("sales_transactions.csv")
    parser.add_argument(
        "csv_file",
        nargs="?",
        type=Path,
        default=default_csv,
        help="Lokasi CSV transaksi (default: sales_transactions.csv di folder proyek).",
    )
    args = parser.parse_args()

    transactions = load_transactions(args.csv_file)
    results = [
        (transaction, inspect_transaction(transaction))
        for transaction in transactions
    ]

    true_positive = sum(
        bool(reasons) and transaction["actual_label"] == 1
        for transaction, reasons in results
    )
    false_positive = sum(
        bool(reasons) and transaction["actual_label"] == 0
        for transaction, reasons in results
    )
    true_negative = sum(
        not reasons and transaction["actual_label"] == 0
        for transaction, reasons in results
    )
    false_negative = sum(
        not reasons and transaction["actual_label"] == 1
        for transaction, reasons in results
    )

    total = len(transactions)
    predicted_anomalies = true_positive + false_positive
    actual_anomalies = true_positive + false_negative
    accuracy = (true_positive + true_negative) / total
    precision = true_positive / predicted_anomalies if predicted_anomalies else 0
    recall = true_positive / actual_anomalies if actual_anomalies else 0

    print("DETEKSI ANOMALI DISKON - PT MAJU BERSAMA")
    print(f"File data          : {args.csv_file}")
    print(f"Jumlah transaksi   : {total}")
    print(f"Anomali terdeteksi : {predicted_anomalies}")
    print(f"Anomali pada label : {actual_anomalies}")
    print(f"Accuracy           : {accuracy:.2%}")
    print(f"Precision          : {precision:.2%}")
    print(f"Recall             : {recall:.2%}")
    print(
        "Confusion matrix   : "
        f"TP={true_positive}, FP={false_positive}, "
        f"TN={true_negative}, FN={false_negative}"
    )

    print("\nTransaksi yang ditandai:")
    for transaction, reasons in results:
        if reasons:
            print(f"- {transaction['transaction_id']}: {', '.join(reasons)}")


if __name__ == "__main__":
    main()
