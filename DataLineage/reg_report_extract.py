from py2pdf import VisioFile

#C:\\Users\\NITINS\\OneDrive - Capgemini\\CAPGEMINI\\PROJECT\\GEN AI\\DataLineage

# Open the Visio file
visio_file = VisioFile(r"C:\\Users\\NITINS\\OneDrive - Capgemini\\CAPGEMINI\\PROJECT\\GEN AI\\DataLineage\\PRA110 HBUK Data Flows Examples v3.vsdx")

# Iterate through pages and shapes
for page in visio_file.pages:
    for shape in page.shapes:
        # Extract shape name and text
        shape_name = shape.name
        shape_text = shape.text
        print(f"Shape Name: {shape_name}\nShape Text: {shape_text}\n")

# Close the Visio file
visio_file.close()
