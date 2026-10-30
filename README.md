\# Web-Based Student Academic Requisition Form with PDF Generation



\## 1. Project Overview

This project is a web-based application developed using Python and Streamlit. It allows students to fill out the Student Academic Requisition Form online and generate a downloadable PDF following the institute's prescribed format.



\## 2. Objectives

\- Digitise the student academic requisition process.

\- Collect student and application details.

\- Validate mandatory information.

\- Generate downloadable PDF forms.

\- Store submitted records using SQLite.



\## 3. Technologies Used

\- Python

\- Streamlit

\- ReportLab

\- SQLite

\- GitHub



\## 4. Features

\- Student details entry.

\- Department and semester information.

\- Application type selection.

\- Purpose and supporting document details.

\- Email and mobile number validation.

\- Student declaration confirmation.

\- Automatic PDF generation.

\- PDF download.

\- SQLite database storage.



\## 5. Project Structure

\- `app.py` – Main web application.

\- `pdf\_generator.py` – Generates the requisition PDF.

\- `db.py` – Handles SQLite database operations.

\- `requirements.txt` – Required Python packages.

\- `logo.png` – Institute logo.

\- `screenshots/` – Application screenshots.

\- `sample\_output/` – Sample generated PDF.

\- `Project\_Report.pdf` – Project documentation.



\## 6. How to Run the Project

1\. Install Python.

2\. Install dependencies using `pip install -r requirements.txt`.

3\. Run `streamlit run app.py`.

4\. Open the local URL displayed in the terminal.



\## 7. Application Workflow

1\. Student opens the web application.

2\. Enters personal and academic details.

3\. Selects the application type.

4\. Enters the purpose and supporting document details.

5\. Accepts the student declaration.

6\. Application validates the information.

7\. PDF is generated and made available for download.



\## 8. Sample Output

A sample generated requisition PDF is available in the `sample\_output` folder.



\## 9. Conclusion

The application provides a convenient way to submit student academic requisition details and generate the institute-formatted PDF digitally. It reduces manual form-filling effort and improves the overall process.

