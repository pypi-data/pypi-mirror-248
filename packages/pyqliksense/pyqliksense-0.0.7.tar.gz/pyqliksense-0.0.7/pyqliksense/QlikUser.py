class QlikSenseUser:
    def __init__(self, qrs_json: dict):
        self.id = qrs_json['id']
        self.user_id = qrs_json['userId']
        self.user_directory = qrs_json['userDirectory']
        self.user_name = qrs_json['name']
        self.inactive = qrs_json['inactive']
        self.removed_externally = qrs_json['removedExternally']
        self.blacklisted = qrs_json['blacklisted']

        self.roles = set(qrs_json['roles'])
        self.attributes = self.__serialize_attributes(qrs_json['attributes'])

    def __str__(self):
        return f"QlikUser: {self.user_directory}\{self.user_name}"

    def has_role(self, role):
        return role in self.roles

    def has_attribute(self, attribute: str, value: str) -> bool:
        return (attribute in self.attributes) and (value in self.attributes[attribute])

    def get_attribute(self, attribute: str):
        return self.attributes[attribute] if attribute in self.attributes else None

    @staticmethod
    def __serialize_attributes(attributes):
        serialized_attributes: dict[str, set] = {}

        for a in attributes:
            attr_type = a['attributeType']
            attr_value = a['attributeValue']

            if attr_type not in serialized_attributes:
                serialized_attributes[attr_type] = set()

            serialized_attributes[attr_type].add(attr_value)

        return serialized_attributes




