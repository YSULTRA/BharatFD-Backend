![image](https://github.com/user-attachments/assets/20609596-31ba-4e68-ac8f-d55ff673b368)

# BharatFD-Backend

## **Hiring Test for Backend Developers**

### **Objective**
The objective of this test was to evaluate the ability to:
- Design and implement Django models with **WYSIWYG editor support**.
- Store and manage **FAQs with multi-language translation**.
- Follow **PEP8 conventions** and best practices.
- Write a **clear and detailed README**.
- Use **proper Git commit messages**.

### **Project Overview:**
This project showcases a fully-functional FAQ management system built with Django. It supports **multilingual content** (over 70+ languages), integrates a **WYSIWYG editor** for rich-text formatting of FAQ answers, implements **background task processing** via **Celery**, utilizes **Redis caching** for enhanced performance, and provides a clear **REST API** for managing FAQs.

### **Task Requirements and Our Implementation:**

#### **1. Model Design:**
I've created a **FAQ model** that supports the following fields:
- **Question**: Stored as a `TextField` for the FAQ question.
- **Answer**: A `RichTextField` for the answer, utilizing **django-ckeditor** to allow for WYSIWYG formatting.
- **Language-specific Translations**: Each FAQ object is translated to more then 70+ languages which are precomputed and then saved for fast reterival.
- I've also implemented a **model method** to dynamically retrieve the translated text based on the language selected by the user.

#### **2. WYSIWYG Editor Integration:**
- We integrated **django-ckeditor-5** into the system to allow rich-text editing for the FAQ answers.
- This allows for formatting the content with features like bold, italics, hyperlinks, etc., making the answers more informative and visually appealing.
- The WYSIWYG editor is configured to handle **multilingual content**, ensuring that the editor works seamlessly for all languages.

#### **3. API Development:**
- A **REST API** was created for managing FAQs.
- The API supports the `?lang=` query parameter, which allows users to fetch FAQs in different languages.
  - Example: `GET /api/faqs/?lang=hi` to fetch FAQs in Hindi.
- The API is optimized to provide fast responses by caching frequently requested FAQs, reducing the need to re-fetch translations.

#### **4. Caching Mechanism:**
- We implemented **Redis** for caching translated FAQ content.
- By using Redis, we reduce the latency associated with fetching translations for the FAQs. Frequently accessed translations are cached for improved performance.

#### **5. Multi-language Translation Support:**
- We used the **Google Translate API** (via `googletrans`) to automate the translation of FAQ questions.
- During the creation of new FAQ objects, if a translation is missing, the system automatically translates the question to the specified language.
- If a translation is unavailable, the system **falls back to English** to ensure no content is left untranslated.

#### **6. Admin Panel:**
- We registered the FAQ model in the **Django Admin panel**.
- The admin interface is user-friendly and allows easy management of FAQs, including the addition, editing, and deletion of questions and answers.
- We ensured that the multilingual translation fields are well-organized and manageable in the admin.

#### **7. Unit Tests & Code Quality:**
- We wrote **unit tests** for model methods, API endpoints, and translation features using **pytest**.
- The code adheres to **PEP8** conventions, ensuring clean, readable, and maintainable code.
- We used **flake8** for linting and ensuring code quality throughout the development process.

#### **8. Documentation:**
- The **README** is detailed and includes:
  - **Installation instructions** for setting up the project.
  - **API usage examples** to demonstrate how to fetch FAQs in different languages.
  - **Contribution guidelines** for potential contributors to the project.
- The README is structured clearly, making it easy for developers to understand the setup and use of the system.

#### **9. Git & Version Control:**
- **Git** was used for version control, with **atomic commits**.
- Each commit follows **conventional commit messages**, such as:
  - `feat: Add multilingual FAQ model`
  - `fix: Improve translation caching`
  - `docs: Update README with API examples`
- The repository is managed on **GitHub**, and we made sure all commits were meaningful and focused on one task.

#### **10. Deployment & Docker Support (Bonus):**
- We have provided a **Dockerfile** and **docker-compose.yml** to containerize the application and run it in isolated environments.
- **Deployment** instructions for Heroku and AWS were added in the README for easy deployment.

### **API Usage Examples:**

Here are some examples of how to interact with the API:

1. **Fetch FAQs in English (default language)**:
   ```bash
   curl http://localhost:8000/api/faqs/
   ```

2. **Fetch FAQs in Hindi**:
   ```bash
   curl http://localhost:8000/api/faqs/?lang=hi
   ```

3. **Fetch FAQs in Bengali**:
   ```bash
   curl http://localhost:8000/api/faqs/?lang=bn
   ```

### **Technologies Used:**

- **Backend Framework**: Django (Python)
- **WYSIWYG Editor**: django-ckeditor
- **Database**: SQLite (with support for PostgreSQL in production)
- **Caching**: Redis
- **Background Task Processing**: Celery
- **Translation API**: Google Translate API (via `googletrans` library)
- **API Documentation**: Swagger (if integrated)
- **Testing**: pytest
- **Version Control**: Git, GitHub



### **Project Setup Directory**

Ensure you are in the correct directory before running any commands. The following directory structure should be present:

```
>>\faq_project
│
├── .pytest_cache
├── faqs
├── faq_project
├── media
├── db.sqlite3
├── manage.py
└── pytest.ini
```

1. **Open the Terminal in the Project Directory:**

   Navigate to the project directory:
   ```bash
   cd faq_project
   ```

2. **Run the Commands:**

   Once in the `faq_project` directory, follow the setup instructions as mentioned previously to start the Celery worker, Redis server, migrate the database, and run the Django development server.




### **Project Setup Instructions**

To set up and run the FAQ management system with background translations and faster webpage loading, follow the steps below:


1. **Install Required Dependencies:**

   Install the necessary dependencies by running the following command:
   ```bash
   pip install celery redis pytest googletrans djangorestframework django
   ```

2. **Clone the Repository:**

   Clone the repository to your local machine:
   ```bash
   git clone <repository_url>
   ```

3. **Start the Celery Worker:**

   Open the first terminal and run the following command to start the Celery worker:
   ```bash
   celery -A faq_project worker --loglevel=info --pool=solo
   ```

4. **Start the Redis Server:**

   In the second terminal, run the following command to start the Redis server:
   ```bash
   redis-server --port 6380
   ```

5. **Run Database Migrations:**

   In the third terminal, run the following commands to apply the database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the Django Development Server:**

   Finally, run the Django development server with the following command:
   ```bash
   python manage.py runserver
   ```
   
### **Background Processing for Translations (Multithreaded)**  
The translation process for FAQs is being handled in the background using multithreading to ensure efficiency and scalability. This approach significantly reduces processing time and ensures smooth operations, even with large datasets.

![Background Processing](https://github.com/user-attachments/assets/f21e5246-516e-4e3b-b27e-242fc7cf4785)

---

### **FAQ Translations to Gujarati and Arabic**  
The FAQs have been successfully translated into multiple languages, including **Gujarati** and **Arabic**, enabling a broader range of users to access the content in their preferred languages.

- **Gujarati Translation:**  
![FAQ in Gujarati](https://github.com/user-attachments/assets/74723a8a-97c8-4a83-8b5a-5e76bb9ff0dc)

- **Arabic Translation:**  
![FAQ in Arabic](https://github.com/user-attachments/assets/085d8ec1-3be4-4b60-990d-599d287e0a54)

---

### **User-Friendly FAQ Management**  
Users can now easily create, edit, and manage FAQ answers using an intuitive graphical user interface (GUI). The system allows seamless interaction, enabling users to update answers directly without any technical knowledge.

- **Creating and Editing FAQ Answers:**  
![Editing FAQ Answer](https://github.com/user-attachments/assets/44abdad3-4829-4b06-aac0-1b02bea02d9e)

- **Save and Submit Changes via GUI:**  
![Saving FAQ Answer](https://github.com/user-attachments/assets/a70568eb-3038-43bc-9f6c-bc8b328eb4d3)

---

-**API**
![image](https://github.com/user-attachments/assets/0806108c-939f-42ff-aa23-ce9775dbba3b)
![image](https://github.com/user-attachments/assets/1197cea8-95db-424b-a007-194921053342)








