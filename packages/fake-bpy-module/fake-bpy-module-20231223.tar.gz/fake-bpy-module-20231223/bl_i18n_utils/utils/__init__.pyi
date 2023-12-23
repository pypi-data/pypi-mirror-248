import sys
import typing

GenericType = typing.TypeVar("GenericType")


class I18n:
    parsers: typing.Any
    ''' '''

    py_file: typing.Any
    ''' '''

    writers: typing.Any
    ''' '''

    def check_py_module_has_translations(self, src, settings):
        ''' 

        '''
        ...

    def escape(self, do_all):
        ''' 

        '''
        ...

    def parse(self, kind, src, langs):
        ''' 

        '''
        ...

    def parse_from_po(self, src, langs):
        ''' 

        '''
        ...

    def parse_from_py(self, src, langs):
        ''' 

        '''
        ...

    def print_stats(self, prefix, print_msgs):
        ''' 

        '''
        ...

    def unescape(self, do_all):
        ''' 

        '''
        ...

    def update_info(self):
        ''' 

        '''
        ...

    def write(self, kind, langs):
        ''' 

        '''
        ...

    def write_to_po(self, langs):
        ''' 

        '''
        ...

    def write_to_py(self, langs):
        ''' 

        '''
        ...


class I18nMessage:
    comment_lines: typing.Any
    ''' '''

    is_commented: typing.Any
    ''' '''

    is_fuzzy: typing.Any
    ''' '''

    is_tooltip: typing.Any
    ''' '''

    msgctxt: typing.Any
    ''' '''

    msgctxt_lines: typing.Any
    ''' '''

    msgid: typing.Any
    ''' '''

    msgid_lines: typing.Any
    ''' '''

    msgstr: typing.Any
    ''' '''

    msgstr_lines: typing.Any
    ''' '''

    settings: typing.Any
    ''' '''

    sources: typing.Any
    ''' '''

    def copy(self):
        ''' 

        '''
        ...

    def do_escape(self, txt):
        ''' 

        '''
        ...

    def do_unescape(self, txt):
        ''' 

        '''
        ...

    def escape(self, do_all):
        ''' 

        '''
        ...

    def normalize(self, max_len):
        ''' 

        '''
        ...

    def unescape(self, do_all):
        ''' 

        '''
        ...


class I18nMessages:
    parsers: typing.Any
    ''' '''

    writers: typing.Any
    ''' '''

    def check(self, fix):
        ''' 

        '''
        ...

    def clean_commented(self):
        ''' 

        '''
        ...

    def escape(self, do_all):
        ''' 

        '''
        ...

    def find_best_messages_matches(self, msgs, msgmap, rna_ctxt,
                                   rna_struct_name, rna_prop_name,
                                   rna_enum_name):
        ''' 

        '''
        ...

    def gen_empty_messages(self, uid, blender_ver, blender_hash, time, year,
                           default_copyright, settings):
        ''' 

        '''
        ...

    def invalidate_reverse_cache(self, rebuild_now):
        ''' 

        '''
        ...

    def merge(self, msgs, replace):
        ''' 

        '''
        ...

    def normalize(self, max_len):
        ''' 

        '''
        ...

    def parse(self, kind, key, src):
        ''' 

        '''
        ...

    def parse_messages_from_po(self, src, key):
        ''' 

        '''
        ...

    def print_info(self, prefix, output, print_stats, print_errors):
        ''' 

        '''
        ...

    def rtl_process(self):
        ''' 

        '''
        ...

    def unescape(self, do_all):
        ''' 

        '''
        ...

    def update(self, ref, use_similar, keep_old_commented):
        ''' 

        '''
        ...

    def update_info(self):
        ''' 

        '''
        ...

    def write(self, kind, dest):
        ''' 

        '''
        ...

    def write_messages_to_mo(self, fname):
        ''' 

        '''
        ...

    def write_messages_to_po(self, fname, compact):
        ''' 

        '''
        ...


def enable_addons(addons, support, disable, check_only):
    ''' 

    '''

    ...


def find_best_isocode_matches(uid, iso_codes):
    ''' 

    '''

    ...


def get_best_similar(data):
    ''' 

    '''

    ...


def get_po_files_from_dir(root_dir, langs):
    ''' 

    '''

    ...


def is_valid_po_path(path):
    ''' 

    '''

    ...


def list_po_dir(root_path, settings):
    ''' 

    '''

    ...


def locale_explode(locale):
    ''' 

    '''

    ...


def locale_match(loc1, loc2):
    ''' 

    '''

    ...
