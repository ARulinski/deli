import os
import pdfplumber
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Document
from django.shortcuts import redirect, get_object_or_404

def upload_pdf(request):
    if request.method == 'POST' and 'pdf_file' in request.FILES:
        pdf_file = request.FILES['pdf_file']

        # Save the uploaded PDF to the model
        document = Document(title=pdf_file.name)
        document.pdf.save(pdf_file.name, pdf_file, save=True)

        # Initialize the total sum and column name variables
        total_sum = 0.0 
        column_name = None  # To store the name of the third column from the end

        # Get the file path of the uploaded PDF
        pdf_path = os.path.join(settings.MEDIA_ROOT, document.pdf.name)

        # Open the PDF and process tables
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()

                if table:
                    # Get the column name from the header row (first row)
                    header_row = table[0]  # First row should be the header

                    # Ensure there are enough columns and identify the correct column
                    if len(header_row) >= 3:
                        column_name = header_row[-3]  # Name of the third column from the end

                        # Process the table rows and calculate the sum
                        for row in table[1:]:  # Skip the header row
                            try:
                                # Get the value from the third column from the end
                                value_str = row[-3]  # Adjusted column position
                                
                                # Clean and parse the value
                                if value_str:
                                    value_str = value_str.replace(',', '').replace(' ', '').strip()  # Remove commas and spaces
                                    value = float(value_str)  # Convert to float
                                    total_sum += value  # Accumulate total

                                    # Debugging output to verify each row value
                                    print(f"Adding value from row: {value}, Current Total: {total_sum}")

                            except (ValueError, IndexError) as e:
                                print(f"Error processing row {row}: {e}")

        # Save the calculated total to the Document model
        document.total_amount = total_sum
        document.save()

        # Pass the column name and total sum to the template for display
        return render(request, 'routes/upload_pdf.html', {
            'document': document,
            'column_name': column_name,
            'total_sum': total_sum,
        })

    return render(request, 'routes/upload_pdf.html')

def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()  # Deletes the document instance and file
    return redirect('upload_pdf')  # Redirect back to the upload page