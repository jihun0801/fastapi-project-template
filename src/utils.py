import logging
import random
import string
from datetime import datetime

from pytz import timezone

logger = logging.getLogger(__name__)
alpha_num = string.ascii_letters + string.digits
korea_timezone = timezone('Asia/Seoul')


def get_kst_now() -> datetime:
    return datetime.now(korea_timezone)


def generate_random_alphanum(length: int = 20) -> str:
    return "".join(random.choices(alpha_num, k=length))
