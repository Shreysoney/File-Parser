from app import app
import filecmp

def test_index_page(test_client):
    """
    GIVEN a test_client Server to see successful request recieved
    WHEN Index Page is Accessed
    THEN check Request is received successfully and valid response is provided.
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Parser' in response.data
    assert b'Please Enter a Valid File' in response.data

def test_Summary_Rolling_MoM_page(test_client):
    """
    GIVEN a test_client Server to see successful request recieved
    WHEN Summary_Rolling_MoM Page is Accessed
    THEN check Request is received successfully and valid response is provided.
    """
    response = test_client.get('/allVRM')
    assert response.status_code == 200
    assert b'Data Displayed' in response.data

def test_VOC_Rolling_MoM_page(test_client):
    """
    GIVEN a test_client Server to see successful request recieved
    WHEN VOC_Rolling_MoM Page is Accessed
    THEN check Request is received successfully and valid response is provided.
    """
    response = test_client.get('/allSRO')
    assert response.status_code == 200
    assert b'Data Displayed' in response.data
