#!/usr/bin/env python

import os
import unittest

from docopt import docopt

from landslide import cli
from landslide.slide import Slide
from landslide.options import Options
from landslide.presentation import Presentation


class LandslideTestCase(unittest.TestCase):
    def get_options(self, s):
        return Options(docopt(cli.__doc__, s.split(' ')))


class CliTestCase(LandslideTestCase):
    def test_cli(self):
        try:
            os.unlink('presentation.html')
        except OSError:
            pass

        cli.main(['test-data/a.md'])

        self.assertTrue(os.path.exists('presentation.html'))

        os.unlink('presentation.html')


class OptionsTestCase(LandslideTestCase):
    def get_option(self, switch, name):
        return getattr(self.get_options('in.md %s' % switch), name)

    def test_single_source(self):
        options = self.get_options('in.md')

        self.assertEqual(options.sources, ['in.md'])

    def test_multiple_sources(self):
        options = self.get_options('a.md b.md c.md d.md')

        self.assertEqual(options.sources, ['a.md', 'b.md', 'c.md', 'd.md'])

    def test_default_options(self):
        options = self.get_options('in.md')

        self.assertEqual(options.theme, 'default')
        self.assertEqual(options.linenos, 'inline')
        self.assertEqual(options.destination, 'presentation.html')
        self.assertEqual(options.encoding, 'utf8')
        self.assertEqual(options.extensions, [])
        self.assertEqual(options.css, [])
        self.assertEqual(options.js, [])
        self.assertFalse(options.copy_theme)
        self.assertFalse(options.debug)
        self.assertFalse(options.embed)
        self.assertFalse(options.direct_output)
        self.assertFalse(options.no_presenter_notes)
        self.assertFalse(options.quiet)
        self.assertFalse(options.relative)
        self.assertFalse(options.watch)
        self.assertFalse(options.math_output)

    def test_all_options_config_file(self):
        options = self.get_options('test-data/all-options.cfg')

        self.assertEqual(options.sources, ['a.md', 'b-dir'])
        self.assertEqual(options.theme, '/path/to/theme')
        self.assertEqual(options.linenos, 'no')
        self.assertEqual(options.destination, 'out.html')
        self.assertEqual(options.encoding, 'utf16')
        self.assertEqual(options.extensions, ['a', 'b'])
        self.assertEqual(options.css, ['style-1.css', 'style-2.css'])
        self.assertEqual(options.js, ['js-1.js', 'js-2.js'])
        self.assertTrue(options.copy_theme)
        self.assertTrue(options.debug)
        self.assertTrue(options.embed)
        self.assertTrue(options.direct_output)
        self.assertTrue(options.no_presenter_notes)
        self.assertTrue(options.quiet)
        self.assertTrue(options.relative)
        self.assertTrue(options.watch)
        self.assertTrue(options.math_output)

    def test_source_only_config_file(self):
        options = self.get_options('test-data/sources-only.cfg')

        self.assertEqual(options.theme, 'default')
        self.assertEqual(options.linenos, 'inline')
        self.assertEqual(options.destination, 'presentation.html')
        self.assertEqual(options.encoding, 'utf8')
        self.assertEqual(options.extensions, [])
        self.assertEqual(options.css, [])
        self.assertEqual(options.js, [])
        self.assertFalse(options.copy_theme)
        self.assertFalse(options.debug)
        self.assertFalse(options.embed)
        self.assertFalse(options.direct_output)
        self.assertFalse(options.no_presenter_notes)
        self.assertFalse(options.quiet)
        self.assertFalse(options.relative)
        self.assertFalse(options.watch)
        self.assertFalse(options.math_output)

    def test_no_source_config_file(self):
        options = self.get_options('test-data/no-source.cfg test-data/a.md')

        self.assertEqual(options.sources, ['test-data/a.md'])
        self.assertEqual(options.theme, 'tango')

    def test_config_file_with_multiple_sources(self):
        options = self.get_options('test-data/sources-only.cfg c.md')

        self.assertEqual(options.sources, ['a.md', 'b-dir', 'c.md'])

    def test_theme_cli_option(self):
        self.assertEqual(self.get_option('-t blue', 'theme'), 'blue')
        self.assertEqual(self.get_option('--theme blue', 'theme'), 'blue')

    def test_linenos_cli_option(self):
        self.assertEqual(self.get_option('-l table', 'linenos'), 'table')
        self.assertEqual(self.get_option('--linenos no', 'linenos'), 'no')

    def test_destination_cli_option(self):
        name = 'destination'

        self.assertEqual(self.get_option('-d out', name), 'out')
        self.assertEqual(self.get_option('--destination out', name), 'out')

    def test_encoding_cli_option(self):
        name = 'encoding'

        self.assertEqual(self.get_option('-e utf16', name), 'utf16')
        self.assertEqual(self.get_option('--encoding utf16', name), 'utf16')

    def test_extensions_cli_option(self):
        name = 'extensions'

        self.assertTrue(self.get_option('-x a,b', name), ['a', 'b'])
        self.assertTrue(self.get_option('--extensions a,b', name), ['a', 'b'])

    def test_copy_theme_cli_option(self):
        self.assertTrue(self.get_option('-c', 'copy_theme'))
        self.assertTrue(self.get_option('--copy-theme', 'copy_theme'))

    def test_debug_cli_option(self):
        self.assertTrue(self.get_option('-b', 'debug'))
        self.assertTrue(self.get_option('--debug', 'debug'))

    def test_embed_cli_option(self):
        self.assertTrue(self.get_option('-i', 'embed'))
        self.assertTrue(self.get_option('--embed', 'embed'))

    def test_direct_output_cli_option(self):
        self.assertTrue(self.get_option('-o', 'direct_output'))
        self.assertTrue(self.get_option('--direct-output', 'direct_output'))

    def test_no_presenter_notes_cli_options(self):
        name = 'no_presenter_notes'

        self.assertTrue(self.get_option('-P', name))
        self.assertTrue(self.get_option('--no-presenter-notes', name))

    def test_quiet_cli_option(self):
        self.assertTrue(self.get_option('-q', 'quiet'))
        self.assertTrue(self.get_option('--quiet', 'quiet'))

    def test_relative_cli_option(self):
        self.assertTrue(self.get_option('-r', 'relative'))
        self.assertTrue(self.get_option('--relative', 'relative'))

    def test_watch_cli_option(self):
        self.assertTrue(self.get_option('-w', 'watch'))
        self.assertTrue(self.get_option('--watch', 'watch'))

    def test_match_output_cli_option(self):
        self.assertTrue(self.get_option('-m', 'math_output'))
        self.assertTrue(self.get_option('--math-output', 'math_output'))


class PresentationTestCase(LandslideTestCase):
    def tearDown(self):
        try:
            os.unlink('presentation.html')
        except OSError:
            pass

    def test_single_source(self):
        options = self.get_options('test-data/a.md')
        presentation = Presentation(options)

        self.assertEqual(presentation.sources, ['test-data/a.md'])

    def test_multiple_sources(self):
        options = self.get_options('test-data/a.md test-data/b.md')
        presentation = Presentation(options)

        sources = ['test-data/a.md', 'test-data/b.md']

        self.assertEqual(presentation.sources, sources)

    def test_shallow_dir_source(self):
        options = self.get_options('test-data/shallow')
        presentation = Presentation(options)

        sources = ['test-data/shallow/c.md', 'test-data/shallow/d.md']

        self.assertEqual(presentation.sources, sources)

    def test_deep_dir_source(self):
        options = self.get_options('test-data/deep')
        presentation = Presentation(options)

        sources = [
            'test-data/deep/e-f/e.md',
            'test-data/deep/e-f/f.md',
            'test-data/deep/g-h/g.md',
            'test-data/deep/g-h/h.md',
        ]

        self.assertEqual(presentation.sources, sources)

    def test_crazy_source(self):
        inputs = ' '.join([
            'test-data/a.md',
            'test-data/b.md',
            'test-data/shallow',
            'test-data/deep',
        ])

        options = self.get_options(inputs)
        presentation = Presentation(options)

        sources = [
            'test-data/a.md',
            'test-data/b.md',
            'test-data/shallow/c.md',
            'test-data/shallow/d.md',
            'test-data/deep/e-f/e.md',
            'test-data/deep/e-f/f.md',
            'test-data/deep/g-h/g.md',
            'test-data/deep/g-h/h.md',
        ]

        self.assertEqual(presentation.sources, sources)

    def test_set_theme_dir_custom(self):
        options = self.get_options('test-data/a.md -t test-data/theme-all')

        presentation = Presentation(options)

        self.assertEqual(presentation.theme_dir, 'test-data/theme-all')

    def test_set_theme_dir_built_in(self):
        options = self.get_options('test-data/a.md')

        presentation = Presentation(options)

        self.assertTrue(presentation.theme_dir.endswith('themes/default'))

        options = self.get_options('test-data/a.md -t light')

        presentation = Presentation(options)

        self.assertTrue(presentation.theme_dir.endswith('themes/light'))

    def test_set_theme_dir_missing(self):
        options = self.get_options('test-data/a.md -t missing')

        with self.assertRaises(Exception):
            Presentation(options)

    def test_get_css_files_default(self):
        options = self.get_options('test-data/a.md')

        presentation = Presentation(options)

        path_end = 'landslide/themes/default/style.css'

        self.assertEqual(len(presentation.css_files), 1)
        self.assertTrue(presentation.css_files[0].endswith(path_end))

    def test_get_css_files_custom(self):
        options = self.get_options('test-data/a.md -t test-data/theme-all')

        presentation = Presentation(options)

        path = 'test-data/theme-all/style.css'

        self.assertEqual(len(presentation.css_files), 1)
        self.assertEqual(presentation.css_files[0], path)

    def test_get_css_files_custom_missing(self):
        options = self.get_options('test-data/a.md -t test-data/theme-no-css')

        presentation = Presentation(options)

        path_end = 'landslide/themes/default/style.css'

        self.assertEqual(len(presentation.css_files), 1)
        self.assertTrue(presentation.css_files[0].endswith(path_end))

    def test_get_js_files_default(self):
        options = self.get_options('test-data/a.md')

        presentation = Presentation(options)

        path_end = 'landslide/themes/default/slides.js'

        self.assertEqual(len(presentation.js_files), 1)
        self.assertTrue(presentation.js_files[0].endswith(path_end))

    def test_get_js_files_custom(self):
        options = self.get_options('test-data/a.md -t test-data/theme-all')

        presentation = Presentation(options)

        path = 'test-data/theme-all/slides.js'

        self.assertEqual(len(presentation.js_files), 1)
        self.assertEqual(presentation.js_files[0], path)

    def test_get_js_files_custom_missing(self):
        options = self.get_options('test-data/a.md -t test-data/theme-no-js')

        presentation = Presentation(options)

        path_end = 'landslide/themes/default/slides.js'

        self.assertEqual(len(presentation.js_files), 1)
        self.assertTrue(presentation.js_files[0].endswith(path_end))


class SlideTestCase(LandslideTestCase):
    def test_process_header(self):
        header = '<h1>title</h1>'
        body = '<p>test</p>'

        html = '\n'.join([header, body])

        slide = Slide(html, 'test.md')

        self.assertEqual(slide.header_source, header)
        self.assertEqual(slide.header_level, 1)
        self.assertEqual(slide.title, 'title')
        self.assertEqual(slide.content, body)

    def test_process_header_no_header(self):
        html = '<p>test</p>'

        slide = Slide(html, 'test.md')

        self.assertIsNone(slide.header_source)
        self.assertIsNone(slide.header_level)
        self.assertIsNone(slide.title)
        self.assertEqual(slide.content, html)


if __name__ == '__main__':
    unittest.main()
