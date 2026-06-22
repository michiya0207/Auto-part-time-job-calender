def caleculate_total_koma(shifts):
    total_koma = 0
    for shift in shifts:
        total_koma += shift["koma"]
    return total_koma

def caleculate_money(koma , price , days):
    total = koma * price + days * 310

    return total

if __name__ == "__main__":
    from read_pdf import read_pdf, extract_shifts
    shifts = extract_shifts(read_pdf("samples/ブース表_202605_merged.pdf"))
    total = caleculate_money(caleculate_total_koma(shifts), 1500, len(shifts))
    print(f"今月の給料: {total}円")

