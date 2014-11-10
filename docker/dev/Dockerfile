FROM legcowatch/appserver


COPY .bashrc /root/.bashrc
COPY .profile /root/.profile


RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

# Use baseimage-docker's init system.
CMD ["/sbin/my_init", "--enable-insecure-key"]

