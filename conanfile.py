from conans import ConanFile, tools
from conans.util.files import path_exists
from conanos.build import config_scheme
import os, sys
import pickle

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

    def _cache_dir(self):
        if self.settings.os == "Windows":
            return os.path.join(os.getenv("USERPROFILE"),"cache",self.name)
        return ''

    def _cache_file(self):
        return os.path.join(self._cache_dir(), "data.pkl")

    def _load_targets_built(self):
        targets_built = []
        if os.path.exists(self._cache_dir()) and path_exists(self._cache_file(), self._cache_dir()):
            with open(self._cache_file(), 'rb') as f:
                targets_built = pickle.load(f)

        return targets_built

    def _is_target_built(self, cur_target, targets_built):
        return cur_target in targets_built

    def _insert_target_built(self, target, targets_built):
        targets_built.append(target)

    def _dump_targets_built(self, targets_built):
        if not os.path.exists(self._cache_dir()):
            tools.mkdir(self._cache_dir())
        with open(self._cache_file(), 'wb') as f:
            pickle.dump(targets_built, f)

    def _remove_test_folder(self, basedir):
        test_folder = os.path.join(basedir, "test_package")
        test_build_folder = os.path.join(test_folder, "build")
        if path_exists(test_folder, basedir) and path_exists(test_build_folder, test_folder):
            #tools.rmdir(test_build_folder)
            #os.removedirs(test_build_folder)
            if self.settings.os == "Windows":
                self.run('rd/s/q %s'%(test_build_folder))
            if self.settings.os == "Linux":
                self.run('rm -rf %s'%(test_build_folder))

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

        targets_built = self._load_targets_built()
        tools.out.info( "TARGETS BUILT: "+ ';'.join(targets_built) )
        #FIXME lib + pattern


        for lib in targets:
            if self._is_target_built(lib, targets_built):
                tools.out.info("TARGET BUILT: " + lib)
                continue
            tools.out.info("REMOVE: " + lib)
            self.run('conan remove --force ' + lib)

        #for lib in targets:
            tools.out.info("BUILD: " + lib)
            basedir = os.path.join(sys.path[0],"..",lib)
            self._remove_test_folder(basedir)
            with tools.chdir(basedir):
                self.run('python build.py')
            self._insert_target_built(lib, targets_built)
            self._dump_targets_built(targets_built)

    def package(self):
        pass

    def package_info(self):
        pass

