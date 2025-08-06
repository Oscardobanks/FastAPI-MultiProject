# FastAPI-Based APIs Collection

A comprehensive collection of RESTful APIs built with FastAPI, designed to demonstrate practical backend development patterns and real-world use cases. Each API is self-contained and focuses on specific domain requirements while maintaining consistent coding standards and best practices.

## 🚀 Project Overview

This repository contains five distinct FastAPI applications, each addressing different business domains:

1. **Student Result Management API** - Academic performance tracking
2. **Mini Shopping API with Cart** - E-commerce functionality
3. **Job Application Tracker API** - Recruitment process management
4. **Notes App API** - File-based note management
5. **Simple Contact API** - Contact management system

## 📋 Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- Python-multipart

## 🛠️ Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd fastapi_based_apis
```

2. Install dependencies for any specific API:

```bash
# Example for Student Result Management API
cd student_result_management
pip install -r requirements.txt
```

3. Run the application:

```bash
uvicorn main:app --reload
```

## 📚 API Documentation

### 1. Student Result Management API

**Location:** `student_result_management/`

Manages student academic records with automatic grade calculation.

**Key Features:**

- Student CRUD operations
- Automatic grade computation based on scores
- Persistent storage in JSON format
- Comprehensive error handling

**Endpoints:**

- `POST /students/` - Create new student record
- `GET /students/{name}` - Retrieve specific student
- `GET /students/` - List all students

**Data Model:**

```json
{
  "name": "string",
  "subject_scores": { "subject": "score" },
  "average": 0.0,
  "grade": "string"
}
```

### 2. Mini Shopping API with Cart

**Location:** `mini_shopping_cart/`

Complete shopping experience with product catalog and cart functionality.

**Key Features:**

- Product browsing
- Shopping cart management
- Checkout process
- Persistent cart storage

**Endpoints:**

- `GET /products/` - Browse available products
- `POST /cart/add?product_id=1&qty=2` - Add items to cart
- `GET /cart/checkout` - Process checkout

**Data Model:**

```json
{
  "id": 1,
  "name": "string",
  "price": 0.0
}
```

### 3. Job Application Tracker API

**Location:** `job_application_tracker/`

Track and manage job applications throughout the recruitment process.

**Key Features:**

- Application lifecycle management
- Status tracking
- Search and filtering capabilities
- Modular file handling

**Endpoints:**

- `POST /applications/` - Create new application
- `GET /applications/` - List all applications
- `GET /applications/search?status=pending` - Filter by status

**Data Model:**

```json
{
  "name": "string",
  "company": "string",
  "position": "string",
  "status": "pending|interview|rejected|accepted"
}
```

### 4. Notes App API

**Location:** `notes_app/`

File-based note management system with CRUD operations.

**Key Features:**

- Individual note files (.txt)
- File system operations
- Note persistence
- Git branch-based development

**Endpoints:**

- `POST /notes/` - Create new note
- `GET /notes/{title}` - Retrieve specific note
- `PUT /notes/{title}` - Update existing note
- `DELETE /notes/{title}` - Delete note

### 5. Simple Contact API

**Location:** `contact_management_system/`

Basic contact management with path and query parameter usage.

**Key Features:**

- Contact CRUD operations
- Search functionality
- In-memory storage with dictionary
- Input validation and error handling

**Endpoints:**

- `POST /contacts/` - Create contact
- `GET /contacts/?name=John` - Search contacts
- `PUT /contacts/{name}` - Update contact
- `DELETE /contacts/{name}` - Delete contact

**Data Model:**

```json
{
  "name": "string",
  "phone": "string",
  "email": "string"
}
```

## 🔧 Development Guidelines

### Git Best Practices

- Use descriptive commit messages
- Create feature branches for new functionality
- Follow conventional commit format
- Regular commits with meaningful messages

### Error Handling

All APIs implement comprehensive error handling using try-except blocks:

- Input validation errors
- File I/O errors
- JSON parsing errors
- Resource not found scenarios

### Code Structure

Each API follows a consistent structure:

```
api-name/
├── main.py          # FastAPI application entry point
├── requirements.txt  # Python dependencies
├── models.py       # Pydantic models (if applicable)
├── handlers/       # Business logic modules
└── data/          # JSON storage files
```

## 🧪 Testing

Each API can be tested using:

- **Swagger UI:** Access `/docs` endpoint when running
- **Postman:** Import OpenAPI specification
- **curl:** Direct HTTP requests

Example test for Student API:

```bash
curl -X POST "http://localhost:8000/students/" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "subject_scores": {"Math": 85, "Science": 90}}'
```

## 📊 Data Persistence

All APIs use JSON files for data storage:

- `students.json` - Student records
- `products.json` - Product catalog
- `applications.json` - Job applications
- Individual `.txt` files for notes
- In-memory dictionary for contacts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For questions or support, please open an issue in the GitHub repository or contact the development team.

---

**Note:** Each API is designed to be run independently. Navigate to the specific API directory and follow the individual setup instructions for that service.
