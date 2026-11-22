from typing import Generator
from google import genai

class GeminiChatSession:
    """
    Interactions API를 기반으로 대화 문맥(Stateful)과 실시간 스트리밍을 관리하는 세션 클래스입니다.
    """
    def __init__(self, client: genai.Client, model: str = "gemini-3.1-flash-lite"):
        self.client = client
        self.model = model
        self.previous_interaction_id: str | None = None

    def reset(self):
        """대화 기록 초기화"""
        self.previous_interaction_id = None

    def send_message_stream(self, message: str) -> Generator[str, None, None]:
        """
        사용자 메시지를 전송하고 모델의 텍스트 조각(delta)을 스트리밍 Generator로 반환합니다.
        Stateful multi-turn 방식으로 이전 대화 id(previous_interaction_id)를 연속 전달합니다.
        """
        params = {
            "model": self.model,
            "input": message,
            "stream": True,
        }
        if self.previous_interaction_id:
            params["previous_interaction_id"] = self.previous_interaction_id

        stream = self.client.interactions.create(**params)

        for event in stream:
            # event 구조 파싱: event_type 및 delta 확인
            event_type = getattr(event, "event_type", None)

            # 새 interaction ID 저장
            if event_type == "interaction.created":
                interaction_info = getattr(event, "interaction", None)
                if interaction_info and hasattr(interaction_info, "id"):
                    self.previous_interaction_id = interaction_info.id

            # 텍스트 delta 추출
            delta = getattr(event, "delta", None)
            if delta:
                delta_type = getattr(delta, "type", None)
                if delta_type == "text":
                    text = getattr(delta, "text", "")
                    if text:
                        yield text
            elif hasattr(event, "data"):
                data = event.data
                d_delta = getattr(data, "delta", None)
                if d_delta and getattr(d_delta, "type", None) == "text":
                    text = getattr(d_delta, "text", "")
                    if text:
                        yield text

