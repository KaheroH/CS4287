# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "ubuntu/bionic64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
  
  # Note, the actions when performed inside an inline shell are by default
  # executed as root user unless you provide the privileged: false option
  #
  # So if I do the following, the directories will be owned by root and
  # we don't want that. So we could pass a privileged: false option after
  # the ending SHELL. But I am showing a different way to do it by
  # defining a separate shell script that gets called. See below.
  config.vm.provision "shell", inline: <<-SHELL, privileged: false
      mkdir -p /home/vagrant/.ssh
      mkdir -p /home/vagrant/.ansible
      mkdir -p /home/vagrant/.config
      mkdir -p /home/vagrant/.config/openstack
	  mkdir -p /home/vagrant/code
	  mkdir -p /home/vagrant/docker_and_k8s
  SHELL
  
config.vm.provision "shell", inline: <<-SHELL
	sudo apt update
	sudo apt install software-properties-common
	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt update
	sudo apt install -y python3.8
	sudo apt update
	sudo apt install -y python3-pip
	sudo apt-get install -y python3-setuptools
	sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
	sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2
	sudo update-alternatives --set python /usr/bin/python3.8
	
	sudo -H pip3 install --upgrade ansible
	sudo pip3 install --upgrade decorator
	sudo python3 -m pip install --upgrade pip setuptools wheel
	sudo pip3 install --ignore-installed --upgrade openstacksdk
	sudo python3 -m pip install --upgrade openstacksdk
	sudo pip3 install --ignore-installed --upgrade openstacksdk future
	#sudo ansible-galaxy collection install openstack.cloud
 SHELL
  
 # let's also copy our ansible.cfg, MyInventory, cloud.yaml file, ssh key, and playbooks
 config.vm.provision "file", source: "./.ansible.cfg.txt", destination: "~/.ansible.cfg"
 config.vm.provision "file", source: "./MyInventory.txt", destination: "~/.ansible/MyInventory"
 config.vm.provision "file", source: "./clouds.yml", destination: "~/.config/openstack/clouds.yml"
 config.vm.provision "file", source: "./keys/martin_key", destination: "~/.ssh/martin_key"
 config.vm.provision "file", source: "./keys/kahero_key", destination: "~/.ssh/kahero_key"

 config.vm.provision "file", source: "./producer.py", destination: "~/code/producer.py"	
 config.vm.provision "file", source: "./consumer.py", destination: "~/code/consumer.py"	
 config.vm.provision "file", source: "./dockerfile.txt", destination: "~/docker_and_k8s/dockerfile"
 config.vm.provision "file", source: "./k8s/job_ymls", destination: "~/docker_and_k8s/job_ymls"
 config.vm.provision "file", source: "./k8s/svc_ymls", destination: "~/docker_and_k8s/svc_ymls"

 config.vm.provision "file", source: "./daemon.json", destination: "/home/vagrant/docker_and_k8s/daemon.json"
  
  # make sure the permissions on the  pem file are not too open.
  # Note, here I show you using inline and privileged: false so the inline
  # action actually happens as the user vagrant.
  # Moreover, we also show a diff approach to put the inline code in
  # a block, and then use the block name. 
  # Change file name as appropriate. Replace this with your pem file.
  $script = <<-SCRIPT
     chmod go-rwx ~/.ssh/martin_key
	 chmod go-rwx ~/.ssh/kahero_key
  SCRIPT
  config.vm.provision "shell", inline: $script, privileged: false
  
  # We now use the Ansible provisioner
  #
  # in the following, install= true will install ansible in the
  # created or provisioned guest vm. Once ansible is installed, any
  # additional configuration we plan to do will be taken from the
  # supplied playbook. Moreover, we can also tell ansible which
  # Inventory file it should use. This inventory file will appear in the
  # /vagrant directory (which is the same directory on your host that has
  # the vagrantfile but is mounted as /vagrant in the guest machine)
  #
  # Please note that the get facts about cloud will fail because we haven't
  # installed openstacksdk and ansible galaxy plugin. All those steps
  # are left for you to fill up
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "./playbooks/playbook_demo_master.yml"
    ansible.verbose = true
    ansible.install = true  # installs ansible (and hence python on VM)
    ansible.limit = "all"
    ansible.inventory_path = "./MyInventory.txt"  # inventory file
  end
end
