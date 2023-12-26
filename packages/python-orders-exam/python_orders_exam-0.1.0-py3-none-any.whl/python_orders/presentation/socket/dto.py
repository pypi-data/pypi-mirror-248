from dataclasses import dataclass


@dataclass
class ItemRequestDTO:
    Id: int
    Name: str
    Description: str
    Price: int
    Photo: str | None
    Count: int


@dataclass
class UserRequestDTO:
    items: list[ItemRequestDTO]
    Email: str
    Password: str


@dataclass
class SaveOrderRequestDTO:
    User: UserRequestDTO


a = {
    "User": {
        "items": [
            {
                "Id": 2,
                "Name": "test2",
                "Description": "some desc",
                "Price": 1000,
                "Photo": None,
                "Category": {"Id": 1, "Name": "q"},
                "Count": 7,
            },
            {
                "Id": 3,
                "Name": "dff",
                "Description": "dfdfd",
                "Price": 2123,
                "Photo": None,
                "Category": {"Id": 1, "Name": "q"},
                "Count": 10,
            },
        ],
        "Email": "user@user.com",
        "Password": "user",
    },
}
