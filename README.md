# RIKS — family app

One site for **Aanant** (contest) and **Nikita** (INI-CET). The home page asks who is opening RIKS.

## Run

```bash
cd ~/work/opencamp
python3 -m pip install --user -r requirements.txt
python3 -m uvicorn app:app --reload --port 8001
```

Open [http://127.0.0.1:8001](http://127.0.0.1:8001).

- **Aanant** — contest desk (`/camp`): rating target, drills, Codeforces
- **Nikita** — INI-CET desk (`/enter/nikita`): 8-week block, daily MCQs, coach

Contest progress: `data/state.json`. Nikita’s progress: `data/pg.json`.

## Phone (Render)

Same GitHub repo and Render service as before (`AanantJain/riks`). After you push, Render redeploys. The URL stays `https://….onrender.com`. First screen is the chooser.

Keep `RIKS_PASSWORD` set so strangers cannot open either desk.
