# test-cloudrun

Scale-to-zero **test deployment** of the full XAI Demonstrator on a **dedicated
GCP test project** (kept separate from the production project for clean isolation).

- **Backends** run on **Cloud Run** with `min-instances=0` → no compute cost while idle,
  billed only per request-second.
- **Frontends** are served statically from **Firebase Hosting** under
  `https://<PROJECT_ID>.web.app` (free tier, no custom domain / DNS required).
- Deployed by the GitHub Actions workflow
  [`test-deployment-cloudrun.yml`](../../.github/workflows/test-deployment-cloudrun.yml)
  (manual trigger: *workflow_dispatch*).

Covers all four use cases: `sentiment`, `inspection`, `education`
(= visual-inspection in the `digital-education` flavor) and `country`.

> **One rule to remember:** the Cloud Run **region** appears in two places that must
> always match — the `GCP_TESTAPP_REGION` GitHub secret **and** `frontends/firebase.json`
> (the `region` fields). Default is `europe-west3`. If you change it, change it in both.

---

## Prerequisites (once, on your machine)

- [`gcloud` CLI](https://cloud.google.com/sdk/docs/install) installed and logged in:
  `gcloud auth login`
- [`firebase` CLI](https://firebase.google.com/docs/cli) installed:
  `npm install -g firebase-tools` and `firebase login`
- You are **Owner/Billing Admin** on the billing account that should pay for the test project.

> ⚠️ **This whole folder targets its OWN dedicated project — never production.**
> Everything below deploys into `xai-demonstrator-test-app`; the prod project
> `xai-demonstrator-prod` / `www.xaidemo.de` is never touched. (We deliberately do **not**
> reuse the old `xai-demonstrator-test` project — it still holds legacy 2021 services and a
> colleague's work-in-progress and would collide with our service names.)
>
> This is a **permanent, always-reachable** instance (its own `*.web.app` URL, up 24/7).
> "Scale-to-zero" only means it costs ~€0 while idle and spins up on the first request;
> it is not a throwaway. Its purpose vs. prod: it shows **all four** use cases
> (`sentiment`, `inspection`, `education`, `country`), whereas prod only exposes two.

Set these shell variables so you can copy–paste the rest:

```bash
export PROJECT_ID=xai-demonstrator-test-app          # our dedicated project id → URL xai-demonstrator-test-app.web.app
export REGION=europe-west3                  # must match frontends/firebase.json
```

---

## Step 1 — Create the dedicated project and link billing

```bash
# list your billing accounts and copy the id of the one with OPEN = True
gcloud billing accounts list

gcloud projects create "$PROJECT_ID" --name="XAI Demonstrator Test App"
gcloud billing projects link "$PROJECT_ID" --billing-account=XXXXXX-XXXXXX-XXXXXX
gcloud config set project "$PROJECT_ID"
```

> If `xai-demonstrator-test-app` is already taken globally, pick another id and update
> `frontends/.firebaserc` → `"default"` plus the `GCP_TESTAPP_PROJECT_ID` secret to match.

## Step 2 — Enable the required APIs

```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  firebase.googleapis.com \
  firebasehosting.googleapis.com
```

## Step 3 — Create the Artifact Registry repository

(Where the container images are stored inside the test project.)

```bash
gcloud artifacts repositories create xai-demonstrator \
  --repository-format=docker \
  --location="$REGION" \
  --description="XAI Demonstrator test images"
```

## Step 4 — Add Firebase to the project

```bash
firebase projects:addfirebase "$PROJECT_ID"
```

The default Hosting site is created automatically and is named after the project id,
so your site will be reachable at **`https://$PROJECT_ID.web.app`** after the first deploy.
No DNS and no custom domain needed.

## Step 5 — Create the deploy service account + key

```bash
# create the service account
gcloud iam service-accounts create gh-deploy \
  --display-name="GitHub Actions deployer (test)"

SA="gh-deploy@${PROJECT_ID}.iam.gserviceaccount.com"

# grant the roles it needs
for ROLE in \
  roles/run.admin \
  roles/artifactregistry.writer \
  roles/iam.serviceAccountUser \
  roles/firebasehosting.admin ; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA" --role="$ROLE"
done

# create a JSON key (this file becomes the GCP_TESTAPP_SA_KEY secret)
gcloud iam service-accounts keys create gh-deploy-key.json --iam-account="$SA"
```

> `gh-deploy-key.json` is a **secret** — do not commit it. Delete it locally after you
> have pasted its contents into the GitHub secret (Step 7).

## Step 6 — (only for `country`) Google Maps API key

The `country` use case needs a Google Maps / Street View API key. If you already have the
old `STREETVIEW_API_KEY`, reuse it. Otherwise create one in the Google Cloud console
(APIs & Services → Credentials) with the *Street View Static API* enabled, and restrict it.
If you skip this, every use case **except country** still works.

---

## Step 7 — Add the GitHub repository secrets

Repo → *Settings → Secrets and variables → Actions → New repository secret*:

| Secret | Value |
|---|---|
| `GCP_TESTAPP_PROJECT_ID` | your `$PROJECT_ID` |
| `GCP_TESTAPP_REGION` | your `$REGION` (e.g. `europe-west3`) |
| `GCP_TESTAPP_SA_KEY` | the **entire contents** of `gh-deploy-key.json` |
| `STREETVIEW_API_KEY` | Google Maps key (only needed for `country`) |
| `BATCH_SIZE` | *(optional)* street-view images per round, e.g. `16` |

## Step 8 — Run the deployment

GitHub → *Actions → "Test Deployment (Cloud Run)" → Run workflow*.
It builds the five frontends, pushes the four backend images into the test project and
deploys everything. First run takes ~5–8 min.

## Step 9 — Open it

```
https://<PROJECT_ID>.web.app
```

---

## Good to know

- **Cold start:** the first request after an idle period has to load TensorFlow/Torch +
  the model, so expect **~10–30 s** on the first hit; subsequent requests are fast until it
  scales back to zero. If one use case must always be snappy, redeploy that single service
  with `--min-instances 1` (that one then costs a few € per month continuously).
- **Cost while idle:** effectively €0 — Cloud Run bills per request-second, Firebase Hosting
  is static (free tier), only image storage costs a few cents per month.
- **Backend images** come from `ghcr.io/xai-demonstrator/*-service:latest`, built by the
  existing per-service workflows (e.g. the `digital-education-service` image is produced by
  the *Visual Inspection* workflow in the `digital-education` flavor).
- **Isolation:** nothing here touches the production project `xai-demonstrator-prod` or
  `www.xaidemo.de`.
