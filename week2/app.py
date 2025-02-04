import csv
import sys
import matplotlib.pyplot as plt
from jinja2 import Template

# read csv
def read_csv():
    data = []
    with open('data.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            data.append(row)
    return data

# HTML for student details
def generate_student_html(student_data, total_marks):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Details</title>
    </head>
    <body>
        <h1>Student Details</h1>
        <table border="1">
            <tr>
                <th>Student ID</th>
                <th>Course ID</th>
                <th>Marks</th>
            </tr>
            {% for row in student_data %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
            </tr>
            {% endfor %}
            <tr>
                <td colspan="2">Total Marks</td>
                <td>{{ total_marks }}</td>
            </tr>
        </table>
    </body>
    </html>
    """
    template = Template(html_template)
    html_content = template.render(student_data=student_data, total_marks=total_marks)
    with open('output.html', 'w') as file:
        file.write(html_content)

# HTML for course details and histogram
def generate_course_html(course_data, avg_marks, max_marks):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Course Details</title>
    </head>
    <body>
        <h1>Course Details</h1>
        <table border="1">
            <tr>
                <th>Average Marks</th>
                <th>Maximum Marks</th>
            </tr>
            <tr>
                <td>{{ avg_marks }}</td>
                <td>{{ max_marks }}</td>
            </tr>
        </table>
        <h2>Histogram of Marks</h2>
        <img src="marks_histogram.png" alt="Marks Histogram">
    </body>
    </html>
    """
    template = Template(html_template)
    html_content = template.render(avg_marks=avg_marks, max_marks=max_marks)
    with open('output.html', 'w') as file:
        file.write(html_content)

    plt.figure()
    plt.hist(course_data, bins=10, edgecolor='black')
    plt.title('Marks Histogram')
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    plt.savefig('marks_histogram.png')
    plt.close()

def main():
    if len(sys.argv) != 3:
        print("Error: Invalid number of arguments.")
        return

    option = sys.argv[1]
    identifier = sys.argv[2]
    
    data = read_csv()

    if option == '-s':
        student_data = [row for row in data if row[0] == identifier]
        if not student_data:
            print("Error: Student ID not found.")
            return
        total_marks = sum(int(row[2]) for row in student_data)
        generate_student_html(student_data, total_marks)

    elif option == '-c':
        course_data = [int(row[2]) for row in data if row[1].strip() == identifier]
        
        print(f"Filtered course data for course ID {identifier}: {course_data}")
        
        if not course_data:
            print("Error: Course ID not found.")
            return
        
        avg_marks = sum(course_data) / len(course_data)
        max_marks = max(course_data)
        generate_course_html(course_data, avg_marks, max_marks)

    else:
        print("Error: Invalid option. Use '-s' for student ID or '-c' for course ID.")

if __name__ == '__main__':
    main()
