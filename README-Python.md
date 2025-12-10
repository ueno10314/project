# 🎬 映画レコメンデーションシステム

AI開発応用 2025 - 課題3: レコメンデーションアルゴリズムを使って推薦技術を学ぼう

## 📝 概要

協調フィルタリング（アイテムベース）を使用した映画レコメンデーションWebアプリケーションです。

ユーザーが好きな映画を選択すると、類似した映画を推薦します。

## 🎯 主な機能

- ✅ 好きな映画を最大3つ選択可能

- ✅ 選択された映画に基づいてオススメ映画トップ5を表示

- ✅ 映画未選択時は総合ランキング（評価数・評価値が高い映画）を表示

- ✅ レスポンシブデザイン対応

## 🛠️ 技術スタック

- **バックエンド**: Python 3.13, Flask

- **フロントエンド**: HTML5, CSS3, JavaScript

- **データ処理**: Pandas, NumPy

- **機械学習**: scikit-learn (Cosine Similarity)

- **データセット**: MovieLens 100K

## 📂 プロジェクト構成

movie-recommend/

├── app.py # Flaskアプリケーション

├── requirements.txt # 依存パッケージ

├── README.md # このファイル

├── .gitignore # Git除外設定

├── data/

│ ├── movies_100k.csv # 映画データ（1682件）

│ └── ratings_100k.csv # 評価データ（100000件）

├── static/

│ ├── style.css # スタイルシート

│ └── script.js # JavaScript

└── templates/

└── index.html # HTMLテンプレート

## 🚀 セットアップ手順

### 1. リポジトリをクローン

```bash

git clone https://github.com/FumiyaSano238/movie-recommend.git

cd movie-recommend

2. 仮想環境の作成と有効化

bash

# Windows

python -m venv venv

venv\Scripts\activate

# macOS/Linux

python3 -m venv venv

source venv/bin/activate

3. 依存パッケージのインストール

bash

pip install -r requirements.txt

4. データファイルの配置

data/ フォルダに以下のファイルを配置してください：

movies_100k.csv (映画データ)

ratings_100k.csv (評価データ)

5. アプリケーションの起動

bash

python app.py

ブラウザで http://localhost:5000 にアクセスしてください。

🧠 レコメンデーションアルゴリズム

アイテムベース協調フィルタリング

ユーザー-映画の評価行列を作成

943ユーザー × 1682映画のマトリックス

コサイン類似度で映画間の類似度を計算

類似度(映画A, 映画B) = cos(θ) = (A・B) / (||A|| × ||B||)

選択された映画と類似度の高い映画を推薦

類似度スコアの合計が高い順に上位5件を表示

総合ランキング（未選択時）

評価数と評価値を考慮した加重スコアで算出：

加重スコア = 平均評価 × log(評価数 + 1)

📊 システム全体図

┌─────────────┐ ┌─────────────┐ ┌─────────────┐

│ フロントエンド │ ←→ │ バックエンド │ ←→ │ CSVデータ │

│ HTML/CSS/JS │ │ Python/Flask│ │ 映画・評価 │

└─────────────┘ └─────────────┘ └─────────────┘