import simple_salesforce
from prefect.blocks.system import Secret
from cryptography.fernet import Fernet
import base64
import shortuuid
import uuid
from sellpath_test import SellPathHttpClient


# TODO: seperate it
# TODO: debug library dependency
class ClientMgr:
    def __init__(self, tenant_id):
        """
        Initialize the Client Manager with a specific tenant ID and available tools.
        """
        self.tenant_id = tenant_id
        self._available_app_type = ["apollo", "salesforce"]
        self.apollo_base_url = "https://api.apollo.io/v1"

    def health(self):
        """
        Perform a health check and print a message.
        """
        print("health check")
        return "health check"

    def get_client(self, app_id: str, app_type: str):
        """
        Get a client based on the specified app.
        Args:
            app_id (str): The short uuid from task detail context.
            app_type (str): The app for which the client is requested.
        Returns:
            object: The client instance for the specified app_type.
        Raises:
            Exception: If the app is not available.
        """
        self.secret_block_header = self._decode_short_uuid(app_id)
        app_type = app_type.lower()
        if app_type not in self._available_app_type:
            raise Exception("not available app_type")

        if app_type == "salesforce":
            return self._get_client_salesforce()

        if app_type == "apollo":
            return self._get_http_client_apollo()

        else:
            raise Exception("Shouldn't be here")

    def _get_client_salesforce(self):
        """
        Get a Salesforce client using the stored credentials.

        Returns:
            simple_salesforce.Salesforce: The Salesforce client instance.
        """
        try:
            (
                sf_username,
                sf_password,
                sf_security_token,
            ) = self._get_salesforce_credentials()
            sf = simple_salesforce.Salesforce(
                username=sf_username,
                password=sf_password,
                security_token=sf_security_token,
            )
            return sf

        except Exception as e:
            print(f"Error creating Salesforce client: {e}")
            raise e

    def _get_salesforce_credentials(self):
        """
        Get Salesforce credentials from Prefect Secrets.

        Returns:
            tuple: Tuple containing Salesforce username, password, and security token.
        """
        try:
            sf_username = Secret.load(f"{self.secret_block_header}-sf-username").get()
            sf_username = self._decrypt_data(sf_username)

            sf_password = Secret.load(f"{self.secret_block_header}-sf-password").get()
            sf_password = self._decrypt_data(sf_password)

            sf_security_token = Secret.load(f"{self.secret_block_header}-sf-security-token").get()
            sf_security_token = self._decrypt_data(sf_security_token)

            return sf_username, sf_password, sf_security_token

        except Exception as e:
            print(f"Error getting Salesforce credentials: {e}")
            raise e

    def _get_http_client_apollo(self):
        """
        Get an HTTP client for Apollo using the stored API key.

        Returns:
            function: The Apollo HTTP request function.
        """
        self.apollo_api_key = self._get_apollo_credentials()
        sellpath_http_client = SellPathHttpClient("apollo", self.apollo_api_key)
        return sellpath_http_client

    def _get_apollo_credentials(self):
        """
        Get Apollo API key from Prefect Secrets.

        Returns:
            str: Apollo API key.
        """
        try:
            apollo_api_key = Secret.load(
                f"{self.secret_block_header}-apollo-api-key"
            ).get()  # TODO: don't use hard coding. make it params
            apollo_api_key = self._decrypt_data(apollo_api_key)
        except Exception as e:
            print(f"Error getting Apollo credentials: {e}")
            raise e
        return apollo_api_key

    def _decode_short_uuid(self, short_uuid):
        """
        Decode a short UUID to its full-length representation.

        Args:
            short_uuid (str): Short UUID to decode.

        Returns:
            str: Full-length UUID.

        Note:
            Uses the `shortuuid` library for decoding.
        """
        try:
            # Attempt to decode using shortuuid
            decoded_uuid = shortuuid.decode(short_uuid)
            return decoded_uuid
        except Exception:
            try:
                uuid_obj = uuid.UUID(short_uuid)
                return str(uuid_obj)
            except Exception:
                raise Exception(f"Unable to decode short UUID: {short_uuid}")

    def _decrypt_data(self, encoded_data):
        """
        Decrypt encoded data using Fernet symmetric key encryption.

        Args:
            encoded_data (str): Encoded data to decrypt.

        Returns:
            str: Decrypted data (str).

        Note:
            Uses the `cryptography` library for Fernet encryption.
            The symmetric key is derived from the `tenant_id`.
        """
        if self.tenant_id is None:
            raise ValueError(
                "Tenant ID is required for decryption. Please provide a valid tenant ID when you make ClientMgr instance."
            )

        key = self.tenant_id
        uuid_key = key.replace("-", "")
        fernet_key = base64.urlsafe_b64encode(uuid_key.encode())
        cipher_suite = Fernet(fernet_key)
        plain_text = cipher_suite.decrypt(encoded_data)
        result = plain_text.decode("utf-8")

        return result


# Example
# if __name__ == "__main__":
#     client = ClientMgr("2c0e49a6-28f1-4dd2-80b8-372c03982b8d")
#     apollo = client.get_client("DdQCRMZggRUkj55GRHxLUc", "apollo")
#     result = apollo.get(path="auth/health")
#     print(result)
#     print(apollo.type)
#     print(type(apollo))
