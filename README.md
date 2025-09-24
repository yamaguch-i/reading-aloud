# reading-aloud
入力したテキストを音読してくれるAI

## 必要要件
- Windows 10/11
- Python 3.10+（3.13 推奨）
- インターネット接続（edge-tts で外部通信あり）

## セットアップ（PowerShell）
> SSH鍵がない場合は HTTPS の行を使ってください。

```powershell
# どちらか一方（SSH or HTTPS）
git clone git@github.com:yamaguch-i/reading-aloud.git
# git clone https://github.com/yamaguch-i/reading-aloud.git

cd reading-aloud
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 起動
uvicorn app:app --host 0.0.0.0 --port 8000

# ブラウザ
# http://127.0.0.1:8000/   （ローカル）
# http://<PCのIP>:8000/    （LAN内の他PCから）
