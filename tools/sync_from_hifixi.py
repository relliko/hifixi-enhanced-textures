r"""Copy the texture pack builder's sources from a HiFi XI checkout into this repo, at the same relative paths, so the
includes work unchanged. HiFi XI stays the home of the pack format (its plugin reads what this tool writes); this repo
carries only what hifixi-texpack.exe and its tests compile, found by following their #include "..." lines.
  python -I tools\sync_from_hifixi.py <hifixi checkout>
Writes SOURCE.txt with the checkout's commit. Files this script copied before and no longer needs are removed."""
import os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# What tools\build_texpack.cmd in HiFi XI compiles for the tool, its test and the fake upscaler
ROOTS = [
    'tools/texpack/texpack.cpp', 'tools/texpack/keys.cpp', 'tools/texpack/make.cpp', 'tools/texpack/fetch.cpp',
    'tools/texpack/upscale.cpp', 'tools/texpack/keeptexels.cpp', 'tools/texpack/image_io.cpp', 'tools/texpack/bc7.cpp',
    'src/pack/pack.cpp', 'src/pack/pack_write.cpp', 'src/pack/bc2.cpp', 'src/pack/hash.cpp', 'src/pack/validate.cpp',
    'src/bake/dat_core.cpp', 'src/bake/zonemesh.cpp', 'src/chars/tex.cpp', 'src/chars/os2.cpp',
    'tests/texpack_test.cpp', 'tests/fake_esrgan.cpp',
]
EXTRA = ['tests/data/texmake_ref.bin', 'tests/texmake_oracle.py', 'tests/pack_oracle.py', 'docs/texture-pack/format.md',
         'docs/texture-pack/upscaler.md']
INCLUDE = re.compile(r'^\s*#\s*include\s+"([^"]+)"', re.M)


def main():
    src = os.path.abspath(sys.argv[1])
    todo, seen = list(ROOTS), set()
    while todo:
        rel = os.path.normpath(todo.pop()).replace('\\', '/')
        if rel in seen:
            continue
        path = os.path.join(src, rel)
        if not os.path.isfile(path):
            sys.exit('%s is missing in %s' % (rel, src))
        seen.add(rel)
        text = open(path, encoding='utf-8', errors='replace').read()
        for inc in INCLUDE.findall(text):
            todo.append(os.path.join(os.path.dirname(rel), inc))
    files = sorted(seen | set(EXTRA))
    listed = os.path.join(HERE, 'tools', 'synced.txt')
    before = set(open(listed).read().split()) if os.path.exists(listed) else set()
    for rel in sorted(before - set(files)):
        p = os.path.join(HERE, rel)
        if os.path.exists(p):
            os.remove(p)
    for rel in files:
        out = os.path.join(HERE, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(os.path.join(src, rel), out)
    open(listed, 'w', newline='\r\n').write('\n'.join(files) + '\n')
    # build.cmd: this repo's header on HiFi XI's tools\build_texpack.cmd from its "set "VSDIR="" line
    ours = open(os.path.join(HERE, 'build.cmd'), encoding='utf-8').read().replace('\r\n', '\n')
    theirs = open(os.path.join(src, 'tools', 'build_texpack.cmd'), encoding='utf-8').read().replace('\r\n', '\n')
    mark = 'set "VSDIR="'
    open(os.path.join(HERE, 'build.cmd'), 'w', encoding='utf-8', newline='\r\n').write(
        ours[:ours.index(mark)] + theirs[theirs.index(mark):])
    commit = subprocess.run(['git', '-C', src, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    open(os.path.join(HERE, 'SOURCE.txt'), 'w', newline='\r\n').write(
        'The files listed in tools\\synced.txt are copied from HiFi XI (https://github.com/relliko/hifixi)\n'
        'at commit %s by tools\\sync_from_hifixi.py. Change them there, then sync.\n' % commit)
    print('%d files from %s' % (len(files), commit))


if __name__ == '__main__':
    main()
