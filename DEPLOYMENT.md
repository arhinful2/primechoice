# Deployment Guide: GitHub + Vercel

This guide walks you through deploying Prime Choice Kids Care website to Vercel with PostgreSQL database.

## 📋 Pre-Deployment Checklist

Before pushing to GitHub and deploying to Vercel, verify:

- [ ] All admin content is properly configured (school info, programs, staff, etc.)
- [ ] Database configuration is set in SiteSettings admin
- [ ] Email SMTP settings are configured in admin
- [ ] All images and media files are uploaded to admin
- [ ] Static files are in place (`/core/static/`)
- [ ] `.gitignore` exists and configured
- [ ] `requirements.txt` is up-to-date
- [ ] `SECRET_KEY` is changed from default
- [ ] No `.env` file committed to Git
- [ ] `DEBUG = False` will be set in Vercel

---

## Step 1: Create GitHub Repository

### 1.1 Create repo on GitHub

1. Go to [github.com](https://github.com) and log in
2. Click **+ New** (or go to https://github.com/new)
3. Repository name: `primechoice`
4. Description: `Prime Choice Kids Care School Website`
5. Choose **Private** (if you want to keep it private)
6. **DO NOT** initialize with README/gitignore/license (we already have these)
7. Click **Create repository**

### 1.2 Connect your local project to GitHub

Open terminal in your project folder and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Prime Choice Kids Care website"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/primechoice.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME`** with your actual GitHub username.

### 1.3 Verify on GitHub

Go to https://github.com/YOUR_USERNAME/primechoice and confirm all files are uploaded.

---

## Step 2: Create PostgreSQL Database on Vercel

### 2.1 Create Vercel Account (if needed)

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub account (recommended - easier integration)
3. Authorize Vercel to access your GitHub account

### 2.2 Create PostgreSQL Database

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Storage** → **Create** → **Postgres**
3. Choose a project name or create new project: `primechoice`
4. Select region closest to you
5. Click **Create**
6. Wait for database to be created (2-3 minutes)
7. You'll see connection details:
   - **Host**
   - **Database**
   - **Username**
   - **Password**
   - **Connection string**

### 2.3 Save Database Credentials

Copy these values - you'll need them in admin portal:
- Database Host (e.g., `ep-xxxxx.us-east-1.postgres.vercel-storage.com`)
- Database Name
- Database User
- Database Password
- Database Port (usually `5432`)

---

## Step 3: Configure Database in Admin Portal

**IMPORTANT**: Do this BEFORE deploying to Vercel!

### 3.1 Add Database Config to Admin

1. Run locally: `python manage.py runserver`
2. Go to http://localhost:8000/admin
3. Click **Site Settings**
4. Scroll to **Database Configuration** section
5. Fill in:
   - **DB Engine**: Select `PostgreSQL`
   - **DB Host**: Paste your Vercel database host
   - **DB Port**: `5432`
   - **DB Name**: Your database name from Vercel
   - **DB User**: Your database username from Vercel
   - **DB Password**: Your database password from Vercel
6. Click **Save**

### 3.2 Test Database Connection

1. In terminal, run:
   ```bash
   python manage.py migrate
   ```
2. If successful, your database is configured correctly
3. If error, double-check credentials in admin

---

## Step 4: Create Environment Variables File

### 4.1 Create `.env` file (LOCAL ONLY - DO NOT PUSH TO GITHUB)

Create a file called `.env` in your project root:

```bash
# .env file - NEVER commit this to GitHub
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-here-use-at-least-50-characters
ALLOWED_HOSTS=yourdomain.vercel.app,primechoice.vercel.app,localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@host:5432/database
DJANGO_SETTINGS_MODULE=school_site.settings
```

### 4.2 Generate a Strong SECRET_KEY

Run in Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the output and use it for `SECRET_KEY` in `.env`

### 4.3 Test Locally

1. Verify `.env` is in `.gitignore` (it should be)
2. Run: `python manage.py check`
3. Should show: `System check identified no issues`

---

## Step 5: Update Database Configuration in Code

Update `school_site/settings.py` to read PostgreSQL connection from environment:

```python
import dj_database_url
import os

# If DATABASE_URL environment variable is set (Vercel), use it
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Otherwise use SiteSettings config or SQLite fallback
    DATABASES = get_db_config()
```

---

## Step 6: Create Vercel Configuration

### 6.1 Update `vercel.json`

Ensure you have `vercel.json` in project root with:

```json
{
  "buildCommand": "pip install -r requirements.txt && python manage.py collectstatic --noinput",
  "outputDirectory": "staticfiles",
  "framework": "django",
  "env": {
    "PYTHONUNBUFFERED": "1"
  },
  "rewrites": [
    {
      "source": "/static/(.*)",
      "destination": "/static/$1"
    },
    {
      "source": "/media/(.*)",
      "destination": "/media/$1"
    },
    {
      "source": "/(.*)",
      "destination": "/index"
    }
  ]
}
```

---

## Step 7: Deploy to Vercel

### 7.1 Connect GitHub Repository to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Add New...** → **Project**
3. Select **Import Git Repository**
4. Search for `primechoice` repository
5. Click **Import**
6. Configure project:
   - **Framework Preset**: Django
   - **Root Directory**: `.` (current)
   - **Environment Variables**: Add these:
     ```
     DEBUG=False
     SECRET_KEY=[paste your generated key]
     ALLOWED_HOSTS=yourdomain.vercel.app,primechoice.vercel.app
     ```
7. Click **Deploy**

### 7.2 Wait for Deployment

- Vercel will build and deploy your app (3-5 minutes)
- You'll see a URL like: `https://primechoice-xyz.vercel.app`
- Watch the build logs for any errors

### 7.3 Verify Deployment

1. Visit your deployment URL
2. Check if homepage loads correctly
3. Go to `/admin` to access Django admin
4. Log in with your superuser credentials

---

## Step 8: Run Migrations on Vercel

After deployment, run migrations on the live PostgreSQL database:

### 8.1 Using Vercel CLI

```bash
# Install Vercel CLI (if not already)
npm install -g vercel

# Run migrations
vercel env pull  # Pull environment variables
python manage.py migrate --database=production
```

### 8.2 Using Vercel Postgres Console

1. Go to Vercel Dashboard
2. Click your project → **Storage** → **Postgres**
3. Click **Data** or **Query** to run SQL directly
4. Or use the connection string to connect with a database tool

---

## Step 9: Configure Custom Domain (Optional)

### 9.1 Add Domain to Vercel

1. Go to Vercel Dashboard → Your Project → **Settings** → **Domains**
2. Enter your domain (e.g., `primechoicekidscare.com`)
3. Follow DNS configuration instructions
4. Wait 24-48 hours for DNS to propagate

### 9.2 Update ALLOWED_HOSTS

1. Go to Vercel Dashboard → **Settings** → **Environment Variables**
2. Update `ALLOWED_HOSTS`:
   ```
   ALLOWED_HOSTS=primechoicekidscare.com,www.primechoicekidscare.com,primechoice-xyz.vercel.app
   ```
3. Redeploy the app

---

## Step 10: Managing Static Files & Media on Vercel

### Option A: Vercel Blob Storage (Recommended for media uploads)

```bash
pip install vercel-blob
```

Configure in `settings.py`:
```python
if os.getenv('VERCEL'):
    DEFAULT_FILE_STORAGE = 'django_storages.backends.azure_storage.AzureStorage'
    STATIC_URL = '/static/'
```

### Option B: Local Static Files

Static files are automatically collected and served by Vercel.

### Option C: Third-Party Storage (AWS S3, Google Cloud Storage)

Use Django Storages with AWS S3 or Google Cloud Storage for media uploads.

---

## Troubleshooting

### Issue: "ModuleNotFoundError" after deployment

**Solution**: Check `requirements.txt` includes all packages. Run:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Issue: Static files not loading (404 errors)

**Solution**:
1. Verify `STATIC_URL` and `STATICFILES_DIRS` in settings.py
2. Run: `python manage.py collectstatic --noinput`
3. Check Vercel build logs for errors

### Issue: Database connection error

**Solution**:
1. Verify PostgreSQL credentials in environment variables
2. Check database is running on Vercel
3. Test connection with: `python manage.py dbshell`

### Issue: Admin panel shows 500 error

**Solution**:
1. Check Vercel logs: Dashboard → Project → **Deployments** → **View Logs**
2. Verify SECRET_KEY is set
3. Verify DEBUG=False doesn't hide errors during testing

### Issue: Email not sending

**Solution**:
1. Configure SMTP in admin Site Settings
2. Check firewall allows port 587 or 465
3. Verify "Less secure app access" is enabled (for Gmail)

---

## Next Steps

1. ✅ GitHub repository set up
2. ✅ PostgreSQL database configured
3. ✅ Code deployed to Vercel
4. ✅ Admin panel accessible
5. 📊 Set up analytics/monitoring
6. 🔒 Enable HTTPS (Vercel does this automatically)
7. 📧 Test email notifications
8. 🎨 Customize domain name

---

## Quick Reference Commands

```bash
# Test deployment locally before pushing
python manage.py runserver

# Generate new SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Update requirements after installing new packages
pip freeze > requirements.txt

# Push changes to GitHub
git add .
git commit -m "Your message"
git push

# Check Vercel deployment status
vercel status

# View Vercel logs
vercel logs
```

---

## Support

For issues or questions:
- Check Django documentation: https://docs.djangoproject.com/
- Check Vercel documentation: https://vercel.com/docs
- Check PostgreSQL documentation: https://www.postgresql.org/docs/

Good luck! 🚀
