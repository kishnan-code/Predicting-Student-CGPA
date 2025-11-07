from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import joblib
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = joblib.load('model.pkl')

FEATURE_COLUMNS = [
    'Gender',
    'Age',
    'Attendance (%)',
    'HighSchool_GPA',
    'Internal_Assessments (%)',
    'Participation_Score',
    'Projects_Completed',
    'Study_Hours_Per_Week',
    'Backlogs',
    'Sem_1_GPA',
    'Sem_2_GPA'
]

PREDICTED_FILE = os.path.join(UPLOAD_FOLDER, 'predicted_output.xlsx')
PREDICTION_CSV = 'predictions.csv'

# Ensure predictions file exists
if not os.path.exists(PREDICTION_CSV):
    with open(PREDICTION_CSV, 'w') as f:
        f.write(','.join([
            'Timestamp', 'Student_Name', 'Gender', 'Age', 'Attendance (%)',
            'HighSchool_GPA', 'Internal_Assessments (%)', 'Participation_Score',
            'Projects_Completed', 'Study_Hours_Per_Week', 'Backlogs',
            'Sem_1_GPA', 'Sem_2_GPA', 'Predicted_CGPA'
        ]) + '\n')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bulk')
def bulk():
    return render_template('upload.html')

@app.route('/history')
def history():
    student_name = request.args.get('student', '')
    return render_template('hist.html', student=student_name)

@app.route('/api/history')
def get_history():
    student_name = request.args.get('student', '')
    
    try:
        if not os.path.exists(PREDICTION_CSV):
            return jsonify({'error': 'No prediction data available'}), 404
        
        df = pd.read_csv(PREDICTION_CSV)
        if student_name:
            df = df[df['Student_Name'] == student_name]
        
        # Convert to list of dictionaries
        data = df.to_dict('records')
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' in request.files and request.files['file'].filename:
        file = request.files['file']
        filename = file.filename
        ext = filename.split('.')[-1].lower()
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            df = pd.read_csv(filepath) if ext == 'csv' else pd.read_excel(filepath)
            features = df[FEATURE_COLUMNS].copy()
            features['Gender'] = features['Gender'].map({'Male': 1, 'Female': 0})

            if features['Gender'].isnull().any():
                raise ValueError("Gender column must contain only 'Male' or 'Female'")

            predictions = model.predict(features)
            df['Prediction'] = predictions
            
            # Save individual predictions to history
            for _, row in df.iterrows():
                save_data = {
                    'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Student_Name': row.get('Student_Name', 'Unknown'),
                    'Gender': 'Male' if row['Gender'] == 1 else 'Female',
                    'Age': row['Age'],
                    'Attendance (%)': row['Attendance (%)'],
                    'HighSchool_GPA': row['HighSchool_GPA'],
                    'Internal_Assessments (%)': row['Internal_Assessments (%)'],
                    'Participation_Score': row['Participation_Score'],
                    'Projects_Completed': row['Projects_Completed'],
                    'Study_Hours_Per_Week': row['Study_Hours_Per_Week'],
                    'Backlogs': row['Backlogs'],
                    'Sem_1_GPA': row['Sem_1_GPA'],
                    'Sem_2_GPA': row['Sem_2_GPA'],
                    'Predicted_CGPA': row['Prediction']
                }
                pd.DataFrame([save_data]).to_csv(
                    PREDICTION_CSV, 
                    mode='a', 
                    index=False, 
                    header=not os.path.exists(PREDICTION_CSV)
                )

            df.to_excel(PREDICTED_FILE, index=False)
            table_html = df.to_html(classes='table table-bordered', index=False)

            return render_template('pd.html', 
                                message="Bulk prediction successful!", 
                                download_ready=True, 
                                table_html=table_html)
        except Exception as e:
            return render_template('pd.html', 
                                message=f"Error: {e}", 
                                download_ready=False, 
                                table_html=None)

    try:
        form = request.form
        student_name = form['student_name']
        gender = 'Male' if form['gender'] == '1' else 'Female'
        gender_num = 1 if form['gender'] == '1' else 0
        age = float(form['age'])
        attendance = float(form['attendance'])
        highschool_gpa = float(form['highschool_gpa'])
        internal_assessments = float(form['internal_assessments'])
        participation_score = float(form['participation_score'])
        projects_completed = int(form['projects_completed'])
        study_hours = float(form['study_hours'])
        backlogs = int(form['backlogs'])
        sem1_gpa = float(form['sem1_gpa'])
        sem2_gpa = float(form['sem2_gpa'])

        predict_data = {
            'Gender': gender_num,
            'Age': age,
            'Attendance (%)': attendance,
            'HighSchool_GPA': highschool_gpa,
            'Internal_Assessments (%)': internal_assessments,
            'Participation_Score': participation_score,
            'Projects_Completed': projects_completed,
            'Study_Hours_Per_Week': study_hours,
            'Backlogs': backlogs,
            'Sem_1_GPA': sem1_gpa,
            'Sem_2_GPA': sem2_gpa
        }

        input_df = pd.DataFrame([predict_data])
        predicted_cgpa = round(model.predict(input_df)[0], 2)

        save_data = {
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Student_Name': student_name,
            'Gender': gender,
            'Age': age,
            'Attendance (%)': attendance,
            'HighSchool_GPA': highschool_gpa,
            'Internal_Assessments (%)': internal_assessments,
            'Participation_Score': participation_score,
            'Projects_Completed': projects_completed,
            'Study_Hours_Per_Week': study_hours,
            'Backlogs': backlogs,
            'Sem_1_GPA': sem1_gpa,
            'Sem_2_GPA': sem2_gpa,
            'Predicted_CGPA': predicted_cgpa
        }

        pd.DataFrame([save_data]).to_csv(
            PREDICTION_CSV, 
            mode='a', 
            index=False, 
            header=not os.path.exists(PREDICTION_CSV)
        )

        return render_template(
            'result.html',
            student_name=student_name,
            gender=gender,
            age=age,
            attendance=attendance,
            highschool_gpa=highschool_gpa,
            internal_assessments=internal_assessments,
            participation_score=participation_score,
            projects_completed=projects_completed,
            study_hours=study_hours,
            backlogs=backlogs,
            sem1_gpa=sem1_gpa,
            sem2_gpa=sem2_gpa,
            predicted_cgpa=predicted_cgpa
        )

    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/download')
def download():
    if os.path.exists(PREDICTED_FILE):
        return send_file(PREDICTED_FILE, as_attachment=True)
    elif os.path.exists(PREDICTION_CSV):
        return send_file(PREDICTION_CSV, as_attachment=True)
    else:
        return "No file available for download."

if __name__ == '__main__':
    app.run(debug=True)



