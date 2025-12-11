# 映画レコメンデーションシステム

コンテンツベースフィルタリングを使用した映画推薦システムです。ユーザーが選択した映画の傾向に基づいて、オススメの映画を提示します。

## 📋 目次

- [概要](#概要)
- [機能](#機能)
- [技術スタック](#技術スタック)
- [セットアップ](#セットアップ)
- [使い方](#使い方)
- [システム構成](#システム構成)
- [アルゴリズム](#アルゴリズム)
- [ファイル構成](#ファイル構成)

## 概要

このプロジェクトは、MovieLensデータセットを使用した映画レコメンデーションシステムです。ユーザーが好きな映画を最大3つ選択すると、その映画のジャンル傾向と評価データを分析し、類似した映画をトップ5で提案します。

### デモ

![システムイメージ](docs/screenshot.png)

## 機能

### ✨ 主な機能

- **映画選択**: ドロップダウンメニューから最大3つの映画を選択
- **コンテンツベースフィルタリング**: 選択された映画のジャンルと評価に基づくレコメンデーション
- **総合ランキング**: 未選択時は評価値の高い映画を表示
- **リアルタイム計算**: バックエンドで高速にレコメンデーションを計算
- **レスポンシブデザイン**: モダンで使いやすいUI/UX

### 📊 レコメンデーションアルゴリズム

#### 選択時（コンテンツベースフィルタリング）
1. 選択された映画のジャンルを分析
2. ジャンルマッチング度と平均評価値でスコアリング
   - ジャンル一致: 重み 2.0
   - 平均評価値: 重み 0.8
3. スコアの高い順にトップ5を返却

#### 未選択時（総合ランキング）
1. 各映画の平均評価を計算
2. 10件以上の評価がある映画のみ対象
3. 平均評価の高い順にトップ5を表示

## 技術スタック

### バックエンド
- **Python 3.12**
- **Flask 3.1.2** - Webフレームワーク
- **Flask-CORS 6.0.1** - CORS対応
- **Pandas 2.1.4** - データ処理

### フロントエンド
- **HTML5** - 構造
- **CSS3** - スタイリング
- **JavaScript (ES6+)** - ロジック
- **Fetch API** - HTTP通信

### 開発環境
- **Visual Studio Code**
- **Live Server** - フロントエンド開発サーバー
- **Git** - バージョン管理

## セットアップ

### 前提条件

- Python 3.7以上がインストールされていること
- Visual Studio Codeがインストールされていること
- Live Server拡張機能がインストールされていること

### インストール手順

1. **リポジトリをクローン**

```bash
git clone https://github.com/ueno10314/movie-recommendation.git
cd movie-recommendation
```

2. **必要なPythonパッケージをインストール**

```bash
pip install -r requirements.txt
```

または個別にインストール：

```bash
pip install flask flask-cors pandas
```

3. **データファイルの配置**

プロジェクトフォルダに以下のCSVファイルを配置：
- `movies_100k.csv` - 映画データ
- `ratings_100k.csv` - 評価データ

## 使い方

### 1. バックエンドサーバーを起動

```bash
python app.py
```

以下のように表示されれば成功：

```
============================================================
🎬 映画レコメンデーションシステム - バックエンド起動
============================================================

✅ 映画データ読み込み完了: 1682件
✅ 評価データ読み込み完了: 100000件

🌐 アクセスURL: http://localhost:5000
```

### 2. フロントエンドを起動

VSCodeで`index.html`を右クリック → **Open with Live Server**

または、VSCode下部の「**Go Live**」ボタンをクリック

### 3. 映画を選択してレコメンデーションを取得

1. ブラウザで開いたページで映画を3つ選択（または未選択）
2. 「オススメ映画を表示」ボタンをクリック
3. トップ5のオススメ映画が表示されます

### 4. 終了方法

- **Pythonサーバー**: ターミナルで `Ctrl + C`
- **Live Server**: VSCode下部の「Port: 5500」をクリック

## システム構成

```
┌─────────────────┐
│   ブラウザ      │
│  (Live Server)  │
│  Port: 5500     │
└────────┬────────┘
         │ HTTP Request (POST)
         ↓
┌─────────────────┐
│  Flask API      │
│  (Python)       │
│  Port: 5000     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   CSV Files     │
│  - movies.csv   │
│  - ratings.csv  │
└─────────────────┘
         │
         ↓
┌─────────────────┐
│ レコメンデー    │
│ ションアルゴリズム│
└────────┬────────┘
         │ JSON Response
         ↓
┌─────────────────┐
│   ブラウザ      │
│  結果表示       │
└─────────────────┘
```

## アルゴリズム

### コンテンツベースフィルタリングの実装

```python
# スコア計算式
score = (ジャンル一致数 × 2.0) + (平均評価 × 0.8)
```

**例：**
- 選択映画: Toy Story (Animation|Comedy|Children)
- 候補映画: A Bug's Life (Animation|Comedy|Children)
  - ジャンル一致: 3つ → 3 × 2.0 = 6.0
  - 平均評価: 3.5 → 3.5 × 0.8 = 2.8
  - **総合スコア: 8.8**

## ファイル構成

```
project/
├── app.py                  # Pythonバックエンド（Flask）
├── index.html              # フロントエンド（HTML）
├── style.css               # スタイルシート
├── script-python.js        # JavaScript（API通信）
├── movies_100k.csv         # 映画データ
├── ratings_100k.csv        # 評価データ
├── requirements.txt        # Python依存パッケージ
├── .gitignore              # Git除外ファイル
└── README.md               # このファイル
```

### 主要ファイルの説明

#### `app.py`
- Flaskアプリケーション
- API エンドポイント
  - `GET /api/movies` - 映画一覧取得
  - `POST /api/recommend` - レコメンデーション取得
  - `GET /health` - ヘルスチェック
- レコメンデーションアルゴリズムの実装

#### `index.html`
- ユーザーインターフェース
- 映画選択フォーム
- 結果表示エリア

#### `style.css`
- モダンなデザイン
- レスポンシブレイアウト
- アニメーション効果

#### `script-python.js`
- API通信
- DOM操作
- イベント処理

## API エンドポイント

### 1. ヘルスチェック
```
GET http://localhost:5000/health
```

**レスポンス:**
```json
{
  "status": "ok",
  "movies_loaded": true,
  "ratings_loaded": true,
  "movies_count": 1682,
  "ratings_count": 100000
}
```

### 2. 映画一覧取得
```
GET http://localhost:5000/api/movies
```

**レスポンス:**
```json
[
  {
    "id": 1,
    "title": "Toy Story (1995)",
    "genres": "Animation|Children|Comedy"
  },
  ...
]
```

### 3. レコメンデーション取得
```
POST http://localhost:5000/api/recommend
Content-Type: application/json

{
  "selected_movies": [1, 2, 3]
}
```

**レスポンス:**
```json
[
  {
    "id": 10,
    "title": "GoldenEye (1995)",
    "genres": "Action|Adventure|Thriller",
    "avgRating": 3.21
  },
  ...
]
```

## データ仕様

### movies_100k.csv
MovieLensデータセット（パイプ区切り）

| 列名 | 説明 | 型 |
|------|------|-----|
| movie_id | 映画ID | Integer |
| movie_title | 映画タイトル | String |
| genres | ジャンル（複数の列） | Binary |

### ratings_100k.csv
評価データ（カンマ区切り）

| 列名 | 説明 | 型 |
|------|------|-----|
| userId | ユーザーID | Integer |
| movieId | 映画ID | Integer |
| rating | 評価値 (1-5) | Float |
| timestamp | タイムスタンプ | Integer |

## トラブルシューティング

### エラー: バックエンドに接続できません

**原因:** Pythonサーバーが起動していない

**解決策:**
```bash
python app.py
```

### エラー: ModuleNotFoundError

**原因:** 必要なパッケージがインストールされていない

**解決策:**
```bash
pip install flask flask-cors pandas
```

### エラー: CSVファイルが見つかりません

**原因:** CSVファイルが正しい場所にない

**解決策:**
- `movies_100k.csv`と`ratings_100k.csv`を`app.py`と同じフォルダに配置

### エラー: Port 5000 already in use

**原因:** ポート5000が既に使用されている

**解決策:**
```python
# app.pyの最終行を変更
app.run(debug=True, host='0.0.0.0', port=5001)
```

```javascript
// script-python.jsの1行目を変更
const API_BASE_URL = 'http://localhost:5001';
```

## カスタマイズ

### レコメンデーションの重み調整

`app.py`の以下の部分を変更：

```python
# ジャンルの重み（デフォルト: 2.0）
score += genre_counter.get(genre, 0) * 2.0

# 評価値の重み（デフォルト: 0.8）
score += avg_rating * 0.8
```

### 最小評価数の変更

```python
# 未選択時（デフォルト: 10件以上）
movie_stats = movie_stats[movie_stats['count'] >= 10]

# 選択時（デフォルト: 5件以上）
if not movie_rating.empty and movie_rating.iloc[0]['count'] >= 5:
```

## 今後の改善案

- [ ] 協調フィルタリングの追加
- [ ] ユーザー評価の保存機能
- [ ] より詳細なフィルタリング（年代、監督など）
- [ ] お気に入り機能
- [ ] 履歴表示機能
- [ ] データベース連携
- [ ] ユーザー認証機能

## ライセンス

このプロジェクトは教育目的で作成されています。

## 参考資料

- [MovieLens Dataset](https://grouplens.org/datasets/movielens/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## 作者

**ueno10314**

## 謝辞

- MovieLens データセットを提供するGroupLens Research
- 開発をサポートしてくれた全ての方々

---

**開発環境**: Python 3.12 + Flask + Live Server  
**最終更新**: 2025年12月
