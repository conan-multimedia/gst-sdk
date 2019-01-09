from conans import ConanFile, tools
from conanos.build import config_scheme
import os, sys

class GstsdkConan(ConanFile):
    name = "gst-sdk"
    version = "0.1"
    description = "Helper program to create gst-sdk from scratch"
    url = "https://github.com/conan-multimedia/gst-sdk"
    topics = ("gstreamer", "sdk")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
    }
    default_options = { 'shared': True }

    def configure(self):
        del self.settings.compiler.libcxx

        config_scheme(self)

    #def requirements(self):
    #    if self.settings.os == 'Windows':
    #        self.requires.add("7z_installer/1.0@conan/stable")
    #        self.requires.add("cygwin_installer/2.9.0@bincrafters/stable")
    #        self.requires.add("gperf/3.1@bincrafters/stable")
    #        self.requires.add("strawberryperl/5.26.0@conanos/stable")
    #        self.requires.add("msys2_installer/20161025@bincrafters/stable")
    #        self.requires.add("nasm/2.13.01@conanos/stable")

    def source(self):
        pass

    def build(self):
        targets = ["libffi","zlib","glib","gtk-doc-lite","gstreamer","libiconv","libxml2","libogg","libpng","pixman",
                   "expat","bzip2","freetype","fontconfig","cairo","harfbuzz","fribidi","pango","libvorbis","libtheora","orc",
                   "opus","graphene","gst-plugins-base","speex","libtiff","gdk-pixbuf","gmp","nettle","libtasn1","gnutls",
                   "glib-networking","libpsl","sqlite3","libsoup","mpg123","lame","wavpack","flac","taglib","libvpx",
                   "gst-plugins-good","openh264","librtmp","libsrtp","soundtouch","libcroco","openjpeg","openssl","spandsp",
                   "libdca","libnice","librsvg","x264","libass","faad2","libkate","gst-plugins-bad","a52dec","gst-plugins-ugly",
                   "json-glib","gst-rtsp-server","AMF","game-music-emu","libbluray","libcdio","libcdio-paranoia","libgpg-error",
                   "libgcrypt","libilbc","libssh","lzma","mfx_dispatch","modplug","nv-codec-headers","SDL","soxr","x265","xvid",
                   "OpenGL","FFmpeg","gst-libav","gst-env"]
        #FIXME lib + pattern
        for lib in targets:
            tools.out.info("REMOVE: " + lib)
            self.run('conan remove -f ' + lib)
        for lib in targets:
            tools.out.info("BUILD: " + lib)
            with tools.chdir(os.path.join(sys.path[0],"..",lib)):
                self.run('python build.py')

    def package(self):
        pass

    def package_info(self):
        pass

