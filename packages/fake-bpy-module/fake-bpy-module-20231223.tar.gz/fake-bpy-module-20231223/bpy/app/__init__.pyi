import sys
import typing
from . import handlers
from . import icons
from . import timers
from . import translations

GenericType = typing.TypeVar("GenericType")


def help_text(all: typing.Optional[bool] = False):
    ''' Return the help text as a string.

    :param all: Return all arguments, even those which aren't available for the current platform.
    :type all: typing.Optional[bool]
    '''

    ...


def is_job_running(job_type: typing.Optional[str]) -> typing.Any:
    ''' Check whether a job of the given type is running.

    :param job_type: `rna_enum_wm_job_type_items`.
    :type job_type: typing.Optional[str]
    :rtype: typing.Any
    :return: Whether a job of the given type is currently running.
    '''

    ...


alembic: typing.Any
''' Constant value bpy.app.alembic(supported=True, version=(1, 8, 3), version_string=' 1, 8, 3')
'''

autoexec_fail: typing.Any
''' Undocumented, consider `contributing <https://developer.blender.org/>`__.
'''

autoexec_fail_message: typing.Any
''' Undocumented, consider `contributing <https://developer.blender.org/>`__.
'''

autoexec_fail_quiet: typing.Any
''' Undocumented, consider `contributing <https://developer.blender.org/>`__.
'''

background: typing.Any
''' Boolean, True when blender is running without a user interface (started with -b)
'''

binary_path: typing.Any
''' The location of Blender's executable, useful for utilities that open new instances. Read-only unless Blender is built as a Python module - in this case the value is an empty string which script authors may point to a Blender binary.
'''

build_branch: typing.Any
''' The branch this blender instance was built from
'''

build_cflags: typing.Any
''' C compiler flags
'''

build_commit_date: typing.Any
''' The date of commit this blender instance was built
'''

build_commit_time: typing.Any
''' The time of commit this blender instance was built
'''

build_commit_timestamp: typing.Any
''' The unix timestamp of commit this blender instance was built
'''

build_cxxflags: typing.Any
''' C++ compiler flags
'''

build_date: typing.Any
''' The date this blender instance was built
'''

build_hash: typing.Any
''' The commit hash this blender instance was built with
'''

build_linkflags: typing.Any
''' Binary linking flags
'''

build_options: typing.Any
''' Constant value bpy.app.build_options(bullet=True, codec_avi=True, codec_ffmpeg=True, codec_sndfile=True, compositor_cpu=True, cycles=True, cycles_osl=True, freestyle=True, image_cineon=True, image_dds=True, image_hdr=True, image_openexr=True, image_openjpeg=True, image_tiff=True, input_ndof=True, audaspace=True, international=True, openal=True, opensubdiv=True, sdl=True, sdl_dynload=False, coreaudio=False, jack=False, pulseaudio=False, wasapi=False, libmv=True, mod_oceansim=True, mod_remesh=True, collada=True, io_wavefront_obj=True, io_ply=True, io_stl=True, io_gpencil=True, opencolorio=True, openmp=True, openvdb=True, alembic=True, usd=True, fluid=True, xr_openxr=True, potrace=True, pugixml=True, haru=True)
'''

build_platform: typing.Any
''' The platform this blender instance was built for
'''

build_system: typing.Any
''' Build system used
'''

build_time: typing.Any
''' The time this blender instance was built
'''

build_type: typing.Any
''' The type of build (Release, Debug)
'''

debug: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_depsgraph: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_depsgraph_build: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_depsgraph_eval: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_depsgraph_pretty: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_depsgraph_tag: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_depsgraph_time: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_events: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_ffmpeg: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_freestyle: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_handlers: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_io: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_python: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_simdata: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

debug_value: typing.Any
''' Short, number which can be set to non-zero values for testing purposes
'''

debug_wm: typing.Any
''' Boolean, for debug info (started with ``--debug`` / ``--debug-*`` matching this attribute name)
'''

driver_namespace: typing.Any
''' Dictionary for drivers namespace, editable in-place, reset on file load (read-only) File Loading & Order of Initialization Since drivers may be evaluated immediately after loading a blend-file it is necessary to ensure the driver name-space is initialized beforehand. This can be done by registering text data-blocks to execute on startup, which executes the scripts before drivers are evaluated. See *Text -> Register* from Blender's text editor. .. hint:: You may prefer to use external files instead of Blender's text-blocks. This can be done using a text-block which executes an external file. This example runs ``driver_namespace.py`` located in the same directory as the text-blocks blend-file: .. code-block:: import os import bpy blend_dir = os.path.normalize(os.path.join(__file__, "..", "..")) bpy.utils.execfile(os.path.join(blend_dir, "driver_namespace.py")) Using ``__file__`` ensures the text resolves to the expected path even when library-linked from another file. Other methods of populating the drivers name-space can be made to work but tend to be error prone: Using The ``--python`` command line argument to populate name-space often fails to achieve the desired goal because the initial evaluation will lookup a function that doesn't exist yet, marking the driver as invalid - preventing further evaluation. Populating the driver name-space before the blend-file loads also doesn't work since opening a file clears the name-space. It is possible to run a script via the ``--python`` command line argument, before the blend file. This can register a load-post handler (:mod:`bpy.app.handlers.load_post`) that initialized the name-space. While this works for background tasks it has the downside that opening the file from the file selector won't setup the name-space.
'''

factory_startup: typing.Any
''' Boolean, True when blender is running with --factory-startup)
'''

ffmpeg: typing.Any
''' Constant value bpy.app.ffmpeg(supported=True, avcodec_version=(60, 3, 100), avcodec_version_string='60, 3, 100', avdevice_version=(60, 1, 100), avdevice_version_string='60, 1, 100', avformat_version=(60, 3, 100), avformat_version_string='60, 3, 100', avutil_version=(58, 2, 100), avutil_version_string='58, 2, 100', swscale_version=(7, 1, 100), swscale_version_string=' 7, 1, 100')
'''

ocio: typing.Any
''' Constant value bpy.app.ocio(supported=True, version=(2, 2, 0), version_string=' 2, 2, 0')
'''

oiio: typing.Any
''' Constant value bpy.app.oiio(supported=True, version=(2, 4, 15), version_string=' 2, 4, 15')
'''

opensubdiv: typing.Any
''' Constant value bpy.app.opensubdiv(supported=True, version=(3, 5, 0), version_string=' 3, 5, 0')
'''

openvdb: typing.Any
''' Constant value bpy.app.openvdb(supported=True, version=(10, 0, 0), version_string='10, 0, 0')
'''

render_icon_size: typing.Any
''' Reference size for icon/preview renders (read-only)
'''

render_preview_size: typing.Any
''' Reference size for icon/preview renders (read-only)
'''

sdl: typing.Any
''' Constant value bpy.app.sdl(supported=True, version=(2, 28, 2), version_string='2.28.2', available=True)
'''

tempdir: typing.Any
''' String, the temp directory used by blender (read-only)
'''

usd: typing.Any
''' Constant value bpy.app.usd(supported=True, version=(0, 23, 5), version_string=' 0, 23, 5')
'''

use_event_simulate: typing.Any
''' Boolean, for application behavior (started with ``--enable-*`` matching this attribute name)
'''

use_userpref_skip_save_on_exit: typing.Any
''' Boolean, for application behavior (started with ``--enable-*`` matching this attribute name)
'''

version: typing.Any
''' The Blender version as a tuple of 3 numbers. eg. (2, 83, 1)
'''

version_cycle: typing.Any
''' The release status of this build alpha/beta/rc/release
'''

version_file: typing.Any
''' The Blender version, as a tuple, last used to save a .blend file, compatible with ``bpy.data.version``. This value should be used for handling compatibility changes between Blender versions
'''

version_string: typing.Any
''' The Blender version formatted as a string
'''
