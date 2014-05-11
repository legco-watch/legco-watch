# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'rbconfig'
# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
is_windows = (RbConfig::CONFIG['host_os'] =~ /mswin|mingw|cygwin/)

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "hashicorp/precise32"
  config.vm.hostname = "dev"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.222.4"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # If true, then any SSH connections made will enable agent forwarding.
  # Default value: false
  # config.ssh.forward_agent = true

  playbook_path = "devops/dev.yml"
  inventory_path = "devops/hosts/dev_hosts"

  if is_windows
    # Provisioning configuration for shell script.
    config.vm.provision "shell" do |sh|
      sh.path = "provision.sh"
      sh.args = playbook_path + " " + inventory_path
    end
  else
    # Provisioning configuration for Ansible (for Mac/Linux hosts).
    config.vm.provision "ansible" do |ansible|
      ansible.playbook = playbook_path
      ansible.inventory_path = inventory_path
      ansible.sudo = true
    end
  end

end
