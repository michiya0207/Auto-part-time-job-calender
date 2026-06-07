# Auto-part-time-job-calender
1. 概要
PDFで送られてきたバイトのシフトをGoogleカレンダーに自動で割り当ててくれるシステム
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
3. 使い方
    samples/にPDFを置く
    PDF_PATHを変える
    python main.pyで実行
4. 設定項目
    PDF_PATH / NAME_KEY / CLASS_MINUTES / YEARと開始-15分・終了＋10分のオフセット
5. 注意点
    同じ月を2回実行すると重複する
    年はYEARで固定
    PDFの形式が変わると抽出がズレる可能性
    
