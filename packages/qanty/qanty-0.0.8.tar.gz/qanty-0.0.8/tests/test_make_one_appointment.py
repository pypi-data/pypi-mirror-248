# -*- coding: UTF-8 -*-

import datetime
import random
import string

import qanty.common.models as models


def test_make_one_appointment(qanty):
    branches = qanty.get_branches()
    assert isinstance(branches, list)

    if len(branches) > 0:
        for branch in branches:
            lines = qanty.get_lines(branch_id=branch.id, get_deleted=True)
            assert isinstance(lines, list)
            if len(lines) == 0:
                continue

            for line in lines:
                if len(line.appointment_settings.sets) == 0:
                    continue

                user_id = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(16))

                assigned_appointment = qanty.make_one_appointment(
                    branch_id=branch.id,
                    custom_branch_id=getattr(branch, "custom_id", None),
                    user_id=user_id,
                    line_id=line.id,
                    date=datetime.datetime.now().strftime("%Y-%m-%d"),
                    mobile_id=None,
                    customer_doc_type="",
                    customer_doc_id="",
                    customer_name="",
                    customer_last_name="",
                    debug=True,
                )

                assert isinstance(assigned_appointment, models.AssignedAppointment)

                break

            break
