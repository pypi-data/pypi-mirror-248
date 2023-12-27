# Cloudmesh Command ssh

[![GitHub Repo](https://img.shields.io/badge/github-repo-green.svg)](https://github.com/cloudmesh/cloudmesh-ssh)
[![image](https://img.shields.io/pypi/pyversions/cloudmesh-ssh.svg)](https://pypi.org/project/cloudmesh-ssh)
[![image](https://img.shields.io/pypi/v/cloudmesh-ssh.svg)](https://pypi.org/project/cloudmesh-ssh/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![General badge](https://img.shields.io/badge/Status-Production-<COLOR>.svg)](https://shields.io/)
[![GitHub issues](https://img.shields.io/github/issues/cloudmesh/cloudmesh-ssh.svg)](https://github.com/cloudmesh/cloudmesh-ssh/issues)
[![Contributors](https://img.shields.io/github/contributors/cloudmesh/cloudmesh-ssh.svg)](https://github.com/cloudmesh/cloudmesh-ssh/graphs/contributors)
[![General badge](https://img.shields.io/badge/Other-repos-<COLOR>.svg)](https://github.com/cloudmesh/cloudmesh)


[![Linux](https://img.shields.io/badge/OS-Linux-orange.svg)](https://www.linux.org/)
[![macOS](https://img.shields.io/badge/OS-macOS-lightgrey.svg)](https://www.apple.com/macos)
[![Windows](https://img.shields.io/badge/OS-Windows-blue.svg)](https://www.microsoft.com/windows)



## Manual Page

<!-- START-MANUAL -->
```
Command ssh
===========

::

    Usage:
        ssh config list [--output=OUTPUT]
        ssh config add NAME IP [USER] [KEY]
        ssh config delete NAME

    Arguments:
      NAME        Name or ip of the machine to log in
      list        Lists the machines that are registered and
                  the commands to login to them
      PARAMETERS  Register te resource and add the given
                  parameters to the ssh config file.  if the
                  resource exists, it will be overwritten. The
                  information will be written in /.ssh/config
      USER        The username for the ssh resource
      KEY         The location of the public keye used for
                  authentication to the host

    Options:
       --output=OUTPUT   the format in which this list is given
                         formats includes cat, table, json, yaml,
                         dict. If cat is used, it is just printed as
                         is. [default: table]

    Description:
        ssh config list
            lists the hostsnames that are present in the ~/.ssh/config file

        ssh config add NAME IP [USER] [KEY]
            registers a host i ~/.ssh/config file
            Parameters are attribute=value pairs

        ssh config delete NAME
            deletes the named host from the ssh config file

    Examples:

         ssh config add blue 192.168.1.245 gregor

             Adds the following to the !/.ssh/config file

             Host blue
                  HostName 192.168.1.245
                  User gergor
                  IdentityFile ~/.ssh/id_rsa.pub

```
<!-- STOP-MANUAL -->