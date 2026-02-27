import os
import openai

openai.api_key = ''  # Make sure to set your API key

def generate_rca(logs: str, metrics: str = None, alert_summary: str = None) -> str:
    """
    Generate Root Cause Analysis using LLM based on logs, metrics, and alert summary.
    """
    prompt = f"""
You are an expert site reliability engineer.
Based on the following inputs, provide a detailed root cause analysis.

Logs:
{logs}

Metrics:
{metrics or 'No metrics provided'}

Alert Summary:
{alert_summary or 'No alert summary provided'}

Provide:
- Root Cause
- Suggested Remediation
- Potential Preventive Actions
"""
    response = openai.ChatCompletion.create(
        model="gpt-5.2",  # or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500
    )
    return response['choices'][0]['message']['content']


def handle_incident(incident, diagnosis, business):
    logs = incident.get('logs', '')
    metrics = incident.get('metrics', '')
    alert_summary = incident.get('root_cause', '')
    
    # rca = generate_rca(logs, metrics, alert_summary)        
    rca = generate_rca(incident, diagnosis, business)
    
    # Attach RCA to incident record
    incident['llm_rca'] = rca
    
    # Optionally: trigger remediation steps
    print(f"RCA Generated:\n{rca}") 
    return incident