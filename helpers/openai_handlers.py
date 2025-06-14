from openai import OpenAI
import base64

client = OpenAI(api_key="W")

def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def ask_ai_student(transcript_text: str, image_path: str) -> str:
    base64_image = encode_image_to_base64(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",  # Switch to the cheaper model
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a curious, friendly high school student. "
                    "You're watching a video made by your teacher about a topic. Your questions should focus on the environment first and foremost, but address what the teacher says as well."
                    "Ask one short question about what you see and hear, as if you're trying to understand the science behind it."
                    "Only respond with the question, and nothing else."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Here's what the narrator is saying:\n\n{transcript_text}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"  # Specify low detail for cost efficiency
                        }
                    }
                ]
            }
        ],
        max_tokens=100
    )

    return response.choices[0].message.content.strip()
