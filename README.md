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

## Playbooks

__TODO__
