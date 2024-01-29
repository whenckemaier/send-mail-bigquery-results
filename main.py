import requests
import datetime
from google.cloud import bigquery

def main(request):
    # Configurações do BigQuery
    project_id = "project-id"
    query = "minha-query"

    # Executa a query no BigQuery
    results = run_bigquery_query_internal(project_id, query)

    # Cria HTML a partir dos resultados da query
    html_table = create_html_table_from_query_results(results)

    # Monta o corpo do e-mail
    current_date = datetime.datetime.now().strftime("%d/%m")
    body = f"<p>Relatório sobre o uso das APIs no dia {current_date}:</p>{html_table}"

    # Configurações do Mailgun
    api_key = "chave-api-mailgun"
    domain = "domain.com"
    sender_email = "send@domain.com"
    receiver_emails = ["receiver@domain.com", "receiver2@domain.com"]
    subject = "BigQuery Query Result"

    # Envia o e-mail usando Mailgun
    responses = send_email(api_key, domain, sender_email, receiver_emails, subject, body)

    # Verifica o resultado da solicitação
    success_responses = [response for response in responses if response.get("status_code") == 200]

    if success_responses:
        return "E-mail enviado com sucesso!"
    else:
        return f"Erro ao enviar o e-mail. Códigos de status: {[response.get('status_code') for response in responses]}\n{[response.get('text') for response in responses]}"

def run_bigquery_query_internal(project_id, query):
    client = bigquery.Client(project=project_id)
    query_job = client.query(query)
    results = query_job.result()
    return results

def create_html_table_from_query_results(results):
    html_table = "<table border='1'><tr>"
    
    # Adicionar cabeçalhos da tabela
    for field in results.schema:
        html_table += f"<th>{field.name}</th>"
    html_table += "</tr>"
    
    # Adicionar linhas da tabela
    for row in results:
        html_table += "<tr>"
        for value in row:
            html_table += f"<td>{value}</td>"
        html_table += "</tr>"
    
    html_table += "</table>"
    return html_table

def send_email(api_key, domain, sender_email, receiver_emails, subject, body):
    url = f"https://api.mailgun.net/v3/{domain}/messages"
    auth = ("api", api_key)

    responses = []

    for receiver_email in receiver_emails:
        data = {
            "from": sender_email,
            "to": receiver_email,
            "subject": subject,
            "html": body
        }

        try:
            response = requests.post(url, auth=auth, data=data)
            response.raise_for_status()

            responses.append({
                "email": receiver_email,
                "status_code": response.status_code,
                "text": response.text,
                "message": "E-mail enviado com sucesso" if response.status_code == 200 else "Erro ao enviar o e-mail"
            })

        except requests.RequestException as e:
            responses.append({
                "email": receiver_email,
                "status_code": None,
                "text": str(e),
                "message": f"Erro na solicitação HTTP: {str(e)}"
            })

    return responses
