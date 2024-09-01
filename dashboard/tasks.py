import os
from celery import shared_task
from celery.utils.log import get_task_logger
from openai import OpenAI

openai_client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

logger = get_task_logger("monitor")


def contains_bad_words(text: str) -> bool:
    try:
        response = openai_client.chat.completions.create(
            messages=[
                {"role": "user", "content": f"Check if this text contains bad words '{text}'"},
            ],
            model="gpt-3.5-turbo",
        )
        response_text = response["choices"][0].message.content.strip().lower()
        return response_text == "true"
    except Exception as e:
        logger.error(f"Error checking bad words: {e}")
        return False


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def check_comment(self, comment_id: int) -> None:
    from dashboard.models import Comment
    try:
        comment = Comment.objects.get(id=comment_id)
        contains_forbidden_words = contains_bad_words(comment.text)

        if contains_forbidden_words:
            logger.info(f"Detected forbidden words in comment with ID {comment_id}!")
            comment.delete()
    except Comment.DoesNotExist:
        logger.warning(f"Comment with ID {comment_id} does not exist.")
    except Exception as exc:
        logger.error(f"Error processing comment ID {comment_id}: {exc}")
        self.retry(exc=exc)
