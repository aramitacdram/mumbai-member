# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

# this file is meant to be included from other projects

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu/trusty64"

  config.vm.provision :shell, path: "commons/vagrant/apt.sh"

  config.vm.provider :virtualbox do |virtualbox|
    virtualbox.name = "vapaamatikka-headless"
  end

end
