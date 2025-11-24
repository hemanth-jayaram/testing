# Member 3: Frontend & Web Development

## Role: User Interface & Web Application

### Your Responsibilities
- Develop Flask web application
- Create HTML/CSS/JavaScript frontend
- Implement API endpoints
- Design user interface

### Your Files
1. **app.py** - Flask application with routes and APIs
2. **config.py** - Application configuration
3. **templates/** - All HTML templates
   - base.html - Base template with navigation
   - home.html - Dashboard/home page
   - upload.html - Dataset upload interface
   - train.html - Training interface with real-time monitoring
   - models.html - Model version management
   - classify.html - Email classification interface
4. **static/** - CSS and JavaScript
   - style.css - Custom styling
   - app.js - Frontend JavaScript logic

### Git Branch
```bash
git checkout -b feature/web-interface
```

### Key Tasks
1. Create Flask routes and API endpoints in app.py
2. Design responsive HTML templates
3. Implement real-time training monitoring UI
4. Add file upload interface
5. Create email classification form
6. Style with Bootstrap 5 and custom CSS
7. Add JavaScript for dynamic updates

### Testing
```bash
# Test Flask app
python app.py

# Access in browser
# http://localhost:5000
```

### API Endpoints to Implement
- `POST /api/train` - Start training
- `GET /api/training_status` - Get training progress
- `POST /api/classify` - Classify email
- `GET /api/stats` - Get system statistics
- `GET /api/download_model/<version>` - Download model

### Integration Points
- **With Member 1**: Training API, prediction API
- **With Member 2**: File upload to S3, environment config
- **With Member 4**: Sample data integration, documentation

### Commit Examples
```bash
git add app.py config.py
git commit -m "feat(web): Add Flask application and routes"

git add templates/
git commit -m "feat(ui): Create HTML templates"

git add static/
git commit -m "feat(ui): Add CSS and JavaScript"
```
