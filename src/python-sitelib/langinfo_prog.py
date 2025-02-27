# Copyright (c) 2007 ActiveState Software Inc.
# See the file LICENSE.txt for licensing information.

"""LangInfo definitions for some programming languages."""

import re
from langinfo import LangInfo

import logging
log = logging.getLogger("langinfo_prog")
#log.setLevel(logging.DEBUG)

class _PythonCommonLangInfo(LangInfo):
    conforms_to_bases = ["Text"]
    exts = ['.py', '.pyw']
    # http://www.python.org/dev/peps/pep-0263/
    encoding_decl_pattern = re.compile(r"coding[:=]\s*(?P<encoding>[-\w.]+)")

# Where there's a conflict in extensions, put the main
# LangInfo entry last.
class PythonLangInfo(_PythonCommonLangInfo):
    name = "Python"
    default_encoding = "ascii"  #TODO: link to ref defining default encoding
    magic_numbers = [
        (0, "regex", re.compile(r'\A#!.*python(?!3).*$', re.I | re.M))
    ]

class Python3LangInfo(_PythonCommonLangInfo):
    name = "Python3"
    default_encoding = "utf-8"
    magic_numbers = [
        (0, "regex", re.compile(r'\A#!.*python3.*$', re.I | re.M))
    ]
    is_minor_variant = PythonLangInfo

class CompiledPythonLangInfo(LangInfo):
    name = "Compiled Python"
    exts = ['.pyc', '.pyo']

class PerlLangInfo(LangInfo):
    name = "Perl"
    conforms_to_bases = ["Text"]
    exts = ['.pl', '.pm', '.t']
    magic_numbers = [
        (0, "regex", re.compile(r'\A#!.*perl.*$', re.I | re.M)),
    ]
    filename_patterns = ["Construct", "Conscript"] # Cons make-replacement tool files

    # http://search.cpan.org/~rgarcia/encoding-source-0.02/lib/encoding/source.pm
    default_encoding = "iso8859-1"
    # Perl >= 5.8.0
    #   http://perldoc.perl.org/encoding.html
    #   use encoding "<encoding-name>";
    #   "Somewhat broken."
    # Perl >= 5.9.5
    #   http://search.cpan.org/~rgarcia/encoding-source-0.02/lib/encoding/source.pm
    #   use encoding::source "<encoding-name>";
    #   "This is like the encoding pragma, but done right."
    encoding_decl_pattern = re.compile(
        r"""use\s+encoding(?:::source)?\s+(['"])(?P<encoding>[\w-]+)\1""")


class PHPLangInfo(LangInfo):
    name = "PHP"
    conforms_to_bases = ["Text"]
    exts = [".php", ".inc",
            ".phtml"]  # .phtml commonly used for Zend Framework view files
    magic_numbers = [
        (0, "string", "<?php"),
        (0, "regex", re.compile(r'\A#!.*php.*$', re.I | re.M)),
    ]
    #TODO: PHP files should inherit the HTML "<meta> charset" check
    #      and the XML prolog encoding check.

    keywords = set([
            # new to php 5.5
            "finally", "yield",
            # new to php 5.4
            "insteadof", "trait",
            # new to php 5.3
            "e_deprecated", "e_user_deprecated", "php_maxpathlen",
            # existed in php4
            "bool", "boolean", "catch", "define", "double", "false", "float",
            "int", "integer", "null", "object", "parent", "real",
            "self", "string", "this", "true", "virtual",
            # new to php5
            "abstract", "final", "implements", "instanceof", "interface",
            "public", "private", "protected", "throw", "try",
            # http://www.php.net/manual/en/reserved.php#reserved.keywords
            "__file__", "__line__", "_function_", "_class_",
            "and", "array", "as", "break", "case", "cfunction", "class",
            "const", "continue", "declare", "default", "die", "do", "echo",
            "else", "elseif", "empty", "enddeclare", "endfor", "endforeach",
            "endif", "endswitch", "endwhile", "eval", "exit", "extends",
            "for", "foreach", "function", "global", "if", "include",
            "include_once", "isset", "list", "new", "old_function", "or",
            "print", "require", "require_once", "return", "static",
            "switch", "unset", "use", "var", "while", "xor",
            # new to php 5.3
            "__dir__", "__namespace__", "goto", "namespace",
            ])

class TclLangInfo(LangInfo):
    name = "Tcl"
    conforms_to_bases = ["Text"]
    exts = ['.tcl']
    magic_numbers = [
        (0, "regex", re.compile(r'\A#!.*(tclsh|wish|expect).*$', re.I | re.M)),
        # As suggested here: http://www.tcl.tk/man/tcl8.4/UserCmd/tclsh.htm
        # Make sure we properly catch shebang lines like this:
        #   #!/bin/sh
        #   # the next line restarts using tclsh \
        #   exec tclsh "$0" "$@"
        (0, "regex", re.compile(r'\A#!.*^exec [^\r\n|\n|\r]*?(tclsh|wish|expect)',
                                re.I | re.M | re.S)),
    ]
    _magic_number_precedence = ("Bourne shell", -1) # check before "Bourne shell"

class RubyLangInfo(LangInfo):
    name = "Ruby"
    conforms_to_bases = ["Text"]
    exts = ['.rb', '.mab', '.ru']
    filename_patterns = ["Rakefile"]
    magic_numbers = [
        (0, "regex", re.compile('\A#!.*ruby.*$', re.I | re.M)),
    ]
    #TODO: http://blade.nagaokaut.ac.jp/cgi-bin/scat.rb/ruby/ruby-core/12900
    #      Ruby uses similar (same?) coding decl as Python.

class _JSLikeLangInfo(LangInfo):
    conforms_to_bases = ["Text"]
    # Support for Node (server side JavaScript).
    magic_numbers = [
        (0, "regex", re.compile(r'\A#!.*node.*$', re.I | re.M))
    ]

    # These are the keywords that are used in most JavaScript environments.
    common_keywords = set([
                          "arguments",
                          "await",
                          "break",
                          "case",
                          "catch",
                          "class",
                          "const",
                          "continue",
                          "debugger",
                          "default",
                          "delete",
                          "do",
                          "else",
                          "enum",
                          "eval",
                          "export",
                          "extends",
                          "false",
                          "finally",
                          "for",
                          "function",
                          "if",
                          "implements",
                          "import",
                          "in",
                          "instanceof",
                          "interface",
                          "let",
                          "new",
                          "null",
                          "of",
                          "package",
                          "private",
                          "protected",
                          "public",
                          "return",
                          "static",
                          "super",
                          "switch",
                          "this",
                          "throw",
                          "true",
                          "try",
                          "typeof",
                          "var",
                          "void",
                          "while",
                          "with",
                          "yield"
                          ])
    keywords = common_keywords.union(
                # Additional JavaScript reserved keywords.
                set([
                    "Infinity",
                    "NaN",
                    "abstract",
                    "boolean",
                    "break",
                    "byte",
                    "case",
                    "catch",
                    "char",
                    "class",
                    "const",
                    "continue",
                    "debugger",
                    "default",
                    "delete",
                    "do",
                    "double",
                    "else",
                    "enum",
                    "export",
                    "extends",
                    "false",
                    "final",
                    "finally",
                    "float",
                    "for",
                    "function",
                    "goto",
                    "if",
                    "implements",
                    "import",
                    "in",
                    "instanceof",
                    "int",
                    "interface",
                    "long",
                    "native",
                    "new",
                    "null",
                    "package",
                    "private",
                    "protected",
                    "public",
                    "return",
                    "short",
                    "static",
                    "super",
                    "switch",
                    "synchronized",
                    "this",
                    "throw",
                    "throws",
                    "transient",
                    "true",
                    "try",
                    "typeof",
                    "undefined",
                    "var",
                    "void",
                    "volatile",
                    "while",
                    "with"
                  ]))

class JavaScriptLangInfo(_JSLikeLangInfo):
    name = "JavaScript"
    exts = ['.js', '.jsm']

    section_regexes = [
        ("function", re.compile(r'''
            \n.*?[ \t]*                         # Start of line
            ([\w\.]+)[ \t]*=.*?=>                  # The function definition
            ''', re.M | re.X)),
        ("function", re.compile(r'''
            \n.*?[ \t]*                         # Start of line
            ([\w\.]+)[ \t]*=.*?function[ \t]*\(       # The function definition
            ''', re.M | re.X)),
       ("function", re.compile(r'''
            \n[ \t]*                            # Start of line
            function[ \t]+([\w\.]+)[ \t]*\(           # The function definition
            ''', re.M | re.X)),
    ]

    def section_hit_title_processor(self, type, rematch, title):
        if "." in title:
            return ("method", ".".join(title.split(".")[1:]))
        else:
            return title

class NodeJSLangInfo(_JSLikeLangInfo):
    name = "Node.js"
    exts = ['.js']

class CoffeeScriptLangInfo(_JSLikeLangInfo):
    name = "CoffeeScript"
    exts = ['.coffee', '.litcoffee']
    filename_patterns = ['Cakefile']
    
    _inherited_keywords = set().union(_JSLikeLangInfo.keywords)
    _compiler_reserved_words = set(['__hasProp', '__extends', '__slice', '__bind', '__indexOf'])
    _new_keywords = set(['and',
                         'by',
                         'class', 'constructor',
                         'is', 'isnt',
                         'loop',
                         'no', 'not',
                         'of', 'off', 'on', 'or', 'own',
                         'then',
                         'unless', 'until',
                         'when',
                         'yes'])
    
    keywords = _inherited_keywords.union(_compiler_reserved_words).union(_new_keywords)

class TypeScriptLangInfo(_JSLikeLangInfo):
    name = "TypeScript"
    exts = ['.ts']
    _reserved_words = set([
        'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger',
        'default', 'delete', 'do', 'else', 'enum', 'export', 'extends', 'false',
        'finally', 'for', 'function', 'if', 'import', 'in', 'instanceof', 'new',
        'null', 'return', 'super', 'switch', 'this', 'throw', 'true', 'try',
        'typeof', 'var', 'void', 'while', 'with'
    ])
    _strict_reserved_words = set([
        'implements', 'interface', 'let', 'package', 'private', 'protected',
        'public', 'static', 'yield'
    ])
    _type_words = set(['any', 'boolean', 'number', 'string', 'symbol'])
    _special_words = set([
        'abstract', 'as', 'async', 'await', 'constructor', 'declare', 'from',
        'get', 'is', 'module', 'namespace', 'of', 'require', 'set', 'type'
    ])
    keywords = _reserved_words.union(_strict_reserved_words). \
                   union(_type_words).union(_special_words)
    
class JSXLangInfo(LangInfo):
    name = "JSX"
    conforms_to_bases = ["Text"]
    exts = ['.jsx'] # Note: .jsx is not advocated, but adding .js throws off codeintel

class CLangInfo(LangInfo):
    #TODO: rationalize with C++ and Komodo's usage
    name = "C"
    conforms_to_bases = ["Text"]
    exts = [
        ".c", 
        ".xs",  # Perl extension modules. *Are* they legal C?
    ]
    #TODO: Note for Jan:
    # .xs files are *NOT* legal C or C++ code.  However, they are
    # similar enough that I find it useful to edit them using c-mode or
    # c++-mode in Emacs.

class CPlusPlusLangInfo(LangInfo):
    #TODO: consider breaking out headers and have separate
    #      scintilla_lexer attr
    name = "C++"
    conforms_to_bases = ["Text"]
    exts = [
              ".c++", ".cpp", ".cxx",
        ".h", ".h++", ".hpp", ".hxx",
        ".inl", # Inline C++ files.
        ".xs",  # Perl extension modules. *Are* they legal C++?
    ]

    # http://publib.boulder.ibm.com/infocenter/lnxpcomp/v8v101/index.jsp?topic=/com.ibm.xlcpp8l.doc/language/ref/cplr318.htm
    # Also these (but not currently handled): new  delete  new[] delete[]
    _overloadable_operators = """
        +     -     *     /     %     ^     &     |    ~  !     =     <     > ,
        +=     -=     *=     /=     %=  ^=     &=     |=  ==     !=  <=     >=
        <<     >>     <<=     >>=  &&     ||     ++     --       ->*    ->  ()  []
    """.split()

    section_regexes = [
        ("constant", re.compile(r"^#define\s+(\w+)\b", re.M)),
        ("class", re.compile(r"^[ \t]*((typedef|static)\s+)?(class|struct)\s+(?P<name>\w+)\b\s*[;{:]", re.M)),
        ("function", re.compile(r"""
            ^[ \t]*                 # this helps avoid false positives in comments and strings
            (                       # function return type and modifiers
                (?<!\#)
                (\w+::)?\b\w+\b(?<!return)
                ([ \t]*[*&]+)?
                [ \t]*
            )+
            \s*
            (?P<name>               # the function name
                (\w+::)?~?\w+(?<!if)
                |
                operator(%s)
            )
            \s*
            \([^)]*?\)              # argument list
            \s*
            (                       # optional comment trailing the argument list (bug 78046)
                /\* .*? \*/
                |
                //[^\r\n]*?[\r\n|\n|\r]
            )?
            \s*
            [{:]                   # start block, or start initializer
            """ % '|'.join(re.escape(o) for o in _overloadable_operators),
            re.M | re.S | re.X)),
    ]

class HLSLLangInfo(LangInfo):
    """High Level Shader Language is a proprietary shading language developed by
    Microsoft for use with the Microsoft Direct3D API.
    
    http://en.wikipedia.org/wiki/HLSL
    """
    name = "HLSL"
    conforms_to_bases = ["Text"]
    exts = ['.hlsl', '.cg', '.fx']

    # Keywords,etc. from http://www.emeditor.com/pub/hlsl.esy
    _intrinsic_function_names = """asm_fragment
        bool
        column_major
        compile
        compile_fragment
        const
        discard
        do
        double
        else
        extern
        false
        float
        for
        half
        if 
        in
        inline
        inout
        int
        matrix
        out
        pixelfragment
        return
        register
        row_major
        sampler
        sampler1D
        sampler2D
        sampler3D
        samplerCUBE
        sampler_state
        shared
        stateblock
        stateblock_state
        static
        string
        struct
        texture
        texture1D
        texture2D
        texture3D
        textureCUBE
        true
        typedef
        uniform
        vector
        vertexfragment
        void
        volatile
        while""".split()
    _keywords_case_insensitive = "asm decl pass technique".split()
    _keywords_case_sensitive = """asm_fragment
        bool
        column_major
        compile
        compile_fragment
        const
        discard
        do
        double
        else
        extern
        false
        float
        for
        half
        if 
        in
        inline
        inout
        int
        matrix
        out
        pixelfragment
        return
        register
        row_major
        sampler
        sampler1D
        sampler2D
        sampler3D
        samplerCUBE
        sampler_state
        shared
        stateblock
        stateblock_state
        static
        string
        struct
        texture
        texture1D
        texture2D
        texture3D
        textureCUBE
        true
        typedef
        uniform
        vector
        vertexfragment
        void
        volatile
        while
        """.split()
    _reserved_words = """auto
        break
        case
        catch
        char
        class
        const_cast
        continue
        default
        delete
        dynamic_cast
        enum
        explicit
        friend
        goto
        long
        mutable
        namespace
        new
        operator
        private
        protected
        public
        reinterpret_cast
        short
        signed
        sizeof
        static_cast
        switch
        template
        this
        throw
        try
        typename
        union
        unsigned
        using
        virtual""".split()

    keywords = set(_intrinsic_function_names
        + _keywords_case_insensitive
        + _keywords_case_sensitive
        + _reserved_words)

class ADALangInfo(LangInfo):
    name = "Ada"
    conforms_to_bases = ["Text"]
    exts = [".ada"]

class NTBatchLangInfo(LangInfo):
    name = "Batch"
    conforms_to_bases = ["Text"]
    exts = [".bat", ".cmd"]  #TODO ".com"?

class BashLangInfo(LangInfo):
    name = "Bash"
    conforms_to_bases = ["Text"]
    exts = [".sh"]
    filename_patterns = [".bash_profile", ".bashrc", ".bash_logout"]
    magic_numbers = [
        (0, "regex", re.compile(r'\A#!.*/\bbash\b$', re.I | re.M)),
    ]

    section_regexes = [
        ("function", re.compile(r"function\s+(\w+)\s*\(\s*\)")),
    ]

class SHLangInfo(LangInfo):
    name = "Bourne shell"
    conforms_to_bases = ["Text"]
    magic_numbers = [
        (0, "regex", re.compile(r'\A#!.*/\bsh\b$', re.I | re.M)),
    ]
    

class TCSHLangInfo(LangInfo):
    name = "tcsh"
    conforms_to_bases = ["Text"]
    magic_numbers = [
        (0, "regex", re.compile(r'\A#!.*/\btcsh\b$', re.M)),
    ]
    filename_patterns = ["csh.cshrc", "csh.login", "csh.logout",
                         ".tcshrc", ".cshrc", ".login", ".logout"]

class CSharpLangInfo(LangInfo):
    name = "C#"
    conforms_to_bases = ["Text"]
    exts = [".cs"]

class ErlangLangInfo(LangInfo):
    name = "Erlang"
    conforms_to_bases = ["Text"]
    exts = [".erl"]

class Fortran77LangInfo(LangInfo):
    name = "Fortran 77"
    conforms_to_bases = ["Text"]
    exts = [".f"]

class Fortran95LangInfo(LangInfo):
    name = "Fortran"
    conforms_to_bases = ["Text"]
    exts = [".f95"]

class JavaLangInfo(LangInfo):
    name = "Java"
    conforms_to_bases = ["Text"]
    exts = [".java", ".jav", '.groovy']
    section_regexes = [
        ("class", re.compile(r'''
            ^
            \s*
            (\w+\s+)*   # or could be specific about modifiers
            class\s+
            (?P<name>\w+)
            (\s+\w+)*   # or could be specific about 'extends' ...
            \s*{
            ''', re.M | re.X)),
        ("function", re.compile(r'''
            ^
            \s*
            (\w+\s+)*
            (?P<name>\w+\s* \(\s* ([\w\[\]]+\s+\w+ (\s*,\s*[\w\[\]]+\s+\w+)*)?  \s*\))
            (\s+throws\s+[\w\s,]+)?
            \s*({|;)
            ''', re.M | re.X)),
        ("interface", re.compile(r'''
            ^
            \s*
            (\w+\s+)*   # or could be specific about modifiers
            interface\s+
            (?P<name>\w+)
            (\s+\w+)*   # or could be specific about 'extends' ...
            \s*{
            ''', re.M | re.X)),
    ]

class LispLangInfo(LangInfo):
    name = "Lisp"
    conforms_to_bases = ["Text"]
    exts = [".lis"]

class LuaLangInfo(LangInfo):
    name = "Lua"
    conforms_to_bases = ["Text"]
    exts = [".lua"]

class PascalLangInfo(LangInfo):
    name = "Pascal"
    conforms_to_bases = ["Text"]
    exts = [".pas"]

class SmalltalkLangInfo(LangInfo):
    name = "Smalltalk"
    conforms_to_bases = ["Text"]
    exts = [".st"]

class ActionScriptLangInfo(LangInfo):
    """ActionScript source code

    http://en.wikipedia.org/wiki/Adobe_Flash#Related_file_formats_and_extensions
    """
    name = "ActionScript"
    conforms_to_bases = ["Text"]
    exts = [".as", ".asc"]

class AssemblerLangInfo(LangInfo):
    name = "Assembler"
    conforms_to_bases = ["Text"]
    exts = [".asm"]

class EiffelLangInfo(LangInfo):
    name = "Eiffel"
    conforms_to_bases = ["Text"]
    exts = [".e"]

class HaskellLangInfo(LangInfo):
    name = "Haskell"
    conforms_to_bases = ["Text"]
    exts = [".hs"]

class PowerShellLangInfo(LangInfo):
    """Windows PowerShell
    http://www.microsoft.com/windowsserver2003/technologies/management/powershell/default.mspx
    """
    name = "PowerShell"
    conforms_to_bases = ["Text"]
    exts = [".ps1"]

class SchemeLangInfo(LangInfo):
    name = "Scheme"
    conforms_to_bases = ["Text"]
    exts = [".scm"]

class VHDLLangInfo(LangInfo):
    """TODO: desc, reference"""
    name = "VHDL"
    conforms_to_bases = ["Text"]
    exts = [".vhdl"]

class VerilogLangInfo(LangInfo):
    """TODO: desc, reference"""
    name = "Verilog"
    conforms_to_bases = ["Text"]



#---- "Basic"-based languages

class _BasicLangInfo(LangInfo):
    conforms_to_bases = ["Text"]

class FreeBasicLangInfo(_BasicLangInfo):
    """http://www.freebasic.net/"""
    name = "FreeBASIC"
    komodo_name = "FreeBasic"
    exts = [".bas"]

class PureBasicLangInfo(_BasicLangInfo):
    """http://www.purebasic.com/"""
    name = "PureBasic"
    exts = [".pb"]

class PowerBasicLangInfo(_BasicLangInfo):
    """TOOD: ref?
    TODO: which if this and PureBasic should win '.pb' ext? 
    """
    name = "PowerBasic"
    exts = [".pb"]

class BlitzBasicLangInfo(_BasicLangInfo):
    """http://www.blitzbasic.com/Products/blitzmax.php"""
    name = "BlitzBasic"
    exts = [".bb"]


class VisualBasicLangInfo(_BasicLangInfo):
    name = "VisualBasic"  #TODO: should name be "Visual Basic"?
    exts = [".vb"]

class VBScriptLangInfo(_BasicLangInfo):
    name = "VBScript"
    exts = [".vbs"]



#---- less common languages (AFAICT)

class BaanLangInfo(LangInfo):
    """Baan is the scripting language used for the Baan ERP system
    (currently known as SSA ERP according to the Wikipedia article
    below).

    http://en.wikipedia.org/wiki/Baan
    http://baan.ittoolbox.com/
    """
    name = "Baan"
    conforms_to_bases = ["Text"]
    exts = [".bc"]

class REBOLLangInfo(LangInfo):
    """http://www.rebol.com/"""
    name = "REBOL"
    conforms_to_bases = ["Text"]
    exts = [".r"]

class CamlLangInfo(LangInfo):
    """http://caml.inria.fr/"""
    name = "Caml"
    komodo_name = "Objective Caml"
    conforms_to_bases = ["Text"]
    exts = [".ml", ".mli"]

class SwiftScriptLangInfo(LangInfo):
    """https://developer.apple.com/swift/"""
    name = "Swift"
    exts = ['.swift']

