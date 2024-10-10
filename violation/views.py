import os
import io
import re
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DateRangeForm, CameraRangeForm
from fpdf import FPDF
from io import BytesIO
from PIL import Image
import base64
from datetime import datetime
import matplotlib.pyplot as plt
import calendar
from django.conf import settings
from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv
import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render, redirect
from dateutil.parser import parse

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Path to images
    image_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_images', 'images')
    violations = extract_violations_from_images(image_dir)

    # Convert violations to DataFrame
    df = pd.DataFrame(violations, columns=['Image', 'Date', 'Time', 'Camera_Number', 'Without_Jacket', 'Without_Helmet', 'Both', 'ID'])

    # Convert date to datetime with error handling
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%y', errors='coerce')  # Adjust the format as per your data

    # Today's date
    today = pd.Timestamp.now().normalize()

    # Initialize counts for today's violations
    violation_counts_today = {
        'Without_Jacket': 0,
        'Without_Helmet': 0,
        'Both': 0
    }

    # Filter today's violations
    today_data = df[df['Date'] == today]

    # Count violations for today
    if not today_data.empty:
        violation_counts_today['Without_Jacket'] = today_data['Without_Jacket'].str.count("Yes").sum()
        violation_counts_today['Without_Helmet'] = today_data['Without_Helmet'].str.count("Yes").sum()
        violation_counts_today['Both'] = today_data['Both'].str.count("Yes").sum()

    # Total violations for today
    total_violations_today = (
        violation_counts_today['Without_Jacket'] + 
        violation_counts_today['Without_Helmet'] + 
        violation_counts_today['Both']
    )

    # Get the last 5 violations
    last_5_violations = df.sort_values(by='Date', ascending=False).head(5)

    # Get data for the last month
    start_date = today - pd.DateOffset(months=1)
    month_data = df[(df['Date'] >= start_date) & (df['Date'] <= today)]

    # Count violations for the month
    violation_counts_month = {
        'Without_Jacket': month_data['Without_Jacket'].str.count("Yes").sum(),
        'Without_Helmet': month_data['Without_Helmet'].str.count("Yes").sum(),
        'Both': month_data['Both'].str.count("Yes").sum()
    }

    # Total violations for the month
    total_violations_month = (
        violation_counts_month['Without_Jacket'] + 
        violation_counts_month['Without_Helmet'] + 
        violation_counts_month['Both']
    )

    # Handle POST request for date range filtering
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            filtered_violations = df[(df['Date'] >= pd.Timestamp(start_date)) & (df['Date'] <= pd.Timestamp(end_date))]

            if filtered_violations.empty:
                return render(request, 'violation/no_violation.html')

            return render(request, 'violation/report_page.html', {
                'violations': filtered_violations.to_dict('records'),
            })
    else:
        form = DateRangeForm()

    # Generate graph data if necessary
    graph_data = create_graph(df)

    return render(request, 'violation/dashboard.html', {
        'form': form,
        'graph_data': graph_data,
        'last_5_violations': last_5_violations.to_dict('records'),
        'violation_counts_today': violation_counts_today,
        'violation_counts_month': violation_counts_month,
        'total_violations_today': total_violations_today,
        'total_violations_month': total_violations_month,
    })








# from django.shortcuts import redirect, render
# from django.utils import timezone
# import pandas as pd
# import os
# from .forms import DateRangeForm  # Import your form
# from django.conf import settings

# def dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('login')

#     # Dynamic path using settings.MEDIA_ROOT
#     image_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_images', 'images')
#     violations = extract_violations_from_images(image_dir)

#     df = pd.DataFrame(violations, columns=['Image', 'Date', 'Time', 'Camera_Number', 'Without_Jacket', 'Without_Helmet', 'Both', 'ID'])
#     df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert date to datetime

#     # Get last 5 violations
#     last_5_violations = df.sort_values(by='Date', ascending=False).head(5)

#     # Get data for the last month
#     today = pd.Timestamp.now()  # Use Timestamp for consistency
#     start_date = today - pd.DateOffset(months=1)

#     month_data = df[(df['Date'] >= start_date) & (df['Date'] <= today)]

#     # Count occurrences of violations
#     violation_counts = {
#         'Without_Jacket': month_data['Without_Jacket'].sum(),
#         'Without_Helmet': month_data['Without_Helmet'].sum(),
#         'Both': month_data['Both'].sum()
#     }

#     if request.method == 'POST':
#         form = DateRangeForm(request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
#             filtered_violations = df[(df['Date'] >= pd.Timestamp(start_date)) & (df['Date'] <= pd.Timestamp(end_date))]

#             if filtered_violations.empty:
#                 return render(request, 'violation/no_violation.html')

#             return render(request, 'violation/report_page.html', {
#                 'violations': filtered_violations.to_dict('records'),
#             })
#     else:
#         form = DateRangeForm()
#         graph_data = create_graph(df)

#     return render(request, 'violation/dashboard.html', {
#         'form': form,
#         'graph_data': graph_data,
#         'last_5_violations': last_5_violations.to_dict('records'),
#         'violation_counts': violation_counts,
#     })





# Dashboard view

# def dashboard(request):
#     if not request.user.is_authenticated:
#          image_dir = "C:\\Users\\Pankaj Kumar Dubey\\Desktop\\report\\myproject\\media\\uploaded_images\\images"

#          return redirect('login')
    
#     # image_dir = "C:\\Users\\Pankaj Kumar Dubey\\Desktop\\report\\myproject\\media\\uploaded_images\\images"

#     # Dynamic path using settings.MEDIA_ROOT
#     image_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_images', 'images')
#     violations = extract_violations_from_images(image_dir)

#     violations = extract_violations_from_images(image_dir)
#     df = pd.DataFrame(violations, columns=['Image', 'Date', 'Time', 'Camera_Number', 'Without_Jacket', 'Without_Helmet', 'Both', 'ID'])

#     df['Date'] = df['Date'].apply(parse_date_safe)

#     if request.method == 'POST':
#         form = DateRangeForm(request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
#             filtered_violations = df[(df['Date'] >= pd.Timestamp(start_date)) & (df['Date'] <= pd.Timestamp(end_date))]

#             if filtered_violations.empty:
#                 return render(request, 'violation/no_violation.html')

#             # Prepare the data for rendering
#             return render(request, 'violation/report_page.html', {
#                 'violations': filtered_violations.to_dict('records'),
#             })
#     else:
#         form = DateRangeForm()
#         graph_data = create_graph(df)

#     return render(request, 'violation/dashboard.html', {'form': form, 'graph_data': graph_data})


# Helper function to safely parse dates
def parse_date_safe(date_str):
    try:
        return pd.to_datetime(date_str, format='%d-%m-%y')
    except ValueError:
        # Log the invalid date and return None
        print(f"Invalid date format: {date_str}")
        return pd.NaT
    
# Parse filename for violation information, including Camera_Number and Camera_ID
def parse_filename(filename):
    try:
        # Adjusted pattern to extract violation number, date, time, camera ID, and Camera Number
        pattern = r"violation(\d+)_(\d{2})-(\d{2})-(\d{2}) at (\d{2})\.(\d{2})\.(\d{2})_id-(\d+)_no-(\d+)\..+"
        match = re.match(pattern, filename)

        if match:
            violation_number = match.group(1)  # Extract Violation Number
            day = match.group(2)  # Extract day
            month = match.group(3)  # Extract month
            year = f"20{match.group(4)}"  # Extract year
            hour = match.group(5)  # Extract hour
            minute = match.group(6)  # Extract minute
            second = match.group(7)  # Extract second
            camera_id = match.group(8)  # Extract Camera ID
            camera_number = match.group(9)  # Extract Camera Number
            violation_type = match.group(10) if match.group(10) else ''  # Optional violation type

            # Combine date and time into a datetime object
            date_time_str = f"{year}-{month}-{day} {hour}:{minute}:{second}"
            date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

            # Return parsed components as a dictionary
            return {
                'violation_number': violation_number,
                'date_time': date_time,
                'camera_id': camera_id,
                'camera_number': camera_number,
                'violation_type': violation_type  # Optional
            }
        else:
            print(f"Filename does not match the expected pattern: {filename}")
            return None
    except Exception as e:
        print(f"Error parsing filename {filename}: {e}")
        return None
    
def extract_violations_from_images(image_dir):
    violations = []
    
    for filename in os.listdir(image_dir):
        match = re.match(r'violation\d+_(\d{2}-\d{2}-\d{2}) at (\d{2}\.\d{2}\.\d{2})_id-(\d+)_no-(\d+)(?:_(.*))?\.png$', filename)
        if match:
            date_str = match.group(1)
            time_str = match.group(2)
            id_number = match.group(3)
            camera_number = match.group(4)
            extra_info = match.group(5) if match.group(5) else ""

            without_jacket = "No"  # Changed from without_shoes to without_jacket
            without_helmet = "No"
            both = "No"
            image_file = filename
            
            if "wj" in extra_info:  # Changed from "ws" to "wj"
                without_jacket = "Yes"
            if "wh" in extra_info:
                without_helmet = "Yes"
            if "bt" in extra_info:
                both = "Yes"

            violations.append({
                'Image': f'{settings.MEDIA_URL}uploaded_images/images/{image_file}',
                'Date': date_str,
                'Time': time_str,
                'Camera_Number': camera_number,
                'Without_Jacket': without_jacket,  # Updated key
                'Without_Helmet': without_helmet,
                'Both': both,
                'ID': id_number,
            })
        else:
            print(f"Unexpected filename format: {filename}")
    
    return violations

# Create graph for the dashboard
def create_graph(df):
    df = df.dropna(subset=['Date'])
    df['Month'] = df['Date'].dt.month

    monthly_counts = df['Month'].value_counts().sort_index()
    total_violations = monthly_counts.sum()
    monthly_percentages = (monthly_counts / total_violations) * 100

    months = monthly_counts.index
    counts = monthly_counts.values
    percentages = monthly_percentages.values

    plt.switch_backend('Agg')
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Number of Violations', color=color)
    bars = ax1.bar(months, counts, color=color, alpha=0.6, label='Count')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Percentage of Violations (%)', color=color)
    line = ax2.plot(months, percentages, color=color, marker='o', label='Percentage')
    ax2.tick_params(axis='y', labelcolor=color)

    ax1.set_title('Monthly Violations with Percentages')
    ax1.set_xticks(months)
    ax1.set_xticklabels([calendar.month_name[i] for i in months])

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    graph_buffer = BytesIO()
    plt.savefig(graph_buffer, format='png')
    plt.close()
    graph_buffer.seek(0)
    graph_data = base64.b64encode(graph_buffer.read()).decode('utf-8')

    return graph_data


def download_csv(request):
    image_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_images', 'images')
    violations = extract_violations_from_images(image_dir)
    df = pd.DataFrame(violations, columns=['Image', 'Date', 'Time', 'Camera_Number', 'Without_Jacket', 'Without_Helmet', 'Both', 'ID'])
    
    # Optionally filter based on date range or camera number if needed
    # You can also pass request parameters to filter data accordingly

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="violations.csv"'

    writer = csv.writer(response)
    writer.writerow(['Image', 'Date', 'Time', 'Camera_Number', 'Without_Jacket', 'Without_Helmet', 'Both', 'ID'])  # Header row

    for index, row in df.iterrows():
        writer.writerow([row['Image'], row['Date'], row['Time'], row['Camera_Number'], row['Without_Jacket'], row['Without_Helmet'], row['Both'], row['ID']])

    return response


def generate_pdf(violations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)

    headers = ['Date', 'Camera_Number', 'Without_Jacket', 'Without_Helmet', 'Both', 'Image']
    col_widths = [40, 40, 40, 40, 40, 50]
    
    for header, width in zip(headers, col_widths):
        pdf.cell(width, 10, header, border=1)
    pdf.ln()

    image_folder_path = settings.MEDIA_ROOT

    for index, row in violations.iterrows():
        pdf.set_font('Arial', '', 12)
        pdf.cell(40, 10, str(row['Date']), border=1)
        pdf.cell(40, 10, str(row['Camera_Number']), border=1)
        pdf.cell(40, 10, 'Yes' if row['Without_Jacket'] == 'Yes' else 'No', border=1)
        pdf.cell(40, 10, 'Yes' if row['Without_Helmet'] == 'Yes' else 'No', border=1)
        pdf.cell(40, 10, 'Yes' if row['Both'] == 'Yes' else 'No', border=1)

        image_file_name = row['Image'].split('/')[-1]
        image_path = os.path.join(image_folder_path, 'images', image_file_name)
        print(image_file_name)
        print(image_path)
        print(image_folder_path)

        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img_width, img_height = img.size

                max_width = 40
                aspect_ratio = img_height / img_width
                new_height = max_width * aspect_ratio

                pdf.image(image_path, x=pdf.get_x(), y=pdf.get_y(), w=max_width, h=new_height)
                pdf.ln(new_height)
            except Exception as e:
                pdf.cell(40, 10, 'Image Error', border=1)
        else:
            pdf.cell(40, 10, 'Image Not Found', border=1)

        pdf.ln(10)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output, 'F')
    pdf_output.seek(0)

    pdf_base64 = base64.b64encode(pdf_output.read()).decode('utf-8')
    return pdf_base64

    

def no_violation(request):
    return render(request, 'violation/no_violation.html')

def view_violations(request):
    image_dir = "C:\\Users\\Pankaj Kumar Dubey\\Desktop\\report\\myproject\\media\\uploaded_images\\images"
    violations = extract_violations_from_images(image_dir)
    df = pd.DataFrame(violations, columns=['Image', 'Date', 'Time', 'Camera_Number', 'Without_Jacket', 'Without_Helmet', 'Both', 'ID'])

    df['Date'] = df['Date'].apply(parse_date_safe)

    if df.empty:
        return render(request, 'violation/no_violation.html')

    # Drop rows with NaT dates
    df = df.dropna(subset=['Date'])

    # Add month column to group by month
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year

    # Create graphs and charts
    bar_graph_data = create_bar_graph(df)
    line_chart_data = create_line_chart(df)
    camera_violation_chart = create_camera_violation_chart(df)

    return render(request, 'violation/view_violations.html', {
        'bar_graph_data': bar_graph_data,
        'line_chart_data': line_chart_data,
        'camera_violation_chart': camera_violation_chart
    })

def user_settings(request):
    # Your logic for settings
    return render(request, 'help.html')

# @login_required
def logout_view(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Log out the user
    logout(request)
    
    # Redirect to the login page after logout
    return redirect('login')



# def generate_record_by_camera(request):
#     if request.method == 'POST':
#         camera_form = CameraRangeForm(request.POST)
#         if camera_form.is_valid():
#             camera_number = camera_form.cleaned_data['camera_number']
#             camera_range = camera_form.cleaned_data.get('camera_range', '').split(',')

#             image_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_images', 'images')
#             violations = extract_violations_from_images(image_dir)
#             df = pd.DataFrame(violations, columns=['Image', 'Date', 'Time', 'Camera_Number', 'Without_Jacket', 'Without_Helmet', 'Both', 'ID'])

#             # Validate camera number or range input
#             filtered_violations = pd.DataFrame()
#             if camera_number:
#                 filtered_violations = df[df['Camera_Number'] == str(camera_number)]
#             elif camera_range:
#                 try:
#                     start_camera = int(camera_range[0])
#                     end_camera = int(camera_range[1])
#                     filtered_violations = df[df['Camera_Number'].isin(map(str, range(start_camera, end_camera + 1)))]
#                 except ValueError:
#                     return render(request, 'violation/no_violation.html', {'message': 'Invalid range input.'})

#             if filtered_violations.empty:
#                 return render(request, 'violation/no_violation.html', {'message': 'No violations found for the given criteria.'})

#             return render(request, 'violation/report_page.html', {
#                 'violations': filtered_violations.to_dict('records'),
#                 'camera_number': camera_number or f'Range: {camera_range[0]} to {camera_range[1]}'
#             })

#     camera_form = CameraRangeForm()
#     return render(request, 'violation/generate_record.html', {
#         'camera_form': camera_form
#     })

def generate_record(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    image_dir = "C:\\Users\\Pankaj Kumar Dubey\\Desktop\\report\\myproject\\media\\uploaded_images\\images"
    violations = extract_violations_from_images(image_dir)
    df = pd.DataFrame(violations, columns=['Image', 'Date', 'Time', 'Camera_Number', 'Without_Jacket', 'Without_Helmet', 'Both', 'ID'])

    df['Date'] = df['Date'].apply(parse_date_safe)

    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            filtered_violations = df[(df['Date'] >= pd.Timestamp(start_date)) & (df['Date'] <= pd.Timestamp(end_date))]

            if filtered_violations.empty:
                return render(request, 'violation/no_violation.html')

            # Prepare the data for rendering
            return render(request, 'violation/report_page.html', {
                'violations': filtered_violations.to_dict('records'),
            })
    else:
        form = DateRangeForm()
        graph_data = create_graph(df)

    return render(request, 'violation/generate_record.html', {'form': form})


def create_camera_violation_chart(df):
    camera_monthly_counts = df.groupby(['Camera_Number', df['Date'].dt.strftime('%Y-%m')])['ID'].count().unstack(fill_value=0)

    plt.switch_backend('Agg')
    fig, ax = plt.subplots(figsize=(10, 6))
    camera_monthly_counts.T.plot(kind='bar', ax=ax, stacked=True)

    ax.set_title('Violations per Camera Number per Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Violations')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return graph_data

def create_line_chart(df):
    df['Month_Year'] = df['Date'].dt.to_period('M')
    monthly_violations = df.groupby('Month_Year')['ID'].count()

    plt.switch_backend('Agg')
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_violations.plot(kind='line', ax=ax, marker='o', color='green')

    ax.set_title('Trend of Violations Over Time')
    ax.set_xlabel('Month-Year')
    ax.set_ylabel('Number of Violations')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return graph_data

def create_bar_graph(df):
    monthly_counts = df.groupby(df['Date'].dt.strftime('%Y-%m'))['ID'].count()
    
    plt.switch_backend('Agg')
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_counts.plot(kind='bar', ax=ax, color='skyblue')
    
    ax.set_title('Violations per Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Violations')

    # Save to buffer and encode
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    
    return graph_data






# import pandas as pd
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .forms import DateRangeForm
# from fpdf import FPDF
# import os
# from django.conf import settings
# from io import BytesIO
# from PIL import Image
# import matplotlib.pyplot as plt
# import base64
# import calendar
# import numpy as np

# def dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('login')

#     # Load Excel file (for both initial load and after filtering)
#     excel_file_path = "C:\\Users\\Pankaj Kumar Dubey\\Downloads\\bb.xlsx"
#     df = pd.read_excel(excel_file_path)

#     # Strip whitespace from column names
#     df.columns = df.columns.str.strip()

#     # Check if 'Violation Image' column exists
#     if 'Violation Image' not in df.columns:
#         return HttpResponse("The 'Violation Image' column is missing in the Excel file.")

#     # Convert 'Date' column to datetime if needed
#     if not pd.api.types.is_datetime64_any_dtype(df['Date']):
#         df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

#     # Handle POST request (for filtering based on date range)
#     if request.method == 'POST':
#         form = DateRangeForm(request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
            
#             # Filter rows based on date range
#             violations = df[(df['Date'] >= pd.Timestamp(start_date)) & (df['Date'] <= pd.Timestamp(end_date))].copy()
            
#             if violations.empty:
#                 return render(request, 'violation/no_violation.html')

#             # Prepare the graph for the selected date range
#             graph_data = create_graph(violations)

#             # Generate PDF
#             pdf_base64 = generate_pdf(violations)

#             return render(request, 'violation/report_page.html', {
#                 'graph_data': graph_data,
#                 'pdf_base64': pdf_base64,
#                 'violations': violations.to_dict('records'),
#             })
#     else:
#         form = DateRangeForm()

#         # Handle initial page load (show graph for all data)
#         graph_data = create_graph(df)

#     return render(request, 'violation/dashboard.html', {'form': form, 'graph_data': graph_data})

# # Helper function to create graph
# def create_graph(df):
#     # Safely set the 'Month' column
#     df.loc[:, 'Month'] = df['Date'].dt.month

#     # Group by month and count violations
#     monthly_counts = df['Month'].value_counts().sort_index()

#     # Calculate total violations and percentages
#     total_violations = monthly_counts.sum()
#     monthly_percentages = (monthly_counts / total_violations) * 100

#     # Prepare data for plotting
#     months = monthly_counts.index
#     counts = monthly_counts.values
#     percentages = monthly_percentages.values

#     # Create a figure with two y-axes
#     plt.switch_backend('Agg')
#     fig, ax1 = plt.subplots(figsize=(12, 6))

#     # Plot counts on the primary y-axis
#     color = 'tab:blue'
#     ax1.set_xlabel('Month')
#     ax1.set_ylabel('Number of Violations', color=color)
#     bars = ax1.bar(months, counts, color=color, alpha=0.6, label='Count')
#     ax1.tick_params(axis='y', labelcolor=color)

#     # Create a secondary y-axis for percentages
#     ax2 = ax1.twinx()
#     color = 'tab:red'
#     ax2.set_ylabel('Percentage of Violations (%)', color=color)
#     line = ax2.plot(months, percentages, color=color, marker='o', label='Percentage')
#     ax2.tick_params(axis='y', labelcolor=color)

#     # Set titles and labels
#     ax1.set_title('Monthly Violations with Percentages')
#     ax1.set_xticks(months)
#     ax1.set_xticklabels([calendar.month_name[i] for i in months])

#     # Add legends
#     ax1.legend(loc='upper left')
#     ax2.legend(loc='upper right')

#     # Save the graph to a BytesIO object
#     graph_buffer = BytesIO()
#     plt.savefig(graph_buffer, format='png')
#     plt.close()
#     graph_buffer.seek(0)
#     graph_data = base64.b64encode(graph_buffer.read()).decode('utf-8')

#     return graph_data

# # Helper function to generate PDF
# def generate_pdf(violations):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font('Arial', 'B', 16)
#     pdf.cell(200, 10, 'Violation Report', ln=True, align='C')

#     # Add column headers
#     pdf.set_font('Arial', 'B', 12)
#     headers = ['ID', 'Date', 'Time', 'Camera Number', 'Violation Image']
#     for header in headers:
#         pdf.cell(40, 10, header, border=1)
#     pdf.ln(10)

#     # Add violation data
#     for _, row in violations.iterrows():
#         pdf.cell(40, 10, str(row['ID']), border=1)
#         pdf.cell(40, 10, str(row['Date']), border=1)
#         pdf.cell(40, 10, str(row['Time']), border=1)
#         pdf.cell(40, 10, str(row['Camera Number']), border=1)

#         # Check and embed the violation image
#         violation_image_name = row['Violation Image']
#         violation_image_path = f"C:\\Users\\Pankaj Kumar Dubey\\Desktop\\report\\myproject\\violation\\uploaded_images\\images\\{violation_image_name}"

#         if pd.notna(violation_image_name) and os.path.exists(violation_image_path):
#             try:
#                 # Open and resize the image
#                 image = Image.open(violation_image_path)
#                 image.thumbnail((200, 150))  # Resize to fit in the PDF

#                 # Save the image to a temporary path
#                 temp_img_path = os.path.join(settings.MEDIA_ROOT, f'tmp_{violation_image_name}')
#                 image.save(temp_img_path)

#                 # Embed the image in the PDF
#                 pdf.image(temp_img_path, x=pdf.get_x(), y=pdf.get_y(), w=40, h=30)
#                 pdf.ln(30)  # Move to the next line after the image

#                 # Remove the temporary image file after use
#                 os.remove(temp_img_path)

#             except Exception as e:
#                 pdf.cell(40, 10, f"Error loading image: {e}", border=1)
#         else:
#             pdf.cell(40, 10, "No image available", border=1)
#         pdf.ln(10)

#     # Save PDF to a BytesIO object
#     pdf_output = pdf.output(dest='S').encode('latin1')

#     # Convert the PDF content to a base64 string for rendering
#     pdf_base64 = base64.b64encode(pdf_output).decode('utf-8')

#     return pdf_base64
# def no_violation(request):
#     return render(request, 'violation/no_violation.html')













# import pandas as pd
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .forms import DateRangeForm
# from fpdf import FPDF
# import os
# from django.conf import settings
# from io import BytesIO
# from PIL import Image

# def dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('login')

#     if request.method == 'POST':
#         form = DateRangeForm(request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']

#             # Load Excel file
#             excel_file_path = "C:\\Users\\Pankaj Kumar Dubey\\Downloads\\bb.xlsx" 
#             # Update with the correct path
#             df = pd.read_excel(excel_file_path)

#             # Convert 'Date' column to datetime if needed
#             if not pd.api.types.is_datetime64_any_dtype(df['Date']):
#                 df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

#             # Filter rows based on date range
#             violations = df[(df['Date'] >= pd.Timestamp(start_date)) & (df['Date'] <= pd.Timestamp(end_date))]

#             if violations.empty:
#                 return render(request, 'violation/no_violation.html')

#             # Generate PDF
#             pdf = FPDF()
#             pdf.add_page()
#             pdf.set_font('Arial', 'B', 16)
#             pdf.cell(200, 10, 'Violation Report', ln=True, align='C')

#             # Add column headers
#             pdf.set_font('Arial', 'B', 12)
#             headers = ['ID', 'Date', 'Time', 'Camera Number', 'Violation']
#             for header in headers:
#                 pdf.cell(40, 10, header, border=1)
#             pdf.ln(10)

#             # Add violation data and handle images from the C drive
#             for _, row in violations.iterrows():
#                 pdf.cell(40, 10, str(row['ID']), border=1)
#                 pdf.cell(40, 10, str(row['Date']), border=1)
#                 pdf.cell(40, 10, str(row['Time']), border=1)
#                 pdf.cell(40, 10, str(row['Camera Number']), border=1)

#                 # Get the image path from the C drive
#                 violation_image_name = row['Violation Image']
#                 violation_image_path = f"C:\\Users\\Pankaj Kumar Dubey\\Desktop\\report\\myproject\\violation\\uploaded_images\\images\\{violation_image_name}"

#                 if pd.notna(violation_image_name) and os.path.exists(violation_image_path):
#                     try:
#                         # Open and resize the image
#                         image = Image.open(violation_image_path)
#                         image.thumbnail((200, 150))  # Resize to fit in the PDF

#                         # Save the image to a temporary path (Optional, can embed directly)
#                         temp_img_path = os.path.join(settings.MEDIA_ROOT, f'tmp_{violation_image_name}')
#                         image.save(temp_img_path)

#                         # Embed the image in the PDF
#                         pdf.image(temp_img_path, x=pdf.get_x(), y=pdf.get_y(), w=40, h=30)
#                         pdf.ln(30)  # Move to the next line after the image

#                         # Remove the temporary image file after use
#                         os.remove(temp_img_path)

#                     except Exception as e:
#                         pdf.cell(40, 10, f"Error loading image: {e}", border=1)
#                 else:
#                     pdf.cell(40, 10, "No image available", border=1)
#                 pdf.ln(10)

#             # Prepare PDF response
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="violation_report.pdf"'
#             response.write(pdf.output(dest='S').encode('latin1'))

#             return response

#     else:
#         form = DateRangeForm()

#     return render(request, 'violation/dashboard.html', {'form': form})

# def no_violation(request):
#     return render(request, 'violation/no_violation.html')



