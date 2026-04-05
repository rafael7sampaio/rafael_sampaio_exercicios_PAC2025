import re
from typing import Dict, List


EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
PHONE_REGEX = r'\b(?:\+351\s?)?(?:9[1236]\d{7}|2\d{8})\b'
IP_REGEX = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
DOB_REGEX = r'\b(?:0[1-9]|[12][0-9]|3[01])[/-](?:0[1-9]|1[0-2])[/-](?:19\d{2}|20\d{2})\b'
CREDIT_CARD_REGEX = r'\b(?:\d[ -]*?){13,16}\b'

FULL_NAME_REGEX = r'\b[A-ZÁÀÃÂÉÊÍÓÔÕÚÇ][a-záàãâéêíóôõúç]+(?:\s+[A-ZÁÀÃÂÉÊÍÓÔÕÚÇ][a-záàãâéêíóôõúç]+){1,3}\b'

SUSPICIOUS_PATTERNS = [
    r'palavra[- ]?passe',
    r'password',
    r'código de verificação',
    r'codigo de verificacao',
    r'envia[- ]?me o teu email',
    r'envia[- ]?me o teu número',
    r'envia[- ]?me o teu numero',
    r'cartão de crédito',
    r'cartao de credito',
    r'dados pessoais',
    r'confirma a tua conta',
    r'partilha os teus dados',
    r'manda o teu contacto',
]


def detect_personal_data(message: str) -> Dict[str, List[str]]:
    """Deteta possíveis dados pessoais numa mensagem.

    Retorna um dicionário apenas com as categorias encontradas.
    """
    findings = {
        "emails": re.findall(EMAIL_REGEX, message),
        "phones": re.findall(PHONE_REGEX, message),
        "ips": re.findall(IP_REGEX, message),
        "birth_dates": re.findall(DOB_REGEX, message),
        "credit_cards": re.findall(CREDIT_CARD_REGEX, message),
        "full_names": re.findall(FULL_NAME_REGEX, message),
    }

    return {key: value for key, value in findings.items() if value}


def contains_personal_data(message: str) -> bool:
    """Indica se a mensagem contém algum padrão de dado pessoal."""
    findings = detect_personal_data(message)
    return any(findings.values())


def detect_suspicious_social_engineering(message: str) -> List[str]:
    """Deteta padrões simples que podem indicar engenharia social."""
    matches = []
    lower_msg = message.lower()

    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, lower_msg):
            matches.append(pattern)

    request_keywords = [
        "envia", "manda", "partilha", "diz-me", "fornece", "confirma"
    ]
    personal_keywords = [
        "email", "número", "numero", "contacto", "telefone",
        "morada", "password", "palavra-passe", "cartão", "cartao"
    ]

    if any(word in lower_msg for word in request_keywords) and any(word in lower_msg for word in personal_keywords):
        matches.append("possible_data_request_pattern")

    return matches
