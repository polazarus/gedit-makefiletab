# Copyright (c) 2009, Mickael Delahaye <mickael.delahaye@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
A simple plugin for GEdit with a simple purpose:
switching off insert-space-instead-of-tabs for all Makefile documents.
"""
__all__ = ['ismakefile','MakefiletabPlugin']
__version__ = '0.9'

import gedit

class MakefiletabPlugin(gedit.Plugin):
  """Gedit plugin for switching off insert-space-instead-of-views on any active view of a Makefile document"""

  def activate(self,window):
    """Activate the plugin on a given window"""
    hid = window.connect("active-tab-changed", activetabchanged_cb)
    window.set_data("maketab_hook",hid)
    active = window.get_active_tab()
    if active:
      checkmakefile(active)
  def deactivate(self,window):
    """Deactivate the plugin on the given window"""
    hid=window.get_data("maketab_hook")
    window.disconnect(hid)
    window.remove_data("maketab_hook")
  def update_ui(self,window):
    """Update the UI on the given window"""
    hid = window.get_data('maketab_hook')
    if not hid:
      hid = window.connect("active-tab-changed", activetabchanged_cb)
      window.set_data('maketab_hook',hid)
    active = window.get_active_tab()
    if active:
      checkmakefile(active)

def activetabchanged_cb(_window,tab):
  if tab:
    checkmakefile(tab)

def checkmakefile(tab):
  if ismakefile(tab.get_document()):
    tab.get_view().set_insert_spaces_instead_of_tabs(0)

def ismakefile(doc):
  "Checks if a GEdit document corresponds to a Makefile"
  return 'makefile' in doc.get_content_type()
