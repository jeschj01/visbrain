"""
Add deep sources
================

Add sources to the scene. This script also illustrate most of the controls for
sources. Each source is defined by a (x, y, z) MNI coordinate. Then, we can
attach some data to sources and project this activity onto the surface
(cortical projection). Alternatively, you can run the cortical repartition
which is defined as the number of contributing sources per vertex.

Download source's coordinates (xyz_sample.npz) :
https://www.dropbox.com/s/whogfxutyxoir1t/xyz_sample.npz?dl=1

.. image:: ../../picture/picbrain/ex_sources.png
"""
import numpy as np

from visbrain import Brain
from visbrain.objects import SourceObj
from visbrain.io import download_file, path_to_visbrain_data

kwargs = {}

"""
Load the xyz coordinates and corresponding subject name
"""
download_file('xyz_sample.npz')
mat = np.load(path_to_visbrain_data('xyz_sample.npz'))
xyz, subjects = mat['xyz'], mat['subjects']

"""
The "subjects" list is composed of 6 diffrents subjects and here we set one
unique color (u_color) per subject.
"""
u_color = ["#9b59b6", "#3498db", "white", "#e74c3c", "#34495e", "#2ecc71"]
kwargs['color'] = [u_color[int(k[1])] for k in subjects]
kwargs['alpha'] = 0.5

"""
Now we attach data to each source.
"""
kwargs['data'] = np.random.uniform(low=-100., high=100., size=(len(subjects)),)

"""
The source's radius is proportional to the data attached. But this proportion
can be controlled using a minimum and maximum radius (s_radiusmin, s_radiusmax)
"""
kwargs['radius_min'] = 2               # Minimum radius
kwargs['radius_max'] = 15              # Maximum radius
kwargs['edge_color'] = (1, 1, 1, 0.5)  # Color of the edges
kwargs['edge_width'] = .5              # Width of the edges
kwargs['symbol'] = 'square'            # Source's symbol

"""
Next, we mask source's data that are comprised between [-20, 20] and color
each source to orange
"""
mask = np.logical_and(kwargs['data'] >= -20, kwargs['data'] <= 20)
kwargs['mask'] = mask
kwargs['mask_color'] = 'orange'

"""
After defining sources, it's possible to run the cortical projection and/or the
cortical repartition. The lines bellow are used to control the colormap when
opening the interface.
Run the projection from the menu Project/Run projection, from the source's tab
or using the shortcut CTRL + P (for projection) or CTRL + R (repartition)

Use CTRL + D to hide/display the quick-settings panel, the shortcut C to
display the colorbar.
"""
kw_proj = dict(project_radius=12.,
               project_contribute=True,
               project_mask_color='blue',
               project_cmap='inferno',
               project_clim=(-90., 90.),
               project_vmin=-60.,
               project_vmax=60.,
               project_under='gray',
               project_over='red'
               )

"""
It's also possible to add text to each source. Here, we show the name of the
subject in yellow.
To avoid a superposition between the text and sources sphere, we introduce an
offset to the text using the s_textshift input
"""
kwargs['text'] = subjects              # Name of the subject
kwargs['text_color'] = "#f39c12"       # Set to yellow the text color
kwargs['text_size'] = 1.5              # Size of the text
kwargs['text_translate'] = (1.5, 1.5, 0)
kwargs['text_bold'] = True

"""Create the source object. If you want to previsualize the result without
opening Brain, use s_obj.preview()
"""
s_obj = SourceObj('SourceExample', xyz, **kwargs)
# s_obj.preview()

# Pass all arguments in the dictionnary :
vb = Brain(source_obj=s_obj, brain_template='B3', **kw_proj)

vb.show()
