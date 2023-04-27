import posthog
import os

from dotenv import load_dotenv

class LoggerManager:
    def __init__(self) -> None:
        self.posthog = posthog
        self.posthog.project_api_key = os.getenv("POSTHOG_KEY")
        self.posthog.host = 'https://app.posthog.com'
        
    
    def sendEvent(self, eventID, event):
        self.posthog.capture(eventID, event)