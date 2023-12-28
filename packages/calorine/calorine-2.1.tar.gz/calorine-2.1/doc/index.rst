.. raw:: html

  <p>
  <a href="https://badge.fury.io/py/calorine"><img src="https://badge.fury.io/py/calorine.svg" alt="PyPI version" height="18"></a>
  <a href="https://doi.org/10.5281/zenodo.7919206"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.7919206.svg" alt="zenodo" height="18"></a>
  </p>

:program:`calorine`
*******************

:program:`calorine` is a Python library for constructing and sampling neuroevolution potentials (NEPs) via `GPUMD <https://gpumd.org/>`_.
It provides ASE calculators, IO functions for reading and writing :program:`GPUMD` input and output files, as well as a Python interface that allows inspection NEP models.


.. toctree::
   :maxdepth: 2
   :caption: Main

   installation
   credits

.. toctree::
   :maxdepth: 2
   :caption: Tutorials

   tutorials/calculators
   tutorials/nep_descriptors
   tutorials/nep_model_inspection
   tutorials/visualize_descriptor_space_with_pca
   tutorials/generate_training_structures_and_training
   tutorials/structure_relaxation
   tutorials/phonons
   tutorials/elastic_stiffness_tensor
   tutorials/thermal_conductivity_from_bte

.. toctree::
   :maxdepth: 2
   :caption: Function reference

   calculators
   gpumd
   nep
   tools

.. toctree::
   :maxdepth: 2
   :caption: Backmatter

   genindex
