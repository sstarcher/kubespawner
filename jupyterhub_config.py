import os
import socket

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_ip = '0.0.0.0'

# Don't try to cleanup servers on exit - since in general for k8s, we want
# the hub to be able to restart without losing user containers
c.JupyterHub.cleanup_servers = False

# First pulls can be really slow, so let's give it a big timeout
c.KubeSpawner.start_timeout = 60 * 5

# Our simplest user image! Optimized to just... start, and be small!
c.KubeSpawner.image = 'jupyterhub/singleuser:1.0'

# Find the IP of the machine that minikube is most likely able to talk to
# Graciously used from https://stackoverflow.com/a/166589
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
host_ip = s.getsockname()[0]
s.close()

c.JupyterHub.hub_connect_ip = host_ip

c.KubeSpawner.service_account = 'default'
# Do not use any authentication at all - any username / password will work.
c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'

c.KubeSpawner.storage_pvc_ensure = False
c.KubeSpawner.working_dir = '/home/jovyan/'

c.JupyterHub.allow_named_servers = True
c.JupyterHub.internal_ssl = True
c.JupyterHub.recreate_internal_certs = True
c.JupyterHub.trusted_alt_names = ['IP:'+host_ip]
