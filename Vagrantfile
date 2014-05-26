# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'rbconfig'
# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
$is_windows = (RbConfig::CONFIG['host_os'] =~ /mswin|mingw|cygwin/)

def provision(box, playbook, hosts)
  # Run the shell provisioner with a specified playbook and inventory

  playbook_path = "devops/" + playbook
  inventory_path = "devops/" + hosts

  if $is_windows
    # Provisioning configuration for shell script.
    box.vm.provision "shell" do |sh|
      sh.path = "provision.sh"
      sh.args = playbook_path + " " + inventory_path
    end
  else
    # Provisioning configuration for Ansible (for Mac/Linux hosts).
    box.vm.provision "ansible" do |ansible|
      ansible.playbook = playbook_path
      ansible.inventory_path = inventory_path
      ansible.sudo = true
    end
  end
end

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "default" do |dev|
    # Dev box
    dev.vm.box = "hashicorp/precise32"
    dev.vm.hostname = "dev"

    dev.vm.network "private_network", ip: "192.168.221.3"

    dev.vm.provider "virtualbox" do |v|
      v.memory = 1024
      v.cpus = 2
      v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
    end

    dev.vm.synced_folder ".", "/vagrant",
      type: "rsync",
      rsync__exclude: [".idea/"],
      rsync__auto: true,
      rsync__args: ["--verbose", "--archive", "-z", "--chmod=0664"]

    provision(dev, "dev.yml", "dev.hosts")
  end

  config.vm.define "stage", autostart: false do |stage|
    # Staging environment
    
    stage.vm.box = "hashicorp/precise32"
    stage.vm.hostname = "stage"

    stage.vm.network "private_network", ip: "192.168.221.4"

    # must disable default ssh first
    # https://github.com/mitchellh/vagrant/issues/3232
    stage.vm.network "forwarded_port", guest:22, host: 2224, auto_correct: false, id: "ssh"
    # stage.vm.network "forwarded_port", guest:22, host: 2224, auto_correct: true

    stage.vm.provider "virtualbox" do |v|
      v.memory = 1024
      v.cpus = 2
      v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
    end

    stage.vm.synced_folder ".", "/vagrant", disabled: true
=begin
    # Don't provision and sync folders on the stage machine
    # do the provisioning from the dev environment to simulate cloud deploy
    stage.vm.synced_folder ".", "/vagrant",
      type: "rsync",
      rsync__exclude: [".idea/"],
      rsync__auto: true

    provision(stage, "stage.yml", "stage.hosts")
=end

  end

end
