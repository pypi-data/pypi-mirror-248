from erlport.erlang import cast, call
from erlport.erlterms import Atom, Map, List
import traceback
import os
import json
import uuid


class Util:
    """The `Util` class provides utility methods that may be useful during action and service execution.


    """
    def get_id():
        """Utility method that returns a unique ID in the format used by AMPS.
        """
        return uuid.UUID(str(uuid.uuid4())).hex

    @staticmethod
    def unravel_erlport_object(result):
        if isinstance(result, List):
            return [Util.unravel_erlport_object(x) for x in result]
        elif isinstance(result, Map):
            return {k.decode(): Util.unravel_erlport_object(v) for k, v in result.items()}
        elif isinstance(result, Atom):
            return result.decode()
        elif isinstance(result, bytes):
            return result.decode()
        else:
            return result


class Logger:
    """The `Logger` class from AMPS is a utility class for logging events back to AMPS. This class should not be used directly, but rather instances of this class within Actions, Endpoints, and Services should be used.

    Usage:
    ```
    from amps import Action
    class my_action(Action):
        def action(self):
            self.logger.info("Action Execution Started")
            # Perform Action Logic Here
    ```
    """

    def __init__(self, sid="", service=None):
        self.__sid__ = sid
        self.__service__ = service

    def log(self, level: str, message: str):
        """Instance method that logs a given message with the given level.

        Args:
            level (string): The level to use when logging the given message. All valid "level" values are available in the docs for the [Logger](https://hexdocs.pm/logger/1.13/Logger.html#module-levels) Elixir library underlying this class.
            message (string): The message to log.

        Usage:
        ```
        from amps import Action
        class my_action(Action):
            def action(self):
                self.logger.log("info", "Action Execution Started")
                # Perform Action Logic Here
        ```
        """
        if self.__service__:
            self.__service__.__log__(Atom(
                bytes(level, "utf-8")), message)
        else:
            call(Atom(b'Elixir.Amps.PyHandler'), Atom(b'log'), [Atom(
                bytes(level, "utf-8")), message, [(Atom(b'sid'), self.__sid__)]])

    def info(self, message: str):
        """Instance method that logs a given message with the "info" level.

        Args:
            message (string): The message to log.

        Usage:
        ```
        from amps import Action
        class my_action(Action):
            def action(self):
                self.logger.info("Action Execution Started")
                # Perform Action Logic Here
        ```
        """
        self.log("info", message)

    def debug(self, message: str):
        """Instance method that logs a given message with the "debug" level.

        Args:
            message (string): The message to log.

        Usage:
        ```
        from amps import Action
        class my_action(Action):
            def action(self):
                # Perform Action Logic Here
                self.logger.debug("Received message")
        ```
        """
        self.log("debug", message)

    def warning(self, message: str):
        """Instance method that logs a given message with the "warning" level.

        Args:
            message (string): The message to log.

        Usage:
        ```
        from amps import Action
        class my_action(Action):
            def action(self):
                # Perform Action Logic Here
                self.logger.warning("Something minor went wrong.")
        ```
        """
        self.log("warning", message)

    def error(self, message: str):
        """Instance method that logs a given message with the "error" level.

        Args:
            message (string): The message to log.

        Usage:
        ```
        from amps import Action
        class my_action(Action):
            def action(self):
                # Perform Action Logic Here
                self.logger.error("Something major went wrong.")
        ```
        """
        self.log("error", message)


class DB:
    def __init__(self, env):
        self.env = env

    def find(self, collection, clauses={}, opts={}):
        coll = bytes(collection, "utf-8")
        collection = call(Atom(b'Elixir.AmpsUtil'), Atom(
            b'index'), [bytes(self.env, "utf-8"), coll])
        clauses = Map(clauses)
        opts = Map(opts)
        result = call(Atom(b'Elixir.Amps.PyService'),
                      Atom(b'find'), [collection, clauses, opts])
        return Util.unravel_erlport_object(result)

    def find_one(self, collection, clauses={}, opts={}):
        coll = bytes(collection, "utf-8")
        collection = call(Atom(b'Elixir.AmpsUtil'), Atom(
            b'index'), [bytes(self.env, "utf-8"), coll])
        clauses = Map(clauses)
        opts = Map(opts)
        result = call(Atom(b'Elixir.Amps.PyService'),
                      Atom(b'find_one'), [collection, clauses, opts])
        return Util.unravel_erlport_object(result)

    def create(self, collection, body):
        coll = bytes(collection, "utf-8")
        collection = call(Atom(b'Elixir.AmpsUtil'), Atom(
            b'index'), [bytes(self.env, "utf-8"), coll])
        body = Map(body)
        result = call(Atom(b'Elixir.Amps.PyService'),
                      Atom(b'create'), [collection, body])
        return Util.unravel_erlport_object(result)

    def update(self, collection, body, id):
        coll = bytes(collection, "utf-8")
        id = bytes(id, "utf-8")
        collection = call(Atom(b'Elixir.AmpsUtil'), Atom(
            b'index'), [bytes(self.env, "utf-8"), coll])
        body = Map(body)
        result = call(Atom(b'Elixir.Amps.PyService'),
                      Atom(b'update'), [collection, body, id])
        return Util.unravel_erlport_object(result)

    def delete(self, collection, id):
        coll = bytes(collection, "utf-8")
        id = bytes(id, "utf-8")
        collection = call(Atom(b'Elixir.AmpsUtil'), Atom(
            b'index'), [bytes(self.env, "utf-8"), coll])
        result = call(Atom(b'Elixir.Amps.PyService'),
                      Atom(b'delete'), [collection, id])
        return Util.unravel_erlport_object(result)


class Users:
    def __init__(self, env):
        self.env = env

    def find(self, env, clauses={}, opts={}):
        coll = bytes(collection, "utf-8")
        collection = call(Atom(b'Elixir.AmpsUtil'), Atom(
            b'index'), [bytes(self.env, "utf-8"), coll])
        clauses = Map(clauses)
        opts = Map(opts)
        result = call(Atom(b'Elixir.Amps.PyService'),
                      Atom(b'find'), [collection, clauses, opts])
        return Util.unravel_erlport_object(result)

    def find_one(self, env, clauses={}, opts={}):
        coll = bytes(collection, "utf-8")
        collection = call(Atom(b'Elixir.AmpsUtil'), Atom(
            b'index'), [bytes(self.env, "utf-8"), coll])
        clauses = Map(clauses)
        opts = Map(opts)
        result = call(Atom(b'Elixir.Amps.PyService'),
                      Atom(b'find_one'), [collection, clauses, opts])
        return Util.unravel_erlport_object(result)

    def create(self, user):
        user = Map(user)
        result = call(Atom(b'Elixir.Amps.PyService.Users'),
                      Atom(b'create'), [user, self.env])
        return Util.unravel_erlport_object(result)

    def update(self, id, body):
        user = Map(body)
        result = call(Atom(b'Elixir.Amps.PyService.Users'),
                      Atom(b'update'), [id, user, self.env])
        return Util.unravel_erlport_object(result)

    def delete(self, id):
        result = call(Atom(b'Elixir.Amps.PyService.Users'),
                      Atom(b'delete'), [id, self.env])
        return Util.unravel_erlport_object(result)

    def create_session(self, user):
        user = Map(user)
        result = call(Atom(b'Elixir.Amps.PyService.Users'),
                      Atom(b'create_session'), [user, self.env])
        return Util.unravel_erlport_object(result)

    def authenticate(self, access_token):
        result = call(Atom(b'Elixir.Amps.PyService.Users'),
                      Atom(b'authenticate'), [access_token, self.env])
        return Util.unravel_erlport_object(result)

    def renew_session(self, renewal_token):
        result = call(Atom(b'Elixir.Amps.PyService.Users'),
                      Atom(b'renew_session'), [renewal_token, self.env])
        return Util.unravel_erlport_object(result)

    def delete_session(self, access_token):
        result = call(Atom(b'Elixir.Amps.PyService.Users'),
                      Atom(b'delete_session'), [access_token, self.env])
        return Util.unravel_erlport_object(result)


class Action:
    """The `Action` class from AMPS provides a base class for actions that must be extended in a custom action. Actions can be performed by overriding the `Action.action` callback exposed by the class.

    Attributes:
        msg (dict): The msg attribute contains a python of the dictionary and the message with all of its metadata. Message data can be accessed from the msg attribute, either using the "data" key for inline data, or the "fpath" key for a path to the file containing the data.
        parms (dict): The parms attribute contains all the parameters of the configured action including any extra parameters you may have specified under the "parms" key.
        sysparms (dict): The sysparms attribute contains all useful system configuration parameters for use in actions. Currently, sysparms only contains the AMPS temporary directory under the "tempdir" key.
        extra (dict): The extra attribute contains all extra parameters configured in the action.
        provider (dict): If use_provider is true on the configured action, the provider attribute contains the provider parameters. The provider parameters are available under the parms  object as well under the "provider" key.
        logger (Logger): The logger attribute exposes a Logger object for logging events back to AMPS. Any messages logged using this object during the action execution will appear in the corresponding session logs.

    Usage:
    ```
    from amps import Action
    class my_action(Action):
        def action(self):
            # Get Message Data (This example assumes inline).
            data = self.msg["data"]
            # Perform Action Logic Here
            if success:
                self.logger.info("Successfully Processed Message")
                return Action.send_status("completed")
            else:
                self.logger.warn("Failed to process message")
                return Action.send_status("failed", "Reason for Failure")
    ```
    """

    def __init__(self, msgdata):
        msgdata = json.loads(msgdata)
        self.msg = msgdata["msg"]
        self.parms = msgdata["parms"]
        self.sysparms = msgdata["sysparms"]
        self.extra = self.parms["parms"]
        self.env = self.parms["env"]
        self.db = DB(self.env)
        self.users = Users(self.env)

        if self.parms["use_provider"]:
            self.provider = self.parms["provider"]
        if self.msg.get("sid"):
            self.logger = Logger(sid=self.msg["sid"])
        else:
            self.logger = Logger()

    def __run__(self):
        try:
            response = self.action()
        except Exception as e:
            response = {"error": True, "reason": traceback.format_exc()}
        return json.dumps(response)

    def action(self):
        """Callback to override in order to perform action logic in a class that extends `Action`.

        Relevant message data is available via the attributes available on the self object. It expects the method to return a python dictionary with at least a "status" key with the status of the action execution. If the action execution is unsuccessful, a "reason" key can also be returned along with an unsuccessful status. If a new message is intended to be created by this action, it is also expected that a "msg" key will be returned with a dictionary object containing either a "data" key with inline data or an "fpath" key containing the file path to the message. Similarly, actions used in Endpoints can return a "response" object with the response status code specified under the "code" key, and the response body provided via either the "data" or "fpath" key. The action method is automatically wrapped in a try-except block when it is called, so is unnecessary to wrap the overall method in a try-except block. If you wish to have more granular visibility over errors that arise in your actions, feel free to use try-except blocks at various steps throughout action execution to allow for logging specific reasons for failure. To simplify action creation and handling, a number of helper methods are exposed by the class as static methods.

        Usage:
        ```
        from amps import Action
        class my_action(Action):
            def action(self):
                # Perform Action Logic Here
                if success:
                    return Action.send_status("completed")
                else:
                    return Action.send_status("failed", "Reason for Failure")
        ```
        """
        return {"status": "completed"}

    def get_data(self):
        """Convenience method to read get string data from message.

        Returns either the inline message data stored on the "data" key or the data stored in the message's file via the "fpath" key.
        Usage:
        ```
        from amps import Action
        class my_action(Action):
            def action(self):
                # Perform Action Logic Here
                data = self.get_data()
                # Use data here
                if success:
                    return Action.send_status("completed")
                else:
                    return Action.send_status("failed", "Reason for Failure")
        ```
        """
        if self.msg.get("data"):
            return self.msg["data"]
        else:
            return open(self.msg["fpath"]).read()

    @staticmethod
    def send_async(status, key, data):
        """Static method for creating a dictionary with the provided status and an async key with the provided data for asynchronously returning from an API endpoint.

        Args:
            status (string): The Action status to log.
            key (string): The key to use for this data when returning the json object.
            data (string || dict): Either a string containing the response data or a dictionary which will be JSON encoded and return.

        This convenience method allows for returning data asynchronously from a script when used in an API Endpoint-triggered topic workflow.

        Usage:
        ```
        from amps import Action
        class my_action(Action):
            def action(self):
                # Perform Action Logic Here
                if success:
                    return Action.send_async("completed", "Hello, this is my async response.")
                else:
                    return Action.send_status("failed", "Reason for Failure")
        ```
        """
        return {"status": status, "async": {key: data}}

    @staticmethod
    def send_status(status: str, reason: str = None):
        """Static method for creating a dictionary with the provided status and optional reason for returning in the `action` callback.

        Args:
            status (string): The Action status to log.
            reason (string): An optional reason to provide along with the given status.

        Usage:
        ```
        from amps import Action
        class my_action(Action):
            def action(self):
                # Perform Action Logic Here
                if success:
                    return Action.send_status("completed")
                else:
                    return Action.send_status("failed", "Reason for Failure")
        ```
        """
        if reason:
            return {"status": status, "reason": reason}
        else:
            return {"status": status}

    @staticmethod
    def send_file(status: str, fpath: str, meta: dict = {}):
        """Static method for creating a dictionary with the provided status and a new message from the provided fpath and additional metadata for returning in the `Action.action` callback.

        Args:
            status (string): The Action status to log.
            fpath (string): A filepath to a file containing the message data.
            meta (dict): An optional dictionary containing additional metadata to add to the new message.

        This convenience method allows for the creation of a new message using the file specified in `fpath` and any additional metadata supplied in `meta`. File Size (fsize) and File Name (fname) are automatically retrieved from the given file.

        Usage:
        ```
        from amps import Action
        class my_action(Action):
            def action(self):
                # Perform Action Logic Here
                if success:
                    return Action.send_file("completed", "path/to/file", {"partner": "companyX"})
                else:
                    return Action.send_status("failed", "Reason for Failure")
        ```
        """
        fname = os.path.basename(fpath)
        fsize = os.path.getsize(fpath)
        msg = {**{"fname": fname, "fsize": fsize, "fpath": fpath}, **meta}
        return {"status": status, "msgs": [msg]}
    
    def send_files(status: str, files: list):
        """Static method for creating a dictionary with the provided status and new messages from the provided dicts with fpaths and additional metadata for returning in the `Action.action` callback.

        Args:
            status (string): The Action status to log.
            files (list): A list of dicts containing an fpath (string) with a path to the file and an optional meta (dict) containing additional metadata.

        This convenience method allows for the creation of new messages using the a list of files with specified `fpath`s and any additional metadata supplied in `meta`. File Size (fsize) and File Name (fname) are automatically retrieved from the given files.

        Usage:
        ```
        from amps import Action
        class my_action(Action):
            def action(self):
                # Perform Action Logic Here
                if success:
                    return Action.send_file("completed", [{"fpath": path/to/file", "meta": {"partner": "companyX"}}])
                else:
                    return Action.send_status("failed", "Reason for Failure")
        ```
        """
        msgs = []
        for file in files:
            fname = os.path.basename(file["fpath"])
            fsize = os.path.getsize(file["fpath"])
            if file.get("meta"):
                meta = file["meta"]
            else:
                meta = {}
            msgs.append({**{"fname": fname, "fsize": fsize, "fpath": file["fpath"]}, **meta})
        return {"status": status, "msgs": msgs}


    @staticmethod
    def send_data(status: str, data: str, meta: dict = {}):
        """Static method for creating a dictionary with the provided status and a new message with the provided inline data and additional metadata for returning in the `action` callback.

        Args:
            status (string): The Action status to log.
            fpath (string): A string containing the message data.
            meta (dict): An optional dictionary containing additional metadata to add to the new message.

        This convenience method allows for the creation of a new message using the inline data specified in `data` and any additional metadata supplied in `meta`.

        Usage:
        ```
        from amps import Action
        class my_action(Action):
            def action(self):
                # Perform Action Logic Here
                if success:
                    return Action.send_data("completed", "Hello, this is my inline data.", {"partner": "companyX"})
                else:
                    return Action.send_status("failed", "Reason for Failure")
        ```
        """
        msg = {**{"data": data}, **meta}
        return {"status": status, "msgs": [msg]}

    @staticmethod
    def send_error(reason: str):
        """Static method for handling errors by creating a dictionary with a ``failed`` status and the provided reason for returning in the `Action.action` callback.

        Args:
            reason (string): The reason for the action failure.

        This convenience method allows for the quick handling of error using the default ``failed`` status along with the reason specified in :param`reason`.

        Usage:
        ```
        from amps import Action
        class my_action(Action):
            def action(self):
                # Perform Action Logic Here
                if success:
                    return Action.send_status("completed")
                else:
                    return Action.send_error("Reason for Failure")
        ```
        """
        return {"status": "failed", "reason": reason}


class Endpoint(Action):
    """The `Endpoint` class from AMPS extends the `Action` class to provide additional convenience in setting up API endpoint actions. Like regular actions, endpoint actions can be performed by overriding the `Action.action` callback exposed by the class.

    Attributes:
        msg (dict): The msg attribute contains a python of the dictionary and the message with all of its metadata. Message data can be accessed from the msg attribute, either using the "data" key for inline data, or the "fpath" key for a path to the file containing the data.
        parms (dict): The parms attribute contains all the parameters of the configured action including any extra parameters you may have specified under the "parms" key.
        sysparms (dict): The sysparms attribute contains all useful system configuration parameters for use in actions. Currently, sysparms only contains the AMPS temporary directory under the "tempdir" key.
        provider (dict): If use_provider is true on the configured action, the provider attribute contains the provider parameters. The provider parameters are available under the parms  object as well under the "provider" key.
        logger (Logger): The logger attribute exposes a Logger object for logging events back to AMPS. Any messages logged using this object during the action execution will appear in the corresponding session logs.
        path_params (dict): The path_params attribute contains any parameters that were passed to the endpoint via the URL. It is also available on the `msg` attribute via the "path_params" key.
        query_params (dict): The query_params attribute contains any parameters that were passed to the endpoint via the query parameters. It is also available on the `msg` attribute via the "query_params" key.

    Unlike actions, which are typically performed asynchronous via topic workflows, because Endpoints are called synchronously, if the endpoint action executes successfully, but produces an erroneous state, the action should return a successful status with the appropriate error code and response body under the "response" key.

    Usage:
    ```
    from amps import Endpoint
    class my_endpoint(Endpoint):
        def action(self):
            # Perform Endpoint Logic Here
            if success:
                return Endpoint.send_resp_file("path/to/file", 200)
            else:
                return Endpoint.send_resp_data("File not found.", 404)
    ```
    """

    def __init__(self, msgdata):
        super().__init__(msgdata)
        self.path_params = self.msg.get("path_params")
        self.query_params = self.msg.get("query_params")

    def send_resp_data(data: str, code: int):
        """Static method for creating a dictionary with the provided inline data and status code in the "response" object for returning in the `Action.action` callback.

        Args:
            data (string): The inline data to supply in the response body.
            code (integer): An integer containing the response status code to set.

        Usage:
        ```
        from amps import Endpoint
        import json
        class my_endpoint(Endpoint):
            def action(self):
                # Perform Endpoint Logic Here
                if success:
                    return Endpoint.send_resp_data(json.dumps({"id": 1, "name": "Test User"}), 200)
                else:
                    return Endpoint.send_resp_data("User not found.", 404)
        ```
        """
        return {"status": "completed", "response": {"data": data, "code": code}}

    def send_resp_file(fpath, code):
        """Static method for creating a dictionary with the provided file path and status code in the "response" object for returning in the `Action.action` callback.

        Args:
            fpath (string): The path to file to send in the response body.
            code (integer): An integer containing the response status code to set.

        This convenience method allows for the convenient sending of a file in the response of a request along with the specified status code.

        Usage:
        ```
        from amps import Endpoint
        class my_endpoint(Endpoint):
            def action(self):
                # Perform Endpoint Logic Here
                if success:
                    return Endpoint.send_resp_file("path/to/file", 200)
                else:
                    return Endpoint.send_resp_data("File not found.", 404)
        ```
        """
        return {"status": "completed", "response": {"fpath": fpath, "code": code}}


responses = {}


class Service:
    """The `Service` class from AMPS provides a base class for custom python services that can be managed by AMPS, and act as both consumers of messages and producers of new messages.

    Attributes:
        parms (dict): The parms attribute contains all the parameters of the configured service.
        sysparms (dict): The sysparms attribute contains all useful system configuration parameters for use in services. Currently, sysparms only contains the AMPS temporary directory under the "tempdir" key.
        config (dict): The config attribute contains all the custom configuration provided when creating the service. All config is also available in the parms attribute under the "config" key.
        logger (Logger): The logger attribute exposes a Logger object for logging events back to AMPS. Any messages logged using this object during the message handling or creation will appear in the corresponding session logs.
        env (string): The name of the AMPS environment in which this service is running.

    The `Service` class provides even more flexibility than the `Action` class in extending the functionality of AMPS. Unlike actions which are run and stopped, services can manage processes such as consumers/subscribers, web servers and sockets, etc, allowing the service to consume messages from and produce messages to AMPS.

    The class exposes two callback methods, `Service.initialize` and `Service.handle_message`.
    - `initialize` can be used to perform any initialization actions and start any subprocesses. Note that any subprocesses should be started in a separate thread in order to not block the main thread.
    - `handle_message` can be used to receive messages from the topic specified in the service configuration.

    The class additionally contains two methods for creating messages, `Service.send_message` and `Service.send_new`.
    `Service.send_message` should generally be used in handle_message in order to indicate that the message being created is stemming from the received message.
    Conversely, `Service.send_new` should be used to create new messages originating from an external source, such as a web server or consumer.

    Usage:
    ```
    from amps import Service
    class my_service(Service):
        def initialize(self):
            # Start my subprocess here, potentially passing service reference to subprocess so that it can leverage `send_new`.
            # Perform any other startup logic.

        def handle_message(self, msg, logger):
            # Maybe deliver this message to my subprocess or use it to process/transform the message.
            # Send a new message stemming from this message.
            self.send_message(
                msg, {"data": "New Message Data Here", "my_custom": "metadata"})


    ```
    """

    def __init__(self, parms, sysparms, pid, env, lhandler):
        self.parms = json.loads(parms)
        self.sysparms = json.loads(sysparms)
        self.config = self.parms["config"]
        self.env = env
        self.logger = Logger(service=self)
        self.__pid__ = pid
        self.__lhandler__ = lhandler
        self.initialize()

    def __receive__(self, data):
        try:
            msg = json.loads(data)
            logger = Logger(sid=msg["sid"])

            logger.info(
                f'Message received by Custom Service {self.parms["name"]}')
            resp = self.handle_message(msg, logger)
            return (Atom(b'ok'), resp)
        except Exception as e:
            return (Atom(b'error'), str(e))

    def __response__(self, resp, id):
        global responses
        responses[id.encode("ascii")] = resp
        # f = open(id, "w").write(resp)

    def __await_response__(self, id):
        global responses
        resp = responses.get(id)
        while not resp:
            resp = responses.get(id)
        return responses.pop(id)

    def __send__(self, msg):
        cast(self.__pid__, msg)

    def __send_and_receive__(self, msg):
        id = Util.get_id().encode("ascii")
        global responses
        cast(self.__pid__, (msg, id))
        resp = self.__await_response__(id)
        return json.loads(resp)

    def __log__(self, level, msg):
        cast(self.__lhandler__, (Atom(b'log'), (level, msg)))

    def initialize(self):
        """Instance method for performing any initialization logic and starting any subprocesses.  
        Usage:
        ```
        from amps import Service
        class my_service(Service):
            def initialize(self):
                # Start my subprocess here, potentially passing service reference to subprocess so that it can leverage `send_new`.
                # Perform any other startup logic.
        ```
        """
        pass

    def send_message(self, msg: dict, newmsg: dict):
        """Instance method for sending messages transformed by the `handle_message` callback. 
        The method accepts the original message which should be provided as is, as well as the new message with any new metadata to merge with the original message. If a "data" or "fpath" value is provided, it will overwrite the inline "data" or "fpath" on the current message. New message IDs are automatically generated and added by and retuned from this method for convenience.



        Args:
            msg (dict): The original message currently being processed in `handle_message`.
            newmsg (dict): A dictionary containing any new metadata to overwrite in the outgoing message.
        Returns:
            msgid: Message ID of the newly sent message.


        Usage:
        ```
        from amps import Service
        class my_service(Service):
            def initialize(self):
                # Start my subprocess here, potentially passing service reference to subprocess so that it can leverage `send_new`.
                # Perform any other startup logic.

            def handle_message(self, msg, logger):
                # Maybe deliver this message to my subprocess or use it to process/transform the message.
                # Send a new message stemming from this message.
                self.send_message(msg, {"data": "New Message Data Here", "my_custom": "metadata"})
        ```
        """
        msgid = Util.get_id()
        newmsg['parent'] = msg['msgid']
        newmsg['msgid'] = msgid
        if "data" in newmsg:
            del msg["fpath"]
            newmsg["fsize"] = len(newmsg["data"])
        elif "fpath" in newmsg:
            del msg["data"]
            newmsg["fsize"] = os.path.getsize(newmsg["fpath"])
        call(Atom(b'Elixir.Amps.PyHandler'), Atom(b'send_message'),
             [json.dumps({**msg, **newmsg}), json.dumps(self.parms), self.env])
        return msgid

    def send_new(self, newmsg: dict, action: str, response=False, timeout=15000):
        """Instance method for sending new messages generated from an external source. 

        Args:
            newmsg (dict): A dictionary containing the new outgoing message to send. 
            action (str): The output map action to use when sending this message.
            response (boolean): Whether to wait for and receive all the outputs or results of the processing of new message.
            timeout (int): When response is True, this indicates how long to wait for a response from message processing. 

        Returns:
            response: If response is True, will return result of message processing, otherwise will return message ID of the newly sent message.

        The method accepts a new message with any additional metadata. If a "data" of "fpath" is provided, associated metadata is also generated. In order to get a result from the topic-based message processing of the new message, the response parameter can be passed as True.

        Usage:
        ```
        from amps import Service
        class my_service(Service):
            def initialize(self):
                # Start my subprocess here, potentially passing service reference to subprocess so that it can leverage `send_new`.
                # Perform any other startup logic.

            def my_custom_function(self):
                # Any additional method in which are you generating a new message using an external source.
                self.send_new({"data": "New Message Data Here", "my_custom": "metadata"}, "myaction_name")
        ```
        """
        msgid = Util.get_id()
        newmsg['msgid'] = msgid
        if "data" in newmsg:
            newmsg["fsize"] = len(newmsg["data"])
        else:
            newmsg["fsize"] = os.path.getsize(newmsg["fpath"])
        resp = self.__send_and_receive__((Atom(
            b'new'), json.dumps(newmsg), action, response, timeout))
        return resp

    def create_session(self, user={}):
        """Instance method for authenticating and creating a session for an AMPS user.  

        Args:
            user (dict): A dictionary with a username and password key to use for authentication.

        Returns:
            success: A boolean indicating whether the operation was succesful.
            response: Either an error message when the operation fails or a dictionary with the following keys:
                access_token (str): The access token to use to authenticate the user.
                renewal_token (str): The renewal token when renewing the user's session. 
                user (dict): A dictionary containing all the user details. 
        Usage:
        ```
        from amps import Service
        class my_service(Service):
            def my_custom_login(self, user):
                response = self.create_session(user)
                if response["success"]:
                    # Handle Success
                else:
                    # Handle Failure

        ```
        """
        resp = self.__send_and_receive__((Atom(
            b'authenticate'), json.dumps(user)))
        return resp

    def renew_session(self, renewal_token: str):
        """Instance method for renewing an AMPS user's session.

        Args:
            renewal_token (str): A string containing the renewal token received when creating or renewing the session.

        Returns:
            success: A boolean indicating whether the operation was succesful.
            response: Either an error message when the operation fails or a dictionary with the following keys:
                access_token (str): The access token to use to authenticate the user.
                renewal_token (str): The renewal token when renewing the user's session. 
                user (dict): A dictionary containing all the user details. 
        Usage:
        ```
        from amps import Service
        class my_service(Service):
            def my_renewal(self, renewal_token):
                response = self.renew_session(renewal_token)
                if response["success"]:
                    # Handle Success
                else:
                    # Handle Failure

        ```
        """
        resp = self.__send_and_receive__((Atom(
            b'renew'), renewal_token))
        return resp

    def verify(self, access_token: str):
        """Instance method for verifying an AMPS user's session. 

        Args:
            access_token (str): A string containing the current access token for the user's session

        Returns:
            user: Either a dictionary with the user data on successful verification or False for failed verification. 
        Usage:
        ```
        from amps import Service
        class my_service(Service):
            def post(self, *args):
                access_token = self.request.headers.get('Authorization')
                verified = self.verify(access_token)
                if verified:
                    # Perform Logic Here
                else:
                    # Send Error
                    self.send_error(401)

        ```
        """
        resp = self.__send_and_receive__((Atom(
            b'fetch'), access_token))
        return resp

    def delete_session(self, access_token: str):
        """Instance method for deleting an AMPS user's session. 

        Args:
            access_token (str): A string containing the current access token for the user's session

        Returns:
            success: A boolean indicating whether the operation was succesful.

        Usage:
        ```
        from amps import Service
        class my_service(Service):
            def delete(self, *args):
                access_token = self.request.headers.get('Authorization')
                resp = self.delete_session(access_token)

        ```
        """
        resp = self.__send_and_receive__((Atom(
            b'delete'), access_token))
        return resp

    def handle_message(self, msg: dict, logger: Logger):
        """Callback method for receiving messages on the configured topic. 

        Args:
            msg (dict): The msg args contains a python dictionary of the message with all of its metadata. Message data can be accessed from the msg attribute, either using the "data" key for inline data, or the "fpath" key for a path to the file containing the data. 
            logger (Logger): A logger corresponding to the currently received message. Logging event using this object will accordingly render them in the corresponding message event sessions.
        Usage:
        ```
        from amps import Service
        class my_service(Service):
            def initialize(self):
                # Start my subprocess here, potentially passing service reference to subprocess so that it can leverage `send_new`.
                # Perform any other startup logic.
        ```
        """
        return "completed"
