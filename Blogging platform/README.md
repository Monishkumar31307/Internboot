# BlogHub - Django Blogging Platform

A complete, production-ready blogging platform built with Django featuring user authentication, role-based access control, rich text editing, and social features.

## Features

### Core Features

- **User Authentication & Roles**
  - Secure registration and login
  - Three user roles: Admin, Author, Reader
  - User profiles with avatars and bios
  - Email-based authentication

- **Blog Post Management**
  - Create, edit, delete, and publish posts
  - Rich text editor (CKEditor) for content
  - Featured images for posts
  - Draft and published status
  - Post categorization and tagging
  - View counting
  - SEO meta fields

- **Reader Engagement**
  - Comment system on posts
  - Like/unlike posts
  - Comment moderation
  - Reply to comments

- **Content Organization**
  - Categorize posts
  - Tag-based filtering
  - Search functionality
  - Pagination

- **Admin Features**
  - Full admin dashboard
  - Manage users and roles
  - Comment moderation
  - Bulk post operations
  - Analytics (view counts)

## Tech Stack

- **Backend:** Django 5.2.10
- **Database:** SQLite (development), PostgreSQL ready (production)
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Rich Text Editor:** CKEditor 6
- **Form Handling:** Django Crispy Forms with Bootstrap 4

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Quick Setup (Windows)

1. **Navigate to project directory:**
   ```bash
   cd "Blogging platform"
   ```

2. **Run setup script:**
   ```bash
   setup.bat
   ```
   This will:
   - Install all dependencies
   - Run database migrations
   - Collect static files
   - Create a superuser account
   - Load sample data

3. **Start the development server:**
   ```bash
   run_server.bat
   ```

4. **Access the application:**
   - Homepage: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

### Manual Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Load sample data:**
   ```bash
   python sample_data.py
   ```

6. **Start server:**
   ```bash
   python manage.py runserver
   ```

## Usage

### For Readers

1. Register a new account at `/accounts/register/`
2. Login at `/accounts/register/`
3. Browse published posts
4. Comment on posts (requires login)
5. Like posts
6. View author profiles
7. Search and filter posts by category/tags

### For Authors

1. Register and request author role from admin
2. Create new posts at `/post/create/`
3. Save drafts and publish when ready
4. Edit and delete own posts
5. View post statistics (views, comments, likes)
6. Manage own profile

### For Administrators

1. Login to admin panel at `/admin/`
2. Manage users and assign roles
3. Moderate comments
4. Manage categories and tags
5. View site statistics
6. Bulk operations on posts

## Project Structure

```
blog_platform/                  # Main project configuration
├── settings.py               # Django settings
├── urls.py                  # Main URL routing
├── wsgi.py                  # WSGI configuration
│
├── accounts/                 # User management app
│   ├── models.py            # User Profile model
│   ├── views.py             # Auth views
│   ├── forms.py             # Registration & profile forms
│   └── urls.py              # Account URLs
│
├── blog/                     # Blog management app
│   ├── models.py            # Post, Category, Tag models
│   ├── views.py             # Blog views (CRUD, filters)
│   ├── forms.py             # Post form
│   └── urls.py              # Blog URLs
│
├── comments/                 # Comment system app
│   ├── models.py            # Comment model
│   ├── views.py             # Comment views
│   ├── forms.py             # Comment form
│   └── urls.py              # Comment URLs
│
├── likes/                    # Like system app
│   ├── models.py            # Like model
│   ├── views.py             # Like views (AJAX)
│   └── urls.py              # Like URLs
│
├── templates/               # HTML templates
│   ├── base.html           # Main template
│   ├── accounts/           # Auth templates
│   ├── blog/               # Blog templates
│   ├── comments/           # Comment templates
│   └── partials/           # Reusable components
│
├── static/                 # Static files (CSS, JS)
├── media/                  # User uploads
└── db.sqlite3             # SQLite database
```

## API Endpoints

### Authentication
- `GET/POST /accounts/register/` - Register new user
- `GET/POST /accounts/login/` - User login
- `GET /accounts/logout/` - User logout
- `GET/POST /accounts/profile/` - Edit profile

### Blog Posts
- `GET /` - Homepage
- `GET /posts/` - All posts (with search/filter)
- `GET /post/<slug>/` - View single post
- `POST /post/create/` - Create new post (authors)
- `POST /post/<slug>/edit/` - Edit post (author/admin)
- `POST /post/<slug>/delete/` - Delete post (author/admin)
- `GET /category/<slug>/` - Posts by category
- `GET /tag/<slug>/` - Posts by tag
- `GET /my-posts/` - Author's published posts
- `GET /drafts/` - Author's draft posts

### Comments
- `POST /comments/add/<post_id>/` - Add comment
- `POST /comments/edit/<comment_id>/` - Edit comment
- `POST /comments/delete/<comment_id>/` - Delete comment

### Likes
- `POST /likes/toggle/<post_id>/` - Like/unlike post (AJAX)
- `GET /likes/my-likes/` - User's liked posts

## Models

### User Profile
```
- user (OneToOne to User)
- role (admin/author/reader)
- bio
- profile_picture
- website, location, phone
- created_at, updated_at
```

### Post
```
- title, slug
- author (ForeignKey to User)
- category (ForeignKey to Category)
- tags (ManyToMany to Tag)
- content (RichText)
- excerpt, featured_image
- status (draft/published/archived)
- view_count
- published_at, created_at, updated_at
```

### Category
```
- name, slug
- description
- created_at
```

### Tag
```
- name, slug
- created_at
```

### Comment
```
- post (ForeignKey to Post)
- author (ForeignKey to User)
- content
- approved (for moderation)
- created_at, updated_at
```

### Like
```
- post (ForeignKey to Post)
- user (ForeignKey to User)
- created_at
- unique_together: (post, user)
```

## Configuration

### Settings.py

Key configurations:
- **DEBUG:** Set to False in production
- **ALLOWED_HOSTS:** Add your domain
- **DATABASES:** PostgreSQL for production
- **MEDIA_FILES:** Upload directory at `/media/`
- **CRISPY_TEMPLATE_PACK:** Bootstrap 4
- **CKEDITOR_CONFIG:** Rich text editor settings

### Environment Variables (for production)

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:password@host/dbname
```

## Common Tasks

### Add Admin User
```bash
python manage.py createsuperuser
```

### Make User an Author
1. Go to Admin Panel
2. Edit user's Profile
3. Change role to "author"

### Create Categories
1. Go to Admin Panel
2. Click "Categories"
3. Add new category

### Create Tags
1. Go to Admin Panel
2. Click "Tags"
3. Add new tags

### Backup Database
```bash
python manage.py dumpdata > backup.json
```

### Restore Database
```bash
python manage.py loaddata backup.json
```

## Troubleshooting

### Issue: Migration errors
**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Static files not loading
**Solution:**
```bash
python manage.py collectstatic --noinput
```

### Issue: CKEditor not working
**Solution:**
- Ensure Pillow is installed: `pip install Pillow`
- Check media directory permissions

### Issue: Port 8000 already in use
**Solution:**
```bash
python manage.py runserver 8001  # Use different port
```

## Performance Optimization

1. **Database Indexes:** Already added on frequently queried fields
2. **Pagination:** 10 posts per page by default
3. **Query Optimization:** Using select_related and prefetch_related
4. **Caching:** Add Django cache framework for production
5. **Static Files:** Use CDN for Bootstrap and Font Awesome

## Security

- **CORS:** Configure for specific domains
- **CSRF Protection:** Enabled by default
- **SQL Injection:** Protected by Django ORM
- **XSS Protection:** Template auto-escaping enabled
- **Password Hashing:** Using PBKDF2 with SHA256
- **Permissions:** Role-based access control

## Deployment

### Deploy to Heroku

1. Add Procfile:
```
web: gunicorn blog_platform.wsgi
```

2. Add runtime.txt:
```
python-3.11.0
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

### Deploy to PythonAnywhere

1. Upload code
2. Create virtual environment
3. Configure web app
4. Install dependencies
5. Run migrations
6. Reload web app

## Future Enhancements

- [ ] Email notifications
- [ ] Social media sharing
- [ ] Advanced analytics dashboard
- [ ] Scheduled posts
- [ ] Post series/collections
- [ ] Reading time estimation
- [ ] User newsletters
- [ ] Advanced search with Elasticsearch
- [ ] API (REST/GraphQL)
- [ ] PWA support

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions:
1. Check existing documentation
2. Search GitHub issues
3. Create a new issue with detailed description

## Credits

- Django Documentation
- Bootstrap 5
- CKEditor
- Font Awesome Icons

---

**Happy Blogging! 🚀**

Built with ❤️ using Django
