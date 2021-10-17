# ProxmoxManager
## Introduction
ProxmoxManager is a smart Python wrapper for Proxmox VE API. It's purpose is to allow easy automatic management for many users with many virtual machines and LXC containers. The idea is that users from external website would unknowingly be registered in Proxmox environment, which will allow them to seamlessly use virtucal machines and containers.

ProxmoxManager is based on [proxmoxer](https://github.com/proxmoxer/proxmoxer) library and requires it as a dependency.

Required version of Python: >=3.7

## Installation
```shell
pip install proxmoxmanager
```

## Useful info
Proxmox VE is a virtualization platfrom that supports both containers and virtual machines.

### Nodes
Node is a real computer on which Proxmox runs. Proxmox can run on multiple nodes which are united into cluster.

Each node has it's own unique string ID.

### Users
Proxmox VE has a complex user and permission system. There are two realms in which users are created: PAM (built-in Linux authentication, primarily used for root user) and PVE (Proxmox VE authentication).

This library only supports PVE users, because not all API features are availible for PAM users.

Usernames are unique string values in format `username@pam` or `username@pve`. Because this library only supports PVE realm, `@pve` is appended automatically to usernames.

Users are NOT linked to specific nodes, and they can have access to any VMs/containers.

### Permissions
Each user has a set of permissions, which consist of a path (e.g., `/vms/100`) and a role name (e.g. `Administrator`). Each role itself contains a set of permissions.

Proxmox allows to give root permissions (with path `/`) or permissions to all VMs/containers (with path like `/vms`), but this library for the sake of simplicity only allows to give permissions for specific user to specific VM/container.

### Virtual machines and containers
Each VM/container is located on it's own node and has a unique integer ID (100-99999999), which has to be unique for ALL the nodes.

Despite being different objects, VMs and containers cannot share the same ID.

This library allows to pass VM/container IDs both as integers and strings, but internally they are always hadnled as strings for the sake of simplicity.

## Use
ProxmoxManager library features a ProxmoxManager class that contains all of the library's functionality. To start using it, you will need to generate API key with root access and full permissions.

Creating `ProxmoxManager` instance:
```python
from proxmoxmanager import ProxmoxManager
proxmox_manager = ProxmoxManager(host="example.com:8006", user="root@pam", token_name = "TOKEN_NAME", token_value = "SECRET_VALUE")
```

`ProxmoxManager` class contains separate classes for nodes, users, virtual machines and containers, which contain methods needed for managing them.

By calling `nodes`, `users`, `vms` or `containers` field of `ProxmoxManager` object you will get a collection of respective objects that behaves like a Python dict and has some additional features.

### Example of usage for nodes
Listing all nodes:
```python
proxmox_manager.nodes
```

Accessing specific node:
```python
proxmox_manager.nodes["node_id"]
```

Randomly choosing a node (useful for distributing loads evenly):
```python
proxmox_manager.nodes.choose_at_random()
```

Choose node with most free memory (in %) and get it's id:
```python
id = proxmox_manager.nodes.choose_by_most_free_ram(absolute=False).id
```

### Example of usage for users
Listing all users:
```python
proxmox_manager.users
```

Creating new user:
```python
proxmox_manager.users.create("username", "password")
```

Accessing specific user:
```python
proxmox_manager.users["username"]
```

Getting auth and csrf tokens of user:
```python
proxmox_manager.users["username"].get_tokens("password")
```

Changing user password:
```python
proxmox_manager.users["username"].change_password("password", "better_new_password")
```

Deleting user:
```python
proxmox_manager.users["username"].delete()
```

### Example of usage for virtual machines (containers are almost exactly the same)
Listing all VMs:
```python
proxmox_manager.vms
```

Accessing specific VM:
```python
proxmox_manager.vms["100"]
```

It can also be accessed by integer ID:
```python
proxmox_manager.vms[100]
```

Check if VM is a template:
```python
proxmox_manager.vms["100"].is_template()
```

Start VM:
```python
proxmox_manager.vms["100"].start()
```

Shutdown VM with timeout of 10 seconds after which it will be stopped by force:
```python
proxmox_manager.vms["100"].start(timeout=10)
```

Add permission for user to use this VM:
```python
proxmox_manager.vms["100"].add_permission(user="username", role="SomeRoleName")
```

Clone VM to the same node and choose ID that is not taken:
```python
proxmox_manager.vms["100"].clone(newid=proxmox_manager.smallest_free_vmid())
```

Clone VM to node with most free memory:
```python
proxmox_manager.vms["100"].clone(newid="101", newnode=proxmox_manager.nodes.choose_by_most_free_ram())
```

Delete VM:
```python
proxmox_manager.vms["100"].delete()
```
