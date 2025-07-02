# Import tools to make the PDF
from reportlab.lib.pagesizes import letter  # Page size
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table  # PDF elements
from reportlab.lib.styles import getSampleStyleSheet  # For text formatting

class PDFExporter:
    """This class creates a PDF file with trip info"""

    def export(self, trip_data):
        """This function creates the PDF using the trip data"""

        # Make a name for the PDF using the city name
        filename = f"trip_{trip_data['destination'].replace(', ', '_')}.pdf"

        # Create the PDF document with letter size paper
        doc = SimpleDocTemplate(filename, pagesize=letter)

        # This is where we add things (title, text, table)
        story = []

        # Load default text styles (font sizes, etc.)
        styles = getSampleStyleSheet()

        # Add the main title
        story.append(Paragraph(f"Trip to {trip_data['destination']}", styles['Title']))
        story.append(Spacer(1, 20))  # Space after title

        # Add trip details (duration, type, budget)
        details = f"""
        Duration: {trip_data['duration']} days<br/>
        Type: {trip_data['trip_type']}<br/>
        Budget: ${trip_data['budget']['total']}
        """
        story.append(Paragraph(details, styles['Normal']))
        story.append(Spacer(1, 20))  # Space after details

        # Add weather title
        story.append(Paragraph("Weather Forecast", styles['Heading2']))

        # Create a table of weather data
        weather_data = [[day['date'], f"{day['temp']}°C", day['description']]
                        for day in trip_data['weather']]
        # Add table header
        weather_table = Table([['Date', 'Temp', 'Conditions']] + weather_data)
        story.append(weather_table)

        # Save and generate the PDF
        doc.build(story)

        return filename  # Return the file name of the PDF
