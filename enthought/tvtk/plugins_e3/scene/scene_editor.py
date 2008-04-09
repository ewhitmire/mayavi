""" A TVTK scene editor. """

# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2005, Enthought, Inc.
# License: BSD Style.


# Enthought library imports.
from enthought.preferences.api import bind_preference
from enthought.pyface.tvtk.scene import Scene
from enthought.pyface.workbench.api import Editor
from enthought.traits.api import Any, Instance, Str, Event


##############################################################################
# Handy functions
def _id_generator():
    """Returns a sequence of numbers for the title of the scene editor
    window."""
    n = 1
    while True:
        yield(n)
        n += 1

_id_generator = _id_generator()


class SceneEditor(Editor):
    """ A TVTK scene editor. """

    #### 'IWorkbenchPart' interface ###########################################
    
    # The scene manager.
    scene_manager = Instance(
        'enthought.tvtk.plugins_e3.scene.scene_manager.SceneManager'
    )
    
    # The TVTK scene object.
    scene = Instance(Scene)

    #### Events #####

    ## FIXME: These are temporary and should be removed once (and if)
    ## Martin adds them to the framework.

    # The editor has been activated.
    activated = Event

    # The editor is being closed.
    closing = Event

    # The editor has been closed.
    closed = Event

    ###########################################################################
    # `object` interface
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """
        
        super(SceneEditor, self).__init__(**traits)

        # Create a unique Id.
        self.id = self.name = 'TVTK Scene %d' % (_id_generator.next())        

        return
    
    ###########################################################################
    # 'IWorkbenchPart' interface.
    ###########################################################################

    def create_control(self, parent):
        """ Create the toolkit-specific control that represents the editor. """

        scene = self._create_decorated_scene(parent)
        scene.render()

        # Hold a reference to the scene itself, to make sure it does not get
        # garbage collected (because we only return the scene's 'control' not
        # the scene itself).
        self.scene = scene

        # Add this editor to the plugin's editors.  We do this only here and
        # not at initialization time because the browser plugin listens for
        # this and requires that the scene attribute be set.
        self.scene_manager.editors.append(self)
        self.scene_manager.current_editor = self

        return self.scene.control

    ###########################################################################
    # FIXME: these should be changed when the framework's editor has
    # lifecycle events added.
    # 'Editor' interface
    ###########################################################################

    def set_focus(self):
        """ Sets the focus to the appropriate control in the editor. """

        super(SceneEditor, self).set_focus()
        if self.control is not None:
            self.activated = self

        return

    def _closing_fired(self, event):
        """ This event fires when the window closes. """

        # Remove ourselves from the scene manager at this time.
        self.scene_manager.editors.remove(self)

        return
    
    def _activated_fired(self, event):
        """ This event fires when this frame/editor is activated. """

        self.scene_manager.current_editor = self

        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_decorated_scene(self, parent):
        """ Create a new decorated scene. """

        scene = Scene(parent)

        # Bind the scene's traits to preferences.
        bind_preference(
            scene, 'stereo', 'enthought.tvtk.scene.stereo'
        )

        bind_preference(
            scene, 'magnification', 'enthought.tvtk.scene.magnification'
        )

        bind_preference(
           scene, 'foreground', 'enthought.tvtk.scene.foreground_color'
        )

        bind_preference(
            scene.renderer,'background','enthought.tvtk.scene.background_color'
        )

        return scene
        
#### EOF ######################################################################