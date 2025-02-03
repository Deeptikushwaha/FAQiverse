import requests

BASE_URL = 'http://127.0.0.1:8000/api/faqs/'

def test_get_faqs():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    faqs = response.json()
    print("Total FAQs:", len(faqs))
    for faq in faqs:
        print(f"ID: {faq['id']}, Question: {faq['question']}")

def test_create_faq():
    new_faq = {
        "question": "What is REST API?",
        "answer": "REST (Representational State Transfer) is an architectural style for designing networked applications."
    }
    response = requests.post(BASE_URL, json=new_faq)
    assert response.status_code == 201
    created_faq = response.json()
    print("Created FAQ:", created_faq)

if __name__ == '__main__':
    test_get_faqs()
    test_create_faq()