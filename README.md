# RIKS Contest (OpenCamp)

Same governance as board-exam RIKS, for competitive programming:

- a **rating target** and a **contest date**
- strong / needs work / **conscious skip**
- a **schedule** for the remaining days
- a **daily bot**: minimum set before sleep, impact of skipping yesterday
- **periodic** = sit a public Codeforces/AtCoder round and upsolve
- a **coach desk** (what to help with — not generic gyan)

Problems and articles are only free public pages (CSES, USACO Guide, CP-Algorithms, Codeforces, AtCoder).

## Run

```bash
cd ~/work/opencamp
python3 -m pip install --user -r requirements.txt
python3 -m uvicorn app:app --reload --port 8001
```

Open [http://127.0.0.1:8001](http://127.0.0.1:8001). Board-exam RIKS stays on port 8000.

Progress is stored in `data/state.json`.

## Phone (not this computer)

Put the app on a free host so Aanant opens a link in Safari/Chrome. This PC can stay off.

1. Create a GitHub account and a **Render** account (https://render.com) — both free.
2. Put this folder on GitHub, then in Render: **New → Web Service → connect that repo**.
3. Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Environment variables (optional but recommended):
   - `RIKS_HANDLE=Aanant`
   - `RIKS_PASSWORD=` a family password (he types it once on the phone)
5. After deploy, text him the `https://….onrender.com` URL. On iPhone: Share → **Add to Home Screen**.

Free Render apps sleep when idle; the first open after a while can take ~30 seconds. Progress on the free plan can reset if the server is rebuilt — fine for trying; add a disk later if you want it to last.
