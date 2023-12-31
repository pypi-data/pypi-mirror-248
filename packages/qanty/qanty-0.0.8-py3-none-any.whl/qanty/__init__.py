# -*- coding: UTF-8 -*-
import logging
from typing import List, Optional

import httpx
from dateutil.parser import parse

import qanty.common.models as models
import qanty.exceptions


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class Qanty:
    __url = "https://qanty.com/api"

    def __init__(self, auth_token: str, company_id: str) -> None:
        headers = {"Authorization": auth_token}
        self.client = httpx.Client(http2=True, headers=headers)
        self.company_id = company_id

    def __del__(self) -> None:
        self.client.close()

    def get_branches(self, filters: Optional[dict] = None, get_deleted: Optional[bool] = False) -> Optional[List[models.Branch]]:
        """
        Retrieves a list of branches for the company associated with this Qanty instance.

        :param filters: A dictionary of filters to apply to the branch list. Optional.
        :param get_deleted: Whether to include deleted branches in the list. Optional.
        :return: A list of Branch objects representing the branches for the company, or None if an error occurred.
        """
        url = f"{self.__url}/company/get_branches"
        try:
            response = self.client.post(url, json={"company_id": self.company_id, "filters": filters, "get_deleted": get_deleted})
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        sites = data.get("sites", [])
        output: List[models.Branch] = [models.Branch.model_validate(item) for item in sites]
        return output

    def get_lines(
        self, branch_id: str, custom_branch_id: Optional[str] = None, get_deleted: Optional[bool] = False
    ) -> Optional[List[models.Line]]:
        """
        Retrieves a list of lines for a given branch ID.

        Args:
            branch_id (str): The ID of the branch to retrieve lines for.
            custom_branch_id (Optional[str], optional): The custom ID of the branch to retrieve lines for. Defaults to None.
            get_deleted (Optional[bool], optional): Whether to include deleted lines in the response. Defaults to False.

        Returns:
            Optional[List[models.Line]]: A list of Line objects representing the lines in the branch, or None if an error occurred.
        """
        url = f"{self.__url}/branches/get_lines"
        try:
            response = self.client.post(
                url,
                json={
                    "company_id": self.company_id,
                    "branch_id": branch_id,
                    "custom_branch_id": custom_branch_id,
                    "get_deleted": get_deleted,
                },
            )
            data = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        if data.get("success") is False:
            if data.get("code") == "BRANCH_NOT_FOUND":
                raise qanty.exceptions.BranchNotFound(branch_id=branch_id)

            raise qanty.exceptions.QantyError

        lines = data.get("lines", [])
        output: List[models.Line] = [models.Line.model_validate(item) for item in lines]
        return output

    def get_users(
        self,
        user_id: str,
        filters: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        get_deleted: Optional[bool] = False,
    ) -> Optional[List[models.User]]:
        """
        Get a list of users based on the provided filters.

        Args:
            user_id (str): The user identifier.
            filters (Optional[List[str]]): A list of filters to apply to the user list.
            start_date (Optional[str]): The start date to filter users by.
            end_date (Optional[str]): The end date to filter users by.
            get_deleted (Optional[bool]): Whether or not to include deleted users in the list.

        Returns:
            Optional[List[models.User]]: A list of User objects that match the provided filters.
        """
        url = f"{self.__url}/get_users"
        try:
            response = self.client.post(
                url,
                json={
                    "company_id": self.company_id,
                    "user_id": user_id,
                    "filter": filters,
                    "start_date": start_date,
                    "end_date": end_date,
                    "get_deleted": get_deleted,
                },
            )
            data = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        if data.get("success") is False:
            if data.get("code") == "INVALID_USER_IDENTIFIER":
                raise qanty.exceptions.InvalidUserIdentifier(user_id=user_id)

            if data.get("code") == "USER_NOT_FOUND":
                raise qanty.exceptions.UserNotFound(user_id=user_id)

            raise qanty.exceptions.QantyError

        return [models.User.model_validate(item) for item in data.get("users", [])]

    def get_user(
        self,
        user_id: str,
        target_user_id: Optional[str] = None,
        target_email: Optional[str] = None,
        get_deleted: Optional[bool] = False,
    ) -> Optional[models.User]:
        """
        Retrieves a user by ID.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            Optional[models.User]: A User object representing the user, or None if an error occurred.
        """
        url = f"{self.__url}/get_user"
        try:
            response = self.client.post(
                url,
                json={
                    "company_id": self.company_id,
                    "user_id": user_id,
                    "target_user_id": target_user_id,
                    "target_email": target_email,
                    "get_deleted": get_deleted,
                },
            )
            data = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        if data.get("success") is False:
            if data.get("code") == "INVALID_USER_IDENTIFIER":
                raise qanty.exceptions.InvalidUserIdentifier(user_id=user_id)

            if data.get("code") == "USER_NOT_FOUND":
                raise qanty.exceptions.UserNotFound(user_id=user_id)

            raise qanty.exceptions.QantyError

        try:
            return models.User.model_validate(data.get("user", {}))
        except Exception as exc:
            logger.error(f"Error validating user: {exc}")
            return None

    def list_day_appointments_schedule(
        self, branch_id: str, line_id: str, day: str, custom_branch_id: Optional[str] = None
    ) -> Optional[List[models.AppointmentDaySchedule]]:
        """
        Retrieve the day schedule for a given branch and line on a specific day.

        Args:
            branch_id (str): The ID of the branch to retrieve the schedule for.
            line_id (str): The ID of the line to retrieve the schedule for.
            day (str): The day to retrieve the schedule for, in the format "YYYY-MM-DD".
            custom_branch_id (Optional[str], optional): The ID of a custom branch to retrieve the schedule for. Defaults to None.

        Returns:
            Optional[List[models.DaySchedule]]: A list of DaySchedule objects representing the appointments scheduled for the given branch and line on the given day, or None if an error occurred.
        """
        url = f"{self.__url}/appointments/list_day_schedule"
        try:
            response = self.client.post(
                url,
                json={
                    "company_id": self.company_id,
                    "branch_id": branch_id,
                    "line_id": line_id,
                    "day": day,
                    "custom_branch_id": custom_branch_id,
                },
            )
            data = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        if data.get("success") is False:
            logger.error(f"Error retrieving day schedule for branch '{branch_id}' and line '{line_id}': {data.get('msg')}")
            return None

        appointments = data.get("appointments", {})

        output: List[models.AppointmentDaySchedule] = []
        for date, slots in appointments.items():
            entry = {"date_time": parse(date), "slots": []}
            for index, details in slots.items():
                entry["slots"].append({"index": index, **details})
                try:
                    output.append(models.AppointmentDaySchedule.model_validate(entry))
                except Exception:
                    logger.error(f"Error validating appointment day schedule entry: {entry}")
                    continue

        return output

    def list_day_orders_schedule(
        self, branch_id: str, line_id: str, day: str, custom_branch_id: Optional[str] = None
    ) -> Optional[List[models.AppointmentDaySchedule]]:
        pass

    def make_one_appointment(
        self,
        branch_id: str,
        custom_branch_id: str,
        user_id: str,
        line_id: str,
        date: str,
        mobile_id: Optional[str] = None,
        customer_doc_type: Optional[str] = None,
        customer_doc_id: Optional[str] = None,
        customer_name: Optional[str] = None,
        customer_last_name: Optional[str] = None,
        debug: bool = False,
    ) -> Optional[models.AssignedAppointment]:
        """
        Makes an appointment for a customer.

        Args:
            branch_id (str): The ID of the branch where the appointment will be made.
            custom_branch_id (str): The custom ID of the branch where the appointment will be made.
            user_id (str): The ID of the user that is making the request.
            line_id (str): The ID of the line where the appointment will be made.
            date (str): The date of the appointment in the format 'YYYY-MM-DD'.
            mobile_id (str, optional): The ID of the mobile device. Defaults to None.
            customer_doc_type (str, optional): The type of document of the customer. Defaults to None.
            customer_doc_id (str, optional): The ID of the document of the customer. Defaults to None.
            customer_name (str, optional): The name of the customer. Defaults to None.
            customer_last_name (str, optional): The last name of the customer. Defaults to None.
            debug (bool, optional): Whether to enable debug mode. Defaults to False.

        Returns:
            Optional[models.AssignedAppointment]: An AssignedAppointment object if the appointment was made successfully, None otherwise.
        """

        url = f"{self.__url}/appointments/make_one"
        try:
            response = self.client.post(
                url,
                json={
                    "company_id": self.company_id,
                    "branch_id": branch_id,
                    "custom_branch_id": custom_branch_id,
                    "user_id": user_id,
                    "line_id": line_id,
                    "date": date,
                    "mobile_id": mobile_id,
                    "customer_doc_type": customer_doc_type,
                    "customer_doc_id": customer_doc_id,
                    "customer_name": customer_name,
                    "customer_last_name": customer_last_name,
                    "debug": debug,
                },
            )
            data = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        if data.get("success") is False:
            if data.get("code") == "INVALID_USER_IDENTIFIER":
                raise qanty.exceptions.InvalidUserIdentifier(user_id=user_id, branch_id=branch_id, line_id=line_id)

            if data.get("code") == "USER_NOT_FOUND":
                raise qanty.exceptions.UserNotFound(user_id=user_id)

            raise qanty.exceptions.QantyError

        try:
            assigned_appointment = data.get("assigned_appointment", {})
            return models.AssignedAppointment.model_validate(assigned_appointment)
        except Exception as exc:
            logger.error(f"Error validating assigned appointment: {exc}")
            return None

    def create_user(
        self,
        user_id: str,
        email: str,
        doc_id: str,
        name: str,
        role_id: str,
        branches: List[str],
        password: Optional[str] = None,
        doc_type: Optional[str] = None,
        doc_type_id: Optional[str] = None,
        last_name: Optional[str] = None,
        debug: Optional[bool] = False,
    ) -> Optional[str]:
        """
        Creates a new user

        Args:
            user_id (str): The user ID.
            email (str): The user's email address.
            doc_id (str): The user's document ID.
            name (str): The user's name.
            role_id (str): The user's role ID.
            branches (List[str]): A list of branches the user has access to.
            password (Optional[str], optional): The user's password. Defaults to None.
            doc_type (Optional[str], optional): The user's document type. Defaults to None.
            doc_type_id (Optional[str], optional): The user's document type ID. Defaults to None.
            last_name (Optional[str], optional): The user's last name. Defaults to None.
            debug (Optional[bool], optional): Whether to enable debug mode. Defaults to False.

        Returns:
            Optional[str]: The ID of the newly created user, or None if the user could not be created.
        """

        url = f"{self.__url}/create_user"
        try:
            response = self.client.post(
                url,
                json={
                    "company_id": self.company_id,
                    "user_id": user_id,
                    "email": email,
                    "doc_id": doc_id,
                    "name": name,
                    "role_id": role_id,
                    "branches": branches,
                    "password": password,
                    "doc_type": doc_type,
                    "doc_type_id": doc_type_id,
                    "last_name": last_name,
                    "debug": debug,
                },
            )
            data = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        if data.get("success") is False:
            if data.get("code") == "INVALID_USER_IDENTIFIER":
                raise qanty.exceptions.InvalidUserIdentifier(user_id=user_id)

            if data.get("code") == "USER_NOT_FOUND":
                raise qanty.exceptions.UserNotFound(user_id=user_id)

            raise qanty.exceptions.QantyError

        return data.get("id")

    def get_roles(
        self,
        user_id: str,
        filters: Optional[List[str]] = None,
        get_deleted: Optional[bool] = False,
    ) -> Optional[List[models.UserRole]]:
        url = f"{self.__url}/get_roles"
        try:
            response = self.client.post(
                url,
                json={
                    "company_id": self.company_id,
                    "user_id": user_id,
                    "filters": filters,
                    "get_deleted": get_deleted,
                },
            )
            data = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        if data.get("success") is False:
            raise qanty.exceptions.QantyError

        roles = data.get("roles", [])

        output: List[models.UserRole] = []
        for role in roles:
            try:
                output.append(models.UserRole.model_validate(role))
            except Exception:
                logger.error(f"Error validating user role: {role}")
                continue

        return output
