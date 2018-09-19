# Vault Utilities

This repository contains some helper Ansible playbooks and roles to manage a
[Vault](https://www.vaultproject.io/) installation.

## Alternatives

There are other Ansible lookup plugins and modules to manage Vault. These plugins differ from this
repository in that they use the HTTP API of Vault directly. This module simply invokes the Vault
CLI.

- [Official Lookup Plugin](https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/lookup/hashi_vault.py)
- [Lookup Plugin](https://github.com/jhaals/ansible-vault)
- [Ansible Module](https://github.com/TerryHowe/ansible-modules-hashivault)

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

The semantics of where the CLI is executing will affect the Vault server address, the certificate
validation and the Vault tokens being used.

## Vault Tokens

Vault commands are executed via the Vault CLI and follow its
[token semantics](https://www.vaultproject.io/docs/commands/index.html#token-helper). In some of the
playbooks, a `token` variable is expected. This is simply equivalent to providing a token via the
`VAULT_TOKEN` environment variable.

If this is not provided, the CLI will follow its usual means of finding a token. You must remember
whether you are executing the CLI command locally on your machine or remotely on another host. The
CLI will take the tokens *locally* on wherever it is executed.

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

### `vault-init`

This role
[initialise](https://www.vaultproject.io/intro/getting-started/deploy.html#initializing-the-vault)
a new Vault server. This is the only time the Unseal key for a Vault server is ever available. If
you lose the unseal keys, you will not be able to recover the data from your Vault server.

You can use the `init.yml` playbook to use this Role.

### `vault-unseal`

This role [unseals](https://www.vaultproject.io/docs/concepts/seal.html) a Vault server with one
unseal token.

For security reasons, you generally should use the
[`vault operator unseal`](https://www.vaultproject.io/docs/commands/operator/unseal.html) command
directly. This role is provided in case you want to unseal multiple servers automatically.

### `vault-exec`

Executes any arbitrary Vault commands.

### `vault-wrtie`

Write values to any Vault path.

### `vault-audit-enable`

Enables an [audit device](https://www.vaultproject.io/docs/audit/index.html) for Vault.

## Playbooks

### Initialise Vault

The `init.yml` playbook initialises a Vault cluster. You might want to read up the
[concepts](https://www.vaultproject.io/docs/concepts/seal.html) regarding sealing and unsealing
a Vault server.

This playbook should not be executed locally, especially if your Vault remote endpoint is behind a
load balancer.

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

## Unseal Vault via Prompts

The `unseal-prompt.yml` playbook prompts for one unseal token to unseal every Vault server in your
inventory. You might want to read up the
[concepts](https://www.vaultproject.io/docs/concepts/seal.html) regarding sealing and unsealing
a Vault server. You should run this playbook as many times as needed.

This playbook will be forced to execute locally. You should provide the list of servers in the
inventory.

By default, the playbook assumes the following:

- The Vault server does not enforce client TLS authentication
- A human is manually executing the playbook to provide the unseal key.

If these assumptions do not hold, you can modify the playbook accordingly and change the variables
for the roles.

You will then need to configure the following variables:

- `port`: The port of the Vault server. Defaults to `8200`.
- `ca_cert`: Path locally to the certificate of the CA that signed the Vault server TLS certificate.
- `tls_skip_verify`: If set to True, the Vault CLI will not validate the certificate. This is not recommended.
- `tls_server_name`: The Name to use to verify the certificate. The default is `vault.service.consul`.

## Seal Servers

The `seal.yml` playbook seals servers. This will cause downtime.

By default, the playbook assumes the following:

- The Vault server does not enforce client TLS authentication

You will then need to configure the following variables:

- `token`: A Vault token.
- `address`: Address of the Vault server for the CLI to connect to.
- `ca_cert` and `ca_cert_copy`: If `ca_cert_copy` is True, then `ca_cert` is a path on the local computer of the certificate of the CA that signed the Vault server TLS certificate. Otherwise, `ca_cert` is the path on the remote server of the certificate of the CA that signed the Vault server TLS certificate.
- `tls_skip_verify`: If set to True, the Vault CLI will not validate the certificate. This is not recommended.

## LDAP Authentication

The `ldap-config.yml` playbook enables and configures Vault for LDAP authentication.

By default, the playbook assumes the following:

- The Vault server does not enforce client TLS authentication

You will then need to configure the following variables:

- `token`: A Vault token.
- `address`: Address of the Vault server for the CLI to connect to.
- `ca_cert` and `ca_cert_copy`: If `ca_cert_copy` is True, then `ca_cert` is a path on the local computer of the certificate of the CA that signed the Vault server TLS certificate. Otherwise, `ca_cert` is the path on the remote server of the certificate of the CA that signed the Vault server TLS certificate.
- `tls_skip_verify`: If set to True, the Vault CLI will not validate the certificate. This is not recommended.
- `ldap_description`: Description of the authentication method.
- `ldap_path`: Path to mount the authentication on.
- `1dap` and `ldap_local`: Refer to the playbook and Vault's LDAP documentation on the meaning of the values.

## Enable File Audit Device

The `audit-file.yml` playbook enables a file audit device for Vault.

By default, the playbook assumes the following:

- The Vault server does not enforce client TLS authentication
- [Defaults](https://www.vaultproject.io/docs/audit/file.html) for the logging device that are not exposed by the variables below are assumed.

You will then need to configure the following variables:

- `token`: A Vault token.
- `address`: Address of the Vault server for the CLI to connect to.
- `ca_cert` and `ca_cert_copy`: If `ca_cert_copy` is True, then `ca_cert` is a path on the local computer of the certificate of the CA that signed the Vault server TLS certificate. Otherwise, `ca_cert` is the path on the remote server of the certificate of the CA that signed the Vault server TLS certificate.
- `tls_skip_verify`: If set to True, the Vault CLI will not validate the certificate. This is not recommended.
- `audit_path`: Path to mount the the audit device on. Defaults to `file`.
- `audit_description`: Human friendly description of the Audit device.
- `file_path`: Path where the log file will be written to.
- `log_prefix`: A customizable string prefix to write before the actual log line

## Enable Syslog Audit Device

The `audit-syslog.yml` playbook enables a Syslog audit device for Vault.

By default, the playbook assumes the following:

- The Vault server does not enforce client TLS authentication
- [Defaults](https://www.vaultproject.io/docs/audit/syslog.html) for the logging device that are not exposed by the variables below are assumed.

You will then need to configure the following variables:

- `token`: A Vault token.
- `address`: Address of the Vault server for the CLI to connect to.
- `ca_cert` and `ca_cert_copy`: If `ca_cert_copy` is True, then `ca_cert` is a path on the local computer of the certificate of the CA that signed the Vault server TLS certificate. Otherwise, `ca_cert` is the path on the remote server of the certificate of the CA that signed the Vault server TLS certificate.
- `tls_skip_verify`: If set to True, the Vault CLI will not validate the certificate. This is not recommended.
- `audit_path`: Path to mount the the audit device on. Defaults to `file`.
- `audit_description`: Human friendly description of the Audit device.
- `syslog_facility`: The syslog facility to use.
- `syslog_tag`: The syslog tag to use.
- `log_prefix`: A customizable string prefix to write before the actual log line
