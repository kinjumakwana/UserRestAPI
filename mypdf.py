import requests


email = input("Enter Emailid: ")
password = input("Enter Password: ")

# Set up the API endpoint
api_endpoint = "http://127.0.0.1:8000/users/login/"

# Set up the payload with the login parameters
payload = { "email": email, "password": password}

# Make the POST request to the login endpoint
response_login = requests.post(api_endpoint, json=payload)

# Handle the response
if response_login.status_code == 200:
    # access_token = response_login.json()
    # print("Login successful. Access token:", access_token)
    # # Login was successful
    access_token = response_login.json()["token"]["access"]

    print("Login successful. Access token:", access_token)

    # Make a request to the service's API to generate the PDF
    response_u = requests.get('http://127.0.0.1:8000/users/user-pdf/',
    headers={'Authoripostzation': 'Bearer ' + access_token},
    )
    # response_u.content
    # Save the PDF to a file
    with open('pdf.pdf', 'wb') as f:
        f.write(response_u.content)
    print('PDF generated and saved successfully!')
else:
    print('There was an error generating the PDF:')
    
