from flask import Flask, render_template, request, redirect, url_for
import csv
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Function to read the CSV file and return the data
def read_csv():
    with open('data.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve form data
        id_type = request.form.get('ID')  # student_id or course_id
        id_value = request.form.get('id_value')

        # Handle invalid inputs
        if not id_value:
            return render_template('error.html', message="ID value cannot be empty!", back_link=url_for('index'))
        
        data = read_csv()

        if id_type == 'student_id':
            # Filter data by Student ID
            student_data = [row for row in data if row['Student id'] == id_value]
            
            if not student_data:
                return render_template('error.html', message="Student ID not found!", back_link=url_for('index'))
            
            total_marks = sum(int(row[' Marks']) for row in student_data)
            
            return render_template('student_details.html', student_data=student_data, total_marks=total_marks)
        
        elif id_type == 'course_id':
            # Filter data by Course ID
            course_data = [row for row in data if row[' Course id'] == id_value]
            
            if not course_data:
                return render_template('error.html', message="Course ID not found!", back_link=url_for('index'))

            # Calculate average and max marks
            marks = [int(row[' Marks']) for row in course_data]
            average_marks = sum(marks) / len(marks)
            maximum_marks = max(marks)

            # Create histogram
            img = BytesIO()
            plt.hist(marks, bins=10, edgecolor='black')
            plt.title(f"Marks Distribution for Course {id_value}")
            plt.xlabel('Marks')
            plt.ylabel('Frequency')
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode('utf8')

            return render_template('course_details.html', average_marks=average_marks, maximum_marks=maximum_marks, plot_url=plot_url)
        
        else:
            return render_template('error.html', message="Invalid input selected!", back_link=url_for('index'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
