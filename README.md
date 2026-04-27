# Prime Choice Kids Care School Website

A fully admin-controlled Django website for Prime Choice Kids Care school. All content is managed through Django Admin - no code editing needed.

## Features

- **Admin-Controlled Content**: Manage all website content from Django Admin portal
- **PostgreSQL Support**: Configure PostgreSQL database for Vercel deployment directly from admin
- **Staff Management**: Upload and manage staff member profiles with photos and bios
- **Programs**: Display school programs (Crèche, Preschool, Lower Primary)
- **News & Events**: Create and publish news articles and events with dates and details
- **Contact Management**: Manage contact messages and automated replies
- **Social Media**: Configure 8 social media platforms (Facebook, Instagram, YouTube, TikTok, LinkedIn, Twitter, Pinterest, WhatsApp)
- **Email Configuration**: Set SMTP settings from admin portal
- **Analytics**: Track clicks on CTAs, calls, WhatsApp messages, and more
- **Responsive Design**: Mobile-friendly design that works on all devices

## Project Structure

```
primechoice_school/
├── core/                      # Main app
│   ├── models.py             # Database models
│   ├── views.py              # Views and logic
│   ├── admin.py              # Admin configuration
│   ├── templates/            # HTML templates
│   └── static/               # CSS, JS, images
├── school_site/              # Project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI config for Vercel
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── vercel.json              # Vercel deployment config
```

## Installation & Local Development

### Prerequisites
- Python 3.10+
- pip
- Virtual environment

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/primechoice.git
   cd primechoice
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin login

6. **Run development server**
   ```bash
   python manage.py runserver
   ```
   Visit: http://localhost:8000

7. **Access Admin Panel**
   Visit: http://localhost:8000/admin
   Login with your superuser credentials

## Managing Content

### Adding School Information
1. Go to Django Admin → Site Settings
2. Edit school name, logo, tagline, contact info, etc.
3. Save changes

### Adding Staff Members
1. Go to Django Admin → Staff Members
2. Click "Add Staff Member"
3. Fill in name, role, bio, and upload photo
4. Set order (lower numbers appear first)
5. Check "Is Active" to display on website
6. Save

### Adding Testimonials
1. Go to Django Admin → Testimonials
2. Click "Add Testimonial"
3. Fill in name, role, quote, and upload avatar
4. Set order
5. Check "Is Active"
6. Save

### Configuring Social Media
1. Go to Django Admin → Site Settings
2. Scroll to social media section
3. Enter URLs for Facebook, Instagram, YouTube, TikTok, LinkedIn, Twitter, Pinterest, WhatsApp
4. Save

### Configuring Email (SMTP)
1. Go to Django Admin → Site Settings
2. Scroll to SMTP Configuration section
3. Enter your email provider settings:
   - **SMTP Host**: Your email provider's SMTP server (e.g., smtp.gmail.com)
   - **SMTP Port**: Usually 587 or 465
   - **SMTP Username**: Your email address
   - **SMTP Password**: Your app-specific password
   - **From Email**: The email address to send from
4. Save

### Configuring Database (PostgreSQL for Vercel)
1. Go to Django Admin → Site Settings
2. Scroll to "Database Configuration" section
3. Select **PostgreSQL** from DB Engine dropdown
4. Fill in:
   - **DB Host**: Your Vercel PostgreSQL host
   - **DB Port**: Usually 5432
   - **DB Name**: Your database name
   - **DB User**: Database username
   - **DB Password**: Database password
5. Save
6. **IMPORTANT**: Restart the application for database changes to take effect

## Deployment to Vercel

See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions on:
1. Setting up GitHub repository
2. Configuring PostgreSQL on Vercel
3. Deploying the application
4. Setting environment variables
5. Managing static files

## Environment Variables

For production deployment, set these environment variables in Vercel:

```
DEBUG=False
SECRET_KEY=your-secure-random-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/database
```

## Static Files & Media

- **Static Files**: CSS, JS, images (served by Vercel)
- **Media Files**: User uploads (staff photos, testimonials, gallery images)
  - In development: Stored locally in `/media/` folder
  - In production (Vercel): Configure blob storage or external storage

## Support & Documentation

- **Django Documentation**: https://docs.djangoproject.com/
- **Vercel Docs**: https://vercel.com/docs
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

## Security Notes

- Never commit `.env` files or database passwords to GitHub
- Use strong SECRET_KEY in production
- Keep Django updated for security patches
- Use HTTPS in production (Vercel handles this automatically)

## License

This project is proprietary to Prime Choice Kids Care.
