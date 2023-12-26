import general, time
import linode_api4 as linode_api

def remote_update(config,keyfile):
    if config.get("ssh_port") is None:
        ssh_port = 22
    else:
        ssh_port =  config.get("ssh_port") 
    if config.get('update_script') is None:
        update_script = 'updater/remote_updates.py'
    else:
        update_script = config.get('update_script')
    
    print(f"****************** Updating {config.get('ssh_username')} *******************")
    ssh = general.create_ssh_connection(config.get('ssh_hostname'), 
                        config.get('ssh_username'),
                        keyfile,
                        port=ssh_port)
    general.execute_ssh_command(ssh, command=f"python3 {update_script}")

def wait_for_completion(polling_thread):
    print(f"waiting for completion")   
    polling_thread.start()
    start_time = time.time()
    while polling_thread.is_alive():
        elapsed_time_seconds = time.time() - start_time
        minutes, seconds = divmod(elapsed_time_seconds, 60)
        elapsed_time_formatted = f"{round(minutes)} minutes, {round(seconds)} seconds"
        print(f"Elapsed Time: {elapsed_time_formatted}", end="\r", flush=True)
    # Wait for the polling thread to finish
    print(f"Elapsed Time: {elapsed_time_formatted}", flush=True)
    polling_thread.join()
    print("Operation Complete")

def get_type_label(api_client, id):
    try:
        all_types = api_client.linode.types()
        type_mapping = {type.id: type.label for type in all_types}
        return type_mapping.get(id, f"Label for type ID {id} not found")
    except linode_api.errors.ApiError as e:
        print(f"Error during Linode API call: {e}")

def wait_for_running(api_client, linode_id, linode_name):
    while True:
        try:
            linodes = api_client.linode.instances(linode_api.Instance.label == linode_name)
        except linode_api.errors.ApiError as e:
            print(f"Error during Linode API call: {e}")

        # Parse Data
        for current_linode in linodes:
            if current_linode.id == linode_id:
                linode_instance = current_linode

        # Print the current status
        current_status = linode_instance.status
        if current_status != "running":
            print(f"Current Linode Status is '{current_status}'. Waiting for status of 'running'", end='\r', flush=True)

        # Exit the loop if the status is 'running'
        else:
            print("Linode is now running.")
            break

        # Wait for 1 second before the next iteration
        time.sleep(1)

    return current_status

def rename_linode_instance(instance, new_name):
    """
    Rename a Linode instance.

    :param instance: A linode_api4.Instance object representing the Linode instance to rename.
    :param new_name: The new name for the Linode instance.
    :param api_client: The linode_api4.Api object to use for making API calls.
    :return: True if the renaming is successful, False otherwise.
    """
    try:
        # Perform the Linode instance rename
        instance.label = new_name
        instance.save()

        # Display success message
        print(f"Linode instance {instance.id} renamed to {new_name}")
        return True
    except linode_api.ApiError as e:
        # Display error message
        print(f"Error renaming Linode instance: {e}")
        return False

def create_linode_instance(api_client, plan, region, image, linode_username, label, root_password, firewall, stackscript, booted):
    """
    Create a new Linode instance with the specified parameters.

    :param api_client: The linode_api4.Api object to use for making API calls.
    :param plan: The Linode plan ID specifying the resources for the new instance.
    :param region: The Linode region ID where the new instance will be created.
    :param image: The Linode image ID to use for the new instance.
    :param linode_username: Linode user that can access the instance. Assigns SSH Key
    :param label: The label for the new Linode instance.
    :param root_password: The root password for the new Linode instance.
    :param firewall: Optional firewall ID to assign to the new Linode instance.
    :param stackscript: Optional Stackscript ID to assign to the new Linode Instance
    :param booted: Optional Bool to keep instance powered off after provisioning
    :return: A linode_api4.Instance object representing the newly created Linode instance.
    """

    try:
        new_instance = api_client.linode.instance_create(plan,
                                                   region,
                                                   image,
                                                   None,
                                                   authorized_users=[linode_username],
                                                   label=label,
                                                   root_pass=root_password,
                                                   stackscript=stackscript,
                                                   firewall=firewall,
                                                   booted=booted)
        # Display success message
        print(f"Linode instance {new_instance.id} created successfully.")
        return new_instance
    except linode_api.ApiError as e:
        # Display error message
        print(f"Error creating Linode instance: {e}")
        return None

def get_ssh_key_id_by_label(api_client, ssh_key_label):
    """
    Get the ID of an SSH key based on its label.

    :param api_client: The linode_api4.Api object to use for making API calls.
    :param ssh_key_label: The label of the SSH key.
    :return: The ID of the SSH key, or None if not found.
    """
    try:
        # Retrieve SSH keys
        ssh_keys = api_client.profile.ssh_keys()

        # Find the SSH key with the specified label
        matching_ssh_key = next((key for key in ssh_keys if key.label == ssh_key_label), None)

        if matching_ssh_key:
            # Return the ID of the matching SSH key
            return matching_ssh_key.id
        else:
            print(f"SSH key with label '{ssh_key_label}' not found.")
            return None
    except linode_api.ApiError as e:
        # Display error message
        print(f"Error retrieving SSH keys: {e}")
        return None

def get_firewall_id_by_label(api_client, firewall_label):
    """
    Get the ID of a firewall based on its label.

    :param api_client: The linode_api4.Api object to use for making API calls.
    :param firewall_label: The label of the firewall.
    :return: The ID of the firewall, or None if not found.
    """
    try:
        # Retrieve firewalls
        firewalls = api_client.networking.firewalls()

        # Find the firewall with the specified label
        matching_firewall = next((fw for fw in firewalls if fw.label == firewall_label), None)

        if matching_firewall:
            # Return the ID of the matching firewall
            return matching_firewall.id
        else:
            print(f"Firewall with label '{firewall_label}' not found.")
            return None
    except linode_api.ApiError as e:
        # Display error message
        print(f"Error retrieving firewalls: {e}")
        return None

def get_stackscript_id_by_label_and_username(api_client, stackscript_label, stackscript_username):
    """
    Get the ID of a StackScript based on its label and username.

    :param api_client: The linode_api4.Api object to use for making API calls.
    :param stackscript_label: The label of the StackScript.
    :param stackscript_username: The username associated with the StackScript.
    :return: The ID of the StackScript, or None if not found.
    """
    try:
        # Retrieve StackScripts
        obj = linode_api.linode.StackScript
        stackscripts = api_client.linode.stackscripts(linode_api.linode.StackScript.mine==True)

        # Find the StackScript with the specified label and username
        matching_stackscript = next(
            (script for script in stackscripts if script.label == stackscript_label and script.username == stackscript_username),
            None
        )

        if matching_stackscript:
            # Return the ID of the matching StackScript
            return matching_stackscript.id
        else:
            print(f"StackScript with label '{stackscript_label}' and username '{stackscript_username}' not found.")
            return None
    except linode_api.ApiError as e:
        # Display error message
        print(f"Error retrieving StackScripts: {e}")
        return None
    
def detach_all_volumes(instance):
    # Get a list of attached volumes
    attached_volumes = instance.volumes()

    if not attached_volumes:
        print(f"No volumes attached to Linode instance {instance.id}.")
        return

    # Detach each attached volume
    for volume in attached_volumes:
        volume.detach()
        print(f"Volume {volume.id} detached from Linode instance {instance.id}.")

def attach_volume(api_client, volume_label, instance):

    # Find the volume by label
    volumes = api_client.volumes()
    for volume in volumes:
        if volume.label == volume_label:
            datavol = volume
    if not datavol:
        print(f"Volume with label '{volume_label}' not found.")
        return

    # Attach the volume to the Linode instance
    datavol.attach(instance.id)
    
    print(f"Volume '{volume_label}' attached to Linode instance {instance.id}.")

def wait_for_instance_state(api_client, linode_id, linode_name, required_state='running'):
    while True:
        try:
            linodes = api_client.linode.instances(linode_api.Instance.label == linode_name)
        except linode_api.errors.ApiError as e:
            print(f"Error during Linode API call: {e}")

        # Parse Data
        for current_linode in linodes:
            if current_linode.id == linode_id:
                linode_instance = current_linode

        # Print the current status
        current_status = linode_instance.status
        if current_status != required_state:
            print(f"Current Linode Status is '{current_status}'. Waiting for status of '{required_state}'", end='\r', flush=True)

        else:
            print(f"Linode is now {required_state}.")
            break

        # Wait for 1 second before the next iteration
        time.sleep(1)

    return current_status

def swap_ipv4_addresses(api_client, instance1, instance2):
    try:
        ipv4_address1 = instance1.ipv4[0]
        ipv4_address2 = instance2.ipv4[0]

        result = api_client.networking.ips_assign(instance1.region,
            {
            "address": ipv4_address1,
            "linode_id": instance2.id
            },
            {
            "address": ipv4_address2,
            "linode_id": instance1.id
            }
        )
        print(f"IPv4 addresses swapped between Linode instances {instance1.id} and {instance2.id}.")
    except linode_api.errors.ApiError as e:
        print(f"Error during Linode API call: {e}")