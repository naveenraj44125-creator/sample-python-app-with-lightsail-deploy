# 📋 Action Items Tracker

A Python Flask web application for tracking action items for employees under managers. Automatically deployed to AWS Lightsail using GitHub Actions.

## 🚀 Features

- **Manager Management**: Add and manage managers
- **Employee Management**: Add employees and assign them to managers
- **Action Items Tracking**: Create, update, and track action items
- **Status Management**: Track items through pending → in progress → completed
- **Priority Levels**: High, medium, and low priority assignments
- **Dashboard**: Overview of all managers, employees, and action items
- **Filtering**: Filter action items by status and priority
- **Due Dates**: Set and track due dates for action items

## 🛠️ Technology Stack

- **Backend**: Python 3.9 + Flask
- **Database**: SQLite
- **Web Server**: Gunicorn + Nginx
- **Deployment**: GitHub Actions + AWS Lightsail
- **Infrastructure**: Automated deployment with reusable workflows

## 📦 Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/naveenraj44125-creator/sample-python-app-lightsail-deploy.git
cd sample-python-app-lightsail-deploy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and visit: `http://localhost:8000`

## 🌐 Deployment

This application is automatically deployed to AWS Lightsail when you push to the `main` branch.

### Deployment Configuration

- **Instance**: sample-python-app
- **Static IP**: 23.20.95.172
- **Region**: us-east-1
- **Dependencies**: Python, Nginx, MySQL, Redis, Docker, Git, Firewall

### Deployment Process

1. Push changes to `main` branch
2. GitHub Actions workflow triggers automatically
3. Application is built and packaged
4. Deployed to Lightsail instance
5. Services are restarted
6. Health checks verify deployment

## 📊 Application Structure

```
sample-python-app-lightsail-deploy/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Dashboard
│   ├── managers.html              # Managers list
│   ├── add_manager.html           # Add manager form
│   ├── manager_detail.html        # Manager details
│   ├── employees.html             # Employees list
│   ├── add_employee.html          # Add employee form
│   ├── employee_detail.html       # Employee details
│   ├── actions.html               # Action items list
│   └── add_action.html            # Add action item form
├── deployment-generic.config.yml  # Deployment configuration
└── .github/workflows/deploy.yml   # GitHub Actions workflow
```

## 🔧 API Endpoints

- `GET /` - Dashboard
- `GET /managers` - List all managers
- `POST /managers/add` - Add new manager
- `GET /managers/<id>` - Manager details
- `GET /employees` - List all employees
- `POST /employees/add` - Add new employee
- `GET /employees/<id>` - Employee details
- `GET /actions` - List all action items
- `POST /actions/add` - Add new action item
- `POST /actions/<id>/update` - Update action item status
- `POST /actions/<id>/delete` - Delete action item
- `GET /api/stats` - Get statistics (JSON)
- `GET /health` - Health check endpoint

## 📝 Usage

### Adding a Manager

1. Navigate to "Managers" tab
2. Click "Add Manager"
3. Enter name and email
4. Click "Add Manager"

### Adding an Employee

1. Navigate to "Employees" tab
2. Click "Add Employee"
3. Enter name, email, select manager, and position
4. Click "Add Employee"

### Creating an Action Item

1. Navigate to "Action Items" tab
2. Click "Add Action Item"
3. Enter title, description, assign to employee
4. Set priority and due date
5. Click "Add Action Item"

### Managing Action Items

- **Start**: Change status from pending to in progress
- **Complete**: Mark action item as completed
- **Reopen**: Change completed item back to pending
- **Delete**: Remove action item permanently

## 🔐 Environment Variables

- `PORT`: Application port (default: 8000)
- `SECRET_KEY`: Flask secret key for sessions

## 📈 Monitoring

- **Health Check**: `http://23.20.95.172/health`
- **API Stats**: `http://23.20.95.172/api/stats`
- **GitHub Actions**: [View Workflows](https://github.com/naveenraj44125-creator/sample-python-app-lightsail-deploy/actions)

## 🚦 Status

- **Application**: http://23.20.95.172
- **Deployment**: Automated via GitHub Actions
- **Instance**: AWS Lightsail (us-east-1)

## 📄 License

MIT License

## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 🆘 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/naveenraj44125-creator/sample-python-app-lightsail-deploy/issues)
- Deployment Logs: Check GitHub Actions workflow runs

---

**Deployed with ❤️ using GitHub Actions and AWS Lightsail**
