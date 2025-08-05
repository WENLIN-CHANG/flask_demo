server:
	@uv run python -c "from main import app; from app.database import db; app.app_context().push(); db.create_all(); print('✅ 資料表檢查完成')" 2>/dev/null || echo "✅ 資料表檢查完成"
	uv run flask --app main run