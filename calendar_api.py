import os.path


from datetime import datetime, timedelta
from google.auth.transport.requests import Request          # トークンの更新に使う
from google.oauth2.credentials import Credentials            # 保存済みの認証情報を読む
from google_auth_oauthlib.flow import InstalledAppFlow       # 初回ログイン(ブラウザ)の処理
from googleapiclient.discovery import build                  # カレンダー操作の窓口を作る

# このアプリに許可してもらう権限の範囲。
# calendar.events = 「予定の読み書き」だけ。必要最小限にしておくのが安全。
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def get_calendar_service():
    """Google認証を済ませて、カレンダー操作用の窓口(service)を返す"""
    creds = None

    # token.json があれば「前回ログインした証明書」を読み込む（2回目以降はこれで済む）
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # 証明書が無い or 期限切れ などで使えない場合の処理
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # 期限切れだが更新できるなら、ログインし直さず更新する
            creds.refresh(Request())
        else:
            # 初回：credentials.json(鍵)を使ってブラウザを開き、ログイン許可をもらう
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # もらった証明書を token.json に保存（次回からブラウザ不要にするため）
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # カレンダーを操作するための窓口を作って返す
    service = build("calendar", "v3", credentials=creds)
    return service

def add_shift(service, shift):
    
    start_time = datetime.strptime(f"{shift['year']}-{shift['month']}-{shift['day']} {shift['start']}", "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(f"{shift['year']}-{shift['month']}-{shift['day']} {shift['end']}", "%Y-%m-%d %H:%M")
    start_time = start_time - timedelta(minutes=15)
    end_time = end_time + timedelta( minutes=10)

    event = {
        "summary": "塾バイト",
        "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Tokyo"},
        "end":   {"dateTime": end_time.isoformat(),   "timeZone": "Asia/Tokyo"},
    }


    created_event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"シフトを追加しました: {created_event.get('htmlLink')}")

def add_salary(service, year, month, day, amount):
    # amount を使ってタイトルを作り、その日に予定を1件登録する
    if month == 12:
        next_year, next_month = year + 1, 1   # 12月だけ翌年1月
    else:
        next_year, next_month = year, month + 1

    event = {
        "summary": f"バイト給料 ¥{amount}",
        "start": {"date": f"{next_year}-{next_month:02d}-{day:02d}"},
        "end":   {"date": f"{next_year}-{next_month:02d}-{day+1:02d}"},   # 終わりは翌日
    }
    created_event = service.events().insert(calendarId="primary", body=event).execute()




if __name__ == "__main__":
    # 動作確認：認証して、primaryカレンダーの予定を1件だけ取得してみる
    # （calendar.events 権限の範囲内でできる操作）
    service = get_calendar_service()
    result = service.events().list(calendarId="primary", maxResults=1).execute()
    print("認証成功！ primaryカレンダーにアクセスできました")
   

