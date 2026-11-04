@echo off
rem Builds hifixi-texpack.exe (build\hifixi-texpack.exe), its test build\texpack_test.exe and the test's stand-in for
rem the upscaler, build\fake_esrgan.exe, all 64-bit, with Visual Studio's C++ tools (2022 or newer, "Desktop development
rem with C++"). The sources are HiFi XI's (SOURCE.txt); this is HiFi XI's tools\build_texpack.cmd run from this folder.
setlocal
cd /d "%~dp0"

set "VSDIR="
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
for /f "usebackq delims=" %%i in (`call "%VSWHERE%" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`) do set "VSDIR=%%i"
if not defined VSDIR (
  echo Visual Studio with the C++ tools not found.
  exit /b 1
)
call "%VSDIR%\VC\Auxiliary\Build\vcvarsall.bat" amd64 >nul 2>&1 || exit /b 1

if not exist build mkdir build
if not exist build\obj64 mkdir build\obj64
if not exist build\obj64\texpack mkdir build\obj64\texpack
if not exist build\obj64\texpack_test mkdir build\obj64\texpack_test
if not exist build\obj64\fake_esrgan mkdir build\obj64\fake_esrgan

set "PACK=src\pack\pack.cpp src\pack\pack_write.cpp src\pack\bc2.cpp src\pack\hash.cpp src\pack\validate.cpp"
set "MAKE=tools\texpack\make.cpp tools\texpack\fetch.cpp tools\texpack\upscale.cpp tools\texpack\keeptexels.cpp tools\texpack\image_io.cpp"
cl /nologo /MP /std:c++20 /O2 /MT /EHsc /W4 /permissive- /utf-8 /DWIN32_LEAN_AND_MEAN /DNOMINMAX /DNDEBUG ^
  tools\texpack\texpack.cpp tools\texpack\keys.cpp %MAKE% %PACK% src\bake\dat_core.cpp src\bake\zonemesh.cpp src\chars\tex.cpp src\chars\os2.cpp ^
  /Fo"build\obj64\texpack\\" /Fe"build\hifixi-texpack.exe" /link /NOLOGO user32.lib advapi32.lib ole32.lib windowscodecs.lib bcrypt.lib urlmon.lib || exit /b 1
echo Built build\hifixi-texpack.exe
rem The tool on a few of the game's DATs and hand-made overlays (tests\texpack_test.cpp; tests\pack_oracle.py on what it writes)
cl /nologo /MP /std:c++20 /O2 /MT /EHsc /W4 /permissive- /utf-8 /DWIN32_LEAN_AND_MEAN /DNOMINMAX /DNDEBUG ^
  tests\texpack_test.cpp %PACK% src\bake\dat_core.cpp tools\texpack\upscale.cpp tools\texpack\keeptexels.cpp tools\texpack\image_io.cpp ^
  /Fo"build\obj64\texpack_test\\" /Fe"build\texpack_test.exe" /link /NOLOGO user32.lib ole32.lib windowscodecs.lib || exit /b 1
echo Built build\texpack_test.exe
cl /nologo /MP /std:c++20 /O2 /MT /EHsc /W4 /permissive- /utf-8 /DWIN32_LEAN_AND_MEAN /DNOMINMAX /DNDEBUG ^
  tests\fake_esrgan.cpp tools\texpack\image_io.cpp ^
  /Fo"build\obj64\fake_esrgan\\" /Fe"build\fake_esrgan.exe" /link /NOLOGO user32.lib ole32.lib windowscodecs.lib || exit /b 1
echo Built build\fake_esrgan.exe
