from behave import given, when, then, step
import requests

api_endpoint = {}
request_headers = {}
response = {}
request_body = {}
request_data = {}
global method_type
method_type = ''

@given(u'que a URL da API é "{api_url}"')
def step_impl(context, api_url):
    api_endpoint['ENDPOINT_URL'] = api_url

@given(u'defino o parâmetro Content Type do cabeçalho como "{header_content_type}"')
def step_impl(context, header_content_type):
    request_headers['content-type'] = header_content_type

@given(u'defino o parâmetro Accept do cabeçalho como "{header_response_type}"')
def step_impl(context, header_response_type):
    request_headers['Accept'] = header_response_type

@when(u'defino a "{coluna}" e o "{valor}" como segue')
def step_impl(context, coluna, valor):
    for row in context.table:
        temp_value = row['valor']
        request_body[row['coluna']] = temp_value

@when(u'informo que o ID da publicação que quero ler é o "{post_id}"')
def step_impl(context, post_id):
    request_data['post_id_to_read'] = post_id

@when(u'informo que o ID da publicação que quero apagar é o "{post_id}"')
def step_impl(context, post_id):
    request_data['post_id_to_delete'] = post_id

@when(u'faço a requisição "{request_type}"')
def step_impl(context, request_type):
    method_type = request_type
    if request_type == 'GET':
        api_endpoint['ENDPOINT_URL'] += request_data['post_id_to_read']
        response['GET_REQUEST'] = requests.get(url=api_endpoint['ENDPOINT_URL'], headers=request_headers)
    elif request_type == 'POST':
        response['POST_REQUEST'] = requests.post(url=api_endpoint['ENDPOINT_URL'], json=request_body,
                                                 headers=request_headers)
    elif request_type == 'PUT':
        api_endpoint['ENDPOINT_URL'] += request_body['id']
        response['PUT_REQUEST'] = requests.put(url=api_endpoint['ENDPOINT_URL'], json=request_body,
                                               headers=request_headers)
    elif request_type == 'DELETE':
        api_endpoint['ENDPOINT_URL'] += request_data['post_id_to_delete']
        response['DELETE_REQUEST'] = requests.delete(url=api_endpoint['ENDPOINT_URL'], headers=request_headers)

@then(u'o código da resposta deve ser "{expected_response_code}"')
def step_impl(context, expected_response_code):
    if method_type == 'GET':
        assert response['GET_REQUEST'].status_code == int(expected_response_code)
    elif method_type == 'POST':
        assert response['POST_REQUEST'].status_code == int(expected_response_code)
    elif method_type == 'PUT':
        assert response['PUT_REQUEST'].status_code == int(expected_response_code)
    elif method_type == 'DELETE':
        assert response['DELETE_REQUEST'].status_code == int(expected_response_code)

@then(u'o conteúdo do BODY não deve estar vazio')
def step_impl(context):
    if method_type == 'GET':
        assert request_data['post_id_to_read'] in response['GET_REQUEST'].text
    elif method_type == 'POST':
        assert request_body['userId'] in response['POST_REQUEST'].text
    elif method_type == 'PUT':
        assert request_body['userId'] in response['PUT_REQUEST'].text

@then(u'o conteúdo do BODY deve estar vazio')
def step_impl(context):
    assert request_data['post_id_to_delete'] not in response['DELETE_REQUEST'].text