# Vault Utilities

This repository contains some helper Ansible playbooks and roles to manage a
[Vault](https://www.vaultproject.io/) installation.

## Pre-requisite

- A Vault Cluster setup
- [Vault CLI](https://www.vaultproject.io/) on your machine
- Ansible 2.5

## Setting up a Vault Cluster

There are many ways to setup a Vault cluster. You can refer to Vault
[documentation](https://www.vaultproject.io/guides/index.html).

If you are using AWS, you can try the Hashicorp's
[Vault Terraform Module](https://github.com/hashicorp/terraform-aws-vault). Alternatively, you can
also try our opinionated
[Terraform module](https://github.com/GovTechSG/terraform-modules/tree/master/modules/core).

If you use Google Cloud, you can try this Hashicorp's
[module](https://github.com/hashicorp/terraform-google-vault).

If you use Azure, you can try this Hashicorp's
[module](https://github.com/hashicorp/terraform-azurerm-vault).

## Creating an Inventory

Before you can use the playbooks, you should provide an
[Ansible Inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) with
your Vault servers. The inventory file can be as simple as a line separated list of IP Addresses.

If you use our
[Terraform module](https://github.com/GovTechSG/terraform-modules/tree/master/modules/core), you
can use the
[helper script](https://github.com/GovTechSG/terraform-modules/tree/master/modules/core#post-terraforming-tasks)
to automatically generate the inventory.

## Interacting with the Vault Server

Ansible usually involves a local controlling server executing commands on a Remote server. This
usually involves opening a SSH connection to a remote server to execute commands.

For the purposes of the scripts in this repository, you can perform tasks using either by:

- Performing a SSH to one or more Vault servers and then executing the Vault CLI remotely on the Vault servers themselves using `localhost`.
- Providing a HTTPS endpoint to one or more Vault servers and then executing the task locally with the CLI using the provided address.

The `vault-env` role documented below will facilitate the kinds of connection needed.

If you intend to execute the CLI commands locally using a remote Vault server address, you might
want to add the following switches to Ansible:

```bash
ansible-playbook \
    -i "localhost", \ # Use a "localhost" Inventory
    -c local \ # Use a "local" connection
    -e "address=https://vault.example.com" \ # Provide the URL to the Vault Server
    playbook.yml
```

## Roles

### `filters`

This role contains some Ansible filters that are used by the rest of the roles.

### `vault-env`

This role sets host facts containing various
[environment variables](https://www.vaultproject.io/docs/commands/index.html#environment-variables)
that the Vault CLI will use. This fact can then be passed as
[environment variable](https://docs.ansible.com/ansible/latest/user_guide/playbooks_environment.html)
dictionary when executing the various Vault CLI commands.

Optionally, this role can also copy any necessary certificates to the remote server.

Refer to the `defaults` for the options available.

## Playbooks

### Initialise Vault

The `init.yml` playbook initialises a Vault cluster. You might want to read up the
[concepts](https://www.vaultproject.io/docs/concepts/seal.html) regarding sealing and unsealing
a Vault server.

By default, the playbook assumes the following:

- The Vault server does not enforce client TLS authentication
- Vault server is initialised with five key shares with a threshold of three.

If these assumptions do not hold, you can modify the playbook accordingly and change the variables
for the roles.

You will then need to configure the following variables:

- `address`: Address of the Vault server for the CLI to connect to.
- `ca_cert` and `ca_cert_copy`: If `ca_cert_copy` is True, then `ca_cert` is a path on the local computer of the certificate of the CA that signed the Vault server TLS certificate. Otherwise, `ca_cert` is the path on the remote server of the certificate of the CA that signed the Vault server TLS certificate.
- `tls_skip_verify`: If set to True, the Vault CLI will not validate the certificate. This is not recommended.
- `unseal_keys_output`: Directory to output the unseal keys to.
- `root_token_output`: Path to output the root tokens to.

__DO NOT__ lose the unseal keys. This is the only time in the lifetime of your Vault server where
the unseal keys are available to you. If you lose the keys, your data will be lost and
unrecoverable.

You can distribute the keys after this. You might want to consider encrypting the keys if you, for
some reason, want to check the keys into source control. You can consider using the
[`kms-aes`](https://github.com/GovTechSG/kms-aes/) utilities to encrypt your unseal keys with KMS
if you use AWS.
