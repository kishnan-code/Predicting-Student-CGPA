# Student CGPA Prediction System

## Overview
This project is a Machine Learning-powered web application built with Flask that predicts a student's Final CGPA based on their academic performance and other influencing factors. It supports both single-student prediction via a web form and bulk prediction via file upload.

🔗 **Live App:** https://predicting-student-cgpa-ttmi.onrender.com/

🌐 **Project Page (Portfolio):** [https://lnkd.in/eenjfwsG](https://lnkd.in/eenjfwsG)

## Features
- **Individual Prediction**: Enter student details manually to get an instant CGPA prediction.
- **Bulk Prediction**: Upload a CSV or Excel file containing data for multiple students to generate predictions in batch.
- **Prediction History**: View a history of past predictions stored in the system.
- **Downloadable Results**: Download bulk prediction results as a file.

## Input Parameters
The model considers the following factors for prediction:
- **Gender**: Male/Female
- **Age**: Student's age
- **Attendance (%)**: Percentage of classes attended
- **High School GPA**: GPA secured in high school
- **Internal Assessments (%)**: Scores in internal exams
- **Participation Score**: Score based on class participation
- **Projects Completed**: Number of projects completed
- **Study Hours Per Week**: Average study hours
- **Backlogs**: Number of accumulated backlogs
- **Sem 1 GPA**: GPA of the first semester
- **Sem 2 GPA**: GPA of the second semester

## Tech Stack
- **Backend**: Flask (Python)
- **Machine Learning**: Scikit-learn (Model served via Joblib)
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML, CSS, JavaScript

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Predicting-Student-CGPA
   ```

2. **Install dependencies:**
   Make sure you have Python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the app:**
   Open your browser and navigate to `http://localhost:5000`.

## Project Structure
- `app.py`: Main Flask application file.
- `model.pkl`: Pre-trained machine learning model.
- `requirements.txt`: List of Python dependencies.
- `templates/`: HTML templates for the web interface.
- `uploads/`: Directory for storing uploaded files for bulk prediction.
- `predictions.csv`: Log file storing prediction history.
- `UG_Student_CGPA_Prediction.xlsx`: Dataset used for training/reference.

## Usage
1. **Home Page**: Navigate to the home page to start.
2. **Predict**: Fill in the form for a single student or go to the "Bulk Predict" section to upload a file.
3. **View Results**: See the predicted CGPA on the results page.
4. **History**: Check the history of predictions (if enabled/implemented).
