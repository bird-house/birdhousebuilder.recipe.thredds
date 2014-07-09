# -*- coding: utf-8 -*-
# Copyright (C)2014 DKRZ GmbH

"""Recipe tomcat"""

import os
from mako.template import Template

import zc.buildout
from birdhousebuilder.recipe import conda, tomcat

wms_config = Template(filename=os.path.join(os.path.dirname(__file__), "wmsConfig.xml"))
thredds_config = Template(filename=os.path.join(os.path.dirname(__file__), "threddsConfig.xml"))
catalog_config = Template(filename=os.path.join(os.path.dirname(__file__), "catalog.xml"))

class Recipe(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        self.anaconda_home = b_options.get('anaconda-home', conda.anaconda_home())
        self.options['prefix'] = self.anaconda_home
        self.data_root = options.get('data_root', '/tmp')

    def install(self):
        installed = []
        installed += list(self.install_thredds())
        installed += list(self.install_thredds_config())
        installed += list(self.install_catalog_config())
        installed += list(self.install_wms_config())
        return installed

    def install_thredds(self):
        script = conda.Recipe(
            self.buildout,
            self.name,
            {'pkgs': 'thredds'})

        return script.install()

    def install_thredds_config(self):
        result = thredds_config.render(**self.options)

        output = os.path.join(self.anaconda_home, 'opt', 'apache-tomcat', 'webapps', 'thredds', 'threddsConfig.xml')
        conda.makedirs(os.path.dirname(output))

        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_catalog_config(self):
        result = catalog_config.render(**self.options)

        output = os.path.join(self.anaconda_home, 'opt', 'apache-tomcat', 'webapps', 'thredds', 'catalog.xml')
        conda.makedirs(os.path.dirname(output))

        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_wms_config(self):
        result = wms_config.render(**self.options)

        output = os.path.join(self.anaconda_home, 'opt', 'apache-tomcat', 'webapps', 'thredds', 'wmsConfig.xml')
        conda.makedirs(os.path.dirname(output))

        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def update(self):
        return self.install()

def uninstall(name, options):
    pass

