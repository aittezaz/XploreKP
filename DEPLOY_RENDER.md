# Deploy XploreKP on Render

Render is the recommended free host for this Flask project.

## Settings

- Service type: Web Service
- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Plan: Free

## Steps

1. Push this project to GitHub.
2. Open https://render.com and sign in.
3. Click New, then Web Service.
4. Connect your GitHub repository.
5. Use the settings above.
6. Click Deploy Web Service.

Render will give you a public link like:

```text
https://xplorekp.onrender.com
```

## Note

The Add Place form saves to a JSON file locally. On a free live server, file changes may not be permanent after redeploys. For permanent online place submissions, connect a database such as Render Postgres or Supabase later.
