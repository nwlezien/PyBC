# -*- coding: utf-8 -*-

# %% Imports

from py3.Chain import Chain


# %% Create chain

c = Chain(verb=1,
          datStart=3,
          datn=1,
          outputPath="ExportedBlocks/")
c.read_all()
