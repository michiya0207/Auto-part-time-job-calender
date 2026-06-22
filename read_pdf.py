import pdfplumber
from datetime import datetime, timedelta

# ===== 設定（ここを変えれば挙動を調整できる）=====

NAME_KEY = "河江"      # 自分(寒河江)の目印。2文字'河江T'でも3文字'寒河江T'でも当たる部分文字列
CLASS_MINUTES = 65     # 1コマの長さ(分)。終了時刻の計算に使う。実際の勤務に合わせて調整
YEAR = 2026            # シフト表に「年」が無いので、ここで指定


def read_pdf(PDF_PATH):
    with pdfplumber.open(PDF_PATH) as pdf:
        table = []
        for page in pdf.pages:
            t = page.extract_table()
            if t is not None:           # 表が無いページは飛ばす
                table.append(t)
        return table


def extract_shifts(tables):
    """表の中から「河江」が入っているコマを探し、日付ごとの勤務時間を返す"""
    # (月, 日) -> その日に入っているコマの開始時刻の集合(set=重複を自動で消す)
    hits = {}

    for table in tables:
        # --- その週の6日分の「日」を取り出す(先頭行からNoneを飛ばして集める) ---
        date_row = table[0]                          # ['6月','1',None,...,'2',...]
        month = int(date_row[0].replace("月", ""))    # '6月' -> 6
        days = [c for c in date_row[1:] if c is not None]   # ['1','2','3','4','5','6']

        # --- 行を上から見て、時刻を覚えながら名前を探す ---
        current_time = None
        for row in table:
            cell0 = row[0]
            # 列0が時刻(14:55など)なら、そのブロックの開始時刻 → 覚えておく
            if cell0 is not None and ":" in str(cell0):
                current_time = cell0
            if current_time is None:
                continue   # まだ時間ブロックに入っていない行は無視

            # 6日分の「先生名の列」(= 2 + 5*d)を1つずつ見る
            for d in range(6):
                col = 2 + 5 * d
                if col >= len(row):
                    continue
                cell = row[col]
                if cell is None:
                    continue
                name = cell.replace("\n", "")        # '河\n江\nT' -> '河江T'
                if NAME_KEY in name:
                    day = int(days[d])
                    hits.setdefault((month, day), set()).add(current_time)

    # --- 日付ごとに 開始=一番早いコマ, 終了=一番遅いコマ+1コマ を計算 ---
    shifts = []
    for (month, day), times in hits.items():
        # 時刻を「時刻として」並べ替える(文字列のままだと誤る場合があるため)
        starts = sorted(times, key=lambda t: datetime.strptime(t, "%H:%M"))
        start = starts[0]
        last = starts[-1]
        end_dt = datetime.strptime(last, "%H:%M") + timedelta(minutes=CLASS_MINUTES)
        end = end_dt.strftime("%H:%M")
        shifts.append({
            "year": YEAR, "month": month, "day": day,
            "start": start, "end": end,
            "koma":len(times),
        })

    shifts.sort(key=lambda s: (s["month"], s["day"]))   # 月→日 の順に並べる
    return shifts


if __name__ == "__main__":
    PDF_PATH = "samples/ブース表_202605_merged.pdf"
    tables = read_pdf(PDF_PATH)
    shifts = extract_shifts(tables)
    print(f"見つかったシフト: {len(shifts)}件")
    for s in shifts:
        print(f"{s['year']}/{s['month']:02d}/{s['day']:02d}  {s['start']} - {s['end']}")
