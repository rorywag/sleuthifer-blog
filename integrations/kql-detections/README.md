# Rebuild the site when KQL-Detections changes

The site's Detections section is generated from
[rorywag/KQL-Detections](https://github.com/rorywag/KQL-Detections) at build time.
The site only rebuilds when something triggers its deploy workflow, so a new or
edited detection won't show up until the next build.

`trigger-site-rebuild.yml` in this folder fixes that. It's a workflow for the
**KQL-Detections** repo, not this one (GitHub only runs workflows from
`.github/workflows/`, so it's inert here). On every push to KQL-Detections' `main`
branch it sends a `repository_dispatch` event of type `kql-detections-updated` to
`rorywag/sleuthifer-blog`. This repo's `.github/workflows/deploy.yml` listens for
that event and rebuilds the site.

Sending that event needs a token with access to `sleuthifer-blog`. The built-in
`GITHUB_TOKEN` in KQL-Detections can only act on KQL-Detections, so you need a
Personal Access Token (PAT) stored as a secret.

## 1. Create the Personal Access Token

Use a fine-grained token limited to the one repository it needs.

1. On GitHub, click your profile picture, then **Settings**.
2. In the left sidebar, at the bottom, click **Developer settings**.
3. Click **Personal access tokens**, then **Fine-grained tokens**, then **Generate new token**.
4. Fill in the form:
   - **Token name:** `KQL-Detections site rebuild`
   - **Expiration:** pick a date (for example 1 year) and set yourself a reminder to renew it.
   - **Resource owner:** `rorywag`
   - **Repository access:** **Only select repositories**, then choose `rorywag/sleuthifer-blog`.
   - **Permissions**, under **Repository permissions**: set **Contents** to **Read and write**.
     This is the permission GitHub requires to create a `repository_dispatch` event.
     **Metadata: Read-only** is added automatically. Leave everything else as **No access**.
5. Click **Generate token** and copy it. GitHub only shows it once.

## 2. Add the token as a secret in KQL-Detections

1. Go to <https://github.com/rorywag/KQL-Detections>.
2. Click **Settings**, then in the left sidebar **Secrets and variables**, then **Actions**.
3. Click **New repository secret**.
4. **Name:** `SITE_DISPATCH_TOKEN` (the workflow reads exactly this name).
   **Secret:** paste the token.
5. Click **Add secret**.

Never put the token itself in a workflow file, a commit or an issue.

## 3. Add the workflow to KQL-Detections

Copy `trigger-site-rebuild.yml` into the KQL-Detections repo at
`.github/workflows/trigger-site-rebuild.yml` and commit it to `main`.

## 4. Test it

1. In KQL-Detections, open **Actions**, pick **Trigger Sleuthifer site rebuild** and
   click **Run workflow** (or push any change to `main`).
2. In sleuthifer-blog, open **Actions**. A **Deploy site to GitHub Pages** run
   should start, with the event shown as `repository_dispatch`.

`repository_dispatch` only runs workflows from the site repo's default branch, so
this works once the deploy workflow change is merged to `main`.

## Troubleshooting

- **The dispatch step fails with 401 or "Bad credentials":** the token has expired or
  the secret is wrong. Create a new token (step 1) and update the secret (step 2).
- **It fails with 403 or 404:** the token can't reach `sleuthifer-blog`. Check that the
  repository is selected under **Repository access** and **Contents** is **Read and write**.
- **The dispatch succeeds but no deploy starts:** check that the deploy workflow on
  `main` lists `repository_dispatch` with type `kql-detections-updated`.
