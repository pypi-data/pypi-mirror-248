import argparse, threading
import linode_api4 as linode_api
import my_functions_beatzaplenty.linode as linode

def main(api_key,linode_name,small_type,big_type,arg_direction=None,arg_monitor=False):
    ################  Static Variables ####################

        # Get script parent dir
    # parent_dir = os.path.dirname(os.path.abspath(__file__))
    # config = configparser.ConfigParser()
    # config.read(f'{parent_dir}/resize_linode_instance_config.ini')
    # default_config = config['default']
    ################## Linode Data Aquisition ###########################
    try:
        api_client = linode_api.LinodeClient(api_key)
        linodes = api_client.linode.instances(linode_api.Instance.label == linode_name)
    except linode_api.errors.ApiError as e:
        print(f"Error during Linode API call: {e}")
    try:
        if len(linodes) == 1:
            instance = linodes[0]
        else:
            raise ValueError(f"linode with label {instance.label} not found")
    except ValueError as e:
        exit(e)

####################   Parse Command line arguments ##############################
    parser=argparse.ArgumentParser()
    parser.add_argument("--up", action='store_true')
    parser.add_argument("--down", action='store_true')
    parser.add_argument("--monitor", action='store_true')
    args=parser.parse_args()

    if args.up is True or arg_direction == '--up':
        arg_direction = big_type
    if args.down is True or arg_direction == '--down':
        arg_direction = small_type
    if args.monitor or arg_monitor:
        arg_monitor = True
    else:
        arg_monitor = False
    
    #################   Perform Actions #####################
    try:
        if arg_direction is not None:
            # create event poller
            event_poller = api_client.polling.event_poller_create('linode', 
                                                                  'linode_resize',
                                                                  entity_id=instance.id)
            if arg_direction != instance.type.id:
                # Resize instance
                instance.resize(arg_direction, allow_auto_disk_resize=False)
                #Get type label for output string
                type_label = linode.get_type_label(api_client,arg_direction)
                # print resize message
                print(f"Linode instance {instance.id} with label '{instance.label}' has been resized to '{type_label}'.")
                # create polling thread
                polling_thread = threading.Thread(target=event_poller.wait_for_next_event_finished, daemon=True)
            else:
                # set type label for output string
                type_label = linode.get_type_label(api_client,arg_direction)
                # Print no action take message
                print(f"Linode instance {instance.id} with label '{instance.label}' is already sized to '{type_label}'. No Resize Performed.")
                # Create polling thread
                polling_thread = threading.Thread(target=api_client.polling.wait_for_entity_free, args=("linode",instance.id), daemon=True)
        else:
            #create polling thread
            polling_thread = threading.Thread(target=api_client.polling.wait_for_entity_free, args=("linode",instance.id), daemon=True)
    except linode_api.errors.ApiError as e:
        print(f"Error during Linode API call: {e}")

    if arg_monitor:
        linode.wait_for_completion(polling_thread,api_client,instance,instance.label)
        linode.wait_for_running(api_client,instance.id, instance.label)

if __name__ == "__main__":
    
    main(api_key=None,linode_name=None,small_type=None,big_type=None,arg_direction=None,arg_monitor=False)