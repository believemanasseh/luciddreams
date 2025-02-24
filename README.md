# Luciddreams Test

## Live Deployment

[https://luciddreams.daimones.xyz](https://luciddreams.daimones.xyz)

## Development

Create virtualenv

```bash
pipenv shell
```

Install dependencies

```bash
pipenv install
```

Start dev server

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
