const API_BASE_URL = 'http://localhost:5000';
let movies = [];

// ページ読み込み時にデータを取得
window.onload = async function() {
    const loading = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const selectionForm = document.getElementById('selection-form');
    
    loading.style.display = 'block';
    errorDiv.style.display = 'none';
    selectionForm.style.display = 'none';
    
    try {
        // バックエンドの状態確認
        await checkBackendHealth();
        
        // 映画データを取得
        await loadMovies();
        
        loading.style.display = 'none';
        selectionForm.style.display = 'block';
        
        console.log(`✅ データ読み込み完了: ${movies.length}件`);
    } catch (error) {
        console.error('❌ エラー:', error);
        loading.style.display = 'none';
        errorDiv.style.display = 'block';
    }
};

// バックエンドの状態確認
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            throw new Error('バックエンドが応答しません');
        }
        
        const data = await response.json();
        console.log('🔧 バックエンド状態:', data);
        
        if (!data.movies_loaded || !data.ratings_loaded) {
            throw new Error('CSVデータが読み込まれていません');
        }
        
        return true;
    } catch (error) {
        throw new Error(`バックエンド接続エラー: ${error.message}`);
    }
}

// 映画一覧を取得
async function loadMovies() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/movies`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTPエラー: ${response.status}`);
        }
        
        movies = await response.json();
        populateSelects();
        
        console.log(`📥 映画データ取得: ${movies.length}件`);
    } catch (error) {
        console.error('映画データ取得エラー:', error);
        throw error;
    }
}

// セレクトボックスに映画を追加
function populateSelects() {
    const selects = ['movie1', 'movie2', 'movie3'];
    
    selects.forEach(selectId => {
        const select = document.getElementById(selectId);
        
        // 既存のオプションをクリア（デフォルトオプション以外）
        select.innerHTML = '<option value="">— 映画を選択してください —</option>';
        
        movies.forEach(movie => {
            const option = document.createElement('option');
            option.value = movie.id;
            option.textContent = movie.title;
            select.appendChild(option);
        });
        
        // 変更イベントで重複選択を防ぐ
        select.addEventListener('change', updateSelectOptions);
    });
}

// 選択済みの映画を他のセレクトボックスから除外
function updateSelectOptions() {
    const selected = [
        document.getElementById('movie1').value,
        document.getElementById('movie2').value,
        document.getElementById('movie3').value
    ].filter(id => id !== '');
    
    const selects = ['movie1', 'movie2', 'movie3'];
    
    selects.forEach(selectId => {
        const select = document.getElementById(selectId);
        const currentValue = select.value;
        
        Array.from(select.options).forEach(option => {
            if (option.value === '') return; // デフォルトオプションはスキップ
            
            // 他で選択されている場合は無効化
            if (selected.includes(option.value) && option.value !== currentValue) {
                option.disabled = true;
                option.style.color = '#ccc';
            } else {
                option.disabled = false;
                option.style.color = '';
            }
        });
    });
}

// レコメンデーションを取得
async function getRecommendations() {
    const movie1 = document.getElementById('movie1').value;
    const movie2 = document.getElementById('movie2').value;
    const movie3 = document.getElementById('movie3').value;
    
    const selectedMovies = [movie1, movie2, movie3]
        .filter(id => id !== '')
        .map(Number);
    
    console.log('🎬 選択された映画ID:', selectedMovies);
    
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'オススメ映画を解析中...';
    
    try {
        console.log('📤 POSTリクエスト送信:', {
            url: `${API_BASE_URL}/api/recommend`,
            body: { selected_movies: selectedMovies }
        });
        
        const response = await fetch(`${API_BASE_URL}/api/recommend`, {
            method: 'POST',  // 重要: POSTメソッドを使用
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                selected_movies: selectedMovies 
            })
        });
        
        console.log('📥 レスポンス受信:', response.status, response.statusText);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('サーバーエラー:', errorText);
            throw new Error(`HTTPエラー: ${response.status} - ${errorText}`);
        }
        
        const recommendations = await response.json();
        console.log('🎯 レコメンデーション結果:', recommendations);
        
        displayRecommendations(recommendations);
    } catch (error) {
        console.error('❌ レコメンデーション取得エラー:', error);
        alert(`レコメンデーションの取得に失敗しました。\n\nエラー: ${error.message}\n\nバックエンドサーバーを確認してください。`);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'オススメ映画を表示';
    }
}

// レコメンデーションを表示
function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations');
    container.innerHTML = '<h1>🌟 オススメ映画トップ5</h1>';
    
    if (!recommendations || recommendations.length === 0) {
        container.innerHTML += '<p style="text-align: center; color: #6b7280; margin-top: 2rem;">レコメンデーションを生成できませんでした</p>';
        return;
    }
    
    recommendations.forEach((movie, index) => {
        const item = document.createElement('div');
        item.className = 'recommendation-item';
        
        const ratingHtml = movie.avgRating 
            ? `<div class="movie-rating">⭐ ${movie.avgRating}</div>`
            : '';
        
        item.innerHTML = `
            <div class="rank">${index + 1}</div>
            <div class="movie-info">
                <div class="movie-title">${movie.title}</div>
                <div class="movie-genres">${movie.genres || 'ジャンル不明'}</div>
                ${ratingHtml}
            </div>
        `;
        
        container.appendChild(item);
    });
    
    const backBtn = document.createElement('button');
    backBtn.className = 'back-button';
    backBtn.textContent = '戻る';
    backBtn.onclick = () => {
        container.innerHTML = '';
        document.getElementById('selection-form').style.display = 'block';
        
        // 選択をリセット
        document.getElementById('movie1').value = '';
        document.getElementById('movie2').value = '';
        document.getElementById('movie3').value = '';
        updateSelectOptions();
    };
    container.appendChild(backBtn);
    
    document.getElementById('selection-form').style.display = 'none';
    
    // 結果が表示されたら一番上にスクロール
    window.scrollTo({ top: 0, behavior: 'smooth' });
}