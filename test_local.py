import requests
from google.cloud import bigquery

def run_bigquery_query(project_id, query):
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

    for receiver_list in receiver_emails:
        data = {
            "from": sender_email,
            "to": receiver_emails,
            "subject": subject,
            "html": body
    }

    response = requests.post(url, auth=auth, data=data)
    return response

def main():
    # Configurações do BigQuery
    project_id = "project-id"
    query = "sua-query"
    
    # Configurações do Mailgun
    api_key = "api-key-mailgun"
    domain = "domian.com"
    sender_email = "send@domain.com"
    receiver_emails = ["receiver@domain.com", "receiver2@domain.com"]
    subject = "Result Query BigQuery"
    
    # Executa a query no BigQuery
    results = run_bigquery_query(project_id, query)
    
    # Cria HTML a partir dos resultados da query
    html_table = create_html_table_from_query_results(results)
    
    # Monta o corpo do e-mail
    body = f"<p>Segue o relatório sobre o uso das APIs:</p>{html_table}"
    
    # Envia o e-mail usando Mailgun
    response = send_email(api_key, domain, sender_email, receiver_emails, subject, body)
    
    # Verifica o resultado da solicitação
    if response.status_code == 200:
        print("E-mail enviado com sucesso!")
    else:
        print(f"Erro ao enviar o e-mail. Código de status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()