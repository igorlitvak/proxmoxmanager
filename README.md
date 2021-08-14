# ProxmoxManager
## Introduction
ProxmoxManager is a smart Python wrapper for Proxmox VE API. It's purpose is to allow easy automatic management for many users with many virtual machines and LCX containers. The idea is that users from external website would unknowingly be registered in Proxmox environment, which will allow them to seamlessly use virtucal machines and containers.

ProxmoxManager is based on [proxmoxer](https://github.com/proxmoxer/proxmoxer) library and requires it as a dependency.

Required version of Python: >=3.8

## Installation
Will be added to PyPi soon

## Use
ProxmoxManager library features a ProxmoxManager class that contains all of the library's functionality. To start using it, you will need to generate public and private API keys with root access.

Creating `ProxmoxManager` instance:
```python
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
proxmox_manager.vms["vm_id"]
```

Check if VM is a template:
```python
proxmox_manager.vms["vm_id"].is_template()
```

Start VM:
```python
proxmox_manager.vms["vm_id"].start()
```

Shutdown VM with timeout of 10 seconds after which it will be stopped by force:
```python
proxmox_manager.vms["vm_id"].start(timeout=10)
```

Add permission for user to use this VM:
```python
proxmox_manager.vms["vm_id"].add_permission(user="username", role="SomeRoleName")
```

Clone VM to node with most free memory:
```python
proxmox_manager.vms["vm_id"].clone(newid="new_vm_id", newnode=proxmox_manager.nodes.choose_by_most_free_ram())
```

Delete VM:
```python
proxmox_manager.vms["vm_id"].delete()
```
