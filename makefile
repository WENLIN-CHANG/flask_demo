server:
	@uv run python -c "from main import app, db; app.app_context().push(); db.create_all(); print('✅ 資料表檢查完成')"
	uv run flask --app main run