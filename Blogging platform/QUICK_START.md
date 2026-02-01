# Quick Start Guide - BlogHub

Get your blogging platform up and running in 5 minutes!

## 5-Minute Setup

### Windows Users

1. **Open Command Prompt** and navigate to the project:
   ```bash
   cd "C:\Users\YourUsername\Downloads\internboot\Blogging platform"
   ```

2. **Run setup:**
   ```bash
   setup.bat
   ```
   > Takes 2-3 minutes. Follow prompts to create admin account.

3. **Start server:**
   ```bash
   run_server.bat
   ```

4. **Open browser:**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

### Linux/Mac Users

1. **Navigate to project:**
   ```bash
   cd ~/Downloads/internboot/Blogging\ platform
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install and setup:**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python sample_data.py
   ```

4. **Start server:**
   ```bash
   python manage.py runserver
   ```

5. **Visit:**
   - http://localhost:8000

---

## Test the Platform

### Login Credentials (from sample data)

**Admin Account:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@example.com`

**Author Accounts:**
- `author1` / `pass123`
- `author2` / `pass123`
- `author3` / `pass123`

**Reader Accounts:**
- `reader1` / `pass123`
- `reader2` / `pass123`
- `reader3` / `pass123`

### Test as Reader

1. Login with `reader1` / `pass123`
2. Browse posts on homepage
3. Click "Read More" on any post
4. Add a comment
5. Like the post
6. View author profile

### Test as Author

1. Login with `author1` / `pass123`
2. Click "Write" → "New Post"
3. Create a post with:
   - Title
   - Category
   - Content (use the rich editor)
   - Featured image
4. Save as draft or publish
5. View "My Posts" and "Drafts"
6. Edit and delete posts

### Test as Admin

1. Login with `admin` / `admin123`
2. Click "Admin Panel" (appears in profile menu)
3. Manage:
   - Users (change roles)
   - Posts (edit/delete all)
   - Comments (approve/reject)
   - Categories and Tags

---

## Project Urls

| Page | URL |
|------|-----|
| Homepage | / |
| All Posts | /posts/ |
| Post Detail | /post/\<slug\>/ |
| Create Post | /post/create/ |
| My Posts | /my-posts/ |
| Drafts | /drafts/ |
| Categories | /category/\<slug\>/ |
| Tags | /tag/\<slug\>/ |
| Login | /accounts/login/ |
| Register | /accounts/register/ |
| Profile | /accounts/profile/ |
| Admin | /admin/ |

---

## Key Features to Try

✅ **User Registration** - Create new account with email validation  
✅ **Role-Based Access** - Different permissions for admin/author/reader  
✅ **Post Creation** - Use CKEditor for rich content  
✅ **Categorization** - Filter posts by category  
✅ **Tagging** - Find posts by tags  
✅ **Comments** - Discuss posts  
✅ **Likes** - Like posts  
✅ **Search** - Find posts by keyword  
✅ **Pagination** - Navigate through posts  
✅ **Admin Panel** - Full management interface  

---

## Troubleshooting

### Port 8000 in use?
```bash
python manage.py runserver 8001
```

### Database errors?
```bash
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

### Static files not loading?
```bash
python manage.py collectstatic --noinput
```

### Need to reset everything?
```bash
del db.sqlite3
python manage.py migrate
python sample_data.py
```

---

## Next Steps

1. ✅ Run the app
2. ✅ Test all features
3. ✅ Create your own posts
4. ✅ Check admin panel
5. ✅ Customize colors/styling
6. ✅ Read full README.md for advanced features

---

## Support

- Full docs: See `README.md`
- Django docs: https://docs.djangoproject.com/
- CKEditor: https://ckeditor.com/
- Bootstrap: https://getbootstrap.com/

**Enjoy your blogging platform! 🎉**
