# 🛡️ Scam Reports API

> A Django REST Framework-based community platform for reporting and tracking scam incidents. Empowering users to share experiences, provide supporting evidence, and build a safer digital community through collective awareness.

## ✨ Features

- 🚨 **Scam Reporting**: Submit detailed reports about scammers with location data
- 🤝 **Community Support**: Users can add supporting evidence to existing reports  
- 👎 **Voting System**: Downvote functionality to help filter content
- 🔐 **User Authentication**: Token-based authentication for secure API access
- 🌍 **Global/Local Reports**: Support for both location-specific and global scam reports
- 📄 **Pagination**: Efficient data loading with paginated responses
- 🔍 **REST API**: Full CRUD operations with proper HTTP status codes
- 📱 **Mobile Ready**: JSON API suitable for web and mobile applications

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [API Endpoints](#-api-endpoints)
- [Models](#-models)
- [Authentication](#-authentication)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Django 4.0+
- Django REST Framework
- django-countries

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/scam-reports-api.git
   cd scam-reports-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # OR install manually:
   pip install django djangorestframework django-countries
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

## 🔗 API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/account/register/` | Register new user |
| POST | `/account/login/` | Login user |
| POST | `/account/logout/` | Logout user |

### Scam Reports Endpoints
| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/reports/list/` | List all scam posts (paginated) | Optional |
| POST | `/reports/list/` | Create new scam report | Required |
| GET | `/reports/<id>/` | Get specific scam report details | Optional |
| PUT | `/reports/<id>/` | Update scam report | Required |
| DELETE | `/reports/<id>/` | Delete scam report | Required |

### Support Posts Endpoints
| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/reports/supports/` | List all support posts | Optional |
| POST | `/reports/<id>/support-create/` | Add support to specific report | Required |
| GET | `/reports/<id>/supports/` | Get support details | Optional |
| PUT | `/reports/<id>/supports/` | Update support post | Required |
| DELETE | `/reports/<id>/supports/` | Delete support post | Required |

### Voting Endpoints
| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/reports/<id>/downvote/` | Toggle downvote on report | Required |

## 📊 Models

### ScamPost
- `scammer_name`: Name of the reported scammer
- `socials`: JSON field for social media profiles
- `incidence_description`: Detailed description of the scam
- `country`: Country where scam occurred (using django-countries)
- `isglobal`: Boolean flag for global scams
- `evidence_drive_link`: Optional URL to evidence files
- `created_at`: Timestamp of report creation

### SupportPost
- `supporter`: User who created the support post
- `description`: Supporting evidence description (min 50 characters)
- `evidence_link`: URL to supporting evidence
- `scampost`: Foreign key to associated ScamPost
- `created_at`: Timestamp of support creation

### Downvote
- `user`: User who downvoted
- `post`: ScamPost being downvoted
- `created_at`: Timestamp of downvote
- Unique constraint on (user, post) to prevent duplicate votes

## 🔐 Authentication

The API uses Django REST Framework's token authentication:

1. **Register**: Create account and receive auth token
2. **Login**: Get auth token for existing users
3. **Logout**: Delete auth token

Include the token in request headers:
```
Authorization: Token <your-token-here>
```

## 💻 Usage Examples

### Register a new user
```bash
curl -X POST http://localhost:8000/account/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Create a scam report
```bash
curl -X POST http://localhost:8000/reports/list/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <your-token>" \
  -d '{
    "scammer_name": "John Doe",
    "incidence_description": "Fake investment scheme promising 100% returns",
    "country": "US",
    "isglobal": false
  }'
```

### Add support to a report
```bash
curl -X POST http://localhost:8000/reports/1/support-create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <your-token>" \
  -d '{
    "description": "I also fell victim to this scammer. They used the same tactics and promised similar returns.",
    "evidence_link": "https://example.com/evidence"
  }'
```

### Toggle downvote on a report
```bash
curl -X POST http://localhost:8000/reports/1/downvote/ \
  -H "Authorization: Token <your-token>"
```

## 📁 Project Structure

```
scam_reports_project/
├── reports_app/
│   ├── api/
│   │   ├── serializers.py      # Data serialization
│   │   ├── views.py           # API view logic
│   │   ├── permissions.py     # Custom permissions
│   │   ├── pagination.py      # Pagination settings
│   │   └── urls.py           # API URL routing
│   ├── models.py             # Database models
│   └── admin.py              # Admin interface
├── user_app/
│   └── api/
│       ├── views.py          # Authentication views
│       ├── serializer.py     # User serialization
│       └── urls.py          # Auth URL routing
└── manage.py
```

## 📝 Additional Notes

<details>
<summary>🔧 Technical Details</summary>

- Uses Django Countries for standardized location data
- JSON fields store social media profile information  
- Token-based authentication provides stateless API access
- Proper HTTP status codes and error handling
- Custom pagination for optimal performance
- Foreign key relationships with proper cascade handling

</details>

<details>
<summary>⚠️ Known Issues</summary>

1. Missing error handling in some PUT/DELETE operations  
2. `startsWith` should be `startswith` in URL validation (Python syntax)
3. Some serializer validation methods need proper indentation
4. Consider adding request rate limiting for production

</details>

<details>
<summary>🚀 Roadmap</summary>

- [ ] Image upload support for evidence files
- [ ] Real-time notifications for new reports  
- [ ] Advanced search and filtering capabilities
- [ ] Report categorization system
- [ ] User reputation and credibility scoring
- [ ] API rate limiting and throttling
- [ ] Email verification for user registration
- [ ] Export functionality for reports
- [ ] Admin dashboard with analytics
- [ ] Mobile app integration

</details>

## 🤝 Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add: amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python manage.py test

# Check code style
flake8 .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django REST Framework for the excellent API framework
- Django Countries for location data handling  
- The open-source community for inspiration and tools

## 📞 Support

If you have any questions or run into issues:

- 📝 [Open an issue](https://github.com/yourusername/scam-reports-api/issues)
- 📧 Email: your.email@example.com
- 💬 [Discussions](https://github.com/yourusername/scam-reports-api/discussions)

---

<div align="center">

**⭐ Star this repository if it helped you! ⭐**

Made with ❤️ by [Your Name](https://github.com/yourusername)

[Report Bug](https://github.com/yourusername/scam-reports-api/issues) · [Request Feature](https://github.com/yourusername/scam-reports-api/issues) · [Documentation](https://github.com/yourusername/scam-reports-api/wiki)

</div>