# 🎓 Uni-Connect

## Lost & Found + Notes Exchange System

A comprehensive Streamlit-based campus utility platform that helps students report and recover lost items while facilitating academic notes sharing. Built using **in-memory Python data structures** (lists & dictionaries) without external databases.

---

## 🎯 Project Goal

To create a beginner-friendly, real-world campus management system that:
- Helps students report lost items and find their belongings
- Enables peer-to-peer academic notes sharing
- Demonstrates clean software architecture
- Uses only Python data structures (no external database)
- Provides an attractive, modern user interface

---

## ✨ Features

### 🔍 Lost & Found System
- **Report Lost Items**: Submit details about items you've lost
- **Report Found Items**: Help others by reporting items you've found
- **Smart Matching**: Automatic matching based on category and location
- **Search & Filter**: Find items by name, category, or location
- **Claim System**: Verify and claim your lost items
- **Real-time Updates**: Instant synchronization across the platform

### 📚 Notes Exchange System
- **Upload Notes**: Share your academic notes with peers
- **Browse by Subject**: Organized by subjects and semesters
- **Popular Notes**: Discover trending and most downloaded notes
- **Search Functionality**: Find notes by subject, topic, or contributor
- **Download Tracking**: Monitor how many times notes are downloaded
- **Contributor Leaderboard**: Recognize top contributors with rankings

### 📊 Analytics Dashboard
- **Visual Statistics**: Interactive charts using Plotly
- **Category Distribution**: See what types of items are reported most
- **Location Heatmap**: Identify common locations for lost items
- **Subject-wise Stats**: Track notes uploads and downloads by subject
- **User Activity**: Monitor platform engagement

---

## 📂 Project Structure

```
campus_exchange_hub/
│
├── app.py                          # Main Streamlit entry point
│
├── database/                       # In-memory data storage
│   ├── __init__.py                # Database package initialization
│   ├── lost_found_db.py           # Lost & Found data (list of dicts)
│   ├── notes_db.py                # Notes data (dict of lists)
│   └── users_db.py                # User session data
│
├── services/                       # Business logic layer
│   ├── __init__.py                # Services package initialization
│   ├── lost_found_service.py      # Lost & Found business logic
│   ├── notes_service.py           # Notes exchange business logic
│   └── analytics_service.py       # Statistics and analytics logic
│
├── ui/                            # User interface components
│   ├── __init__.py               # UI package initialization
│   ├── dashboard_ui.py           # Home page and analytics
│   ├── lost_found_ui.py          # Lost & Found interface
│   └── notes_ui.py               # Notes exchange interface
│
├── utils/                         # Helper utilities
│   ├── __init__.py               # Utils package initialization
│   ├── validators.py             # Input validation functions
│   └── helpers.py                # Common helper functions
│
├── myenvn/                        # Virtual environment
│
└── README.md                      # Project documentation (this file)
```

---

## 🧠 Design Principles

### 1. **Separation of Concerns**
- **Database Layer**: Pure data storage (no business logic)
- **Service Layer**: Business logic (no UI code)
- **UI Layer**: Presentation only (calls services)
- **Utils Layer**: Reusable helper functions

### 2. **In-Memory Data Structures**

#### Lost & Found Database
```python
# List of dictionaries - Easy to iterate and filter
lost_found_items = [
    {
        'id': 1,
        'type': 'lost',  # or 'found'
        'item_name': 'Black Water Bottle',
        'category': 'Bottle',
        'location': 'Library',
        'description': '...',
        'reporter_name': '...',
        'reporter_contact': '...',
        'date': '2026-01-08',
        'status': 'open',  # or 'claimed'
        'matched_with': None
    },
    # ... more items
]
```

#### Notes Database
```python
# Dictionary of lists - Fast subject-wise access
notes_data = {
    'Data Structures': [
        {
            'id': 1,
            'subject': 'Data Structures',
            'topic': 'Arrays and Linked Lists',
            'semester': 'Semester 3',
            'uploaded_by': '...',
            'file_name': '...',
            'description': '...',
            'upload_date': '2026-01-05',
            'downloads': 45,
            'rating': 4.5
        },
        # ... more notes
    ],
    'Database Management': [...],
    # ... more subjects
}
```

### 3. **No External Database**
- All data stored in Python lists and dictionaries
- Data persists only during runtime
- Perfect for learning and demonstrations
- Easy to understand and debug

### 4. **Modern, Attractive UI**
- Gradient backgrounds
- Card-based layouts
- Interactive charts with Plotly
- Responsive design
- Custom CSS styling
- Smooth transitions and animations

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd "C:\Users\Gaurav Pathak\Desktop\campus exchange hub"
```

### Step 2: Activate Virtual Environment
The virtual environment `myenvn` is already created. Activate it:

**On Windows (PowerShell):**
```powershell
.\myenvn\Scripts\Activate.ps1
```

**On Windows (CMD):**
```cmd
myenvn\Scripts\activate.bat
```

### Step 3: Install Required Packages
All packages are already installed, but if needed:
```bash
pip install streamlit plotly pandas
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

---

## 📖 How to Use

### 1. **Login/Sign In**
- Enter your name, roll number, and email in the sidebar
- Click "Sign In" to access all features
- No password required (simplified for demo)

### 2. **Navigate the Platform**
- Use sidebar buttons to switch between sections:
  - 🏠 **Dashboard**: View statistics and analytics
  - 🔍 **Lost & Found**: Report or search for items
  - 📚 **Notes Exchange**: Upload or browse notes

### 3. **Lost & Found Operations**

#### Report a Lost Item:
1. Go to Lost & Found section
2. Click "Report Lost" tab
3. Fill in item details (name, category, location, description)
4. Submit the form
5. System automatically checks for potential matches

#### Report a Found Item:
1. Go to Lost & Found section
2. Click "Report Found" tab
3. Fill in item details
4. Submit the form
5. Owner can claim it later

#### Search Items:
1. Use the "Search Items" tab
2. Enter keywords (item name, category, or location)
3. Browse results
4. Claim items if you're the owner

### 4. **Notes Exchange Operations**

#### Upload Notes:
1. Go to Notes Exchange section
2. Click "Upload Notes" tab
3. Enter subject, topic, semester, file name, and description
4. Submit the form
5. Your notes are now available to all students

#### Browse Notes:
1. Click "Browse All" tab
2. Filter by subject or semester
3. Sort by recency or popularity
4. Click "Download" to get notes

#### View Top Contributors:
1. Click "Contributors" tab
2. See leaderboard with top uploaders
3. View contribution statistics

---

## 🎨 UI Features

### Attractive Design Elements
- **Gradient Headers**: Eye-catching purple and pink gradients
- **Card Layouts**: Clean, organized information display
- **Interactive Charts**: Plotly visualizations for analytics
- **Smooth Animations**: Hover effects and transitions
- **Color-coded Status**: Visual indicators for item status
- **Responsive Layout**: Works on different screen sizes

### Color Scheme
- Primary: Blue (#1E88E5)
- Accent 1: Purple Gradient (#667eea to #764ba2)
- Accent 2: Pink Gradient (#f093fb to #f5576c)
- Success: Green (#28A745)
- Warning: Orange (#FFA500)
- Error: Red (#DC3545)

---

## 🔧 Technical Details

### Technology Stack
- **Frontend/Backend**: Streamlit (Python web framework)
- **Charts**: Plotly (interactive visualizations)
- **Data Processing**: Pandas (optional, for advanced operations)
- **Language**: Python 3.10.6

### Data Flow
```
User Action
    ↓
Streamlit UI (ui/*.py)
    ↓
Service Layer (services/*.py)
    ↓
Database Layer (database/*.py)
    ↓
In-Memory Data Structures (list/dict)
    ↑
Updated Data Returned
    ↑
UI Re-renders with New Data
```

### Key Functions

#### Lost & Found Service
- `add_lost_item()`: Add new lost item
- `add_found_item()`: Add new found item
- `find_potential_matches()`: Smart matching algorithm
- `claim_item()`: Mark item as claimed
- `search_items()`: Search functionality

#### Notes Service
- `upload_note()`: Add new note
- `get_notes_by_subject()`: Filter by subject
- `increment_download_count()`: Track downloads
- `get_top_contributors()`: Leaderboard logic
- `search_notes()`: Search functionality

#### Analytics Service
- `get_lost_found_stats()`: Lost & Found statistics
- `get_notes_stats()`: Notes statistics
- `get_category_distribution()`: Category breakdown
- `get_subject_wise_stats()`: Subject analysis

---

## 📚 Learning Outcomes

This project demonstrates:
1. **Clean Architecture**: Separation of concerns with layers
2. **Data Structures**: Practical use of lists and dictionaries
3. **Web Development**: Building interactive web apps with Streamlit
4. **User Interface Design**: Creating attractive, user-friendly interfaces
5. **Business Logic**: Implementing real-world features
6. **Data Validation**: Input sanitization and error handling
7. **State Management**: Handling user sessions and app state
8. **Visualization**: Creating charts and analytics dashboards

---

## 🎓 Perfect for

- **College Projects**: Demonstrates full-stack development
- **Python Learning**: Practical application of Python concepts
- **Portfolio**: Showcases your development skills
- **Viva Presentations**: Easy to explain and demonstrate
- **Campus Utility**: Actually useful for students

---

## 🤔 Viva Questions & Answers

### Q1: Why use in-memory data structures instead of a database?
**A:** For learning purposes and simplicity. It demonstrates core programming concepts without database complexity. Perfect for understanding data structures and algorithms.

### Q2: How does the matching algorithm work?
**A:** It matches lost and found items based on category (exact match) and location (bonus points). Items with higher match scores appear first.

### Q3: What happens when the app restarts?
**A:** All data is lost since it's stored in memory. In production, we would use a database like SQLite, PostgreSQL, or MongoDB.

### Q4: Can you scale this application?
**A:** Yes! The layered architecture makes it easy to replace the in-memory database with a real database without changing service or UI code.

### Q5: How is user authentication handled?
**A:** Simplified login without passwords for demo purposes. In production, we'd implement proper authentication with hashed passwords and session tokens.

### Q6: What are the main challenges you faced?
**A:** 
- Designing clean architecture with separation of concerns
- Creating an attractive UI with Streamlit limitations
- Implementing smart matching algorithms
- Managing state across page refreshes

### Q7: How would you improve this project?
**A:**
- Add real database (SQLite/PostgreSQL)
- Implement actual file upload for notes
- Add email notifications for matches
- Include user authentication with passwords
- Add admin panel for moderation
- Implement image upload for lost items
- Add chat/messaging between users

---

## 🐛 Known Limitations

1. **Data Persistence**: Data is lost when app restarts
2. **File Upload**: Notes upload is simulated (no actual files)
3. **Authentication**: Simplified login (no password)
4. **Scalability**: In-memory storage limits scalability
5. **Concurrency**: No multi-user concurrency handling

These are intentional design choices for educational purposes.

---

## 🚀 Future Enhancements

- [ ] Add SQLite database for persistence
- [ ] Implement real file upload and storage
- [ ] Add email notifications
- [ ] Include image upload for lost items
- [ ] Add user ratings and reviews
- [ ] Implement chat/messaging system
- [ ] Add mobile responsive design
- [ ] Include export functionality (PDF reports)
- [ ] Add admin dashboard
- [ ] Implement API for mobile apps

---

## 📞 Support & Contact

For questions or improvements:
- **Developer**: Gaurav Pathak
- **Project**: Uni-Connect
- **Version**: 1.0.0
- **Date**: January 2026

---

## 📄 License

This project is created for educational purposes. Feel free to use, modify, and distribute as needed for learning.

---

## 🙏 Acknowledgments

- Built with **Streamlit** - Amazing Python web framework
- Visualizations powered by **Plotly**
- Inspired by real campus needs
- Developed for student community

---

## 🎉 Quick Start Commands

```bash
# Activate environment
.\myenvn\Scripts\Activate.ps1

# Run application
streamlit run app.py

# Install packages (if needed)
pip install streamlit plotly pandas

# Stop application
# Press Ctrl+C in terminal
```

---

**Made with ❤️ for students, by students**

**Happy Coding! 🚀**
