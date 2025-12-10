from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from collections import Counter
import csv

app = Flask(__name__)
CORS(app)  # Live Serverからのアクセスを許可

# グローバル変数でデータを保持
movies_df = None
ratings_df = None

def load_data():
    """CSVファイルを読み込む"""
    global movies_df, ratings_df
    try:
        # movies_100k.csvを読み込む（パイプ区切り）
        print("📂 movies_100k.csvを読み込んでいます...")
        movies_df = pd.read_csv(
            'movies_100k.csv',
            encoding='latin-1',  # エンコーディング変更
            sep='|',  # パイプ区切り
            header=0,  # 最初の行をヘッダーとして扱う
            on_bad_lines='skip'
        )
        
        # ヘッダー行を削除（データとして読み込まれている場合）
        if movies_df.iloc[0].astype(str).str.contains('movie_id|movie_title').any():
            movies_df = movies_df.iloc[1:]
        
        # 列名を確認
        print(f"   列名: {list(movies_df.columns)[:5]}...")
        
        # 列名を標準化
        if len(movies_df.columns) >= 24:
            movies_df.columns = [
                'movieId', 'title', 'release_date', 'video_release_date', 
                'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation', 
                'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 
                'Fantasy', 'Film_Noir', 'Horror', 'Musical', 'Mystery', 
                'Romance', 'Sci_Fi', 'Thriller', 'War', 'Western'
            ]
            
            # movieIdを整数に変換
            movies_df['movieId'] = pd.to_numeric(movies_df['movieId'], errors='coerce')
            movies_df = movies_df.dropna(subset=['movieId'])
            movies_df['movieId'] = movies_df['movieId'].astype(int)
            
            # ジャンル列を結合
            genre_columns = ['unknown', 'Action', 'Adventure', 'Animation', 'Childrens', 'Comedy', 
                            'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film_Noir', 
                            'Horror', 'Musical', 'Mystery', 'Romance', 'Sci_Fi', 
                            'Thriller', 'War', 'Western']
            
            def create_genres(row):
                try:
                    genres = [col.replace('_', '-') for col in genre_columns if pd.to_numeric(row[col], errors='coerce') == 1]
                    return '|'.join(genres) if genres else 'Unknown'
                except:
                    return 'Unknown'
            
            movies_df['genres'] = movies_df.apply(create_genres, axis=1)
            
            # 必要な列のみ残す
            movies_df = movies_df[['movieId', 'title', 'genres']]
        
        print(f"✅ 映画データ読み込み完了: {len(movies_df)}件")
        print(f"   サンプル: {movies_df.head(3).to_dict('records')}")
        
        # ratings_100k.csvを読み込む
        print("📂 ratings_100k.csvを読み込んでいます...")
        
        # まず1行目を読んで区切り文字を判定
        with open('ratings_100k.csv', 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if '\t' in first_line:
                separator = '\t'
                print("   区切り文字: タブ")
            elif ',' in first_line:
                separator = ','
                print("   区切り文字: カンマ")
            else:
                separator = '|'
                print("   区切り文字: パイプ")
        
        # 区切り文字を使って読み込み
        ratings_df = pd.read_csv(
            'ratings_100k.csv',
            encoding='utf-8',
            sep=separator,
            on_bad_lines='skip'
        )
        
        # 列名を確認
        print(f"   列名: {list(ratings_df.columns)}")
        
        # 列名を標準化
        ratings_df.columns = ratings_df.columns.str.strip()
        
        # 列名が想定と違う場合の対応
        if 'user_id' in ratings_df.columns:
            ratings_df = ratings_df.rename(columns={
                'user_id': 'userId',
                'item_id': 'movieId'
            })
        elif len(ratings_df.columns) == 4:
            ratings_df.columns = ['userId', 'movieId', 'rating', 'timestamp']
        
        # データ型を変換
        ratings_df['userId'] = pd.to_numeric(ratings_df['userId'], errors='coerce')
        ratings_df['movieId'] = pd.to_numeric(ratings_df['movieId'], errors='coerce')
        ratings_df['rating'] = pd.to_numeric(ratings_df['rating'], errors='coerce')
        
        # NaN行を削除
        ratings_df = ratings_df.dropna(subset=['userId', 'movieId', 'rating'])
        
        # 整数に変換
        ratings_df['userId'] = ratings_df['userId'].astype(int)
        ratings_df['movieId'] = ratings_df['movieId'].astype(int)
        ratings_df['rating'] = ratings_df['rating'].astype(float)
        
        print(f"✅ 評価データ読み込み完了: {len(ratings_df)}件")
        print(f"   サンプル: {ratings_df.head(3).to_dict('records')}")
        
        return True
        
    except FileNotFoundError as e:
        print(f"❌ ファイルが見つかりません: {e}")
        print("💡 movies_100k.csvとratings_100k.csvをapp.pyと同じフォルダに配置してください")
        return False
    except Exception as e:
        print(f"❌ データ読み込みエラー: {e}")
        print(f"   エラータイプ: {type(e).__name__}")
        
        # 別の読み込み方法を試す
        try:
            print("\n🔄 別の方法で読み込みを試みています...")
            
            # moviesを再試行（区切り文字を明示的に指定）
            movies_df = pd.read_csv(
                'movies_100k.csv',
                encoding='utf-8',
                sep=',',
                engine='python',
                on_bad_lines='skip'
            )
            print(f"✅ 映画データ読み込み完了（再試行）: {len(movies_df)}件")
            
            # ratingsを再試行
            ratings_df = pd.read_csv(
                'ratings_100k.csv',
                encoding='utf-8',
                sep=',',
                engine='python',
                on_bad_lines='skip'
            )
            print(f"✅ 評価データ読み込み完了（再試行）: {len(ratings_df)}件")
            
            return True
            
        except Exception as e2:
            print(f"❌ 再試行も失敗: {e2}")
            print("\n💡 CSVファイルのフォーマットを確認してください")
            print("   - ファイルがカンマ区切りであること")
            print("   - ヘッダー行が存在すること")
            print("   - ファイルが破損していないこと")
            return False

def get_recommendations(selected_movie_ids):
    """レコメンデーションアルゴリズム（コンテンツベースフィルタリング）"""
    
    if not selected_movie_ids or len(selected_movie_ids) == 0:
        # 未選択: 評価値が高い映画を返す
        print("📊 総合ランキングモード")
        
        movie_stats = ratings_df.groupby('movieId').agg({
            'rating': ['mean', 'count']
        }).reset_index()
        movie_stats.columns = ['movieId', 'avg_rating', 'count']
        
        # 10件以上の評価がある映画のみ
        movie_stats = movie_stats[movie_stats['count'] >= 10]
        movie_stats = movie_stats.sort_values('avg_rating', ascending=False).head(5)
        
        # 映画情報と結合
        result = movie_stats.merge(movies_df, on='movieId', how='left')
        
        recommendations = []
        for _, row in result.iterrows():
            recommendations.append({
                'id': int(row['movieId']),
                'title': str(row['title']),
                'genres': str(row['genres']) if pd.notna(row['genres']) else 'ジャンル不明',
                'avgRating': round(float(row['avg_rating']), 2)
            })
        
        print(f"🎯 総合ランキングトップ5を返却")
        return recommendations
    
    else:
        # 選択された映画に基づくレコメンデーション
        print(f"🎬 選択された映画ID: {selected_movie_ids}")
        
        selected_movies = movies_df[movies_df['movieId'].isin(selected_movie_ids)]
        
        # ジャンル分析
        genre_counter = Counter()
        for _, movie in selected_movies.iterrows():
            if pd.notna(movie['genres']):
                genres = str(movie['genres']).split('|')
                for genre in genres:
                    genre_counter[genre] += 1
        
        print(f"🏷️ ジャンル傾向: {dict(genre_counter)}")
        
        # 映画の平均評価を事前計算
        movie_stats = ratings_df.groupby('movieId').agg({
            'rating': ['mean', 'count']
        }).reset_index()
        movie_stats.columns = ['movieId', 'avg_rating', 'count']
        
        # スコア計算（コンテンツベースフィルタリング）
        scored_movies = []
        for _, movie in movies_df.iterrows():
            if movie['movieId'] in selected_movie_ids:
                continue
            
            score = 0
            
            # ジャンルマッチングスコア（重み: 2.0）
            if pd.notna(movie['genres']):
                genres = str(movie['genres']).split('|')
                for genre in genres:
                    score += genre_counter.get(genre, 0) * 2
            
            # 評価値スコア（重み: 0.8）
            movie_rating = movie_stats[movie_stats['movieId'] == movie['movieId']]
            if not movie_rating.empty and movie_rating.iloc[0]['count'] >= 5:
                avg_rating = movie_rating.iloc[0]['avg_rating']
                score += avg_rating * 0.8
            else:
                avg_rating = 0
            
            if score > 0:
                scored_movies.append({
                    'id': int(movie['movieId']),
                    'title': str(movie['title']),
                    'genres': str(movie['genres']) if pd.notna(movie['genres']) else 'ジャンル不明',
                    'score': score,
                    'avgRating': round(float(avg_rating), 2) if avg_rating > 0 else None
                })
        
        # スコア順にソート
        scored_movies.sort(key=lambda x: x['score'], reverse=True)
        
        # トップ5を返す
        top_5 = scored_movies[:5]
        for movie in top_5:
            print(f"  {movie['title']} - スコア: {movie['score']:.2f}")
            del movie['score']  # スコアは返さない
        
        print(f"🎯 レコメンデーション完了: {len(top_5)}件")
        return top_5

@app.route('/api/movies', methods=['GET', 'OPTIONS'])
def get_movies():
    """映画一覧を取得するAPI"""
    # OPTIONSリクエスト（プリフライト）に対応
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        return response
    
    if movies_df is None:
        return jsonify({'error': 'データが読み込まれていません'}), 500
    
    movies_list = []
    for _, row in movies_df.iterrows():
        movies_list.append({
            'id': int(row['movieId']),
            'title': str(row['title']),
            'genres': str(row['genres']) if pd.notna(row['genres']) else 'ジャンル不明'
        })
    
    print(f"📤 映画一覧送信: {len(movies_list)}件")
    return jsonify(movies_list)

@app.route('/api/recommend', methods=['POST', 'OPTIONS'])
def recommend():
    """レコメンデーションを取得するAPI"""
    # OPTIONSリクエスト（プリフライト）に対応
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    if movies_df is None or ratings_df is None:
        return jsonify({'error': 'データが読み込まれていません'}), 500
    
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'JSONデータが送信されていません'}), 400
        
        selected_movies = data.get('selected_movies', [])
        
        print(f"\n{'='*50}")
        print(f"📥 リクエスト受信")
        print(f"メソッド: {request.method}")
        print(f"Content-Type: {request.headers.get('Content-Type')}")
        print(f"選択された映画数: {len(selected_movies)}")
        print(f"選択された映画ID: {selected_movies}")
        
        recommendations = get_recommendations(selected_movies)
        
        print(f"📤 レスポンス送信: {len(recommendations)}件")
        print(f"{'='*50}\n")
        
        return jsonify(recommendations)
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """ヘルスチェック用エンドポイント"""
    status = {
        'status': 'ok',
        'movies_loaded': movies_df is not None,
        'ratings_loaded': ratings_df is not None,
        'movies_count': len(movies_df) if movies_df is not None else 0,
        'ratings_count': len(ratings_df) if ratings_df is not None else 0
    }
    return jsonify(status)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎬 映画レコメンデーションシステム - バックエンド起動")
    print("="*60 + "\n")
    
    # データ読み込み
    if load_data():
        print("\n" + "="*60)
        print("✅ サーバー起動準備完了")
        print("🌐 アクセスURL: http://localhost:5000")
        print("🔧 ヘルスチェック: http://localhost:5000/health")
        print("💡 停止するには Ctrl+C を押してください")
        print("="*60 + "\n")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("\n❌ データ読み込みに失敗したため、サーバーを起動できません")
        print("💡 CSVファイルを確認してください:")
        print("   1. ファイル名が正確か（movies_100k.csv, ratings_100k.csv）")
        print("   2. app.pyと同じフォルダにあるか")
        print("   3. ファイルが破損していないか")
        print("   4. ファイルがカンマ区切り形式か\n")