# Luciddreams Test

## Run application
1.) Run migrations after setting up environment variables 
```bash
alembic upgrade head
```

2.) Start dev server
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
