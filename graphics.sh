#!/bin/bash

echo "deb https://download.01.org/gfx/ubuntu/14.04/main trusty main" > /etc/apt/sources.list.d/graphics.list

wget --no-check-certificate https://download.01.org/gfx/RPM-GPG-KEY-ilg -O - | apt-key add -

aptitude update
aptitude upgrade
