# pylint: disable=too-many-branches
#   This is fine.
#
"""
Smash command-line interface client.
"""
import json
from smash import config
from smash import smash


def json_result(result):
    """ Print result as JSON. """
    print(json.dumps(result, indent=2))


def json_error(errmsg):
    """ Print error as JSON. """
    print(f'"error":"{errmsg}"')


def print_result(result):
    """ Print result as text. """
    # result might be a list
    for item in result:
        print(item)

def print_error(errmsg):
    """ Print error as text. """
    print(f"Error: {errmsg}")


def main():
    """ Main client routine. """

    # load configuration
    # pylint: disable=invalid-name,broad-except
    try:
        conf = config.common(config.cli)

    except Exception as e:
        print(f"Could not load Smash configuration: {e}")
        return

    api = smash.ApiHandler(api_url=f"{conf['server']}/api",
        timeout=conf['request_timeout'])

    # for collecting output and result
    output = None

    # DO put this next section in a try..except thingy (maybe)
    # the idea being to capture any exceptions and output them appropriately

    # handle command
    if conf.cmd == 'get':

        output = []
        if conf.nodestatus:
            for ns in conf.nodestatus:
                if ns[1]:
                    output.append(api.get_node_status(ns[0], ns[1]))
                else:
                    output.append(api.get_node(ns[0]))
        elif conf.group_by:
            #output.append(api.get_nodes_by_attribute(conf.group_by))
            output.append(
                smash.get_nodes_by_attribute(
                    f"{conf['server']}/api", conf['request_timeout'], conf.group_by))
        else:
            output.append(smash.get_nodes(f"{conf['server']}/api", conf['request_timeout']))

# Delete operation not yet supported--requires authentication
#    elif args.cmd in ['del', 'delete']:
#
#        output = []
#        for ns in args.nodestatus:
#            if ns[1]:
#                output.append(api.delete_node_status(ns[0], ns[1]))
#            else:
#                output.append(api.delete_node(ns[0]))

    elif conf.cmd in ['ack', 'acknowledge']:
        output = api.acknowledge(conf.nodestatus[0], conf.nodestatus[1],
            conf.message, conf.state, conf.expire_after)

    elif conf.cmd == 'tag':

        output = []
        node = conf.node
        if not conf.untag:
            for markspec in conf.mark:
                output.append(api.set_attribute(node, markspec))
        else:
            for markspec in conf.markspec:
                output.append(api.clear_attribute(node, markspec))

    else:
        print_error(f"Command not recognized: {conf.cmd}")

    # handle output
    if not output:
        if conf.json:
            json_error(f"{conf.cmd} unsuccessful")
        else:
            print_error(f"{conf.cmd} unsuccessful")
    else:
        if conf.json:
            json_result(output)
        else:
            print_result(output)


# if this module was called directly
if __name__ == '__main__':
    main()
