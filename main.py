from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

def luhn_check(id_num):
    """
    Validates an ID number using the Luhn algorithm (checksum).
    """
    total = 0
    reverse_digits = id_num[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 != 0:  # Double every second digit (starting from the second digit)
            n = n * 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

def validate_south_african_id(id_number):
    if len(id_number) != 13:
        return "Invalid ID: Must be 13 digits long."

    # Step 1: Birthdate validation
    try:
        birthdate = id_number[:6]  # YYMMDD format
        year = int(birthdate[:2])
        month = int(birthdate[2:4])
        day = int(birthdate[4:6])

        if not (1 <= month <= 12):
            return "Invalid ID: Month out of range."

        # Adjust year for century
        if year < 22:  # For example, 22 will be interpreted as 2022
            year += 2000
        else:
            year += 1900

        # Basic check for date validity
        datetime(year, month, day)  # Will throw error if the date is invalid
    except ValueError:
        return "Invalid ID: Date is incorrect."

    # Step 2: Gender check (7th digit)
    gender_digit = int(id_number[6])
    if gender_digit % 2 == 0:
        gender = "Female"
    else:
        gender = "Male"

    # Step 3: Citizenship check (11th digit)
    citizenship_digit = int(id_number[10])
    if citizenship_digit == 0:
        citizenship = "South African Citizen"
    elif citizenship_digit == 1:
        citizenship = "Permanent Resident"
    else:
        return "Invalid ID: Invalid citizenship digit."

    # Step 4: Validate checksum (Luhn algorithm) -- optional to allow failure
    luhn_valid = luhn_check(id_number)
    if not luhn_valid:
        luhn_message = "Luhn check failed. This ID number may not be valid."
    else:
        luhn_message = "Luhn check passed."

    # Return validation result including Luhn check status
    return f"ID: {id_number} - Valid ID: {gender}, {citizenship}. {luhn_message}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        id_number = request.form['id_number']
        validation_result = validate_south_african_id(id_number)
        return render_template_string("""
            <h1>South African ID Validator</h1>
            <form method="POST">
                <label for="id_number">Enter ID Number:</label>
                <input type="text" id="id_number" name="id_number" required>
                <button type="submit">Validate</button>
            </form>
            <p>{{ validation_result }}</p>
        """, validation_result=validation_result)
    
    return render_template_string("""
        <h1>South African ID Validator</h1>
        <form method="POST">
            <label for="id_number">Enter ID Number:</label>
            <input type="text" id="id_number" name="id_number" required>
            <button type="submit">Validate</button>
        </form>
    """)

if __name__ == "__main__":
    app.run(debug=True)
