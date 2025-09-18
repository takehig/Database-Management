# Database Management System v1.2.0

## 概要
WealthAI Enterprise Systems用統合データベース管理システム

## 🎯 主要機能
- **複数データベース対応**: CRM・ProductMaster・AIChat切り替え
- **テーブル一覧表示**: 自動取得・リアルタイム更新
- **クイックアクセス**: テーブル名クリックでSQL自動生成
- **SQL実行・結果表示**: 手動入力・自動生成両対応

## 🏗️ 技術スタック
- **Backend**: FastAPI + Jinja2Templates
- **Frontend**: HTML5 + Bootstrap 5 + JavaScript ES6+
- **Database**: PostgreSQL (複数DB対応)
- **Port**: 8006

## 📊 対応データベース

### CRM Database (crm)
- **接続**: crm_user/crm123
- **主要テーブル**: customers, sales_notes, holdings, cash_inflows
- **用途**: 顧客管理・営業メモ・保有資産管理

### ProductMaster Database (productmaster)
- **接続**: productmaster_user/productmaster123
- **主要テーブル**: products, product_categories
- **用途**: 商品情報管理・商品マスター

### AIChat Database (aichat)
- **接続**: aichat_user/aichat123
- **主要テーブル**: system_prompts
- **用途**: SystemPrompt Management・AI設定管理

## 🎨 UI構成

### 2カラムレイアウト
```
┌─────────────────────────┬─────────────────┐
│ SQL実行エリア (8列)      │ テーブル一覧(4列) │
│ ┌─────────────────────┐ │ ┌─────────────┐ │
│ │ データベース選択     │ │ │ system_prompts│ │
│ │ [CRM Database ▼]   │ │ │ customers    │ │
│ │                    │ │ │ sales_notes  │ │
│ │ SQLクエリ入力       │ │ │ holdings     │ │
│ │ ┌─────────────────┐ │ │ │ ...         │ │
│ │ │SELECT * FROM... │ │ │ └─────────────┘ │
│ │ └─────────────────┘ │ │                 │
│ │ [実行] [クリア]     │ │                 │
│ └─────────────────────┘ └─────────────────┘
└─────────────────────────────────────────────┘
│              実行結果表示エリア              │
└─────────────────────────────────────────────┘
```

## 🔧 API仕様

### エンドポイント
```
GET  /                      # メインページ
GET  /api/tables/{db_name}  # テーブル一覧取得
POST /api/execute-sql       # SQL実行
```

### API詳細

#### テーブル一覧取得
```http
GET /api/tables/crm
```
```json
{
  "status": "success",
  "tables": ["customers", "sales_notes", "holdings"]
}
```

#### SQL実行
```http
POST /api/execute-sql
Content-Type: application/json

{
  "sql": "SELECT * FROM customers LIMIT 10;",
  "database": "crm"
}
```
```json
{
  "status": "success",
  "results": [...],
  "count": 10
}
```

## 🚀 使用方法

### 基本操作
1. **データベース選択**: ドロップダウンでCRM/ProductMaster/AIChat選択
2. **テーブル確認**: 右側に自動表示されるテーブル一覧を確認
3. **クイックアクセス**: テーブル名をクリック → `SELECT * FROM table LIMIT 10;` 自動入力
4. **SQL実行**: 「実行」ボタンで結果表示

### 高度な使用例
```sql
-- CRM: 営業メモ検索
SELECT customer_id, content FROM sales_notes 
WHERE content LIKE '%投資%' LIMIT 5;

-- ProductMaster: 商品検索
SELECT product_code, product_name FROM products 
WHERE product_type = '債券' LIMIT 10;

-- AIChat: システムプロンプト確認
SELECT prompt_key, LEFT(prompt_text, 100) as preview 
FROM system_prompts ORDER BY updated_at DESC;
```

## 🏛️ アーキテクチャ

### システム構成
```
Database Management (Port 8006)
├── FastAPI Application
│   ├── Multiple DB Connection Pool
│   │   ├── CRM (crm_user/crm123)
│   │   ├── ProductMaster (productmaster_user/productmaster123)
│   │   └── AIChat (aichat_user/aichat123)
│   ├── REST API Endpoints
│   └── Jinja2 Template Engine
└── Frontend (Bootstrap 5 + JavaScript)
    ├── Database Selector
    ├── Table List (Auto-refresh)
    ├── SQL Editor
    └── Result Display
```

### データフロー
```
User Action → Frontend JS → FastAPI → PostgreSQL → Response → UI Update
     ↓              ↓           ↓          ↓          ↓         ↓
DB選択 → onchange → /api/tables → SELECT → JSON → テーブル一覧更新
テーブルクリック → onclick → SQL自動生成 → 入力欄更新
SQL実行 → fetch → /api/execute-sql → クエリ実行 → 結果表示
```

## 🔗 アクセス情報
- **直接アクセス**: http://44.217.45.24:8006/
- **プロキシアクセス**: http://44.217.45.24/database/
- **GitHub**: https://github.com/takehig/Database-Management

## 🛠️ 開発・運用

### ローカル開発
```bash
# 依存関係インストール
pip install -r requirements.txt

# 開発サーバー起動
python main.py
```

### デプロイ手順
```bash
# 1. ローカル修正
git add . && git commit -m "[UPDATE] 機能追加"

# 2. GitHub反映
git push origin main

# 3. EC2反映
# SSM経由でgit pull → ファイルコピー → サービス再起動
```

### systemd管理
```bash
# サービス管理
sudo systemctl start|stop|restart database-mgmt
sudo systemctl status database-mgmt

# ログ確認
sudo journalctl -u database-mgmt -f
```

## 📈 バージョン履歴

### v1.2.0 (2025-09-19)
- ✅ テーブル一覧表示機能追加
- ✅ AIChat データベース接続設定修正
- ✅ クイックアクセス機能実装
- ✅ 2カラムレイアウト採用

### v1.1.0 (2025-09-19)
- ✅ データベース選択機能追加
- ✅ 複数データベース対応実装
- ✅ 動的接続切り替え機能

### v1.0.0 (2025-09-19)
- ✅ FastAPI + Jinja2統一構造実装
- ✅ HTMLハードコード削除・MVC分離
- ✅ 基本SQL実行機能実装

## 🔒 セキュリティ
- データベース認証情報は環境変数・設定ファイルで管理
- SQL実行は接続プール経由で安全に処理
- エラーハンドリング・ロールバック機能完備

## 🎯 今後の拡張予定
- [ ] SQLクエリ履歴機能
- [ ] エクスポート機能（CSV/Excel）
- [ ] クエリ保存・共有機能
- [ ] データベーススキーマ表示機能
