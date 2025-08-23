"""
WhatsApp Integration Script
Simula integração básica com WhatsApp Business API
"""

import requests
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class WhatsAppConnector:
    def __init__(self, webhook_url: str = "http://localhost:8000/api/whatsapp/webhook"):
        self.webhook_url = webhook_url
        self.phone_token = None  # Configure com seu token do WhatsApp Business
        self.phone_number_id = None  # Configure com seu Phone Number ID
        
    def send_message(self, to_number: str, message: str) -> bool:
        """Envia mensagem de texto para WhatsApp"""
        try:
            # Placeholder para integração real com WhatsApp Business API
            # Em produção, usar as APIs oficiais do Meta
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "text",
                "text": {"body": message}
            }
            
            # Simula envio (em produção, usar URL da API do WhatsApp)
            logger.info(f"📤 Enviando para {to_number}: {message}")
            
            # Para teste local, apenas loga
            print(f"WhatsApp -> {to_number}: {message}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return False
    
    def send_audio(self, to_number: str, audio_url: str) -> bool:
        """Envia áudio para WhatsApp"""
        try:
            payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "audio",
                "audio": {"link": audio_url}
            }
            
            logger.info(f"🔊 Enviando áudio para {to_number}")
            print(f"WhatsApp Audio -> {to_number}: {audio_url}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar áudio: {e}")
            return False
    
    def simulate_incoming_message(self, from_number: str, message: str):
        """Simula mensagem recebida do WhatsApp"""
        try:
            payload = {
                "from_number": from_number,
                "message": message,
                "message_type": "text",
                "timestamp": "2024-01-01T10:00:00Z"
            }
            
            response = requests.post(self.webhook_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Resposta recebida: {result.get('response', 'Sem resposta')}")
                return result
            else:
                print(f"❌ Erro no webhook: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao simular mensagem: {e}")
            return None

def test_whatsapp_integration():
    """Testa a integração com WhatsApp"""
    print("🧪 Testando integração WhatsApp...")
    
    connector = WhatsAppConnector()
    
    # Simula mensagens de teste
    test_messages = [
        ("5511999999999", "Olá! Como você pode me ajudar?"),
        ("5511999999999", "Qual é o status do meu pedido?"),
        ("5511999999999", "Preciso de suporte técnico")
    ]
    
    for phone, message in test_messages:
        print(f"\n📱 Simulando mensagem de {phone}: {message}")
        result = connector.simulate_incoming_message(phone, message)
        
        if result and result.get('success'):
            # Simula resposta de volta
            response_text = result.get('response', '')
            if response_text:
                connector.send_message(phone, response_text)

if __name__ == "__main__":
    test_whatsapp_integration()