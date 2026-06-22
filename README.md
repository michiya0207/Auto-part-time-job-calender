# Auto-part-time-job-calender

1. 概要
    PDFのバイトのシフト表から、自分のシフトを抽出して
    - 各シフトをGoogleカレンダーに「塾バイト」として登録する
    - その月の給料を計算し、翌月25日（給料日）に「バイト給料 ¥XXXX」として登録する
    システム

2. 必要なもの/準備
    - Python（3.13で動作確認）
    - 仮想環境(venv)を作成して有効化する
        python -m venv .venv
        .\.venv\Scripts\Activate.ps1   （Windows PowerShell の場合）
    - 必要なライブラリをインストール
        pip install pdfplumber google-api-python-client google-auth-httplib2 google-auth-oauthlib
    - Google Calendar API の認証ファイル credentials.json を用意する
        Google Cloud でプロジェクト作成 → Calendar API を有効化
        → OAuth クライアントID（デスクトップアプリ）を作成 → JSONをダウンロード
        → ファイル名を credentials.json にして、このプロジェクトの直下に置く
        ※ 初回実行時にブラウザでログイン許可を行うと token.json が自動生成される
        ※ credentials.json と token.json は秘密情報。gitには含めない（.gitignore済み）

3. ファイル構成
    read_pdf.py        … PDFを読み、自分のシフト（日付・開始/終了・コマ数）を抽出する
    calendar_api.py    … Google認証 / シフト登録(add_shift) / 給料登録(add_salary)
    caleculate_money.py… 給料の計算（コマ数×時給 + 日数×準備手当）
    main.py            … 司令塔。毎回変える入力をまとめ、上記を順に呼び出す

4. 使い方
    - samples/ に対象月のPDFを置く
    - main.py の先頭の入力を、その月に合わせて変更する
        PDF_PATH   … 置いたPDFのパス
        money_hour … 時給
        year       … 年
        month      … PDFの月（※必ずPDFと合わせる。給料は month の翌月25日に入る）
    - 実行： python main.py
        → シフト全件 + 給料1件 がカレンダーに登録される
    - シフトはもう登録済みで「給料だけ」入れたいときは、main.py の
      for ループ（add_shift の2行）をコメントアウトしてから実行する

5. 設定項目（変える場所）
    main.py           … PDF_PATH / money_hour / year / month（毎回変える入力）
    read_pdf.py       … NAME_KEY（探す名前）/ CLASS_MINUTES（1コマの長さ）/ YEAR
    calendar_api.py   … シフト予定の開始-15分・終了+10分のオフセット、タイトル「塾バイト」
    caleculate_money.py… 準備手当 310円（時給は main.py の money_hour から渡す）

6. 注意点
    - 同じ月を2回実行するとシフト/給料が重複する（重複防止は未実装）
    - month は手動設定なので、PDFの月と必ず一致させる（ズレると給料の登録月がずれる）
    - 給料は「正しい給料額」ではなく「PDFに書かれた内容」での計算。
      シフト確定後に変更があると実際の支給額とズレることがある
    - 年は YEAR / year で固定。年が変わったら更新する
    - PDFの形式（レイアウト）が変わると抽出がズレる可能性がある
