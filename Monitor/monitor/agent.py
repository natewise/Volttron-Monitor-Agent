"""
Agent documentation goes here.
Remember to remove and then re-add agent whenever agent source code is modified. 
--> vctl remove --tag monitor
--> python scripts/install-agent.py -s Monitor/ -c Monitor/config -t monitor
"""

__docformat__ = 'reStructuredText'

import logging
import sys
import socket
import json
import time
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, PubSub, compat, RPC

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"


def monitor(config_path, **kwargs):
    """Parses the Agent configuration and returns an instance of
    the agent created using that configuration.

    :param config_path: Path to a configuration file.

    :type config_path: str
    :returns: Monitor
    :rtype: Monitor
    """
    try:
        config = utils.load_config(config_path)
    except StandardError:
        config = {}

    if not config:
        _log.info("Using Agent defaults for starting configuration.")

    setting1 = int(config.get('setting1', 1))
    setting2 = config.get('setting2', "some/random/topic")

    return Monitor(setting1,
                   setting2,
                   **kwargs)


class Monitor(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, setting1=1, setting2="some/random/topic",
                 **kwargs):
        super(Monitor, self).__init__(**kwargs)
        _log.debug("vip_identity: " + self.core.identity)

        self.setting1 = setting1
        self.setting2 = setting2

        self.default_config = {"setting1": setting1,
                               "setting2": setting2}

        # Set a default configuration to ensure that self.configure is called immediately to setup
        # the agent.
        self.vip.config.set_default("config", self.default_config)
        # Hook self.configure up to changes to the configuration file "config".
        self.vip.config.subscribe(self.configure, actions=[
                                  "NEW", "UPDATE"], pattern="config")

    def configure(self, config_name, action, contents):
        """
        Called after the Agent has connected to the message bus. If a configuration exists at startup
        this will be called before onstart.

        Is called every time the configuration in the store changes.
        """
        config = self.default_config.copy()
        config.update(contents)

        _log.debug("Configuring Agent")

        try:
            setting1 = int(config["setting1"])
            setting2 = str(config["setting2"])
        except ValueError as e:
            _log.error("ERROR PROCESSING CONFIGURATION: {}".format(e))
            return

        self.setting1 = setting1
        self.setting2 = setting2

        # self._create_subscriptions(self.setting2)

    def _create_subscriptions(self, topic):
        # Unsubscribe from everything.
        self.vip.pubsub.unsubscribe("pubsub", None, None)

        self.vip.pubsub.subscribe(peer='pubsub',
                                  prefix=topic,
                                  callback=self._handle_publish)

    def _handle_publish(self, peer, sender, bus, topic, headers,
                        message):
        pass

    def _topic_socket(self):
        self.s = socket.socket()
        ai = socket.getaddrinfo("0.0.0.0", 8080)
        addr = ai[0][-1]
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(addr)
        self.s.listen(5)
        _log.info("Listening on " + str(addr))
        self.client = self.s.accept()
        _log.info("Connection from addr " + str(self.client[1]) + "!")
        #count = -1
        #while True: 
        #    count = count + 1
        #    self.client[0].send(json.dumps({"something":"data "+str(count)}))
        #send is now happening in the @PubSub Decorator
        #    time.sleep(5)
        #    if(count == 15):
        #        break
    
    @PubSub.subscribe('pubsub', 'heartbeat')
    def on_match(self, peer, sender, bus, topic, headers, message):
        self.client[0].send(json.dumps({"topic":topic, "peer":peer, 
                                        "sender":sender, "message":message, 
                                        "headers":headers}))
        _log.info("Heartbeat!! Inside monitor agent")
    
    @Core.receiver("onstart")
    def onstart(self, sender, **kwargs):
        """
        This is method is called once the Agent has successfully connected to the platform.
        This is a good place to setup subscriptions if they are not dynamic or
        do any other startup activities t  hat require a connection to the message bus.
        Called after any configurations methods that are called at startup.

        Usually not needed if using the configuration store.
        """
        #self._create_subscriptions("heartbeat/")
        self._topic_socket()
        # Example publish to pubsub
        #self.vip.pubsub.publish('pubsub', "heartbeat/", message="HI!")

        # Exmaple RPC call
        #self.vip.rpc.call("some_agent", "some_method", arg1, arg2)

    @Core.receiver("onstop")
    def onstop(self, sender, **kwargs):
        """
        This method is called when the Agent is about to shutdown, but before it disconnects from
        the message bus.
        """
        pass

    @RPC.export
    def rpc_method(self, arg1, arg2, kwarg1=None, kwarg2=None):
        """
        RPC method

        May be called from another agent via self.core.rpc.call """
        return self.setting1 + arg1 - arg2

    


def main():
    """Main method called to start the agent."""
    utils.vip_main(monitor,
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
