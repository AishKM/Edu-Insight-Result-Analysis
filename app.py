import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from flask import Flask, render_template, send_file
import os

# Initialize Flask app
app = Flask(__name__)

# Path for saving images and PDF
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to process and analyze the data
def process_data(sem_data, semester):
    # Calculate Total Marks
    sem_data['Total Marks'] = sem_data.iloc[:, 1:].sum(axis=1)

    # Define passing marks (adjust as needed)
    passing_marks = 50
    sem_data['Result'] = sem_data['Total Marks'].apply(lambda x: 'Pass' if x >= passing_marks else 'Fail')

    # Plot Total Marks for the semester
    plt.figure(figsize=(10, 6))
    plt.bar(sem_data['Name'], sem_data['Total Marks'])
    plt.title(f'{semester} Total Marks')
    plt.xlabel('Student')
    plt.ylabel('Total Marks')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Save the chart as an image
    chart_filename = f'{semester}_total_marks.png'
    chart_filepath = os.path.join(UPLOAD_FOLDER, chart_filename)
    plt.savefig(chart_filepath)
    plt.close()

    return chart_filepath

# Function to generate the PDF report
def generate_pdf():
    # Create a new PDF document
    pdf = FPDF()

    # Add cover page
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Student Result Analysis Report", ln=True, align="C")

    # Read and process data for each semester
    sem1_data = pd.read_excel('sem1_student_results.xlsx')
    sem2_data = pd.read_excel('sem2_student_results.xlsx')
    sem3_data = pd.read_excel('sem3_student_results.xlsx')
    sem4_data = pd.read_excel('sem4_student_results.xlsx')

    # Process and generate chart for each semester
    sem1_chart = process_data(sem1_data, 'Semester 1')
    sem2_chart = process_data(sem2_data, 'Semester 2')
    sem3_chart = process_data(sem3_data, 'Semester 3')
    sem4_chart = process_data(sem4_data, 'Semester 4')

    # Add charts to the PDF
    def add_semester_page(pdf, semester_name, chart_image):
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"{semester_name} Performance", ln=True, align="L")
        pdf.image(chart_image, x=10, y=40, w=180)

    # Add each semester's chart to the PDF
    add_semester_page(pdf, 'Semester 1', sem1_chart)
    add_semester_page(pdf, 'Semester 2', sem2_chart)
    add_semester_page(pdf, 'Semester 3', sem3_chart)
    add_semester_page(pdf, 'Semester 4', sem4_chart)

    # Output the final PDF to a file
    pdf_output_path = os.path.join(UPLOAD_FOLDER, "Result_Analysis_Report.pdf")
    pdf.output(pdf_output_path)

    return pdf_output_path

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html')


# Route for generating the PDF report
@app.route('/generate_report')
def generate_report():
    pdf_path = generate_pdf()
    return send_file(pdf_path, as_attachment=True)

# Route to view the analysis
@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

# Route to view the langing page
@app.route('/landing_page')
def landing_page():
    return render_template('landing_page.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
