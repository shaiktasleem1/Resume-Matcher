import requests
import time

def wait_for_server(url, timeout=10):
    start_time = time.time()
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        if time.time() - start_time > timeout:
            return False
        time.sleep(1)

def test_homepage():
    url = "http://127.0.0.1:5000/"
    if not wait_for_server(url):
        raise Exception("Server not responding on " + url)
    response = requests.get(url)
    assert response.status_code == 200
    print("Homepage loaded successfully.")

def test_post_no_job_description():
    url = "http://127.0.0.1:5000/matcher"
    files = {}
    data = {'job_description': ''}
    response = requests.post(url, data=data, files=files)
    assert "Please enter a job description." in response.text
    print("Validation for empty job description works.")

def test_post_less_than_five_files():
    url = "http://127.0.0.1:5000/matcher"
    data = {'job_description': 'Test job description'}
    files = {
        'resumes': ('test1.txt', 'Dummy resume content', 'text/plain'),
        'resumes': ('test2.txt', 'Dummy resume content', 'text/plain'),
        'resumes': ('test3.txt', 'Dummy resume content', 'text/plain')
    }
    response = requests.post(url, data=data, files=files)
    assert "Please upload at least 5 resumes." in response.text
    print("Validation for minimum resume upload count works.")

def test_post_unsupported_file_type():
    url = "http://127.0.0.1:5000/matcher"
    data = {'job_description': 'Test job description'}
    files = {
        'resumes': ('test.unsupported', 'Dummy content', 'application/octet-stream'),
        'resumes': ('test2.txt', 'Dummy resume content', 'text/plain'),
        'resumes': ('test3.txt', 'Dummy resume content', 'text/plain'),
        'resumes': ('test4.txt', 'Dummy resume content', 'text/plain'),
        'resumes': ('test5.txt', 'Dummy resume content', 'text/plain'),
    }
    response = requests.post(url, data=data, files=files)
    assert "Unsupported file type" in response.text
    print("Validation for unsupported file type works.")

def test_post_valid():
    url = "http://127.0.0.1:5000/matcher"
    data = {'job_description': 'Software engineer with Python skills'}
    files = [
        ('resumes', ('resume1.txt', 'Experienced Python developer', 'text/plain')),
        ('resumes', ('resume2.txt', 'Java developer', 'text/plain')),
        ('resumes', ('resume3.txt', 'Python and Java developer', 'text/plain')),
        ('resumes', ('resume4.txt', 'Data scientist with Python', 'text/plain')),
        ('resumes', ('resume5.txt', 'Frontend developer', 'text/plain')),
    ]
    response = requests.post(url, data=data, files=files)
    assert "Top matching resumes" in response.text
    print("Valid resume matching works.")

if __name__ == "__main__":
    test_homepage()
    test_post_no_job_description()
    test_post_less_than_five_files()
    test_post_unsupported_file_type()
    test_post_valid()
