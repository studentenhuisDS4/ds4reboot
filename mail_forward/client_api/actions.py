import requests, json

from ds4reboot.secret_settings import EMAIL_FORWARD_HOST_USER, EMAIL_FORWARD_HOST_PASSWORD
from mail_forward.server_client import ServerClient
from mail_forward.client_api.filter_schema import MijndomeinMailFilterSchema, ActionCmdSchema

# Skip overwriting these rules as they serve a different purpose
SKIP_FILTER = 'SKIPPED_STATIC_RULE'

DEFAULT_RULENAME_BASE = "ds4 site"
DEFAULT_FILTER = MijndomeinMailFilterSchema().load({
    'rulename': DEFAULT_RULENAME_BASE,
    'actioncmds': [],
    'test': {
        'id': 'true'
    },
    'active': True
})


def get_mijndomein_filters(client=None):
    with requests.Session() as sesh:
        if client is None:
            client = ServerClient()
            call_auth(client, sesh)

        result = client.action_list()
        if "data" not in result:
            raise Exception("data field not found in result")

        serializable_data = result["data"]
        schema = MijndomeinMailFilterSchema(data=serializable_data, many=True)
        if schema.is_valid():
            filters = schema.validated_data
            return filters
        else:
            raise Exception("ERROR validation." + str(schema.errors))


def update_mijndomein_filters(buckets):
    with requests.Session() as sesh:
        client = ServerClient()
        call_auth(client, sesh)
        all_filters = get_mijndomein_filters(client=client)

        dynamic_filters = []
        if all_filters is not None:
            dynamic_filters = [f for f in all_filters if SKIP_FILTER not in f["rulename"]]

        filter_index = 0
        filter_entries = []
        for bucket in buckets:
            action_cmds = []
            for email in bucket:
                action_cmd = ActionCmdSchema().dump({
                    'to': email,
                    'id': 'redirect'
                })
                action_cmds.append(action_cmd)

            filter_entry = dict(DEFAULT_FILTER)
            filter_entry[
                "rulename"] = DEFAULT_RULENAME_BASE + f"{filter_index * 4}"
            filter_entry["actioncmds"] = action_cmds

            if not len(action_cmds) >= 1:
                raise Exception("Action cmd list too short. Aborting.")

            # Check if there are more filters to overwrite
            if len(dynamic_filters) > filter_index:
                filter_entry["id"] = dynamic_filters[filter_index]["id"]
                filter_serializer = MijndomeinMailFilterSchema().dump(filter_entry)
                client.update_filter(filter_serializer)
            else:
                # Create new filter
                filter_serializer = MijndomeinMailFilterSchema().dump(filter_entry)
                client.new_filter(filter_serializer)

            filter_entries.append(filter_entry)
            filter_index += 1

        return filter_entries


def call_auth(client: ServerClient, session):
    client.authenticate(username=EMAIL_FORWARD_HOST_USER, password=EMAIL_FORWARD_HOST_PASSWORD, session=session)


if __name__ == '__main__':
    filterz = get_mijndomein_filters()
    print(filterz)
