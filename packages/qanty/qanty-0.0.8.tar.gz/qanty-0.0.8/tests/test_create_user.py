# -*- coding: UTF-8 -*-

import random
import string


def test_create_user(qanty, user):
    # Generate a random user_id
    role_id = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
    doc_id = "".join(random.choice(string.digits) for _ in range(10))

    new_user = qanty.create_user(
        user_id=user.id,
        email="test@domain.com",
        doc_id=doc_id,
        name="test",
        role_id=role_id,
        branches=["*"],
        debug=True,
    )

    assert isinstance(new_user, str)
