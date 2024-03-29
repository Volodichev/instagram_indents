from perenos_bot import main_logic
import pytest

pytestmark = pytest.mark.asyncio  # All test coroutines will be treated as marked.


async def test_main_logic():
    text = \
"""Привет!❤️

Мы уже выяснили, что нельзя использовать чужой контент без разрешения автора (если вы не с нами, скорее читайте предыдущие посты).

❓Отвечаю на возмущённые вопросы в директ по типу "Что теперь каждый раз автора искать и платить за каждую картинку?"

✅Нет! У нас тут адекватный подход! Мораль не читаю, пальцем не грожу, глаза не закатываю, а рассказываю как с авторским правом жить, чтобы и авторам и пользователям хорошо было.

Поэтому сегодня делюсь элегантным, абсолютно легальным и бесплатным способом использовать чужие фото и картинки как фантазия решит.

Подобрала фотостоки, контент с которых можно использовать в блогах в коммерческих целях бесплатно.

Не забудьте сохранить👌🏻
https://instagram.com/avtorprava"""
    result_text = \
"""Привет!❤️
⠀
Мы уже выяснили, что нельзя использовать чужой контент без разрешения автора (если вы не с нами, скорее читайте предыдущие посты).
⠀
❓Отвечаю на возмущённые вопросы в директ по типу "Что теперь каждый раз автора искать и платить за каждую картинку?"
⠀
✅Нет! У нас тут адекватный подход! Мораль не читаю, пальцем не грожу, глаза не закатываю, а рассказываю как с авторским правом жить, чтобы и авторам и пользователям хорошо было.
⠀
Поэтому сегодня делюсь элегантным, абсолютно легальным и бесплатным способом использовать чужие фото и картинки как фантазия решит.
⠀
Подобрала фотостоки, контент с которых можно использовать в блогах в коммерческих целях бесплатно.
⠀
Не забудьте сохранить👌🏻
https://instagram.com/avtorprava"""
    new_text = await main_logic(text)
    assert new_text == result_text
